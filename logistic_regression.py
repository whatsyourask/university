from sklearn.datasets import load_digits
import matplotlib.pyplot as plt
import numpy as np


class LogisticRegression:
    def __init__(self, data=None, labels=None, labels_name=None):
        # Конструктор, принимающий на вход данные, их метки,
        # и названия параметров
        # Инициализировать данные
        self.__x = data
        # Инциализировать массив меток
        self.__labels = labels
        # Инициализировать длину меток
        self.__n = len(labels)
        # Инициализировать кол-во классов
        self.__k = len(labels_name)
        # Инициализировать пустую матрицу Y
        self.__y = np.float128(np.empty([self.__n, self.__k]))
        # Инициализировать списка для сбора E(w, b) и
        # accuracy в ходе итерации
        self.__e_w_b_arr = [[],[]]
        self.__acc_arr = [[],[]]
      

    def __preparation(self):
        # Вычислить вектор средних отклонений
        mean = np.mean(self.__x, 0)
        # Вычислить вектор стандартных отклонений
        std = np.std(self.__x, 0)
        # Отнять вектор средних и
        # разделить на вектор стандартных отклонений
        for i in range(len(self.__x)):
            self.__x[i] -= mean
            for j in range(len(std)):
                # Делить, если не ноль 
                if std[j]!=0:
                    self.__x[i][j] /= std[j]
    
    
    def __shuffle(self):
        # Рандомизировать данные и метки 
        # Задать массив индексов 
        self.__ind_arr = np.arange(self.__n) 
        # Рандомизировать его 
        np.random.shuffle(self.__ind_arr) 
        ind_arr_len = len(self.__ind_arr) 
        # Поделить 80 на 20 
        self.__train_ind_arr = self.__ind_arr[:np.int32(0.8 
            * ind_arr_len)] 
        self.__valid_ind_arr = self.__ind_arr[np.int32(0.8 
            * ind_arr_len):np.int32(ind_arr_len)]
            

    def __one_hot_encoding(self):
        # Представление данных в one-hot_encoding
        # Инициализировать матрицу one-hot encoding нулями
        self.__t = np.zeros((self.__n, self.__k))
        # Заполнить в нужных столбцах единицы
        for label, row in zip(self.__labels, self.__t):
            row[label]=1
    

    def __softmax(self, z):
        # Вычисление y = Softmax(Wx+b)
        e_z = np.exp(z)
        sum_e_z = sum(e_z)
        y = e_z/sum_e_z
        return y 


    def __calculate_y_i(self, x_i):
       # print(type(x_i))
        # Вычисление i-ого вектора уверенности y
        # Вычислить z
        z_i = (self.__w @ x_i) + self.__b
        # Найти максимум 
        max_z_i = max(z_i)
        # Вычесть максимум из каждого элемента
        z_i -= max_z_i 
        # Передать softmax
        return self.__softmax(z_i)

    
    def __calculate_y(self, ind_arr):
        # Вычиcление всей матрицы y
        for i in ind_arr:
            self.__y[i] = self.__calculate_y_i(self.__x[i])


    def __calculate_e_w_b(self, ind_arr, mode):
        # Вычисление целевой функции, y и кол-во TruePositive 
        # В зависимости от mode и ind_arr
        # она будет вычислять либо для обучающей, либо для валидационной выборок
        # Инициализировать нулями списки
        self.__e_w_b.append(0)
        self.__tp.append(0)
        # Цикл для вычисления E(W, b)
        for i in ind_arr:
            self.__y[i] = self.__calculate_y_i(self.__x[i])
            ln_y = np.log(self.__y[i])
            # Вычислить сумму произведений массивов t_i и ln_y
            t_y = self.__t[i] @ ln_y
            # Вычислить разность(из-за минуса) сумм
            self.__e_w_b[mode] -= t_y
            # Вычислить индекс максимального в векторе уверенности
            ind_max_y = np.argmax(self.__y[i])
            # Вычислить условие: совпадает ли индекс максимального
            # в векторе уверенности с индексом в векторе меток
            ind_1 = self.__t[i, ind_max_y] == 1
            if ind_1:
                self.__tp[mode] += 1
            

    def __grad_w(self, ind_arr):
        # Вычисление градиента от W
        return (self.__y[ind_arr] - self.__t[ind_arr]).T @ self.__x[ind_arr]

    
    def __grad_b(self, ind_arr):
        # Вычисление градиента от b
        return (self.__y[ind_arr] - self.__t[ind_arr]).T @ np.ones(len(ind_arr))


    def __calculate_acc(self, mode, count):
        # Вычисление accuracy
        # Опять же в зависимости от mode и count
        # происходит вычисление либо для обучающей, либо для валидационной выборки
        self.__accuracy.append(self.__tp[mode]/count)


    def __gradient_descent(self, gamma, sigma):
        # Вычислить стартовые w и b
        self.__w = np.float128(sigma * np.random.rand(self.__k, len(self.__x[0])))
        self.__b = np.float128(sigma * np.random.rand(self.__k))
        # Вычислить стартовую матрицу y для дальнейшего вычисления градиентов
        self.__calculate_y(self.__train_ind_arr)
        # Метки для списков e_w_b, tp и accuracy
        train = 0
        valid = 1
        # Инициализировать переменную для сравнения 
        # с точностью на валидац. выборке
        best_acc = 0
        # Кол-во итераций
        iter_num = 100
        self.__iteration = 0
        # Установить условия вхождения в цикл в True
        iteration_end = True
        acc_is_best = True
        while iteration_end and acc_is_best:
            # Вычислить новые w и b
            self.__w = self.__w - gamma * self.__grad_w(self.__train_ind_arr)
            self.__b = self.__b - gamma * self.__grad_b(self.__train_ind_arr)
            # Инициализировать списки, где будут храниться
            # e_w_b и tp для обуч. и валид. выборок
            self.__e_w_b = []
            self.__tp = []
            self.__calculate_e_w_b(self.__train_ind_arr, train)
            self.__calculate_e_w_b(self.__valid_ind_arr, valid)
            # Инициализация аналогично e_w_b и tp
            self.__accuracy = []
            self.__calculate_acc(train, len(self.__train_ind_arr))
            self.__calculate_acc(valid, len(self.__valid_ind_arr))
            # Вывод данных по итерации в консоль
            print(f"{self.__iteration}\ttrain: E(w, b) = {self.__e_w_b[train]}")
            print(f"\ttrain: Accuracy = {self.__accuracy[train]}")
            print(f"\tvalid: E(w, b) = {self.__e_w_b[valid]}")
            print(f"\tvalid: Accuracy = {self.__accuracy[valid]}\n")
            # Проверить точность, лучше ли она, чем предыдущая
            acc_is_best = self.__accuracy[valid] > best_acc
            if acc_is_best:
                best_acc = self.__accuracy[valid]
            # Добавить в массивы всех E(w,b) и Accuracy
            # для обуч. и валид. выборок
            self.__e_w_b_arr[train].append(self.__e_w_b[train])
            self.__e_w_b_arr[valid].append(self.__e_w_b[valid])
            self.__acc_arr[train].append(self.__accuracy[train])
            self.__acc_arr[valid].append(self.__accuracy[valid])
            self.__iteration += 1
            # Проверить, что итерация не последняя
            iteration_end = self.__iteration < iter_num
        print(f"Best Accuracy = {best_acc}")
        # Найти лучшую целевую функцию на валид. выборке
        min_e_w = np.min(self.__e_w_b_arr)
        print(f"Best E(w, b) = {min_e_w}")
        self.__e_w_b_arr[train] = np.array(self.__e_w_b_arr[train])
        self.__e_w_b_arr[valid] = np.array(self.__e_w_b_arr[valid])
        self.__acc_arr[train] = np.array(self.__acc_arr[train])
        self.__acc_arr[valid] = np.array(self.__acc_arr[valid])
        self.__iteration = np.arange(self.__iteration)
    

    def teach(self, gamma, sigma):
        # Функция для обучения
        self.__preparation()
        self.__shuffle()
        self.__one_hot_encoding()
        self.__gradient_descent(gamma, sigma)

    
    def draw(self):
        # Метки для обуч. и валид. выборок
        train = 0
        valid = 1
        # Шаблоны для заголовков графиков
        template_title = "График зависимости {}\n от номера итерации для {} выборки"
        template_e = "целевой функции"
        template_acc = "точности"
        template_train = "обучающей" 
        template_valid = "валидационной"
        fig, axs = plt.subplots(2, 2)
        axs[0, 0].set_title(template_title.format(template_e, template_train))
        axs[0, 0].plot(self.__iteration, self.__e_w_b_arr[train])
        axs[0, 1].set_title(template_title.format(template_e, template_valid))
        axs[0, 1].plot(self.__iteration, self.__e_w_b_arr[valid])
        axs[1, 0].set_title(template_title.format(template_acc, template_train))
        axs[1, 0].plot(self.__iteration, self.__acc_arr[train])
        axs[1, 1].set_title(template_title.format(template_acc, template_valid))
        axs[1, 1].plot(self.__iteration, self.__acc_arr[valid])
        plt.show()
    

    def prediction(self, test_data):
        return np.argmax(self.__calculate_y_i(test_data))       


digits = load_digits()
lr = LogisticRegression(digits.data[10:], digits.target[10:], digits.target_names)
gamma = 0.001
sigma = 0.01
lr.teach(gamma, sigma)
lr.draw()
print(f"Предсказан класс: {lr.prediction(digits.data[9])}")
