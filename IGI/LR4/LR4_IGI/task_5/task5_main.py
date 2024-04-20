from array_task import MatrixOperations
import numpy as np


def main():
    # Создание объекта класса MatrixOperations
    matrix_operations = MatrixOperations(5, 5)

    # Печать матрицы
    matrix_operations.print_matrix()

    # Вычисление и печать статистики
    matrix_operations.calculate_statistics()

    # Поиск и печать минимальных элементов и их индексов
    matrix_operations.find_min_elements()

    # Вычисление и печать стандартного отклонения
    matrix_operations.calculate_std_dev()

    # Создание массива с помощью функций array() и arange()
    arr = np.array([1, 2, 3, 4, 5])
    print("Array created using np.array():\n", arr)

    arr = np.arange(0, 10, 2)
    print("\nArray created using np.arange():\n", arr)

    # Создание массива заданного вида
    zeros = np.zeros((3, 3))
    print("\nArray of zeros:\n", zeros)

    # Создание массива из единиц
    ones = np.ones((3, 3))
    print("\nArray of ones:\n", ones)

    # Создание массива заданного вида с заданным значением
    full = np.full((3, 3), 7)
    print("\nArray of sevens:\n", full)

    # Создание единичной матрицы
    eye = np.eye(3)
    print("\nIdentity array:\n", eye)

    # Создание массива случайных чисел
    random = np.random.random((3, 3))
    print("\nRandom array:\n", random)

    # Индексирование массивов NumPy
    print("\nElement at index 2:", arr[2])
    print("Elements from index 1 to 3:", arr[1:4])

    # Операции с массивами
    arr1 = np.array([1, 2, 3])
    arr2 = np.array([4, 5, 6])

    print("\nSum of arrays:", np.add(arr1, arr2))
    print("Difference of arrays:", np.subtract(arr1, arr2))
    print("Product of arrays:", np.multiply(arr1, arr2))
    print("Division of arrays:", np.divide(arr1, arr2))


if __name__ == "__main__":
    main()
