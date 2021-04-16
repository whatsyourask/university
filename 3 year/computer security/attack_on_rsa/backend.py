import sys
sys.path.insert(0, '..')
from random import randint
from math import gcd
from rsa.backend import RSA


class AttackOnRSA:
    @staticmethod
    def attack(e: int, n: int, encrypted: str) -> str:
        possible_divisor = pollards_rho_method(n)
        second_divisor = n // possible_divisor
        rsa = RSA()
        rsa.n = n
        rsa.euler_func = (possible_divisor - 1) * (second_divisor - 1)
        d = rsa.generate_private_key(e)
        decrypted = rsa.decrypt(encrypted)
        return decrypted


def pollards_rho_method(n: int) -> int:
    # https://www.geeksforgeeks.org/pollards-rho-algorithm-prime-factorization/
    if n == 1:
        return n
    if n % 2 == 0:
        return 2
    x = randint(0, 2) % (n - 2)
    y = x
    c = randint(0, 1) % (n - 1)
    d = 1
    while d == 1:
        x = (pow(x, 2, n) + c + n) % n
        y = (pow(y, 2, n) + c + n) % n
        y = (pow(y, 2, n) + c + n) % n
        d = gcd(abs(x - y), n)
        if d == n:
            return pollards_rho_method(n)
    return d
