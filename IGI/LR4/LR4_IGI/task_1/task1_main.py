from task_1.vacation_chart import VacationChart
from task_1.employee import Employee
from prettytable import PrettyTable


chart = VacationChart()

Employee("John Doe", "01-01-2022", "15-01-2022")
Employee("Jane Doe", "16-01-2022", "31-01-2022")
Employee("Alice Smith", "01-02-2022", "15-02-2022")
Employee("Bob Johnson", "16-02-2022", "28-02-2022")
Employee("Charlie Brown", "01-03-2022", "15-03-2022")
Employee("David Williams", "16-03-2022", "31-03-2022")
Employee("Rosa Tims", "16-07-2022", "31-08-2022")

chart.save_to_csv("D:/3 SEM/253503_TIMOSHEVICH_25/IGI/LR4/LR4_IGI/data_dir/data.csv")
chart.save_to_pickle("D:/3 SEM/253503_TIMOSHEVICH_25/IGI/LR4/LR4_IGI/data_dir/data.pckl")

print("Данные сохранены в CSV и pickle.")

chart.load_from_csv("D:/3 SEM/253503_TIMOSHEVICH_25/IGI/LR4/LR4_IGI/data_dir/data.csv")
chart.load_from_pickle("D:/3 SEM/253503_TIMOSHEVICH_25/IGI/LR4/LR4_IGI/data_dir/data.pckl")

print("Данные загружены из CSV и pickle.")

print("Данные о сотрудниках:")
print(chart.employees)

print("Статистика отпусков:")
statistics = chart.vacation_statistics()

table = PrettyTable(["Месяц", "Количество сотрудников", "Процент от общего числа"])
months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
for i in range(12):
    table.add_row([months[i], statistics[i][0], f"{statistics[i][1]:.2f}%"])

print(table)

employee_name = input("Введите имя сотрудника: ")
employee = chart.find_employee(employee_name)

if employee is not None:
    print(f"Информация о сотруднике {employee_name}:")
    print(f"Дата начала отпуска: {employee[0].strftime('%d-%m-%Y')}")
    print(f"Дата окончания отпуска: {employee[1].strftime('%d-%m-%Y')}")
else:
    print(f"Сотрудник с именем {employee_name} не найден.")

print("Сортировка сотрудников по дате начала отпуска:")
sorted_employees = chart.sort_by_vacation_start()

for employee in sorted_employees:
    print(f"{employee[0]}: {employee[1][0].strftime('%d-%m-%Y')} - {employee[1][1].strftime('%d-%m-%Y')}")