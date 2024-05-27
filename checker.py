import csv

def check_csv_columns(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        line_number = 0
        for row in csv_reader:
            line_number += 1
            if len(row) != 3:
                print(f"Line {line_number}: {row}")
                print("------------------------------------")

# Specify the path to your CSV file
csv_file_path = 'invoice_words.csv'

# Check the CSV file for rows with extra columns
check_csv_columns(csv_file_path)
