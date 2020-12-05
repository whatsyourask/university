import csv
import numpy as np
from typing import List


class LogisticRegression:
    def __init__(self, data, labels) -> None:
        self._x      = data
        self._labels = labels
        self._n      = len(labels)
        self._k      = len(data[0])

    def teach(self, gamma: float, sigma: float, iter_count: int) -> None:
        self._normalization()
        self._shuffle()
        self._gradient_descent(gamma, sigma, iter_count)

    def _normalization(self):
        mean = np.mean(self._x, 0)
        std  = np.std(self._x, 0)
        self._x -= mean
        self._x /= std

    def _shuffle(self) -> None:
        # Рандомизировать данные и метки
        # Задать массив индексов
        self._ind_arr = np.arange(self._n)
        # Рандомизировать его
        np.random.shuffle(self._ind_arr)
        ind_arr_len = len(self._ind_arr)
        # Поделить 80 на 20
        self._train_ind_arr = self._ind_arr[:np.int32(0.8
            * ind_arr_len)]
        self._test_ind_arr = self._ind_arr[np.int32(0.8
            * ind_arr_len):np.int32(ind_arr_len)]

    def _gradient_descent(self, gamma: float, sigma: float, iter_count: int) -> None:
        self._b = np.float128(sigma * np.random.rand(self._k))
        self._calculate_y(self._train_ind_arr)
        self._b += gamma * self._grad_l_b(self._train_ind_arr)
        max_likelihood_func = self._likelihood_func(self._train_ind_arr)
        print(f'Max likelihood function = {max_likelihood_func}')
        iter_count -= 1
        best_b = self._b
        while iter_count:
            self._calculate_y(self._train_ind_arr)
            self._b += gamma * self._grad_l_b(self._train_ind_arr)
            cur_likelihood_func = self._likelihood_func(self._train_ind_arr)
            print(cur_likelihood_func)
            if cur_likelihood_func > max_likelihood_func:
                print('Found MAX')
                max_likelihood_func = cur_likelihood_func
                best_b = self._b
            iter_count -= 1
            print(iter_count)
        print(f'Max likelihood function = {max_likelihood_func}')

    def _calculate_y(self, ind_arr: List) -> None:
        self._temp = 1 / (1 + np.exp(-self._b.T @ self._x[ind_arr].T))
        print(self._temp)
        self._temp2 = np.ones(self._x[ind_arr].shape[0]) - self._temp
        print(self._temp2)
        self._y    = [1 if item > 0.5 else 0 for item in self._temp]
        print(self._y)
        print(len(self._y))
        print(self._labels[ind_arr])
        print(len(self._labels[ind_arr]))

    def _grad_l_b(self, ind_arr: List):
        return (self._y - self._labels[ind_arr]).T @ self._x[ind_arr]

    def _likelihood_func(self, ind_arr):
        return np.sum(np.log((self._temp ** self._labels[ind_arr]) * ((1 - self._temp) ** self._labels[ind_arr])))

    def _calculate_accuracy(self, ind_arr: List):
        return np.sum(self._y == self._labels) / self._x[ind_arr].shape[0]


def get_data_from_csv(filename: str):
    f = open(filename, newline='')
    reader = csv.reader(f, delimiter=' ', quotechar='|')
    data = []
    for row in reader:
        row = ''.join(row)[1:][:-1].split(',')
        data.append(row)
    data = np.array(data[1:], dtype=np.float32)
    return data


def main():
    data = get_data_from_csv('titanic.csv')
    print(data)
    labels = data[:, 0]
    data = data[:,1:]
    l = LogisticRegression(data, labels)
    gamma = 0.001
    sigma = 0.01
    l.teach(gamma, sigma, 1)


main()
