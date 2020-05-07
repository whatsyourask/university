from sklearn.datasets import load_digits
import matplotlib.pyplot as plt
import numpy as np


class Node:
    __depth = 0
    __max_depth = None
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
        Node.__max_depth = tree_depth


    def __entropy(self, s, labels):
        # Вычисление энтропии
        entropy = 0
        s_len = len(s)
        for i in range(0, 10):
            k_len = len([label for label in labels if label == i])
            if k_len == 0:
                continue
            div = np.float128(k_len/s_len)
            entropy -= div * np.log(div)
        # print(f"entropy: {entropy}")
        return entropy


    def __information_gain(self, x_i, *child_x):
        # Вычисление прироста информации
        sum_child_entropy = 0
        for i in range(2):
            if child_x[i]:
                sum_child_entropy -= self.__entropy(child_x[i], child_x[i+2])
        gain = self.__entropy(x_i, self.__labels) + sum_child_entropy
        #print(f'\tgain = {gain}')
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
        if Node.__depth != Node.__max_depth:
            print("divide")
            best_gain = 0
            # Цикл по столбцам матрицы данных
            # или по координатам данных,
            # Например, координата 0 для всех данных
            for column in range(len(self.__x[0])):
                # Цикл перебора t
                for t in range(0, 17):
                    left_x, right_x = [], []
                    left_labels, right_labels = [], []
                    # Цикл перебора координат 0 для каждого объекта
                    for row in range(len(self.__x[:,column])):
                        if self.__x[row, column] < t:
                            left_x.append(self.__x[row])
                            left_labels.append(self.__labels[row])
                        else:
                            right_x.append(self.__x[row])
                            right_labels.append(self.__labels[row])
                    print(f"")
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
            print(f"best gain: {best_gain}") 
            # Увеличение глубины всего дерева
            Node.__depth += 1
            # Создание потомков и запуск деления данныx
            self.left = Node(np.array(left_x), np.array(left_labels))
            self.right = Node(np.array(right_x), np.array(right_labels))
            self.left.divide_data()
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
                np.int32(indexes_len)]

    
    def __build(self):
        # Построение дерева
        # Создание корня дерева
        self.__main_root = Node(self.__x[self.__train_indexes],
                self.__labels[self.__train_indexes])
        self.__main_root.set_max_depth(4)
        # Запуск деления данных, рекурсивно
        self.__main_root.divide_data()


    def teach(self):
        # Обучение дерева
        self.__shuffle()
        self.__build()


data = load_digits()
tree = DecisionTree(data.data, data.target, data.target_names)
tree.teach()
