import numpy as np


def char2ascii_code(char: str) -> int:
    # Получение кода ASCII в кодировке cp1251
    return char.encode('cp1251')[0]


def code2binary(code: int) -> str:
    # Перевод кода в бинарное представление
    return '{0:08b}'.format(code)


def binary2polynom(binary: str) -> str:
    # Получение полинома из бинарного представления
    return np.poly1d(list(map(int, binary)))


def shift_binary(binary: str, shift: int) -> str:
    # сдвиг бинарного представления
    return binary + '0' * shift


def divide_polynoms(polynom1: str, polynom2: str) -> tuple:
    # Деление полиномов
    return np.polydiv(polynom1.c, polynom2.c)


def add_polynoms(polynom1: str, polynom2: str) -> list:
    # Сложение полиномов
    return np.polyadd(polynom1.c, polynom2.c)


def task1(char: str) -> str:
    code = char2ascii_code(char)
    print('Исходный символ:\n\t', char, code)
    binary = code2binary(code)
    print('Бинарное представление символа:\n\t', binary)
    polynom = binary2polynom(binary)
    print('Полином:\n', polynom)
    # сформировать «сдвинутый» на n-k позиций информационный многочлен
    # (его степень не выше n-1).
    shift = 5
    shifted_binary = shift_binary(binary, shift)
    print('Сдвинутое бинарное представление:\n\t', shifted_binary)
    shifted_polynom = binary2polynom(shifted_binary)
    print('Сдвинутый информационный многочлен: \n', shifted_polynom)
    g_x = '00111101'
    print('Бинарное представление порождающего многочлена:\n\t', g_x)
    g_x_polynom = binary2polynom(g_x)
    print('Порождающий многочлен:\n', g_x_polynom)
    # найти остаток от деления этого многочлена на порождающий многочлен.
    _, remainder = divide_polynoms(shifted_polynom, g_x_polynom)
    remainder %= 2
    remainder_polynom = binary2polynom(remainder)
    print('Остаток от деления сдвинутого информационного многочлена \
на порождающий многочлен:\n', remainder_polynom)
    # сформировать кодовый многочлен как сумму «сдвинутого»
    # информационного многочлена и остатка.
    code_polynom_binary = add_polynoms(shifted_polynom, remainder_polynom) % 2
    code_polynom = binary2polynom(code_polynom_binary)
    # Записать полученное кодовое слово.
    print('Бинарное представление кодового многочлена:\n\t', code_polynom_binary)
    print('Сформированный кодовый многочлен:\n', code_polynom)
    print('*'* 85)
    return code_polynom_binary


def task2(alphabet: str) -> list:
    # Для каждого символа из 1-ой лабораторной выполняем 1-ый пункт.
    code_polynoms = []
    for char in alphabet:
        code_polynoms.append(task1(char))
    return code_polynoms


def compare_polynoms(polynom1: str, polynom2: str) -> int:
    # Подсчёт количества неравных разрядов между полиномами
    diff_count = 0
    for bit1, bit2 in zip(polynom1, polynom2):
        if bit1 != bit2:
            diff_count += 1
    return diff_count


def task3(code_polynoms: list) -> None:
    # Вычислить параметры кода.
    n = 13
    k = 8
    length = len(code_polynoms)
    diff_counts = []
    for i in range(length):
        for j in range(length):
            diff_count = compare_polynoms(code_polynoms[i], code_polynoms[j])
            if diff_count:
                diff_counts.append(diff_count)
    # Находим минимум среди подсчитанных значений
    d = min(diff_counts)
    r = k / n
    print('Длина кодового слова:\n\t', n)
    print('Количество информационных разрядов:\n\t', k)
    print('Минимальное кодовое расстояние:\n\t', d)
    print('Скорость передачи:\n\t', r)
    print('*' * 85)


def task4(code_polynoms: list) -> None:
    #  Внести одиночную ошибку и найти синдром.
    # Порождающий многочлен
    g_x = '00111101'
    g_x_polynom = binary2polynom(g_x)
    length = len(code_polynoms[0])
    for code_polynom in code_polynoms:
        print('Кодовый многочлен без ошибки:\n\t', ''.join(map(str, code_polynom)))
        # Делаем ошибку в случайном разряде
        ind = np.random.randint(0, length)
        code_polynom[ind] += 1
        code_polynom[ind] %= 2
        print('Кодовый многочлен с ошибкой:\n\t', ''.join(map(str, code_polynom)))
        # Находим синдром как остаток от деления кодового многочлена на порождающий
        _, syndrom = divide_polynoms(binary2polynom(code_polynom), g_x_polynom)
        syndrom %= 2
        print('Синдром:\n\t', ''.join(map(str, map(int, syndrom))))
        print('-' * 40)


def main():
    char = 'в'
    task1(char)
    alphabet = 'ЛМНОП'
    code_polynoms = task2(alphabet)
    task3(code_polynoms)
    task4(code_polynoms)


if __name__=='__main__':
    main()
