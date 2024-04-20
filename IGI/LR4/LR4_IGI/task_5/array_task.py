import numpy as np


class MatrixOperations:
    def __init__(self, n, m):
        self.matrix = np.random.randint(0, 10, size=(n, m))

    def print_matrix(self):
        print(f"Matrix:\n{self.matrix}")

    def calculate_statistics(self):
        print(f"Mean: {np.mean(self.matrix)}")
        print(f"Median: {np.median(self.matrix)}")
        print(f"Correlation coefficient:\n{np.corrcoef(self.matrix)}")
        print(f"Variance: {np.var(self.matrix)}")
        print(f"Standard deviation (using np.std): {np.std(self.matrix)}")

    def find_min_elements(self):
        min_val = np.min(self.matrix)
        min_elements = np.sum(self.matrix == min_val)
        min_indices = np.where(self.matrix == min_val)
        min_indices = list(zip(min_indices[0], min_indices[1]))
        print(f"Minimum value: {min_val}")
        print(f"Number of minimum elements: {min_elements}")
        print(f"Indices of minimum elements: {min_indices}")

    def calculate_std_dev(self):
        """Calculate standard deviation using the formula."""
        mean = np.mean(self.matrix)
        std_dev = np.sqrt(np.mean((self.matrix - mean) ** 2))
        print(f"Standard deviation (using formula): {std_dev:.2f}")

if __name__ == "__main__":
    matrix_operations = MatrixOperations(5, 5)
    matrix_operations.print_matrix()
    matrix_operations.calculate_statistics()
    matrix_operations.find_min_elements()
    matrix_operations.calculate_std_dev()
