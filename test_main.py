import pytest
import csv
from unittest.mock import patch
import sys
import argparse
from main import process_files, prepare_table_data

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

def test_prepare_table_data_sorting(multiple_csv_files):
    data = process_files(multiple_csv_files)
    table_data = prepare_table_data(data)
    
    assert table_data[0][1] == 'Backend Developer'
    assert table_data[0][2] == '4.80'
    assert table_data[1][1] == 'Frontend Developer'
    assert table_data[1][2] == '4.60'

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