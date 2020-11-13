from fermat import *
from lab1.gui import *


class Application:
    def run(self) -> None:
        # Создать все элементы
        self._create_all_elements()
        # Запустить приложение с интерфейсом
        self._gui.start()

    def _create_all_elements(self):
        self._gui   = GraphicUI()
        self._gui.set_title('Lab №3')
        self._width = 10
        self._gui.label('n ',  1, 1, E)
        self._n_field, _ = self._gui.entry(IntVar(), 2, 1, self._width, W)
        self._gui.label('Целая часть корня из n ', 1, 2, E)
        self._sqrt_n_field, _ = self._gui.entry(IntVar(), 2, 2, self._width, W)
        text1 = 'Будем строить последовательность чисел x 1 = m + 1, x 2 = m + 2'
        text2 = ', . . . и вычислять y i = x 2 i − n, пока не получим полный квадрат.'
        self._gui.label(text1, 1, 3, W, 3)
        self._gui.label(text2, 1, 4, W, 3)
        
