import sys
sys.path.insert(0, '..')
import lab1
from lab1.euler import gcd
from random import randrange
from lab1.ring import Ring
from lab1.fast_powers_mod import fast_powers_mod
from typing import List


class RSA:
    def __init__(self, p=None, q=None) -> None:
        self._p = p
        self._q = q
        self._e = None
        self._n = None
        self._d = None

    def generate_public_key(self) -> None:
        self._n = self._p * self._q
        self._euler_func = (self._p - 1) * (self._q - 1)
        e_arr = []
        for e in range(self._n + 1):
            if gcd(e, self._euler_func) == 1:
                e_arr.append(e)
        ind = randrange(len(e_arr))
        self._e = e_arr[ind]

    @property
    def n(self) -> int:
        return self._n

    @n.setter
    def n(self, n:int) -> None:
        self._n = n

    @property
    def euler_func(self) -> int:
        return self._euler_func

    @euler_func.setter
    def euler_func(self, euler_func) -> None:
        self._euler_func = euler_func

    @property
    def e_arr(self) -> int:
        return self._e_arr

    @e_arr.setter
    def e_arr(self, e_arr: List) -> None:
        self._e_arr = e_arr

    @property
    def e(self) -> int:
        return self._e

    @e.setter
    def e(self, e:int) -> None:
        self._e = e

    def generate_private_key(self) -> None:
        e = Ring(self._euler_func, self._e)
        invert_e, _ = e.invert()
        self._d = invert_e.num

    @property
    def d(self) -> int:
        return self._d

    @d.setter
    def d(self, d: int) -> None:
        self._d = d

    def encrypt(self, m) -> int:
        encrypted = None
        if self._e:
            encrypted, _ = fast_powers_mod(self._n, m, self._e)
        return encrypted

    def decrypt(self, c) -> int:
        decrypted = None
        if self._d:
            decrypted, _ = fast_powers_mod(self._n, c, self._d)
        return decrypted


def test():
    rsa = RSA(17, 31)
    rsa.generate_public_key()
    print(f'Chosen e = {rsa.e}')
    print(f'n = {rsa.n}')
    rsa.generate_private_key()
    print(f'Chosen d = {rsa.d}')
    m = 24
    c = rsa.encrypt(m)
    print(f'encrypted message {m} => {c}')
    new_m = rsa.decrypt(c)
    print(f'decrypted message {c} => {new_m}')
    if m == new_m:
        print('Test passed')



if __name__=='__main__':
    test()
