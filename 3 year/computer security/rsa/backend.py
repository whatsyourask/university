import sys
# To import FastModularExponentiation
sys.path.insert(0, '..')
from miller_rabin_and_solovay_strassen.backend import MillerRabin
from secrets import randbits
from math import log2
from extended_euclidean_algorithm_and_fast_modular_exponentiation.backend import ExtendedEuclideanAlgorithm
from random import randint


class RSA:
    """
    Class that generates public and private key, encrypts and decrypts any text
    """
    LAST_ORD = 8364
    @property
    def n(self) -> int:
        return self._n

    @n.setter
    def n(self, n: int) -> None:
        self._n = n

    @property
    def euler_func(self) -> int:
        return self._euler_func

    @euler_func.setter
    def euler_func(self, e_func: int) -> None:
        self._euler_func = e_func

    def generate_public_key(self, bits_len: int) -> int:
        # To generate public key
        e = randint(pow(2, bits_len), self._n)
        while gcd(e, self._euler_func) != 1:
            e += 1
        self._e = e
        return e

    def generate_private_key(self, e=None) -> int:
        if e:
            self._e = e
        # To generate private key
        eea = ExtendedEuclideanAlgorithm()
        eea.x = self._euler_func
        eea.y = self._e
        _, self._d, _ = eea.algorithm()
        return self._d

    @property
    def e(self) -> int:
        return self._e

    @e.setter
    def e(self, e: int) -> None:
        self._e = e

    @property
    def d(self) -> int:
        return self._d

    @d.setter
    def d(self, d: int) -> None:
        self._d = d

    def encrypt(self, cleartext: str) -> str:
        encrypted = ' '.join(list(map(lambda char: self._chr_encrypt(char),
                                      cleartext)))
        return encrypted

    def _chr_encrypt(self, char: str) -> str:
        if type(char) == str and len(char) == 1:
            return str(pow(ord(char), self._e, self._n))
        elif type(char) == str:
            return str(pow(int(char), self._e, self._n))
        else:
            return str(pow(char, self._e, self._n))

    def decrypt(self, encrypted: str) -> str:
        decrypted = ' '.join(list(map(lambda seq: self._chr_decrypt(seq),
                         encrypted)))
        return decrypted

    def _chr_decrypt(self, seq: str) -> str:
        # To make lambda short
        return str(pow(int(seq), self._d, self._n))


def gcd(a, b) -> int:
    while b:
        a, b = b, a % b
    return a


def miller_rabin_generate(bits_len: int) -> int:
    number = generate_one_time_properly(bits_len)
    while not MillerRabin.test(number, int(log2(number))):
        number = generate_one_time_properly(bits_len)
    return number


def generate_one_time_properly(bits_len: int) -> int:
    number = randbits(bits_len)
    while number < 3:
        number = randbits(bits_len)
    return number
