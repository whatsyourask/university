def gcd(a, b) -> int:
    # Вычисление НОД
    # Запись a, b = b, a аналогична swap(a, b) в С++
    # или
    # temp = a
    # a = b
    # b = temp
    while b:
        a, b = b, a % b
    return a


def euler_func(n) -> int:
    # Вычисление функции Эйлера
    # Начинаем с n - 1
    temp  = n - 1
    # Переменная для подсчёта
    count = 0
    while temp:
        if not gcd(n, temp) - 1:
            count += 1
        temp -= 1
    return count


def test():
    # Проверка правильности выполнения
    n      = 1000
    result = euler_func(n)
    answer = 400
    if answer == result:
        print('Passed')


if __name__=='__main__':
    # Если модуль запущен как `python3 euler.py`, то выполнить функцию проверки
    # при импорте этого модуля в другом месте это выполняться не будет.
    test()
