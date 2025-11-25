import pytest
import csv
from unittest.mock import patch
import sys
import argparse

def process_files(files):
    data = {}
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['position'] not in data:
                    data[row['position']] = {}
                    data[row['position']]['count'] = 1
                    data[row['position']]['performance'] = float(row['performance'])
                else:
                    data[row['position']]['count'] += 1
                    data[row['position']]['performance'] += float(row['performance'])
    
    return data
 
def prepare_table_data(data):
    table_data = []
    for id, (position, values) in enumerate(sorted(data.items(), key=lambda x: x[1]['performance'] / x[1]['count'], reverse=True), start=1):
        avg_performance = values['performance'] / values['count']
        table_data.append([id, position, f"{avg_performance:.2f}"])

    return table_data

@pytest.fixture
def sample_csv_file():
    csv_file = "test_data.csv"
    with open(csv_file, 'w', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['position', 'performance'])
        writer.writeheader()
        writer.writerows([
            {'position': 'Backend Developer', 'performance': '4.85'},
            {'position': 'Frontend Developer', 'performance': '4.7'},
            {'position': 'Data Scientist', 'performance': '4.7'},
        ])
    return csv_file

@pytest.fixture
def multiple_csv_files():
    files = []
    for i in range(2):
        csv_file = f"test_data{i}.csv"
        with open(csv_file, 'w', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['position', 'performance'])
            writer.writeheader()
            writer.writerows([
                {'position': 'Backend Developer', 'performance': f'4.{7+i}5'},
                {'position': 'Frontend Developer', 'performance': f'4.{5+i}5'},
            ])
        files.append(csv_file)
    return files

def test_single_file_processing(sample_csv_file):
    data = process_files([sample_csv_file])
    
    assert data['Backend Developer']['count'] == 1
    assert data['Backend Developer']['performance'] == 4.85
    assert data['Frontend Developer']['count'] == 1
    assert data['Frontend Developer']['performance'] == 4.7

def test_multiple_files_processing(multiple_csv_files):
    data = process_files(multiple_csv_files)
        
    assert data['Backend Developer']['count'] == 2
    assert data['Backend Developer']['performance'] == 4.75 + 4.85
    assert data['Frontend Developer']['count'] == 2
    assert data['Frontend Developer']['performance'] == 4.55 + 4.65

def test_average_calculation(multiple_csv_files):
    data = process_files(multiple_csv_files)
    
    back_avg = data['Backend Developer']['performance'] / data['Backend Developer']['count']
    assert back_avg == 4.8
    
    front_avg = data['Frontend Developer']['performance'] / data['Frontend Developer']['count']
    assert front_avg == 4.6

def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        process_files(['filenotfound.csv'])

def test_argument_parsing_single_file():
    test_args = ['main.py', '--files', 'test.csv']
    with patch.object(sys, 'argv', test_args):
        parser = argparse.ArgumentParser()
        parser.add_argument('--files', required=True, nargs='+')
        parser.add_argument('--report', default='Performance Report')
        args = parser.parse_args()
        
        assert args.files == ['test.csv']
        assert args.report == 'Performance Report'

def test_argument_parsing_multiple_files():
    test_args = ['main.py', '--files', 'test1.csv', 'test2.csv', '--report', 'Performance']
    with patch.object(sys, 'argv', test_args):
        parser = argparse.ArgumentParser()
        parser.add_argument('--files', required=True, nargs='+')
        parser.add_argument('--report', default='Performance Report')
        args = parser.parse_args()
        
        assert args.files == ['test1.csv', 'test2.csv']
        assert args.report == 'Performance'