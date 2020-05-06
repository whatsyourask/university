from sklearn.datasets import load_digits
import matplotlib.pyplot as plt
import numpy as np


class Node:
    depth = 0
    max_depth = None
    def __init__(self, data, labels):
        self.__x = data
        self.__labels = labels
        self.__n = len(labels)
        self.left, self.right = None, None
        self.__child_count = 2
        self.__conf_vector = None
        self.__is_terminal = False


    def set_max_depth(self, tree_depth):
        # Сеттер для максимальной глубины дерева
        max_depth = tree_depth


    def __entropy(self, s, labels):
        # Вычисление энтропии
        entropy = 0
        for i in range(0, 10):
            s_len = len(s)
            k_len = len([label for label in labels if label == i])
            div = k_len/s_len
            entropy -= div * np.log(div)
        return entropy


    def __information_gain(self, x_i, *child_x):
        # Вычисление прироста информации
        sum_child_entropy = 0
        for i in range(2):
            sum_child_entropy -= self.__entropy(child_x[i], child_x[i+2])
        gain = self.__entropy(x_i, self.__labels) + sum_child_entropy
        return gain
        
    def __confidence(self):
        # Вычисление вектора уверенности на основе меток, переданных в конструктор
        conf_vector = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for label in self.__labels:
            conf_vector[label] += 1
        return conf_vector


    def divide_data(self):
        # Деление в узле
        # Если не максимальная глубина, делить
        # Надо добавить ещё 2 критерия остановки
        if depth != max_depth:
            best_gain = 0
            # Цикл по столбцам матрицы данных
            # или по координатам данных,
            # Например, координата 0 для всех данных
            for column in range(len(self.__x[0])):
                # Цикл перебора t
                for t in range(0, 17):
                    # Цикл перебора координат 0 для каждого объекта
                    for i in range(self.__n):
                        if i < t:
                            left_x.append(self.__x[i])
                            left_labels.append(self.__labels[i])
                        else:
                            right_x.append(self.__x[i])
                            right_labels.append(self.__labels[i])
                        gain = self.__information_gain(self.__x[:,column],
                                left_x, right_x, left_labels, right_labels)
                        better = gain > best_gain
                        # Если прирост информации лучше, чем был, то 
                        # Сохранить все лучшие параметры
                        # Возможно, best_left_x, best_right_x не нужны
                        if better:
                            best_gain = gain
                            best_left_x = left_x
                            best_right_x = right_x
                            best_column = column
            # Увеличение глубины всего дерева
            depth += 1
            # Создание потомков и запуск деления данных
            self.left = Node(left_x, left_labels)
            self.left.divide_data()
            self.right = Node(right_x, right_labels)
            self.right.divide_data()
        else:
            # Вычислить вектор уверенности в терминальном узле
            self.__conf_vector = self.__confidence()
            # Обозначить, что этот узел терминальный
            # для будущего метода прохода по дереву
            self.__is_terminal = True
            # Дальше поведение ещё не определено
        return


class DecisionTree:
    def __init__(self, data, labels, labels_name):
        self.__x = data
        self.__labels = labels
        self.__n = len(labels)
        self.__main_root = None
    
    
    def __shuffle(self):
        # Деление данных на обучающую и тестовую выборки
        indexes = np.arange(self.__n)
        np.random.shuffle(indexes)
        indexes_len = len(indexes)
        self.__train_indexes = indexes[:np.int32(0.8 * indexes_len)]
        self.__test_indexes = indexes[np.int32(0.8 * indexes_len):
                np.ind32(indexes_len)]

    
    def __build(self):
        # Построение дерева
        # Создание корня дерева
        self.__main_root = Node(self.__data[self.__train_indexes],
                self.__labels[self.__train_indexes])
        # Запуск деления данных, рекурсивно
        self.__main_root.divide_data()


    def teach(self, t_begin, t_end):
        # Обучение дерева
        self.__t_begin = t_begin
        self.__t_end = t_begin
        self.__shuffle()
        self.__build()
