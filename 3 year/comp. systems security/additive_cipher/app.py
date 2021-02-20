from gui import *
from backend import AdditiveCipher


class Application:
    def run(self) -> None:
        # Создать все элементы
        self._create_all_elements()
        # Запустить приложение с интерфейсом
        self._gui.start()

    def _create_all_elements(self) -> None:
        # Метод для создания начальных элементов интерфейса
        # Создание объекта для графики из лабораторной 1
        self._gui   = GraphicUI()
        self._gui.set_title('Additive Cipher')
        self._gui.label('Plaintext:', 2, 1, W)
        self._plaintext_field = self._gui.text(2, 2, 50, 5, W)
        self._gui.label('Plaintext binary: ', 2, 3, W)
        self._plain_binary_field = self._gui.text(2, 4, 50, 5, W)
        self._gui.label('Key: ', 2, 5, W)
        self._key_field = self._gui.text(2, 6, 50, 5, W)
        self._gui.label('Binary from input key: ', 2, 7, W)
        self._key_field = self._gui.text(2, 8, 50, 5, W)
        self._gui.label('Key binary: ', 2, 9, W)
        self._key_field = self._gui.text(2, 10, 50, 5, W)
        self._gui.label('Text from binary input key: ', 2, 11, W)
        self._key_field = self._gui.text(2, 12, 50, 5, W)
        self._gui.label('Ciphertext: ', 2, 13, W)
        self._key_field = self._gui.text(2, 14, 50, 5, W)
        self._gui.label('Ciphertext binary: ', 2, 15, W)
        self._key_field = self._gui.text(2, 16, 50, 5, W)
        self.__lang_radio = StringVar()
        self._en_radio = self._gui.radiobutton(1, 1, E, 'EN', self.__lang_radio,
                                                'en')
        self._ru_radio = self._gui.radiobutton(1, 2, E, 'RU', self.__lang_radio,
                                                'ru')
        self._gui.button('Encrypt', 3, 2, 30, W, self.__encrypt)
        self._gui.button('Generate key', 3, 10, 30, W, self.__generate)
        self._gui.button('Decrypt', 3, 14, 30, W, self.__decrypt)

    def __encrypt(self):
        pass

    def __generate(self) -> None:
        

    def __decrypt(self):
        pass
