from fermat import *
from lab1.gui import *
from time import time


class Application:
    def run(self) -> None:
        # Создать все элементы
        self._create_all_elements()
        # Запустить приложение с интерфейсом
        self._gui.start()

    def _create_all_elements(self) -> None:
        self._gui   = GraphicUI()
        self._gui.set_title('Lab №3')
        self._width = 12
        self._gui.label('n ',  1, 1, E)
        self._n_field, _ = self._gui.entry(IntVar(), 2, 1, self._width, W)
        self._gui.label('Целая часть корня из n ', 1, 2, E)
        self._sqrt_n_field, _ = self._gui.entry(IntVar(), 2, 2, self._width, W)
        text1 = 'Будем строить последовательность чисел x 1 = m + 1, x 2 = m + 2'
        text2 = ', . . . и вычислять y i = x 2 i − n, пока не получим полный квадрат.'
        self._gui.label(text1, 1, 3, W, 4)
        self._gui.label(text2, 1, 4, W, 4)
        self._x_entries = []
        self._y_entries = []
        self._gui.button('Разложение методом Ферма', 2, 5,
                                self._width * 2, W, self._calculate, 4)
        self._graphic_data = {}
        self._gui.button('Построить график', 2, 6,
                                self._width * 2, W, self._view_graphic, 4)
        self._gui.button('Очистить данные графика', 2, 7,
                                self._width * 2, W, self._remove_data, 4)


    def _calculate(self) -> None:
        start = time()
        n = self._n_field.get()
        f = Fermat(n)
        result = f.factorization()
        self._sqrt_n_field.set(result[0])
        self._table_pos = [2, 8]
        self._create_table(result[1], result[2])
        self._gui.label('Разложение', 1, 11, E)
        self._result_field, _ = self._gui.entry(StringVar(), 2, 11,
                                                                 self._width, W)
        self._result_field.set(str(result[3]) + ' * ' + str(result[4]))
        self._gui.label('(x_i - y_i) / (x_i + y_i)', 3, 11, W, 3)
        end = time()
        self._gui.label('Время разложения', 1, 12, E)
        self._time_field, _ = self._gui.entry(IntVar(), 2, 12,
                                                          self._width * 2, W, 2)
        calculation_time = end - start
        self._graphic_data[n] = calculation_time
        self._time_field.set(calculation_time)


    def _create_table(self, x_arr: List, y_arr: List) -> None:
        length = len(x_arr)
        if self._x_entries and self._y_entries:
            self._delete_old_table()
        self._x_entries = []
        self._y_entries = []
        self._gui.label('Таблица вычислений', self._table_pos[0] - 1,
                        self._table_pos[1], E)
        self._x_entries.append(self._gui.entry(StringVar(), self._table_pos[0],
                                        self._table_pos[1], self._width, W))
        self._x_entries[0][0].set('X')
        self._y_entries.append(self._gui.entry(StringVar(), self._table_pos[0],
                                        self._table_pos[1] + 1, self._width, W))
        self._y_entries[0][0].set('Y')
        for i in range(length):
            self._x_entries.append(self._gui.entry(IntVar(),
                                                   self._table_pos[0] + i + 1,
                                                   self._table_pos[1],
                                                   self._width,
                                                   W))
            self._x_entries[-1][0].set(x_arr[i])
            self._y_entries.append(self._gui.entry(IntVar(),
                                                   self._table_pos[0] + i + 1,
                                                   self._table_pos[1] + 1,
                                                   self._width,
                                                   W))
            self._y_entries[-1][0].set(y_arr[i])

    def _delete_old_table(self) -> None:
        length = len(self._x_entries)
        for i in range(length):
            self._x_entries[i][1].grid_remove()
            self._y_entries[i][1].grid_remove()

    def _view_graphic(self) -> None:
        if len(self._graphic_data) > 20:
            return
        sorted_data = sorted(self._graphic_data.items(),
                             key=lambda item: item[0])
        x = list(map(lambda item: item[0], sorted_data))
        y = list(map(lambda item: item[1], sorted_data))
        self._gui.graphic(x, y)

    def _remove_data(self) -> None:
        self._graphic_data = {}
