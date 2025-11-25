import csv
import argparse
from tabulate import tabulate

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

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--files', required=True, nargs='+', help='CSV файл(ы)')
    parser.add_argument('--report', default='Performance Report', help='Название отчета')
    args = parser.parse_args()

    try:
        data = process_files(args.files)
        table_data = prepare_table_data(data)
    except FileNotFoundError:
        print(f"Ошибка: файл не найден")

    print(f"\n{args.report}\n")
    headers = ['id', 'position', 'performance']
    print(tabulate(table_data, headers=headers, tablefmt='grid'))