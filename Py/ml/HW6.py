from sklearn.datasets import load_digits
import matplotlib.pyplot as plt
import numpy as np


class Node:
    # Промежуточная глубина дерева
    __depth = 0
    # Максимальная глубина дерева
    __max_depth = None
    # Граница по энтропии
    __entropy_bound = None
    # Граница по кол-ву входящих данных в узел
    __count_bound = None
    # Кол-во возможных классов(в нашем случае 10)
    __class_count = None
    __confusion_matrix = None
    def __init__(self, data, labels):
        self.__x = data
        self.__labels = labels
        self.__n = len(labels)
        self.left, self.right = None, None
        self.__child_count = 2
        self.__conf_vector = None
        self.__is_terminal = False
        self.__this_depth = Node.__depth


    def set_max_depth(self, depth):
        # Сеттер для максимальной глубины дерева
        Node.__max_depth = depth


    def set_min_entropy(self, entropy):
        # Сеттер для минимальной энтропии
        Node.__entropy_bound = entropy

    
    def set_min_data_count(self, count):
        # Сеттер для минимального кол-ва входных данных в узел
        Node.__count_bound = count;

    
    def set_class_count(self, count):
        # Сеттер для кол-ва классов для классификации
        Node.__class_count = count
        Node.__confusion_matrix = np.zeros((count, count))


    def __entropy(self, s, labels):
        # Вычисление энтропии
        entropy = 0
        s_len = len(s)
        class_counts = np.unique(labels, return_counts=True)
        for counts in class_counts[1]:
            div = counts/s_len 
            entropy -= div * np.log(div)
        return entropy


    def __information_gain(self, *child_indexes):
        # Вычисление прироста информации
        sum_child_entropy = 0
        for i in range(self.__child_count):
            if child_indexes[i]:
                child_len = len(self.__labels[child_indexes[i]])
                div = child_len/self.__n
                sum_child_entropy -= div * self.__entropy(
                        self.__x[child_indexes[i]],
                        self.__labels[child_indexes[i]]
                        )
        gain = self.__parent_entropy + sum_child_entropy
        return gain


    def __confidence(self):
        # Вычисление вектора уверенности на основе меток,
        # переданных в конструктор
        conf_vector = np.zeros(Node.__class_count)
        for label in self.__labels:
            conf_vector[label] += 1
        return np.array(conf_vector)/self.__n


    def __create_childs(self):
        # Увеличение глубины дерева, т.к. появляются новые потомки
        Node.__depth += 1 
        # Если поделенные части не пустые, то создать потомков
        if self.__best_left:
            self.left = Node(self.__x[self.__best_left],
                    self.__labels[self.__best_left]
                    )
        if self.__best_right:
            self.right = Node(self.__x[self.__best_right],
                    self.__labels[self.__best_right]
                    )
        # Рекурсивно делить данные в потомках
        if self.left:
            self.left.divide_data() 
        if self.right:
            self.right.divide_data()
        # Уменьшить глубину дерева, 
        # т.к. после деления у потомков идёт возврат к родителю
        # Для соблюдения условий построения дерева в остальных ветках
        Node.__depth -= 1
        

    def __assign_terminal(self):
        # Вычислить вектор уверенности в терминальном узле
        self.__conf_vector = self.__confidence()
        # Обозначить, что этот узел терминальный
        self.__is_terminal = True
        # Вычислить какой класс является предсказанным в этом узле
        conf_class = np.argmax(self.__conf_vector)
        # Вычислить кол-во каждого класса в узле
        class_counts = np.unique(self.__labels, return_counts=True)
        # Суммировать в матрицу
        for i in range(len(class_counts[0])):
            Node.__confusion_matrix[conf_class, 
                    class_counts[0][i]] += np.float64(class_counts[1][i])


    def divide_data(self):
        # Деление в узле
        # Если не максимальная глубина и 
        # eсли энтропия от данных не меньше или не равна границе и
        # если кол-во данных не является минимальным, то делить
        reached_depth  = self.__this_depth < Node.__max_depth
        self.__parent_entropy = self.__entropy(self.__x, self.__labels)
        entropy_is_greater = self.__parent_entropy > Node.__entropy_bound
        count_is_greater = self.__n > Node.__count_bound
        if reached_depth and entropy_is_greater and count_is_greater:
            self.__best_gain = 0
            self.__best_left = []
            self.__best_right = []
            # Цикл по столбцам матрицы данных
            # или по координатам данных,
            # например, координата 0 для всех данных
            for column in range(len(self.__x[0])):
                # Цикл перебора t
                for t in range(17):
                    left, right = [], []
                    # Цикл перебора координат 0 для каждого объекта
                    for row in range(len(self.__x[:,column])):
                        if self.__x[row, column] < t:
                            left.append(row)
                        else:
                            right.append(row)
                    gain = self.__information_gain(left, right)
                    better = gain > self.__best_gain
                    # Если прирост информации лучше, чем был, то 
                    # Сохранить все лучшие параметры
                    if better:
                        self.__best_gain = gain
                        self.__best_left = left
                        self.__best_right = right
                        self.__best_column = column
                        self.__best_t = t
            self.__create_childs()
        else:
            self.__assign_terminal()   
        return


    def __calculate_acc(self):
        # Вычисление точности 
        true_positive = 0
        # Вычислить кол-во правильно предсказанных
        for i in range(Node.__class_count):
            true_positive += Node.__confusion_matrix[i,i]
        # Поделить на общее кол-во предсказаний
        self.__acc = true_positive/self.__n

    
    def print_accuracy(self):
        # Вывод точности
        self.__calculate_acc()
        print(self.__acc)


    def print_confusion_matrix(self):
        # Вывод матрицы
        print(Node.__confusion_matrix)


class DecisionTree:
    def __init__(self, data, labels, labels_name):
        self.__x = data
        self.__labels = labels
        self.__n = len(labels)
        self.__class_count = len(labels_name)
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
        self.__main_root.set_class_count(self.__class_count)
        # Назначить границы остановок
        self.__main_root.set_max_depth(15)
        self.__main_root.set_min_entropy(0.1)
        self.__main_root.set_min_data_count(5)
        # Запуск деления данных, рекурсивно
        self.__main_root.divide_data()


    def teach(self):
        # Обучение дерева
        self.__shuffle()
        self.__build()
        # Вывести значение accuracy и confusion matrix
        self.__main_root.print_accuracy()
        self.__main_root.print_confusion_matrix()


    def test(self):
        return


data = load_digits()
tree = DecisionTree(data.data, data.target, data.target_names)
tree.teach()
