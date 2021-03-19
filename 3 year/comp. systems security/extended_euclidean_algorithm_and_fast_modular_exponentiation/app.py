import sys
# sys.path хранит стандартные пути, где python ищет модули для импорта
# Теперь мы можем импортить модули вне папки 2 лабораторной
sys.path.insert(0, '..')
from additive_cipher.gui import *
from backend import FastModularExponentiation, ExtendedEuclideanAlgorithm
import re


class Application:
    """Logic of application"""
    def run(self) -> None:
        # Create all elements
        self._create_all_elements()
        # Start interface
        self._gui.start()

    def _create_all_elements(self) -> None:
        # Create all needed elements
        self._gui   = GraphicUI()
        title = 'Extended Euclidean Algorithm & Fast Modular Exponentiation'
        self._gui.set_title(title)
        self._gui.label('n: ', 1, 1, E)
        width = 30
        self._n_field, _ = self._gui.entry(StringVar(), 2, 1, width, W)
        self._gui.label('a: ', 1, 2, E)
        self._a_field, _ = self._gui.entry(StringVar(), 2, 2, width, W)
        self._gui.label('b: ', 1, 3, E)
        self._b_field, _ = self._gui.entry(StringVar(), 2, 3, width, W)
        self._gui.button('Fast Modular Exponentiation', 1, 4, width, E,
                                                          self._fast_mod_exp, 2)
        self._gui.label('Mod: ', 1, 5, E)
        self._mod_field, _ = self._gui.entry(StringVar(), 2, 5, width, W)
        self._gui.label('x: ', 3, 1, E)
        self._x_field, _ = self._gui.entry(StringVar(), 4, 1, width, W)
        self._gui.label('y: ', 3, 2, E)
        self._y_field, _ = self._gui.entry(StringVar(), 4, 2, width, W)
        self._gui.button('Extended Euclidean Algorithm', 4, 3, width, E,
                                                        self._ext_euclid_alg, 2)
        self._gui.label('a: ', 3, 4, E)
        self._a2_field, _ = self._gui.entry(StringVar(), 4, 4, width, W)
        self._gui.label('b: ', 3, 5, E)
        self._b2_field, _ = self._gui.entry(StringVar(), 4, 5, width, W)
        self._gui.label('GCD: ', 3, 6, E)
        self._gcd_field, _ = self._gui.entry(StringVar(), 4, 6, width, W)


    def _fast_mod_exp(self) -> None:
        fme = FastModularExponentiation()
        n = self._n_field.get()
        a = self._a_field.get()
        b = self._b_field.get()
        try:
            self._validation(n)
            self._validation(a)
            self._validation(b)
        except ValueError:
            self._process_exception()
            return
        fme.n = int(n)
        fme.a = int(a)
        fme.b = int(b)
        mod = fme.algorithm()
        self._mod_field.set(mod)

    def _validation(self, value) -> None:
        if not value.isdigit():
            raise ValueError

    def _process_exception(self) -> None:
        # Method to create a new window on top of main window
        self._gui.message_box('Ошибка', 'Неверные данные')
        
    def __okay_button_handler(self) -> None:
        # Method to clear fields and close the top window
        self._clear_all()
        self._window.destroy()

    def _clear_all(self) -> None:
        self._clear(self._n_field)
        self._clear(self._a_field)
        self._clear(self._b_field)
        self._clear(self._mod_field)
        self._clear(self._x_field)
        self._clear(self._y_field)
        self._clear(self._a2_field)
        self._clear(self._b2_field)
        self._clear(self._gcd_field)

    def _clear(self, field) -> None:
        field.set('')

    def _ext_euclid_alg(self) -> None:
        eea = ExtendedEuclideanAlgorithm()
        x = self._x_field.get()
        y = self._y_field.get()
        try:
            self._validation(x)
            self._validation(y)
        except ValueError:
            self._process_exception()
            return
        eea.x = int(x)
        eea.y = int(y)
        a, b, gcd = eea.algorithm()
        self._a2_field.set(a)
        self._b2_field.set(b)
        self._gcd_field.set(gcd)
