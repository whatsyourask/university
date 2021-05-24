import sys
sys.path.insert(0, '..')
from random import randint, seed
from math import gcd
from rsa.backend import RSA
from typing import Tuple
from extended_euclidean_algorithm_and_fast_modular_exponentiation.backend import FastModularExponentiation, ExtendedEuclideanAlgorithm
from os import cpu_count
import threading
from time import time


class AttackOnRSA:
    @staticmethod
    def attack(e: int, n: int, encrypted: str) -> Tuple:
        iter_count = 0
        possible_divisor, iter_count = AttackOnRSA.pollards_rho_method(n)
        second_divisor = n // possible_divisor
        rsa = RSA()
        rsa.n = n
        rsa.euler_func = (possible_divisor - 1) * (second_divisor - 1)
        d = rsa.generate_private_key(e)
        decrypted = rsa.decrypt(encrypted)
        return possible_divisor, second_divisor, d, decrypted, iter_count

    def threading_pollards_rho_method(self, seed_val: float) -> None:
        seed(seed_val)
        x = randint(1, self.n - 2)
        power = randint(2, 4)
        y = 1
        iter_count = 0
        stage = 2
        d = 1
        while d == 1 and self._not_found:
            if iter_count == stage:
                y = x
                stage *= 2
            x = (x ** power + 1) % self.n
            d = gcd(self.n, abs(x - y))
            iter_count += 1
        if self._not_found:
            self._not_found = False
            self.results.append((d, iter_count))

    def threading_attack(self, e: int, n: int, encrypted: str) -> Tuple:
        iter_count = 0
        thread_count = cpu_count()
        threads = []
        self.results = []
        self.n = n
        self._not_found = True
        for i in range(thread_count):
            seed_val = time() + i
            thread = threading.Thread(target=self.threading_pollards_rho_method, args=(seed_val,))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        possible_divisor, iter_count = self.results[0]
        second_divisor = n // possible_divisor
        rsa = RSA()
        rsa.n = n
        rsa.euler_func = (possible_divisor - 1) * (second_divisor - 1)
        d = rsa.generate_private_key(e)
        decrypted = rsa.decrypt(encrypted)
        return possible_divisor, second_divisor, d, decrypted, iter_count

    @staticmethod
    def pollards_rho_method(n: int) -> Tuple:
        # https://www.geeksforgeeks.org/pollards-rho-algorithm-prime-factorization/
        # python's pow and gcd are faster than our implementations
        if n == 1:
            return n, 1
        if n % 2 == 0:
            return 2, 1
        x = randint(0, 2) % (n - 2)
        y = x
        c = randint(0, 1) % (n - 1)
        d = 1
        # fme = FastModularExponentiation()
        # fme.n = n
        # fme.b = 2
        # eea = ExtendedEuclideanAlgorithm()
        # eea.y = n
        iter_count = 0
        while d == 1:
            x = (pow(x, 2, n) + c + n) % n
            y = (pow(y, 2, n) + c + n) % n
            y = (pow(y, 2, n) + c + n) % n
            d = gcd(abs(x - y), n)
            # fme.a = x
            # x = (fme.algorithm() + c) % n
            # fme.a = y
            # y = (fme.algorithm() + c) % n
            # fme.a = y
            # y = (fme.algorithm() + c) % n
            # eea.x = abs(x - y)
            # _, _, d = eea.algorithm()
            iter_count += 1
            if d == n:
                d, rec_iter_count = pollards_rho_method(n)
                iter_count += rec_iter_count
                return d, iter_count
        return d, iter_count
