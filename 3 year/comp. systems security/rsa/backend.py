import sys
# To import FastModularExponentiation
sys.path.insert(0, '..')
from miller_rabin_and_solovay_strassen.backend import MillerRabin
from secrets import randbits
from math import log2


class RSA:
    @property
    def p(self) -> int:
        return self._p

    @p.setter
    def p(self, p: int) -> None:
        self._p = p

    @property
    def q(self) -> int:
        return self._p

    @q.setter
    def q(self, q: int) -> None:
        self._q = q

    @property
    def n(self) -> int:
        return self._n

    @n.setter
    def n(self, n: int) -> None:
        self._n = n


def miller_rabin_generate(bits_len: int) -> int:
    number = randbits(bits_len)
    while not MillerRabin.test(number, int(log2(number))):
        number = randbits(bits_len)
    return number


def euler_func(n: int) -> int:
    # Euler function calculation
    result = n
    i = 2
    while i ** 2 <= n:
        if n % i == 0:
            while n % i == 0:
                n /= i
            result -= result / i
        i += 1
    if n > 1:
        result -= result / n
    return result 
