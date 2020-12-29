import sys
# sys.path хранит стандартные пути, где python ищет модули для импорта
# Теперь мы можем импортить модули вне папки 2 лабораторной
sys.path.insert(0, '..')
import lab1
import random
from lab1.fast_powers_mod import fast_powers_mod
import math
from lab1.euler import gcd
from typing import Tuple


def miller_rabin_test(n: int, a: int = None) -> Tuple:
    # Метод для вычисления теста Миллера-Рабина
    temp = n - 1
    s    = 0
    # Делим n - 1 на 2, пока не будет остатка больше нуля
    while not temp % 2:
        s    += 1
        temp /= 2
    t = int(temp)
    # Если параметр a не передан, рандомно берём из диапазона
    if not a:
        a = random.randint(2, n - 2)
    # Смотрим не выходит ли a за диапазон
    elif a >= n - 1:
        a -= 1
    elif a >= n - 2:
        a -= 2
    # Проверяем 1 условие
    mod_result, _ = fast_powers_mod(n, a, t)
    if mod_result == 1 or mod_result == n - 1:
        return True, (a, t)
    # Проверяем 2 условие
    if not s:
        s += 1
    # В цикле вычисляем быстрое возведение в степень по модулю и ищем равное n - 1
    for i in range(1, s):
        mod_result, _ = fast_powers_mod(n, mod_result, 2)
        if mod_result == n - 1:
            return True, (a, t)
    return False, (a, t)


def research(begin: int, end: int, a: int) -> Tuple:
    # По теореме n >= 5
    if begin < 5:
        begin = 5
    # Нечётное
    if not begin % 2:
        begin += 1
    # Если a больше begin, нет смысла начинать с begin
    if a > begin:
        begin = a
    mistakes      = 0
    wrong_numbers = ''
    for n in range(begin, end + 1, 2):
        # Определяем число по тесту Миллера-Рабина и по обычному алгоритму
        miller_rabin_result, _ = miller_rabin_test(n, a)
        primary_result         = primary_test(n)
        is_not_equal           = miller_rabin_result != primary_result
        # Смотрим результаты и определяем ошибку
        if is_not_equal:
            mistakes += 1
            wrong_numbers += str(n) + ' '
    return mistakes, wrong_numbers


def primary_test(n: int) -> bool:
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def test():
    # тест модуля
    n      = 13
    answer = True
    test_result, _ = miller_rabin_test(n)
    if test_result == answer:
        print('[+] Miller Rabin test passed.')
    primary_result = primary_test(n)
    if primary_result == answer:
        print('[+] Primary test passed.')
    print(research(1, 100000, 5))


if __name__=='__main__':
    test()
