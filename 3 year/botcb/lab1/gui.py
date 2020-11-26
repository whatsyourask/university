from tkinter import *
from tkinter import ttk
from typing import Tuple
import matplotlib.pyplot as plt


class GraphicUI:
    """Класс, для создания интерфейса,
    его элементов:кнопок, меток полей.
    Также отвечает за все действия с интерфейсом,
    в том числе обновление и запуск."""
    def __init__(self) -> None:
        # Конструктор класса
        # self - переменная, что даёт доступ к атрибутам и методам класса
        # Создать главный объект модуля для создания интерфейса
        self.__root = Tk()
        # Сделать окно неизменяемым по размеру
        self.__root.resizable(0, 0)
        # Создать фрейм, на котором будут располагаться элементы
        # padding - отступы с разных сторон в рамке
        self.__mainframe = ttk.Frame(self.__root, padding="40 20 40 20")
        self.__mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

    def set_title(self, text) -> None:
        # Назначение названия программе
        self.__root.title(text)

    def label(self, text, column, row, sticky, columnspan=None):
        # Созданиe метки с текстом text на сетке в ячейке column, row
        # tkinter позволяет размещать элементы наподобие таблицы
        # т.е. в каждой ячейке элемент интерфейса
        # sticky - указать направление, к какой стороне ячейки приклеить элемент
        # Создание метки, указывается объект фрейма, на который её поставить и текст
        label = ttk.Label(self.__mainframe, text=text)
        # Размещение метки в ячейку
        # columnspan - для объединения ячеек таблицы и лучшего размещения,
        # Допустим метки с длинным текстом или аналогично с кнопкой
        # В этом методе, columnspan имеет параметр по умолчанию, если он не назначен,
        # то ячейки не объединяются
        label.grid(column=column, row=row, sticky=sticky, columnspan=columnspan)
        # Возвращает объект метки
        return label

    def entry(self, type: Variable, column, row, width,
                                             sticky, columnspan=None) -> Tuple:
        # Созданиe поля ввода
        # type - указать тип данных, что будет хранить поле
        # Запись type: Variable - статическая типизация в питоне
        # Variable в данном случае тип переменной type
        # field - объект типа для поля tkinter
        field = type
        # Создание поля, указывается объект фрейма, как и раньше
        # text с переменной field
        # width - ширина элемента
        entry = ttk.Entry(self.__mainframe, text=field, width=width)
        entry.grid(column=column, row=row, sticky=sticky, columnspan=columnspan)
        # Возвращает кортеж, т.е. неизменяемый массив
        # запись -> Tuple - статическая типизация для указания того,
        # что возвращает функция
        return field, entry

    def button(self, text, column, row, width, sticky, func, columnspan=None) -> None:
        # Созданиe кнопки
        # func - функция, которая должна отработать при нажатии на кнопку
        button = ttk.Button(self.__mainframe, text=text,
                                command=func, width=width)
        button.grid(column=column, row=row, sticky=sticky, columnspan=columnspan)

    def start(self) -> None:
        # Запустить интерфейс
        self.__root.mainloop()

    def update(self) -> None:
        # Обновить интерфейс
        self.__root.update()

    def text(self, column, row, width, height, sticky, columnspan=None):
        # Создание текстового поля
        text = Text(self.__mainframe, width=width, height=height)
        text.grid(column=column, row=row, sticky=sticky, columnspan=columnspan)
        # Возврат объекта элемента
        return text

    def graphic(self, x, y) -> None:
        fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.set(xlabel='Число', ylabel='Время',
                         title='График зависимости времени разложения от числа')
        ax.grid()
        plt.show()
