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
        self.__this_depth = Node.__depth


    def set_max_depth(self, tree_depth):
        # Сеттер для максимальной глубины дерева
        Node.__max_depth = tree_depth


    def __entropy(self, s, labels):
        # Вычисление энтропии
        entropy = 0
        s_len = len(s)
        for i in range(10):
            k_len = len([label for label in labels if label == i])
            if k_len == 0:
                continue
            div = np.float128(k_len/s_len)
            entropy -= div * np.log(div)
        return entropy


    def __information_gain(self, *child_indexes):
        # Вычисление прироста информации
        sum_child_entropy = 0
        s_len = len(self.__x)
        for i in range(2):
            if child_indexes[i]:
                child_len = len(self.__labels[child_indexes[i]])
                div = child_len/s_len
                sum_child_entropy -= div * self.__entropy(
                        self.__x[child_indexes[i]],
                        self.__labels[child_indexes[i]]
                        )
        gain = self.__entropy(self.__x, self.__labels) + sum_child_entropy
        return gain


    def __confidence(self):
        # Вычисление вектора уверенности на основе меток,
        # переданных в конструктор
        conf_vector = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for label in self.__labels:
            conf_vector[label] += 1
        return conf_vector


    def divide_data(self):
        # Деление в узле
        # Если не максимальная глубина, делить
        # Надо добавить ещё 2 критерия остановки
        if self.__this_depth < Node.__max_depth:
            print("divide")
            best_gain = 0
            self.__best_left = []
            self.__best_right = []
            print(np.shape(self.__labels))
            # Цикл по столбцам матрицы данных
            # или по координатам данных,
            # Например, координата 0 для всех данных
            for column in range(len(self.__x[0])):
                # Цикл перебора t
                for t in range(0, 17):
                    left, right = [], []
                    # Цикл перебора координат 0 для каждого объекта
                    for row in range(len(self.__x[:,column])):
                        if self.__x[row, column] < t:
                            left.append(row)
                        else:
                            right.append(row)
                    gain = self.__information_gain(left, right)
                    better = gain > best_gain
                    # Если прирост информации лучше, чем был, то 
                    # Сохранить все лучшие параметры
                    if better:
                        best_gain = gain
                        self.__best_left = left
                        self.__best_right = right
                        self.__best_column = column
                        self.__best_t = t
            print(f"best gain: {best_gain}")
            # Создание потомков и запуск деления данныx
            # если в потомки передаются не пустые массивы
            print(f"best left length {np.shape(self.__x[self.__best_left])}\n"
                f"best right length {np.shape(self.__x[self.__best_right])}")
            if self.__this_depth >= Node.__depth:
                Node.__depth += 1 
            print(f"depth: {self.__this_depth}\n")
            if self.__best_left:
                self.left = Node(self.__x[self.__best_left],
                        self.__labels[self.__best_left]
                        )
                self.left.divide_data()
                print(f'this_depth: {self.__this_depth} back')
            if self.right is None:
                if self.__best_right:
                    self.right = Node(self.__x[self.__best_right],
                            self.__labels[self.__best_right]
                            )
                    self.right.divide_data()
        else:
            # Вычислить вектор уверенности в терминальном узле
            self.__conf_vector = self.__confidence()
            # Обозначить, что этот узел терминальный
            # для будущего метода прохода по дереву
            self.__is_terminal = True
            # Дальше поведение ещё не определено


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
        self.__main_root.set_max_depth(3)
        # Запуск деления данных, рекурсивно
        self.__main_root.divide_data()


    def teach(self):
        # Обучение дерева
        self.__shuffle()
        self.__build()


data = load_digits()
tree = DecisionTree(data.data, data.target, data.target_names)
tree.teach()
