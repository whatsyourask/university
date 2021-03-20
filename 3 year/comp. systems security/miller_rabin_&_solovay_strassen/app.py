import sys
# sys.path хранит стандартные пути, где python ищет модули для импорта
# Теперь мы можем импортить модули вне папки 2 лабораторной
sys.path.insert(0, '..')
from additive_cipher.gui import *
from backend import MillerRabin, SolovayStrassen
from secrets import randbits
from math import log2


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
        title = 'MillerRabinTest & SolovayStrassenTest'
        self._gui.set_title(title)
        width = 30
        self._answer_map = { True: 'probably prime', False: 'composite'}
        self._gui.label('Number', 1, 1, W)
        self._num_field, _ = self._gui.entry(StringVar(), 2, 1, width, W)
        self._gui.label('Rounds', 1, 2, W)
        self._rounds_field, _ = self._gui.entry(StringVar(), 2, 2, width, W)
        self._gui.button('Miller-Rabin test', 3, 1, width, W,
                            self._miller_rabin_test)
        self._gui.button('Solovay-Strassen test', 3, 2, width, W,
                            self._solovay_strassen_test)
        self._gui.label('Answer', 1, 3, W)
        self._answ_field, _ = self._gui.entry(StringVar(), 2, 3, width, W)
        self._gui.label('Bits', 1, 4, W)
        self._bits_field, _ = self._gui.entry(StringVar(), 2, 4, width, W)
        self._gui.label('Result', 1, 5, W)
        self._res_field = self._gui.text(2, 5, width, 5, W)
        self._gui.button('Miller-Rabin generation', 3, 4, width, W,
                            self._miller_rabin_generate_number)
        self._gui.button('Solovay-Strassen generation', 3, 5, width, W,
                            self._solovay_strassen_generate_number)
        self._gui.button('Clear', 3, 6, width, W, self._clear)

    def _miller_rabin_test(self):
        try:
            n = int(self._num_field.get())
            counts = int(self._rounds_field.get())
            answer = self._answer_map[MillerRabin.test(n, counts)]
            self._answ_field.set(answer)
        except ValueError:
            self._process_exception()

    def _process_exception(self) -> None:
        # Method to create a new window on top of main window
        self._gui.message_box('Ошибка', 'Неверные данные')

    def _solovay_strassen_test(self):
        try:
            n = int(self._num_field.get())
            counts = int(self._rounds_field.get())
            answer = self._answer_map[SolovayStrassen.test(n, counts)]
            self._answ_field.set(answer)
        except ValueError:
            self._process_exception()

    def _miller_rabin_generate_number(self):
        try:
            self._res_field.delete("1.0", END)
            bits = int(self._bits_field.get())
            num = randbits(bits)
            while not MillerRabin.test(num, int(log2(num))):
                num = randbits(bits)
            self._res_field.insert(INSERT, str(num))
        except ValueError:
            self._process_exception()

    def _solovay_strassen_generate_number(self):
        try:
            self._res_field.delete("1.0", END)
            bits = int(self._bits_field.get())
            num = randbits(bits)
            while not SolovayStrassen.test(num, int(log2(num))):
                num = randbits(bits)
            self._res_field.insert(INSERT, str(num))
        except ValueError:
            self._process_exception()

    def _clear(self):
        self._res_field.delete("1.0", END)
        self._num_field.set('')
        self._rounds_field.set('')
        self._answ_field.set('')
        self._bits_field.set('')
