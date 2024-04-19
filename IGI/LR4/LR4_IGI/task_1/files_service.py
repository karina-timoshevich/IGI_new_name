import csv
import pickle
from datetime import datetime


def save_to_csv(employees, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['name', 'vacation_start', 'vacation_end']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for name, dates in employees.items():
            writer.writerow({'name': name, 'vacation_start': dates[0].strftime("%d-%m-%Y"), 'vacation_end': dates[1].strftime("%d-%m-%Y")})


def load_from_csv(filename):
    employees = {}
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            employees[row['name']] = (datetime.strptime(row['vacation_start'], "%d-%m-%Y"), datetime.strptime(row['vacation_end'], "%d-%m-%Y"))
    return employees


def save_to_pickle(employees, filename):
    with open(filename, 'wb') as f:
        pickle.dump(employees, f)


def load_from_pickle(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)