class node:
    # Constructor
    def __init__(self,info):
        self.__info=info
        self.__list_of_pointers = list()

    # Getter for info
    @property
    def info(self):
        return self.__info

    # Getter for list_of_pointers
    @property
    def get_list(self):
        return self.__list_of_pointers

    # Setter for item of list
    def set_list(self,node):
        self.__list_of_pointers.append(node)

    # Getter for item of list
    def get_item(self,i):
        return self.__list_of_pointers[i]