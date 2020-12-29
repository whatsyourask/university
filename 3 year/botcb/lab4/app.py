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
        self._width = 13
        self._gui.label('n ',  1, 1, E)
        self._n_field, _ = self._gui.entry(IntVar(), 2, 1, self._width, W)
        self._gui.label('a ', 1, 2, E)
        self._a_field, _ = self._gui.entry(IntVar(), 2, 2, self._width, W)
        self._gui.label('t ', 1, 3, E)
        self._t_field, _ = self._gui.entry(IntVar(), 2, 3, self._width, W)
        self._gui.label('Результат ', 1, 4, E)
        self._result_field, _ = self._gui.entry(StringVar(), 2, 4,
                                                            self._width, W)
        self._gui.button('Определить', 2, 5,
                                self._width, W, self._define_number)
        self._gui.label('Интервал ', 1, 6, E)
        self._begin_field, _ = self._gui.entry(IntVar(), 2, 6, self._width, W)
        self._end_field, _   = self._gui.entry(IntVar(), 3, 6, self._width, W)
        self._gui.label('а в исследовании', 1, 7, E)
        self._research_a_field, _ = self._gui.entry(IntVar(), 2, 7,
                                                                self._width, W)
        self._text = None
        self._gui.button('Исследовать', 2, 8,
                                self._width, W, self._research)

    def _define_number(self) -> None:
        # Метод для кнопки определения простоты
        n = self._n_field.get()
        result, (a, t) = miller_rabin_test(n)
        self._a_field.set(a)
        self._t_field.set(t)
        result = 'Простое' if result else 'Составное'
        self._result_field.set(result)

    def _research(self) -> None:
        # Метод для исследования числа ошибочных заключений теста
        a     = self._research_a_field.get()
        begin = self._begin_field.get()
        end   = self._end_field.get()
        start = time()
        mistakes, wrong_numbers = research(begin, end, a)
        end   = time()
        calculation_time = end - start
        explanation = 'Время вычисления: ' + str(calculation_time) + '\n'
        explanation += 'Количество ошибок: ' + str(mistakes) + '\n'
        explanation += 'Ошибки:\n' + wrong_numbers
        text_width = (self._width + 4) * 3
        text_height = 7
        if self._text:
            self._text.grid_remove()
        self._text = self._gui.text(1, 9, text_width, text_height, W, 3)
        self._text.insert(INSERT, explanation)
