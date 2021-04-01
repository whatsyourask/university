import sys
# To import FastModularExponentiation
sys.path.insert(0, '..')
from additive_cipher.gui import *
from backend import miller_rabin_generate, euler_func


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
        title = 'RSA Algorithm'
        self._gui.set_title(title)
        width = 30
        self._gui.label('Bits', 1, 1, W)
        self._bits_field, _ = self._gui.entry(StringVar(), 2, 1, width, W)
        self._gui.button('Generate', 3, 1, width, W, self._generate)
        self._gui.label('p', 1, 2, W)
        self._p_field, _ = self._gui.entry(StringVar(), 2, 2, width, W)
        self._gui.label('q', 1, 3, W)
        self._q_field, _ = self._gui.entry(StringVar(), 2, 3, width, W)
        self._gui.label('n', 1, 4, W)
        self._n_field, _ = self._gui.entry(StringVar(), 2, 4, width, W)
        self._gui.label('Euler func', 1, 5, W)
        self._euler_func_field, _ = self._gui.entry(StringVar(), 2, 5, width, W)

    def _generate(self) -> None:
        try:
            self._p_field.set('')
            self._q_field.set('')
            self._n_field.set('')
            self._euler_func_field.set('')
            bits_len = int(self._bits_field.get())
            if bits_len < 8:
                raise ValueError
            p = miller_rabin_generate(bits_len)
            self._p_field.set(p)
            q = miller_rabin_generate(bits_len)
            self._q_field.set(q)
            n = p * q
            self._n_field.set(n)
            euler_func_result = euler_func(n)
            self._euler_func_field.set(euler_func_result)
        except ValueError:
            self._process_exception()


    def _process_exception(self) -> None:
        # Method to create a new window on top of main window
        self._gui.message_box('Ошибка', 'Неверные данные')
