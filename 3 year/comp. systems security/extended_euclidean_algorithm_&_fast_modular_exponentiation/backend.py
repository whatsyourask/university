from typing import List


class ExtendedEuclideanAlgorithm:
    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    @x.setter
    def x(self, x: int) -> None:
        self.__x = x

    @y.setter
    def y(self, y: int) -> None:
        self.__y = y

    def algorithm(self) -> List:
        a = self.__x
        b = self.__y
        div_arr = []
        while True:
            mod = a % b
            div = a // b
            div_arr.append(div)
            if not mod:
                break
            a, b = b, mod
        div_arr[-1] = None
        x = 0
        y = 1
        copy_div_arr = div_arr[:]
        copy_div_arr.pop()
        while copy_div_arr:
            last = copy_div_arr.pop()
            x, y = y, x - y * last
        return x, y, b


class FastModularExponentiation:
    @property
    def n(self) -> int:
        return self.__n

    @property
    def a(self) -> int:
        return self.__a

    @property
    def b(self) -> int:
        return self.__b

    @n.setter
    def n(self, n: int) -> None:
        self.__n = n

    @a.setter
    def a(self, a: int) -> None:
        self.__a = a

    @b.setter
    def b(self, b: int) -> None:
        self.__b = b

    def __to_binary(self) -> List:
        # Convert to binary view
        return list(map(lambda x: int(x), bin(self.__b)[2:]))

    def algorithm(self) -> int:
        binary_b = self.__to_binary()
        temp = self.__a
        for e in binary_b[1:]:
            temp = (self.__a * (temp ** 2)) % self.__n if int(e) else (temp ** 2) % self.__n
        return temp
