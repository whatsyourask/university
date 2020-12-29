from MillerRabin import *
from lab1.gui import *
from time import time


class Application:
    def run(self) -> None:
        # Создать все элементы
        self._create_all_elements()
        # Запустить приложение с интерфейсом
        self._gui.start()

    def _create_all_elements(self) -> None:
        # Метод для создания начальных элементов интерфейса
        # Создание объекта для графики из лабораторной 1
        self._gui   = GraphicUI()
        self._gui.set_title('Lab №3')
        self._width = 12
