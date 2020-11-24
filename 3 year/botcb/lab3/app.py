from fermat import *
from lab1.gui import *


class Application:
    def run(self) -> None:
        # Создать все элементы
        self._create_all_elements()
        # Запустить приложение с интерфейсом
        self._gui.start()

    def _create_all_elements(self) -> None:
        self._gui   = GraphicUI()
        self._gui.set_title('Lab №3')
        self._width = 10
        self._gui.label('n ',  1, 1, E)
        self._n_field, _ = self._gui.entry(IntVar(), 2, 1, self._width, W)
        self._gui.label('Целая часть корня из n ', 1, 2, E)
        self._sqrt_n_field, _ = self._gui.entry(IntVar(), 2, 2, self._width, W)
        self._gui.label('Результат', 1, 3, E)
        self._result_field, _ = self._gui.entry(IntVar(), 2, 3, self._width, W)
        text1 = 'Будем строить последовательность чисел x 1 = m + 1, x 2 = m + 2'
        text2 = ', . . . и вычислять y i = x 2 i − n, пока не получим полный квадрат.'
        self._gui.label(text1, 1, 4, W, 3)
        self._gui.label(text2, 1, 5, W, 3)
        self._gui.button('Разложение методом Ферма', 1, 6,
                                self._width * 3, W, self._calculate)

    def _calculate(self) -> None:
        n = self._n_field.get()
        f = Fermat(n)
        result = f.factorization()
        self._sqrt_n_field.set(result[0])
        self._table_pos = [2, 7]
        self._create_table(result[1], result[2])

    def _create_table(self, x_arr: List, y_arr: List) -> None:
        length = len(x_arr)
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
