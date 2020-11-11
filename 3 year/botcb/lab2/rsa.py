import sys
sys.path.insert(0, '..')
from lab1.euler import gcd
from random import randrange
from lab1.ring import Ring


class RSA:
    def __init__(self, p, q) -> None:
        self._p = p
        self._q = q

    def generate_encrypt_key(self) -> None:
        self._n = self._p * self._q
        self._euler_func = (self._p - 1) * (self._q - 1)
        e_arr = []
        for e in range(self._n):
            if gcd(e, self._euler_func) == 1:
                e_arr.append(e)
        ind = randrange(len(e_arr))
        self._e = e_arr[ind]

    @property
    def e(self) -> int:
        return self._e

    @e.setter
    def e(self, e:int) -> None:
        self._e = e

    def generate_decrypt_key(self) -> None:
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


def test():
    rsa = RSA(17, 31)
    rsa.generate_encrypt_key()
    print(f'Chosen e = {rsa.e}')
    rsa.generate_decrypt_key()
    print(f'Chosen d = {rsa.d}')


if __name__=='__main__':
    test()
