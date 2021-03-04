from typing import List


class ExtendedEuclideanAlgorithm:
    def __init__(self, a: int, b: int) -> None:
        self.__a = a
        self.__b = b

    def algorithm(self) -> List:
        a = self.__b
        b = self.__b
        div_arr = []
        a_arr = [a]
        b_arr = [b]
        mod_arr = []
        while True:
            mod = a % b
            mod_arr.append(mod)
            div = a // b
            div_arr.append(div)
            if not mod:
                break
            a, b = b, mod
            a_arr.append(a)
            b_arr.append(b)
        div_arr[-1] = None
        return a_arr, b_arr, mod_arr, div_arr


class FastModularExponentiation:
    def __init__(self, n: int, a: int, b: int) -> None:
        self.__n = n
        self.__a = a
        self.__b = b

    def __to_binary(self) -> List:
        # Convert to binary view
        return list(bin(self.__b)[2:])

    def algorthm(self) -> None:
        binary_b = self.__to_binary()
        temp_arr = [self.__a]
        temp = a
        for e in binary_b[1:]:
            temp = (self.__a * (temp ** 2)) % self.__n if e else (temp ** 2) % \
                                                                        self.__n
            temp_arr.append(temp)
        return temp, zip(binary, temp_arr)
