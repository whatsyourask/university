import sys
# sys.path хранит стандартные пути, где python ищет модули для импорта
# Теперь мы можем импортить модули вне папки 2 лабораторной
sys.path.insert(0, '..')
import lab1
import math
from typing import Tuple, List


class Fermat:
    """Класс для метода факторизации Ферма"""
    def __init__(self, n=None) -> None:
        # Конструктор, что принимает нечётное число n
        self._n = n

    def factorization(self) -> Tuple:
        # Метод факторизации  Ферма
        # Вычисляем квадратный корень от n и округляем в меньшую сторону
        m = math.trunc(math.sqrt(self._n))
        # Переменная для остановки цикла при нахождении полного квадрата
        full_sqrt_not_found = True
        # Присваиваем начальное значение x равное m
        x     = m
        # Списки для вычисленных x и y
        x_arr = []
        y_arr = []
        while full_sqrt_not_found:
            x += 1
            # Добавляем x в список
            x_arr.append(x)
            # Вычисляем y
            y = x ** 2 - self._n
            # Добавляем y в список
            y_arr.append(y)
            # Вычисляем квадратный корень от y
            sqrt_y = math.sqrt(y)
            # Округляем корень от y
            trunc_sqrt_y = math.trunc(sqrt_y)
            # Вычисляем разницу между квадратом от y и округлённым квадратом
            double = (sqrt_y - trunc_sqrt_y)
            # Если разницы нет, т.е. число без плавующей точки,
            # то выходим из цикла
            if not double:
                full_sqrt_not_found = False
        # Меняем тип квадрата
        sqrt_y = int(sqrt_y)
        # Берём максимальный из x, что последний в списке
        max_x  = x_arr[-1]
        # По формулам вычисляем два множителя
        first  = max_x + sqrt_y
        second = max_x - sqrt_y
        # Возвращаем всё в формате:
        # m, иксы, игреки, полный квадрат, первый множитель, второй множитель
        return m, x_arr, y_arr, sqrt_y, first, second


def test():
    # Для проверки
    n = 3007
    f = Fermat(n)
    answer = (54,
              [55, 56, 57, 58, 59, 60, 61, 62, 63, 64],
              [18, 129, 242, 357, 474, 593, 714, 837, 962, 1089],
              33,
              97,
              31)
    result = f.factorization()
    print(f'm = {result[0]}')
    print(f'x = {result[1]}')
    print(f'y = {result[2]}')
    print(f'first = {result[3]}')
    print(f'second = {result[4]}')
    if result == answer:
        print('Test passed.')


if __name__=='__main__':
    test()
