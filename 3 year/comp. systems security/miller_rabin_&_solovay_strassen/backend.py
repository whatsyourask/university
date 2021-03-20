import sys
# To import FastModularExponentiation
sys.path.insert(0, '..')
from math import log2, gcd
from random import randint
from extended_euclidean_algorithm_and_fast_modular_exponentiation.backend import FastModularExponentiation


class MillerRabin:
    @staticmethod
    def test(n: int, count: int) -> bool:
        if n <= 2:
            raise ValueError
        d = n - 1
        s = 0
        while not d % 2:
            s += 1
            d //= 2
        # count = log2(n)
        fme = FastModularExponentiation()
        fme.n = n
        for round in range(count):
            a = randint(2, n - 2)
            fme.a = a
            fme.b = d
            x_0 = fme.algorithm()
            if x_0 == 1 or x_0 == n - 1:
                continue
            fme.a = x_0
            fme.b = 2
            for i in range(s - 1):
                x_i = fme.algorithm()
                fme.a = x_i
                if x_i == n - 1:
                    break
            else:
                return False
        return True


class SolovayStrassen:
    @staticmethod
    def test(n: int, count: int) -> bool:
        if n <= 2:
            raise ValueError
        for round in range(count):
            a = randint(2, n - 1)
            if gcd(a, n) > 1:
                return False
            symbol = legenre_symbol(a, n)
            if symbol == -1:
                symbol += n
            else:
                symbol %= n
            if not (a ^ ((n - 1) // 2) == symbol):
                return False
        return True


def legenre_symbol(a: int, p: int):
    # if gcd(a, b) != 1:
    #     return 0
    # answ = 1
    # if a < 0:
    #     a = -a
    #     if b % 4 == 3:
    #         answ = -answ
    # if a != 0:
    #     t = 0
    #     while not a % 2:
    #         t += 1
    #         a = a // 2
    #     if t % 2:
    #         if b % 8 == 3 or b % 8 == 5:
    #             answ = -answ
    #     if a % 4 == b % 4 == 3:
    #         answ = -answ
    # return answ
    if p < 2:
        raise ValueError
    if a == 0:
        return 0
    if a == 1:
        return 1
    if a % 2 == 0:
        result = legenre_symbol(a // 2, p)
        if ((p * p - 1) & 8) != 0:
            result = -result
    else:
        result = legenre_symbol(p % a, a)
        if ((a - 1) * (p - 1) & 4) != 0:
            result = -result
    return result
