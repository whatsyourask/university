class Matrix:
    # Конструктор класса
    def __init__(self, n, m, matrix=None):
        if matrix is None:
            self.__n = n
            self.__m = m
            self.__matrix = list()
            for i in range(self.__n):
                self.__matrix.append(list())
        else:
            self.__n = n
            self.__m = m
            self.__matrix = matrix

    # Геттер для n
    @property
    def n(self):
        return self.__n

    # Сеттер для n
    @n.setter
    def n(self, n):
        self.__n = n

    # Геттер для m
    @property
    def m(self):
        return self.__m

    # Сеттер для m
    @m.setter
    def m(self, m):
        self.__m = m

    # Геттер для matrix
    @property
    def matrix(self):
        return self.__matrix

    # Сеттер для matrix
    @matrix.setter
    def matrix(self, matrix):
        self.__matrix = matrix

    # Метод записи в матрицу
    def write_matrix(self):
        for i in range(self.__n):
            for j in range(self.m):
                count = int(input())
                self.__matrix[i].append(count)

    # Метод вывода матрицы на экран
    def read_matrix(self):
        for i in range(self.__n):
            for j in range(self.m):
                print(self.__matrix[i][j], end=" ")
            print("\n")

    # Перегрузка оператора +
    def __add__(self, other):
        if self.__n == other.n and self.__m == other.m:
            help_matrix = list()
            for i in range(self.__n):
                help_matrix.append([0 for j in range(self.__m)])
            for i in range(other.n):
                for j in range(other.m):
                    help_matrix[i][j] = self.__matrix[i][j] + other.matrix[i][j]
            return Matrix(self.__n, self.__m, help_matrix)

    # Перегрузка оператора -
    def __sub__(self, other):
        if self.__n == other.n and self.__m == other.m:
            help_matrix = list()
            for i in range(self.__n):
                help_matrix.append([0 for j in range(self.__m)])
            for i in range(other.n):
                for j in range(other.m):
                    help_matrix[i][j] = self.__matrix[i][j] - other.matrix[i][j]
            return Matrix(self.__n, self.__m, help_matrix)

    # Перегрузка оператора *
    def __mul__(self, other):
        if self.__m == other.n:
            help_matrix = list()
            for i in range(self.__n):
                help_matrix.append([0 for j in range(other.m)])
            for i in range(self.__n):
                for j in range(other.m):
                    for q in range(other.n):
                        help_matrix[i][j] += self.__matrix[i][q] * other.matrix[q][j]
            return Matrix(self.__n, other.m, help_matrix)

    # Метод транспонирования матрицы
    def transposition(self):
        for i in range(self.__n):
            for j in range(i, self.__m):
                self.__matrix[i][j], self.__matrix[j][i] = self.__matrix[j][i], self.__matrix[i][j]

    # Рекурсивный метод
    def __determinant_recursion(self, matrix):
        if len(matrix) == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        else:
            r = 1
            for j in range(len(matrix)):
                if matrix[0][0] == 0:
                    if matrix[j][0] != 0:
                        matrix[0], matrix[j] = matrix[j], matrix[0]
                        r *= -1
            for i in range(1, len(matrix)):
                t = float(matrix[i][0] / matrix[0][0])
                for j in range(len(matrix)):
                    matrix[i][j] -= matrix[0][j] * t
            help_matrix = list()
            for i in range(len(matrix)-1):
                help_matrix.append([0 for j in range(len(matrix)-1)])
            for i in range(len(help_matrix)):
                for j in range(len(help_matrix)):
                    help_matrix[i][j] = matrix[i + 1][j + 1]
            return r * matrix[0][0] * self.__determinant_recursion(help_matrix)

    # Метод запускающий рекурсию для определителя
    def determinant(self):
        if self.__n == self.__m:
            return self.__determinant_recursion(self.__matrix)
        else:
            print("n != m")
            return -1


def main():
    m = Matrix(3, 3)
    m.write_matrix()
    print(m.determinant())


if __name__ == "__main__":
    main()
