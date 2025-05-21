class SparseMatrix:
    def __init__(self, filepath=None):
        self.matrix = {}
        self.rows = 0
        self.cols = 0
        if filepath:
            self.load_matrix(filepath)

    def load_matrix(self, filepath):
        try:
            with open(filepath, 'r') as file:
                lines = file.readlines()
                self.rows = int(lines[0].strip().split('=')[1])
                self.cols = int(lines[1].strip().split('=')[1])
                for line in lines[2:]:
                    line = line.strip()
                    if line:
                        try:
                            row, col, value = map(int, line.strip('()').split(','))
                            if row not in self.matrix:
                                self.matrix[row] = {}
                            self.matrix[row][col] = value
                        except ValueError:
                            raise ValueError("Input file has wrong format")
        except FileNotFoundError:
            print(f"Error: File {filepath} not found.")
            exit(1)

    def get_element(self, row, col):
        return self.matrix.get(row, {}).get(col, 0)

    def set_element(self, row, col, value):
        if row >= self.rows or col >= self.cols:
            raise IndexError("Index out of matrix bounds")
        if value != 0:
            if row not in self.matrix:
                self.matrix[row] = {}
            self.matrix[row][col] = value
        elif row in self.matrix and col in self.matrix[row]:
            del self.matrix[row][col]

    def add(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must have the same dimensions for addition")
        result = SparseMatrix()
        result.rows = self.rows
        result.cols = self.cols
        result.matrix = {row: cols.copy() for row, cols in self.matrix.items()}
        for row, cols in other.matrix.items():
            for col, value in cols.items():
                result.set_element(row, col, result.get_element(row, col) + value)
        return result

    def subtract(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must have the same dimensions for subtraction")
        result = SparseMatrix()
        result.rows = self.rows
        result.cols = self.cols
        result.matrix = {row: cols.copy() for row, cols in self.matrix.items()}
        for row, cols in other.matrix.items():
            for col, value in cols.items():
                result.set_element(row, col, result.get_element(row, col) - value)
        return result

    def multiply(self, other):
        if self.cols != other.rows:
            raise ValueError("Number of columns of first matrix must equal number of rows of second matrix")
        result = SparseMatrix()
        result.rows = self.rows
        result.cols = other.cols
        for row in self.matrix:
            for col in range(other.cols):
                sum_value = 0
                for k in self.matrix[row]:
                    sum_value += self.get_element(row, k) * other.get_element(k, col)
                if sum_value != 0:
                    result.set_element(row, col, sum_value)
        return result

    def display(self):
        print(f"Matrix ({self.rows} x {self.cols}):")
        for row in self.matrix:
            for col in self.matrix[row]:
                print(f"({row}, {col}) = {self.matrix[row][col]}")


# Testing Block
if __name__ == "__main__":
    try:
        print("Loading matrix1.txt...")
        matrix1 = SparseMatrix("../sample_inputs/matrix1.txt")
        print("Matrix 1:")
        matrix1.display()

        print("\nLoading matrix2.txt...")
        matrix2 = SparseMatrix("../sample_inputs/matrix2.txt")
        print("Matrix 2:")
        matrix2.display()

        print("\nPerforming Addition:")
        try:
            result_add = matrix1.add(matrix2)
            print("Result of Addition:")
            result_add.display()
        except ValueError as e:
            print(f"Error during addition: {e}")

        print("\nPerforming Subtraction:")
        try:
            result_sub = matrix1.subtract(matrix2)
            print("Result of Subtraction:")
            result_sub.display()
        except ValueError as e:
            print(f"Error during subtraction: {e}")

        print("\nPerforming Multiplication:")
        try:
            result_mul = matrix1.multiply(matrix2)
            print("Result of Multiplication:")
            result_mul.display()
        except ValueError as e:
            print(f"Error during multiplication: {e}")

    except Exception as e:
        print(f"Unexpected error: {e}")
