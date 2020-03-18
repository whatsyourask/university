class Complex:
    # Конструктор класса
    def __init__(self, rm, im):
        self.__rm = rm
        self.__im = im

    # Геттер для вещественной части числа
    @property
    def rm(self):
        return self.__rm

    # Сеттер для вещественной части числа
    @rm.setter
    def rm(self):
        self.__rm = input("Write a rational part ")

    # Геттер для мнимой части числа
    @property
    def im(self):
        return self.__im

    # Сеттер для мнимой части числа
    @im.setter
    def im(self):
        self.__im = input("write a imaginary part ")

    # Метод печати комплексного числа
    def print_complex(self):
        print("Rm = {0} Im = {1}".format(self.__rm, self.__im))

    # Перегрузка оператора +
    def __add__(self, other):
        return Complex(self.__rm + other.rm, self.__im + other.im)

    # Перегрузка оператора -
    def __sub__(self, other):
        return Complex(self.__rm - other.rm, self.__im - other.im)

    # Перегрузка оператора *
    def __mul__(self, other):
        return Complex(self.__rm * other.rm - self.__im * other.im, self.__rm * other.rm + self.__im * other.im)

    # Перегрузка оператора /
    def __truediv__(self, other):
        return Complex((self.__rm * other.rm + self.__im * other.im)/(other.rm ** 2 + other.im ** 2),
                       (self.__rm * other.rm - self.__im * other.im)/(other.rm ** 2 + other.im ** 2))

    # Метод нахождения сопряженного числа
    def find_conjugate(self):
        return Complex(self.__rm, self.__im * (-1))

    # Переопределение метода __str__
    def __str__(self):
        return "Rm = {} Im = {}".format(self.__rm, self.__im)


def main():
    z1 = Complex(1, -1)
    z1.print_complex()
    z2 = Complex(2, -2)
    z2.print_complex()
    z3 = z1 + z2
    z3.print_complex()
    z3 = z1 - z2
    z3.print_complex()
    z3 = z1 * z2
    z3.print_complex()
    z3 = z1 / z2
    z3.print_complex()
    print(z3.find_conjugate())


if __name__ == "__main__":
    main()
