from typing import List, Tuple


def to_binary(b) -> List:
    # Конвертирование числа в бинарное представление
    binary = []
    # Пока не получим единицу при делении на 2
    while b != 1:
        # Добавляем остаток в список
        binary.append(b % 2)
        # Делим нацело
        b //= 2
    # В конце добавляем единицу
    binary.append(b)
    # Переворачиваем список и получаем бинарный вид
    binary.reverse()
    # Вид в списке поэтому -> List
    return binary


def fast_powers_mod(n, a, b) -> Tuple:
    # Быстрое возведение в степень по модулю
    # Получение бинарного вида
    binary     = to_binary(b)
    # Список для сохранения промежуточных вычислений, изначально там число a
    temp_arr   = [a]
    temp       = a
    # [1:] - получить копию списка с 1 элемента по последний
    # отрезаем 1 элемент, т.к. мы его не вычисляем
    for e in binary[1:]:
        # Считаем следующий по формуле
        temp = (a * (temp ** 2)) % n if e else (temp ** 2) % n
        # Кладём в список
        temp_arr.append(temp)
    # Возвращаем кортеж с результатом и списком вида
    # [список с 1 и 0, список с вычисленными для них значениями]
    return temp, [binary, temp_arr]


def test():
    # Проверка правильности работы функций
    n = 527
    a = 24
    b = 117
    result, _, _ = fast_powers_mod(n, a, b)
    answer = 232
    if result == answer:
        print('Passed')


if __name__=='__main__':
    test()
