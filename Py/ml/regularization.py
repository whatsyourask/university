import numpy as np
import matplotlib.pyplot as plt

# Создать датасет
def create_dataset(x, t, N):
    index_arr = np.arange(N) # Массив для индексов
    np.random.shuffle(index_arr) # Перемешать массив
    # Взять индексы для обучающей выборки
    train_index_arr = index_arr[:np.int32(0.8 * len(index_arr))]
    # Взять индексы для валидацонной выборки
    valid_index_arr = index_arr[np.int32(0.8 * len(index_arr)) :
            np.int32(0.9 * len(index_arr))]
    # Взять индексы для тестовой выборки
    test_index_arr = index_arr[np.int32(0.9 * len(index_arr)) :
            np.int32(len(index_arr))]
    # Присваиваем соответствующим x и t 
    x_train, t_train = x[train_index_arr], t[train_index_arr]
    x_valid, t_valid = x[valid_index_arr], t[valid_index_arr]
    x_test, t_test = x[test_index_arr], t[test_index_arr]
    return x_train, t_train, x_valid, t_valid, x_test, t_test

# Вычислить значения y
def calculate_y(x, basic_funcs, w):
    fi = calculate_fi(basic_funcs, x)
    y = fi @ w.T
    return y

# Вычислить ошибку
def calculate_e(w, basic_funcs, x, t):
    y = calculate_y(x, basic_funcs, w)
    e = np.sum((y - t)**2)/2
    return e

# Вычислить матрицу плана
def calculate_fi(basic_funcs, x):
    n = len(x)
    m = len(basic_funcs) + 1
    # Сразу заполняем единицами
    fi = np.ones((n, m))
    ''' 1 столбец оставляем единицами,
    поэтому [: ,i + 1]'''
    for i in range(0, m-1):
        fi[: ,i + 1] = basic_funcs[i](x)
    return fi

# Вычислить w
def calculate_w(basic_funcs, cur_lambda, x, t):
    m = len(basic_funcs) + 1
    fi = calculate_fi(basic_funcs, x)
    w = np.linalg.inv(fi.T @ fi + cur_lambda * np.eye(m))@ fi.T @ t
    return w

# Найти лучшие параметры
def find_best_parameters(x_train, t_train, x_valid,
        t_valid, x_test, t_test, N):
    # Массив лямбд
    lambda_arr = np.array([0, 0.000000000000001, 0.000000000001,
        0.000000001, 0.00000001, 0.0000001, 0.000001, 0.0001,
        0.001, 0.01, 0.1, 0.5, 1, 5, 10, 50, 100, 500, 1000,
        5000, 10000])
    # Массив функций
    basic_funcs_arr = [np.sin, np.cos, np.tan, np.exp, np.sqrt,
            lambda x: x**2, lambda x: x**3,
            lambda x: x**4, lambda x: x**5,
            lambda x: x**6, lambda x: x**7,
            lambda x: x**8, lambda x: x**9,
            lambda x: x**10, lambda x: x**11,
            lambda x: x**12, lambda x: x**13]
    iter_count = 5000 # Количество итераций в цикле
    min_e = 10**10 # Принять за минимальную e для проверки
    # Инициализировать переменные для лучших значений
    best_lambda = None
    best_basic_funcs = None
    best_w = None
    best_fi = None
    ''' Вычислить в цикле w, basic_funcs, lambda, e
    Сравнить e с минимальной e
    Если она меньше, то сделать текущую e минимальной
    Также присвоить параметры соответствующим параметрам'''
    for ind_l_func_arr in range(iter_count):
        cur_lambda = np.random.choice(lambda_arr)
        # Взять часть из массива функций
        cur_basic_funcs = np.random.choice(basic_funcs_arr, 
                np.random.randint(len(basic_funcs_arr)), replace=False)
        cur_w = calculate_w(cur_basic_funcs, cur_lambda,
                x_train, t_train)
        cur_e = calculate_e(cur_w, cur_basic_funcs, 
                x_valid, t_valid)
        found = cur_e < min_e
        if found:
            best_lambda = cur_lambda
            best_basic_funcs = cur_basic_funcs
            best_w = cur_w
            min_e = cur_e
    # Вычислить целевую функцию по лучшим параметрам и у
    regular_e  = calculate_e(best_w, best_basic_funcs,
            x_test, t_test)
    print(best_lambda) # Вывод в консоль
    print(best_basic_funcs)
    print(regular_e)
    return best_lambda, best_basic_funcs

# Выполнить задачу
def complete_task():
    # Задать начальное условие
    N = 1000
    x = np.linspace(0, 1, N)
    z = 20 * np.sin(2 * np.pi * 3 * x) + 100 * np.exp(x)
    error = 10 * np.random.randn(N)
    t = z + error
    # Получить соответствующие массивы x и t для каждой выборки
    x_train, t_train, x_valid, t_valid, x_test, t_test = create_dataset(x, t, N)
    # Получить лучшие параметры
    best_lambda, best_basic_funcs = find_best_parameters(x_train, t_train, x_valid,
            t_valid, x_test, t_test, N)
    # Вычислить y по лучшим параметрам
    y = calculate_y(x, best_basic_funcs, calculate_w(best_basic_funcs, best_lambda, x, t))
    fig, ax = plt.subplots()
    ax.plot(x, z) # Построить график z(x)
    # Построить график t(x) в виде точек
    ax.scatter(x, t, 1, color='green') 
    ax.plot(x, y)
    plt.show()


complete_task()
