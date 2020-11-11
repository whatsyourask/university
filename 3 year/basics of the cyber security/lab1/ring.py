from __future__ import annotations


class Ring:
    """Класс для выполнения операций в кольце целых чисел Z"""
    def __init__(self, n: int, num: int) -> None:
        # Конструктор с n и числом
        # Присваиваем их полям класса
        self._n   = n
        self._num = num

    @property
    def num(self) -> int:
        # Геттер для числа
        return self._num

    @num.setter
    def num(self, num: int) -> None:
        # Сеттер для числа
        self._num = num

    def __add__(self, other: Ring) -> Ring:
        # Перегрузка оператора сложения для класса Ring
        # other - второе слагаемое b в выражении a + b, a - self
        return Ring(self._n, (self._num + other.num) % self._n)

    def __sub__(self, other: Ring) -> Ring:
        # Перегрузка оператора вычитания
        if other.num < 0:
            # Если число отрицательное, то прибавляем n к нему
            other.num += self._n
        return Ring(self._n, (self._num - other.num) % self._n)

    def __mul__(self, other: Ring) -> Ring:
        # Перегрузка оператора умножения
        return Ring(self._n, (self._num * other.num) % self._n)

    def invert(self) -> Tuple:
        # Нахождение обратного
        # Получаем промежуточные вычисления из метода алгоритма Евклида
        a_arr, b_arr, mod_arr, div_arr = self._euclid_algorithm()
        x = 0
        y = 1
        # Списки для промежуточных вычислений
        x_arr = [x]
        y_arr = [y]
        # Копируем список целых от деления, чтобы не потерять результаты
        copy_div_arr = div_arr[:]
        # Выталкиваем прочерк(как в таблице, он не нужен)
        copy_div_arr.pop()
        while copy_div_arr:
            # Берём целое от деления
            last = copy_div_arr.pop()
            # Вычисляем новые x и y по формуле
            x, y = y, x - y * last
            x_arr.append(x)
            y_arr.append(y)
        # Переворачиваем списки
        x_arr.reverse()
        y_arr.reverse()
        # Сохраняем все списки промежуточных результатов в один
        result = [a_arr, b_arr, mod_arr, div_arr, x_arr, y_arr]
        return Ring(self._n, y), result

    def _euclid_algorithm(self) -> int:
        # алгоритм Евклида
        # Кладём n и число в промежуточные переменные для наглядности
        a = self._n
        b = self._num
        # Списки для сохранения промежуточных результатов
        div_arr = []
        a_arr   = [a]
        b_arr   = [b]
        mod_arr = []
        while True:
            # Находим остаток
            mod = a % b
            # Кладём в список
            mod_arr.append(mod)
            # Целое от деления
            div = a // b
            # Кладём
            div_arr.append(div)
            if not mod:
                # Если остаток равен 0, выходим из цикла
                break
            # или a = b
            # b = mod
            a, b = b, mod
            a_arr.append(a)
            b_arr.append(b)
        # Ставим None, как прочерк в таблице
        div_arr[-1] = None
        # Возвращаем все промежуточные вычисления
        return a_arr, b_arr, mod_arr, div_arr

    def __truediv__(self, other: Ring) -> Ring:
        # Перегрузка оператора деления
        # Находим обратное от делителя
        invert_other, _ = other.invert()
        # и вызываем метод умножения
        return self.__mul__(invert_other)


def test():
    # Проверка правильности
    a = Ring(26, 22)
    b = Ring(26, 15)
    c = a + b
    if c.num == 11:
        print("[+] Passed.")
    c = a - b
    if c.num == 7:
        print("[-] Passed.")
    c = a * b
    if c.num == 18:
        print("[*] Passed.")
    c, _ = b.invert()
    if c.num == 7:
        print("[invert b] Passed.")
    c, _ = a.invert()
    if c.num == 6:
        print("[invert a] Passed.")
    c = a / b
    if c.num == 24:
        print("[/] Passed.")


if __name__=='__main__':
    test()
