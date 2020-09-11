from tkinter import *
from tkinter import ttk


class GraphicUI:
    def __init__(self) -> None:
        self.__root = Tk()
        self.__root.title('Lab №1')
        self.__root.resizable(0, 0)
        self.__mainframe = ttk.Frame(self.__root, padding="40 20 40 20")
        self.__mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.__root.columnconfigure(0, weight=1)
        self.__root.rowconfigure(0, weight=1)
        self.__mainframe.rowconfigure(1, weight=1)
        self.__entries = {}

    def label(self, text, column, row, sticky) -> None:
        ttk.Label(self.__mainframe, text=text).grid(column=column,
                                                        row=row, sticky=sticky)

    def entry(self, type: Variable, column, row, width, sticky) -> None:
        field = type
        entry = ttk.Entry(self.__mainframe, text=field, width=width)
        entry.grid(column=column, row=row, sticky=sticky)
        return field

    def button(self, text, column, row, width, sticky, func) -> None:
        button = ttk.Button(self.__mainframe, text=text,
                                command=func, width=width)
        button.grid(column=column, row=row, sticky=sticky)

    def start(self) -> None:
        self.__root.mainloop()
