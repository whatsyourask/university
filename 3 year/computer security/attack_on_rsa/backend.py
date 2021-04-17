import sys
sys.path.insert(0, '..')
from random import randint
from math import gcd
from rsa.backend import RSA
from typing import Tuple
#from extended_euclidean_algorithm_and_fast_modular_exponentiation.backend import FastModularExponentiation, ExtendedEuclideanAlgorithm


class AttackOnRSA:
    @staticmethod
    def attack(e: int, n: int, encrypted: str) -> Tuple:
        possible_divisor = pollards_rho_method(n)
        second_divisor = n // possible_divisor
        rsa = RSA()
        rsa.n = n
        rsa.euler_func = (possible_divisor - 1) * (second_divisor - 1)
        d = rsa.generate_private_key(e)
        decrypted = rsa.decrypt(encrypted)
        return possible_divisor, second_divisor, d, decrypted


def pollards_rho_method(n: int) -> int:
    # https://www.geeksforgeeks.org/pollards-rho-algorithm-prime-factorization/
    # python's pow and gcd are faster than our implementations
    if n == 1:
        return n
    if n % 2 == 0:
        return 2
    x = randint(0, 2) % (n - 2)
    y = x
    c = randint(0, 1) % (n - 1)
    d = 1
    # fme = FastModularExponentiation()
    # fme.n = n
    # fme.b = 2
    # eea = ExtendedEuclideanAlgorithm()
    # eea.y = n
    while d == 1:
        #fme.a = x
        x = (pow(x, 2, n) + c + n) % n
        # x = (fme.algorithm() + c + n) % n
        # fme.a = y
        y = (pow(y, 2, n) + c + n) % n
        # y = (fme.algorithm() + c + n) % n
        # fme.a = y
        y = (pow(y, 2, n) + c + n) % n
        # y = (fme.algorithm() + c + n) % n
        # eea.x = abs(x - y)
        d = gcd(abs(x - y), n)
        # _, _, d = eea.algorithm()
        if d == n:
            return pollards_rho_method(n)
    return d
