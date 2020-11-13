import sys
# sys.path хранит стандартные пути, где python ищет модули для импорта
# Теперь мы можем импортить модули вне папки 2 лабораторной
sys.path.insert(0, '..')
import lab1
from lab1.euler import gcd
from random import randrange
from lab1.ring import Ring
from lab1.fast_powers_mod import fast_powers_mod
from typing import List


class RSA:
    """Класс для генерации ключей RSA, шифрования и дешифрования сообщений"""
    def __init__(self, p=None, q=None) -> None:
        # Конструктор с параметрами по умолчанию
        # для того, чтобы можно было создать класс без всего
        # и заполнять поля по мере надобности
        self._p = p
        self._q = q
        self._e = None
        self._n = None
        self._d = None

    def generate_public_key(self) -> None:
        # Генерация публичного ключа
        # Вычисление n = p * q
        self._n = self._p * self._q
        # Вычисление функции эйлера = (p - 1) * (q - 1)
        self._euler_func = (self._p - 1) * (self._q - 1)
        # Массив для сохранения всех возможных публичных ключей
        self._e_arr = []
        for e in range(self._n + 1):
            # Перебираем числа и проверяем взаимно простые ли они с e_f(n)
            if gcd(e, self._euler_func) == 1:
                self._e_arr.append(e)
        # Генерируем случайный индекс
        ind = randrange(len(self._e_arr))
        # Присваиваем из возможных ключ с этим индексом
        self._e = self._e_arr[ind]

    # Геттеры и сеттеры для полей, т.к. они с _
    # Доступны только классам, которые наследуются от RSA
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
        # Генерация приватного ключа
        # Использую класс Ring из 1 лабораторной
        e = Ring(self._euler_func, self._e)
        # Нахожу обратное от е
        invert_e, _ = e.invert()
        self._d = invert_e.num

    @property
    def d(self) -> int:
        return self._d

    @d.setter
    def d(self, d: int) -> None:
        self._d = d

    def encrypt(self, m) -> int:
        # Шифровать только, если были генерация ключа или присвоение поля e
        encrypted = None
        if self._e:
            # Использую функцию из 1 лаборатнорной для быстрого возведения
            # в степень по модулю
            encrypted, _ = fast_powers_mod(self._n, m, self._e)
        return encrypted

    def decrypt(self, c) -> int:
        # Шифровать только, если были генерация ключа или присвоение поля d
        decrypted = None
        if self._d:
            decrypted, _ = fast_powers_mod(self._n, c, self._d)
        return decrypted


def test():
    # Функция для проверки
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
