import csv
import numpy as np
from typing import List
from time import time


class LogisticRegression:
    def __init__(self, data, labels) -> None:
        # Конструктор, что принимает данные и метки
        self._data   = data
        self._labels = labels
        # Кол-во данных
        self._n = labels.shape[0]
        # Кол-во характеристик
        self._k = data.shape[1]

    def teach(self, gamma: float, sigma: float, iter_count: int) -> None:
        # Метод для обучения модели
        start_time = time()
        # Нормализация данных
        self._normalization()
        # Рандомизация данных
        self._shuffle()
        self._gamma   = gamma
        self._sigma   = sigma
        # Берём обучающую выборку
        self._x = self._data[self._train_ind_arr]
        self._t = self._labels[self._train_ind_arr]
        # Делаем градиентный спуск
        self._gradient_descent(iter_count)
        # Вычисляем точность
        train_accuracy = self._calculate_accuracy()
        print(f'train accuracy = {train_accuracy}')
        end_time = time()
        print(f'Time = {end_time - start_time} sec')

    def test(self) -> None:
        # Берём тестовую выборку
        self._x = self._data[self._test_ind_arr]
        self._t = self._labels[self._test_ind_arr]
        # Вычисляем точность
        test_accuracy = self._calculate_accuracy()
        print(f'test accuracy = {test_accuracy}')

    def predict(self, data):
        self._x = np.array(data)
        self._b = np.copy(self._best_b)
        self._calculate_y()
        return self._y

    def _normalization(self):
        # Находим среднее
        mean = np.mean(self._data, 0)
        # Находим вектор стандартных отклонений
        std  = np.std(self._data, 0)
        self._data -= mean
        self._data /= std

    def _shuffle(self) -> None:
        # Рандомизировать данные и метки
        # Задать массив индексов
        self._ind_arr = np.arange(self._n)
        # Рандомизировать его
        np.random.shuffle(self._ind_arr)
        ind_arr_len = len(self._ind_arr)
        # Поделить 80 на 20
        self._train_ind_arr = self._ind_arr[:np.int32(0.8 * ind_arr_len)]
        self._test_ind_arr = self._ind_arr[np.int32(0.8
            * ind_arr_len):np.int32(ind_arr_len)]

    def _gradient_descent(self, iter_count: int) -> None:
        # Инициализация весов
        self._b = np.float64(self._sigma * np.random.rand(self._k))
        # Вычисляем начальную функцию правдоподобия и объявляем её максимальной
        self._calculate_y()
        self._b += self._gamma * self._grad_l_b()
        max_likelihood_func = self._likelihood_func()
        # Это считается за 1 итерацию, поэтому остаётся на 1 итерацию меньше
        iter_count -= 1
        self._best_b = np.copy(self._b)
        while iter_count:
            self._calculate_y()
            self._b += self._gamma * self._grad_l_b()
            cur_likelihood_func = self._likelihood_func()
            if cur_likelihood_func > max_likelihood_func:
                max_likelihood_func = cur_likelihood_func
                self._best_b = np.copy(self._b)
            iter_count -= 1
        print(f'Max likelihood function = {max_likelihood_func}')
        print(f'Best B = {self._best_b}')

    def _calculate_y(self) -> None:
        # Классификатор
        self._temp = np.array(1 / (1 + np.exp(-self._x @ self._b)))
        self._y    = np.int_(self._temp > 0.5)

    def _grad_l_b(self):
        # Градиент функции правдоподобия
        return (self._t - self._y).T @ self._x

    def _likelihood_func(self):
        # Функция правдоподобия
        return np.sum(np.log((self._temp ** self._t)
                                        * ((1 - self._temp) ** (1 - self._t))))

    def _calculate_accuracy(self):
        # Точность
        # Берём лучшие коэффициенты
        self._b = np.copy(self._best_b)
        # Пропускаем наши данные через классификатор
        self._calculate_y()
        # Возвращаем точность
        # как кол-во правильно угаданных на общее кол-во данных
        return np.sum(self._y == self._t) / self._x.shape[0]


def get_data_from_csv(filename: str):
    # Функция для изъятия данных из файла
    # Открываем файл
    f = open(filename, newline='')
    # Создаем объект для чтения формата .csv
    reader = csv.reader(f, delimiter=' ', quotechar='|')
    data   = []
    # Читаем построчно, форматируем и добавляем в общий список данных
    for row in reader:
        row = ''.join(row)[1:][:-1].split(',')
        data.append(row)
    # Преобразуем список в массив numpy,
    # отрезая первую строку матрицы с обозначением характеристик
    data = np.array(data[1:], dtype=np.float32)
    return data


def main():
    data   = get_data_from_csv('titanic.csv')
    labels = data[:, 0]
    data   = data[:,1:]
    l      = LogisticRegression(data, labels)
    gamma  = 0.001
    sigma  = 0.01
    l.teach(gamma, sigma, 1000)
    l.test()
    print(l.predict([3, 0, 20, 0, 0, 70]))

main()
