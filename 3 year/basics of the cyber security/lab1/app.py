from gui import *
import ring
from ring import Ring
from typing import Tuple

class Application:
    def run(self) -> None:
        # To test
        ring.test()
        gui = GraphicUI()
        gui.label('n ', 1, 1, W)
        self.__n_entry = gui.entry(IntVar(), 2, 1, 7, W)
        gui.label('a ', 1, 2, W)
        self.__a_entry = gui.entry(IntVar(), 2, 2, 7, W)
        gui.label('b ', 1, 3, W)
        self.__b_entry = gui.entry(IntVar(), 2, 3, 7, W)
        gui.label('result ', 1, 4, W)
        self.__result_entry = gui.entry(IntVar(), 2, 4, 7, W)
        gui.button('+', 1, 5, 7, W, self.__addition)
        gui.button('-', 2, 5, 7, W, self.__substraction)
        gui.button('*', 3, 5, 7, W, self.__multiplication)
        gui.button('/', 4, 5, 7, W, self.__division)
        gui.button('Invert a', 1, 6, 7, W, self.__invert)
        gui.start()

    def __get_all(self) -> Tuple:
        # Get values of entries
        n = self.__n_entry.get()
        a = Ring(n, self.__a_entry.get())
        b = Ring(n, self.__b_entry.get())
        return n, a, b

    def __addition(self) -> None:
        # Method to connect addition operation with button
        n, a, b = self.__get_all()
        # if there are no zeros
        if n and (a or b):
            c = a + b
            # Set value to entry
            self.__result_entry.set(c.num)

    def __substraction(self) -> None:
        n, a, b = self.__get_all()
        if n and (a or b):
            c = a - b
            self.__result_entry.set(c.num)

    def __multiplication(self) -> None:
        n, a, b = self.__get_all()
        if n and (a or b):
            c = a * b
            self.__result_entry.set(c.num)

    def __division(self) -> None:
        n, a, b = self.__get_all()
        if n and (a or b):
            c = a / b
            self.__result_entry.set(c.num)

    def __invert(self) -> None:
        n = self.__n_entry.get()
        a = Ring(n, self.__a_entry.get())
        if n and a:
            c = a.invert()
            self.__result_entry.set(c.num)
