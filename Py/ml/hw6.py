from sklearn.datasets import load_digits
import matplotlib.pyplot as plt
import numpy as np


class Node:
    def __init__(self, data, labels):
        self.__x = data
        self.__labels = labels
        self.__n = len(labels)
        self.left, self.right = None, None


    def __entropy(self, s):
        

    def __information_gain(self, left_x, right_x):
        gain = self.__entropy() 


    def divide_data(self):
        best_gain = 0
        for x_i in self.__x:
            for t in range(0, 17):
                for i in x_i:
                    if i<t:
                        left_x.append(i)
                    else:
                        right_x.append(i)
                    gain = self.__information_gain(left_x, right_x)
                    better = gain > best_gain
                    if better:
                        best_gain = gain


    def get_child(self, child):
        


class DecisionTree:
    def __init__(self, data, labels, labels_name):
        self.__x = data
        self.__labels = labels
        self.__n = len(labels)
        self.__main_root = None
    

    def __shuffle(self):
        indexes = np.arange(self.__n)
        np.random.shuffle(indexes)
        indexes_len = len(indexes)
        self.__train_indexes = indexes[:np.int32(0.8 * indexes_len)]
        self.__test_indexes = indexes[np.int32(0.8 * indexes_len):
                np.ind32(indexes_len)]

    
    def __build(self):
        self.__main_root = Node(self.__data[self.__train_indexes],
                self.__labels[self.__train_indexes])
        self.__main_root.divide_data()


    def teach(self, t_begin, t_end):
        self.__t_begin = t_begin
        self.__t_end = t_begin
        self.__shuffle()
        self.__build()
