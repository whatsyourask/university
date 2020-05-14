import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# Создание массива координат
def c_arr(n, a, b):
    x = (b - a) * np.random.random_sample(n) + a
    return x

# Проверка точки в окружности
def in_circle(x, y, sh):
    return (x - sh)**2 + (y - sh)**2 <= 1

# Вычисление числа пи
def calculate_pi(n, a, b, x, y, sh):
    s = 0
    for i in range(n):
        if in_circle(x[i], y[i], sh):
            s += 1
    ratio = s/n # Доля точек, попавших внутрь
    pi = ratio*(b - a)**2
    return pi

# Функция для отображения пункта с
def draw(a, b, n, ax1, x, y, sh, max_b):
    t_x, t_y, f_x, f_y = [], [], [], [] # Массивы t_x и t_y для точек, попавших внутрь окружности, f_x и f_y - для непопавших
    for i in range(n): 
        if in_circle(x[i], y[i], sh):
            t_x.append(x[i])
            t_y.append(y[i])
        else:
            f_x.append(x[i])
            f_y.append(y[i])
    circle = plt.Circle((sh, sh), 1, fill=False) # Рисуем круг с центром в точке sh
    rect = plt.Rectangle((a, a), 2, 2, fill=False, color='green') # Рисуем квадрат
    ax1.set_xlim(0, max_b) # Назначаем границы для x
    ax1.set_ylim(0, max_b) # Назначаем границы для y
    ax1.set_title('Случайное бросание N точек')
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.add_artist(circle) 
    ax1.add_artist(rect) 
    ax1.scatter(t_x, t_y, a, color='red') # Точки, попавшие внутрь
    ax1.scatter(f_x, f_y, a, color='blue') # Точки, не попавшие внутрь
    
# Функция для отображения пункта b
def create_dependence(a, b, x, y, sh, ax2):
    n = np.linspace(1, 5000, 5000)
    pi_arr = []
    print(n)
    for i in n:
        x_new = x[0:int(i)]
        y_new = y[0:int(i)]
        print(i)
        pi_arr.append(calculate_pi(int(i), a, b, x_new, y_new, sh))
    ax2.plot(n, pi_arr)
    ax2.set_title('График зависимости оценки числа пи от количества точек')
    ax2.set_xlabel('Количество точек')
    ax2.set_ylabel('Оценка числа пи')

# Функция, для выполнения задания =Р
def complete_task():
    # Координаты границ квадрата по x
    a = 0.5
    b = 2.5
    n = 5000
    # sh и max_b реализованы, если понадобится менять a и b
    sh = (a + b)/2 
    max_b = a + b
    # Создаём массивы координат
    x = c_arr(n, a, b)
    y = c_arr(n, a, b)
    fig, (ax1, ax2) = plt.subplots(1, 2)
    draw(a, b, n, ax1, x, y, sh, max_b)
    create_dependence(a, b, x, y, sh, ax2)
    plt.show()


complete_task()       
