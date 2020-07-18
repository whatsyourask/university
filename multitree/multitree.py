from node import node
from collections import deque


# I tried to transfer the code from C plus plus to Python.
# Unfortunately, I was faced with the problem of passing arguments ...
# So, maybe in the future I will fix this shit
# If you know how to fix it - write
class multitree:
    # Constructor
    def __init__(self):
        self.__main_root=node(input('Write the main root info field:\t'))
        self.__write_r(self.__main_root)

    # Recursive private tree input method
    def __write_r(self,root):
        n = int(input('How many subtrees you want?\t'))
        for i in range(n):
            root.set_list(node(input("Write info-field:\t")))
            answ=bool(int(input('Do you want to continue to enter a new subtree??\nWrite 1,if YES,and 0,if NO:\t')))
            if answ == False:
                print('Subtree is end')
            else:
                self.__write_r(root.get_list)

    # Printing elements with bypass in depth
    def print_depth(self):
        self.__print_depth_r(self.__main_root)

    # Recursive
    def __print_depth_r(self,root):
        length=len(root.get_list)
        print(length)
        if length != 0:
            for i in range(length):
                self.__print_depth_r(root.get_item(i))
        print(root.info,end='\r')

    # Printing elemetns with bypass in width
    def print_width(self):
        print(self.__main_root.info,end='\r')
        width=deque()
        width.append(self.__main_root)
        print('width len = ',len(width))
        while len(width)!=0:
            length=len(width[0].get_list)
            print(width[0].get_list)
            if length!=0:
                for i in range(length):
                    node=width[0].get_item(i)
                    print(node)
                    print(node.info,end='\r')
                    width.append(node)
            width.popleft()
