import numpy as np
import matplotlib.pyplot as plt


def generate_matrix():
    rows    = 4
    columns = 100
    # Генерирую матрицу 4 х 100, заполненную нулями
    matrix  = np.zeros((rows, columns))
    return matrix, columns


def set_height_and_weight(matrix, columns):
    # Заполняю первую строку случайными значениями роста
    min_height = 25
    max_height = 200
    matrix[0]  = np.random.randint(min_height, max_height, columns)
    # Заполняю вторую строку случайными значениями веса
    min_weight = 10
    max_weight = 150
    matrix[1]  = np.random.randint(min_weight, max_weight, columns)


def show_bmi(matrix):
    # Отношение веса к квадрату роста(в метрах)
    bmi = matrix[1] / np.power(matrix[0] / 100, 2)
    print("bmi = ", bmi)


def correct_data(matrix, columns):
    # Body Mass Index или Индекс массы тела
    show_bmi(matrix)
    # Задаю среднее и дисперсию для роста
    height_mean     = 160
    height_variance = 10
    # Normal destribution
    matrix[0]       = height_mean + np.random.randn(columns) * height_variance
    # Задаю среднее и дисперсию для веса
    weight_mean     = 60
    weight_variance = 10
    matrix[1]       = weight_mean + np.random.randn(columns) * weight_variance
    # Показываю индекс массы тела после корректировки
    show_bmi(matrix)


def build_pre_graphic(ax, matrix):
    ax.set_xlabel('Рост, см')
    ax.set_ylabel('Вес, кг')
    ax.scatter(matrix[0], matrix[1])


def build_hist(ax, ratio):
    ax.set_xlabel('Отношение веса к росту')
    ax.set_ylabel('Кол-во элементов в выборке')
    ax.hist(ratio)


def glucose_simulation(variance, matrix, columns, ratio):
    # Шум
    noise     = np.random.randn(columns) * variance
    # Отношение вес/рост + шум
    matrix[2] = ratio + noise


def build_graphic_with_const_t(ax, columns, ratio, t):
    count_sick = []
    variances  = np.linspace(0, 1, columns)
    for variance in variances:
        # Для каждого значения дисперсии вычисляю шум
        noise         = np.random.randn(columns) * variance
        # Добавляю его к отношению
        current_ratio = ratio + noise
        # Считаю больных и кладу ответ в count_sick
        count_sick.append(np.count_nonzero(current_ratio > t))
    ax.set_xlabel('Значения дисперсии при t = 0.5')
    ax.set_ylabel('Кол-во больных')
    ax.plot(variances, count_sick)


def build_graphic_with_const_variance(ax, columns, ratio, variance):
    t_arr      = np.linspace(0, 1, columns)
    noise      = np.random.randn(columns) * variance
    count_sick = []
    for t in t_arr:
        current_ratio = ratio + noise
        count_sick.append(np.count_nonzero(current_ratio > t))
    ax.set_xlabel('Значения t при sigma = 0.05')
    ax.set_ylabel('Кол-во больных')
    ax.plot(t_arr, count_sick)


def main():
    matrix, columns = generate_matrix()
    set_height_and_weight(matrix, columns)
    correct_data(matrix, columns)
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    build_pre_graphic(ax1, matrix)
    # Отношение веса к росту
    ratio = matrix[1] / (matrix[0])
    build_hist(ax2, ratio)
    # Дисперсия
    variance  = 0.05
    glucose_simulation(variance, matrix, columns, ratio)
    # Уровень глюкозы
    t         = 0.5
    # Смотрю по отношению, кто болен, а кто нет
    # и кладу в последнюю строку матрицы
    matrix[3] = (matrix[2] > t).astype(int)
    build_graphic_with_const_t(ax3, columns, ratio, t)
    variance   = 0.05
    build_graphic_with_const_variance(ax4, columns, ratio, variance)
    plt.show()


main()
