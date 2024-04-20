import runpy


def menu():
    while True:
        print("\n1. Execute task 1")
        print("2. Execute task 2")
        print("3. Execute task 3")
        print("4. Execute task 4")
        print("5. Execute task 5")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            runpy.run_path(path_name='task_1/task1_main.py')
        elif choice == '2':
            runpy.run_path(path_name='task_2/task2_main.py')
        # elif choice == '3':
        #    #  task3()
        # elif choice == '4':
        #     task4()
        # elif choice == '5':
        #     task5()
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == '__main__':
    menu()