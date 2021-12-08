import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt


def create_matrix_a(n: int, polynomial: np.array) -> np.array:
    # Функция создания матрицы A
    # Создаём столбец из нулей
    zeros = np.zeros((n - 1, 1))
    # Создаём диагональную матрицу
    diag_matrix = np.eye(n - 1)
    # Присоединяем столбец к матрице слева
    left_concatenated_matrix = np.concatenate((zeros, diag_matrix), axis=1)
    # Присоединияем вектор коэффициентов к матрице снизу
    down_concatenated_matrix = np.concatenate((left_concatenated_matrix, polynomial), axis=0)
    return down_concatenated_matrix


def create_watermark(n: int, matrix_a: np.array, s: np.array, polynomial: np.array) -> np.array:
    # Функция создания водяного знака
    period = 2 ** n - 1
    watermark = []
    for i in range(period):
        # Вычисляем s(k) = a * s(k - 1)
        new_s = matrix_a.dot(s) % 2
        # Вычисляем w(k) = D * a * s(k)
        temp = np.dot(polynomial, new_s) % 2
        # Заменяем 0 на -1
        new_watermark = temp if temp else -1
        watermark.append(new_watermark)
        s = new_s
    return watermark


def search_watermark(filename: str, watermark: np.array) -> tuple:
    # Берём файл
    rate, data         = wavfile.read(filename)
    # Делаем корреляцию сигнала и водяного знака
    correlated_data    = np.correlate(data, watermark, mode='valid')
    # Ищем позицию водяного знака
    watermark_position = np.argmax(correlated_data)
    return correlated_data, watermark_position


def show_results(correlated_data: np.array, watermark_position: int) -> None:
    # Вывод в консоль позицию водяного знака и показ графика корреляции
    print(f'Позиция знака: {watermark_position}')
    plt.figure()
    plt.plot(correlated_data)
    plt.title('График корреляции сигнала с водяным знаком.')
    plt.show()


def main():
    n = 11
    s = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
    # 1+x^9+x^11
    # Коэффициенты неприводимого многочлена
    # Не берём последний, т.к. у нас вектор -p0, -p1, ..., -pN-1
    polynomial = np.array([[1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]])
    matrix_a   = create_matrix_a(n, polynomial)
    watermark  = create_watermark(n, matrix_a, s, polynomial)
    filename   = 'watermark.wav'
    correlated_data, watermark_position = search_watermark(filename, watermark)
    show_results(correlated_data, watermark_position)


if __name__=='__main__':
    main()
