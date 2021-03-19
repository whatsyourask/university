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
            if not (a ^ ((n - 1) // 2) == (legendre_symbol(a, n) % n)):
                return False
        return True


def legendre_symbol(a: int, p: int):
    print(a, p)
    if a == 1:
        return 1
    if not a % 2:
        return legendre_symbol(a // 2, p) * ((-1) ^ ((p ^ 2 - 1) // 8))
    else:
        return legendre_symbol(p % a, a) * ((-1) ^ ((a - 1) * (p - 1) // 4))
