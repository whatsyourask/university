import sys
# sys.path хранит стандартные пути, где python ищет модули для импорта
# Теперь мы можем импортить модули вне папки 2 лабораторной
sys.path.insert(0, '..')
import lab1
import random
from lab1.fast_powers_mod import fast_powers_mod
import math
from lab1.euler import gcd


def miller_rabin_test(n: int, a: int = None) -> bool:
    temp = n - 1
    s    = 0
    while not temp % 2:
        s    += 1
        temp /= 2
    t = int(temp)
    if not a:
        a = random.randint(2, n - 2)
    mod_result, _ = fast_powers_mod(n, a, t)
    if mod_result and mod_result == n - 1:
        return True
    if not s:
        s += 1
    for i in range(s - 1):
        mod_result = fast_powers_mod(n, mod_result, 2)
        if mod_result == n - 1:
            return True
    return False


def research(begin: int, end: int, a: int):
    if begin < 5:
        begin = 5
    if not begin % 2:
        begin += 1
    if a > begin:
        begin = a
    mistakes = 0
    wrong_numbers = ''
    for n in range(begin, end + 1, 2):
        miller_rabin_result = miller_rabin_test(n, a)
        primary_result      = primary_test(n)
        is_not_equal        = miller_rabin_test == primary_test
        if is_not_equal:
            mistakes += 1
            wrong_numbers += str(n)
        


def primary_test(n: int) -> bool:
    end = math.sqrt(n)
    for i in range(2, end):
        if gcd(i, n) != 1:
            return False
    return True


def test():
    n      = 13
    answer = True
    test_result = miller_rabin_test(n)
    if test_result == answer:
        print('[+] Test passed.')
    primary_result = primary_test(n)
    if primary_result == answer:
        print('[+] Test passed.')


if __name__=='__main__':
    test()
