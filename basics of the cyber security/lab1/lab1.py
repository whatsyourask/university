from gui import *


def main():
    gui = GraphicUI()
    gui.label('n ', 1, 1, Sticky.W())
    gui.entry(Var.int(), 2, 1, 5, Sticky.W())
    gui.label('first ', 1, 2, Sticky.W())
    gui.entry(Var.int(), 2, 2, 5, Sticky.W())
    gui.label('second ', 1, 3, Sticky.W())
    gui.entry(Var.int(), 2, 3, 5, Sticky.W())
    gui.label('result ', 1, 4, Sticky.W())
    gui.entry(Var.int(), 2, 4, 5, Sticky.W())
    gui.button('+', 1, 5, 2, Sticky.W(), None)
    gui.button('-', 2, 5, 2, Sticky.W(), None)
    gui.button('*', 3, 5, 2, Sticky.W(), None)
    gui.button('/', 4, 5, 2, Sticky.W(), None)
    gui.start()


if __name__=='__main__':
    main()
