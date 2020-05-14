from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt
import numpy as np


class Clustering:
    def __init__(self,
            x,
            max_clusters_count,
            points_count,
            iterations_count
            ):
        self.__x = x
        self.__max_clusters_count = max_clusters_count
        self.__points_count = points_count
        self.__iterations_count = iterations_count


    def k_means(self):
        # Алгоритм k-means
        # Вектор целевых ошибок для каждого кол-ва кластеров
        self.__e = np.zeros(self.__max_clusters_count)
        # Вектор лучших центроидов для каждого кол-ва кластеров 
        self.__best_centroids = np.zeros(
                (
                    self.__max_clusters_count,
                    self.__max_clusters_count,
                    2
                    )
                )
        # Цикл по кол-ву кластеров
        for count in range(1, self.__max_clusters_count + 1):
            # Вектор центроидов с предыдущей итерации
            self.__prev_centroids = np.zeros((count, 2))
            # Рандомный выбор индексов точек для центроидов
            centroids_ind = np.random.randint(0,
                    self.__points_count,
                    count
                    )
            # Назначение этих точек центроидами
            self.__centroids = self.__x[centroids_ind]
            # Цикл для определения лучших центроидов 
            # и нахождения целевой функции для k-ого кол-ва центроидов
            for iteration in range(self.__iterations_count):
                # Вектор всех точек с минимальным расстоянием
                # до центроидов
                self.__cluster_points_sum = np.zeros((count, 2))
                # Вектор кол-ва точек в кластерах
                self.__cluster_points_count = np.zeros(count)
                point_e = 0
                # Цикл по всем точкам 
                for point in self.__x:
                    # Прибавить минимальное расстояние от точки
                    # до центроида к целевой функции для этой итерации
                    point_e += self.__min_distance(count, point) ** 2
                # Посмотреть не выполняются ли критерии остановки
                # Изменились ли центроиды или
                # не последняя ли это итерация
                stopping_criteria = (self.__update_centroids(count) or 
                        iteration == self.__iterations_count - 1)
                if stopping_criteria:
                    # Если остановка, то сохранить все 
                    self.__save(count, point_e)
        # Найти оптимальное кол-во кластеров
        opt_count = self.__find_opt()
        print(f'e = {self.__e}')
        print(f'd = {self.__d}')
        print(f'optimal count = {opt_count}')
        self.__draw(opt_count)


    def __min_distance(self, count, point):
        # Найти минимальное расстояние от точки до всех центроидов
        # Вектор расстояний от центроидов до точки
        distances = np.zeros(count)
        # Цикл по центроидам
        for number in range(count):
            distances[number] = self.__distance(
                    self.__centroids[number],
                    point
                    )
        min_ind = np.argmin(distances)
        # Положить точку по номеру центроида для нахождения суммы
        self.__cluster_points_sum[min_ind] += point
        # Увеличить кол-во точек для центроида 
        # для подсчёта кол-ва его точек
        self.__cluster_points_count[min_ind] += 1
        return distances[min_ind]


    def __distance(self, centroid, point):
        diff_x = centroid[0] - point[0]
        diff_y = centroid[1] - point[1]
        return np.sqrt(diff_x ** 2 + diff_y ** 2)


    def __update_centroids(self, count):
        # Обновление центроидов и сохранение предыдущих
        # Переменная для проверки критерия, что центроиды меняются
        is_not_immutable = True
        for number in range(count):
            self.__prev_centroids[number] = self.__centroids[number]
            # Если в кластере есть точки, то поменять его
            if self.__cluster_points_count[number]:
                self.__centroids[number] = self.__cluster_points_sum[number]/\
                self.__cluster_points_count[number]
            # Если центроиды изменились, то не останавливаться
            not_changed =  (self.__prev_centroids[number] ==
                    self.__centroids[number]).all()
            if not_changed: 
                is_not_immutable = False
        return is_not_immutable


    def __save(self, count, point_e):
        # Сохранение целевой функции после прохода 
        self.__e[count - 1] = point_e
        # Сохранение лучших центроидов для кластеров размера k
        for number in range(count):
            self.__best_centroids[count - 1, number] =\
                    self.__centroids[number]

    
    def __find_opt(self):
        # Найти оптимальное кол-во кластеров
        # Инициализация вектора критериев оптимальности
        self.__d = np.zeros(self.__max_clusters_count - 2)
        # Вычисление критериев оптимальности
        for count in range(1, self.__max_clusters_count - 1):
            numerator = abs(self.__e[count] - self.__e[count + 1])
            denumerator = abs(self.__e[count - 1] - self.__e[count])
            self.__d[count - 1] = np.float128(numerator / denumerator)
        return np.argmin(self.__d) + 1

    
    def __draw(self, opt_count):
        # Отображение графиков
        # Цвета для кластеров
        colors = self.__color_distribution(opt_count)
        fig, axes = plt.subplots(3, 1)
        # 1..10 для графика e
        counts = np.linspace(1,
                self.__max_clusters_count,
                self.__max_clusters_count
                )
        template = 'График зависимости {} кластеризации oт количества кластеров'
        e_template = 'целевой функции задачи'
        d_template = 'критерия оптимальности'
        axes[0,].set_title(template.format(e_template))
        x_label = 'Кол-во кластеров'
        axes[0,].set_xlabel(x_label)
        axes[0,].set_ylabel('Целевая функция')
        axes[0,].plot(counts, self.__e)
        # 2..9 т.к. для 1 и 10 кол-ва кластеров нельзя вычислить d
        counts = np.linspace(2,
                self.__max_clusters_count-1,
                self.__max_clusters_count-2
                ) 
        axes[1,].set_title(template.format(d_template))
        axes[1,].set_xlabel(x_label)
        axes[1,].set_ylabel('Критерий оптимальности')
        axes[1,].plot(counts, self.__d)
        # Раскидать точки по x и y c разными цветами для каждого кластера
        axes[2,].scatter(self.__x[:,0], self.__x[:,1], 5, c=colors)
        # Раскидать центроиды для каждого кластера
        # Координаты берутся из вектора,
        # который по номеру кол-ва центроидов
        # хранит координаты лучших центроидов
        axes[2,].scatter(self.__best_centroids[opt_count,:opt_count + 1,0],
                self.__best_centroids[opt_count ,:opt_count + 1,1],
                50,
                c='red',
                marker='*'
                )
        plt.show()


    def __color_distribution(self, opt_count):
        colors = []
        # Кол-во возможных кластеров
        counts = np.linspace(1,
                self.__max_clusters_count,
                self.__max_clusters_count
                ) 
        # Снова пройтись по каждой точке
        # только для оптимального кол-ва кластеров
        for point in self.__x:
            distances = np.zeros(opt_count + 1)
            # По каждому кластеру из этого кол-ва
            for number in range(opt_count + 1):
                # Найти расстояние точки до каждого кластера
                distances[number] =self.__distance(
                        self.__best_centroids[opt_count, number],
                        point
                        )
            # Выделить номер кластера с минимальным расстоянием
            # и положить его в лист цветов для раскраски
            colors.append(counts[np.argmin(distances)])
        return colors


centers = [[-1, -1], [0, 1], [1, -1]]
n = 3000
x, _ = make_blobs(n_samples=n, centers=centers, cluster_std=0.5)
k = 10
iterations = 10
clust = Clustering(x, k, n, 10)
clust.k_means()
