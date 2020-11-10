from gui import *
import ring
from ring import Ring
from euler import euler_func
from fast_powers_mod import fast_powers_mod, List, Tuple


class Application:
    def run(self) -> None:
        self._gui = GraphicUI()
        self._gui.label('n ', 1, 1, W)
        self._n_entry = self._gui.entry(IntVar(), 2, 1, 7, W)
        self._gui.label('a ', 1, 2, W)
        self._a_entry = self._gui.entry(IntVar(), 2, 2, 7, W)
        self._gui.label('b ', 1, 3, W)
        self._b_entry = self._gui.entry(IntVar(), 2, 3, 7, W)
        self._gui.label('result ', 1, 4, W)
        self._result_entry = self._gui.entry(IntVar(), 2, 4, 7, W)
        self._gui.button('+', 1, 5, 7, W, self._addition)
        self._gui.button('-', 2, 5, 7, W, self._substraction)
        self._gui.button('*', 3, 5, 7, W, self._multiplication)
        self._gui.button('/', 4, 5, 7, W, self._division)
        self._gui.button('Invert a', 1, 6, 7, W, self._invert)
        self._gui.button('Euler func', 2, 6, 7, W, self._calculate_euler_func)
        self._mod_table_pos = [1, 8]
        self._gui.button('Mod', 3, 6, 7, W, self._mod_powers)
        self._gui.start()

    def _get_all(self) -> Tuple:
        # Get values of entries
        n = self._n_entry.get()
        a = Ring(n, self._a_entry.get())
        b = Ring(n, self._b_entry.get())
        return n, a, b

    def _addition(self) -> None:
        # Method to connect addition operation with button
        n, a, b = self._get_all()
        # if there are no zeros
        if n and (a or b):
            c = a + b
            # Set value to entry
            self._result_entry.set(c.num)

    def _substraction(self) -> None:
        n, a, b = self._get_all()
        if n and (a or b):
            c = a - b
            self._result_entry.set(c.num)

    def _multiplication(self) -> None:
        n, a, b = self._get_all()
        if n and (a or b):
            c = a * b
            self._result_entry.set(c.num)

    def _division(self) -> None:
        n, a, b = self._get_all()
        if n and a and b > 0:
            c = a / b
            self._result_entry.set(c.num)

    def _invert(self) -> None:
        n = self._n_entry.get()
        a = Ring(n, self._a_entry.get())
        if n and a:
            c = a.invert()
            self.__result_entry.set(c.num)

    def _calculate_euler_func(self) -> None:
        n = self._n_entry.get()
        if n:
            result = euler_func(n)
            self._result_entry.set(result)

    def _mod_powers(self) -> None:
        n = self._n_entry.get()
        a = self._a_entry.get()
        b = self._b_entry.get()
        if n and a and b:
            c, arr, binary_form = fast_powers_mod(n, a, b)
            self._result_entry.set(c)
            self._gui.label('Таблица с разрядами b и основаниями a', 1, 7, W, 4)
            self._e_entry = self._gui.entry(StringVar(), self._mod_table_pos[0],
                                            self._mod_table_pos[1], 8, W)
            self._e_entry.set('e')
            self._mod_table_pos[1] += 1
            self._m_entry = self._gui.entry(StringVar(), self._mod_table_pos[0],
                                            self._mod_table_pos[1], 8, W)
            self._m_entry.set('m')
            self._mod_table_pos[0] += 1
            self._mod_table_pos[1] -= 1
            self._create_table(arr, self._mod_table_pos)

    def _create_table(self, arr, position: Tuple[int, int]):
        rows    = len(arr)
        columns = len(arr[0])
        self._mod_entries = [columns * [None] for row in range(rows)]
        #print(self._mod_entries)
        for row in range(rows):
            for column in range(columns):
                self._mod_entries[row][column] = self._gui.entry(IntVar(),
                                                position[0] + column,
                                                position[1] + row,
                                                8,
                                                W)
                self._mod_entries[row][column].set(arr[row][column])
