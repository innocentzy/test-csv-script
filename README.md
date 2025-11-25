# Скрипт для анализа эффективности работы разработчиков	

## Установка зависимостей
```bash
pip install -r requirements.txt
```

## Использование
```bash
# Один файл
python main.py --files data.csv

# Несколько файлов
python main.py --files data1.csv data2.csv data3.csv

# С кастомным названием отчета
python main.py --files data.csv --report performance
```

## Запуск тестов
```bash
pytest test_main.py
```

## Пример запуска скрипта
<picture>
  <img alt="Example picture" src="example.png?raw=true">
</picture>
