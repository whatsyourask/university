from gui import *
from backend import AdditiveCipher


class Application:
    """Logic of application"""
    _EN = 'en'
    _RU = 'ru'
    def run(self) -> None:
        # Create all elements
        self._create_all_elements()
        # Start interface
        self._gui.start()

    def _create_all_elements(self) -> None:
        # Create all needed elements
        self._gui   = GraphicUI()
        self._gui.set_title('Additive Cipher')
        self._gui.label('Plaintext:', 2, 1, W)
        self._plaintext_field = self._gui.text(2, 2, 50, 5, W)
        self._gui.label('Binary plaintext: ', 2, 3, W)
        self._plain_binary_field = self._gui.text(2, 4, 50, 5, W)
        self._gui.label('Input key: ', 2, 5, W)
        self._key_field = self._gui.text(2, 6, 50, 5, W)
        self._gui.label('Binary input key: ', 2, 7, W)
        self._bin_input_key_field = self._gui.text(2, 8, 50, 5, W)
        self._gui.label('Binary generated key: ', 2, 9, W)
        self._gen_bin_key_field = self._gui.text(2, 10, 50, 5, W)
        self._gui.label('Generated key: ', 2, 11, W)
        self._gen_key_field = self._gui.text(2, 12, 50, 5, W)
        self._gui.label('Ciphertext: ', 2, 13, W)
        self._ciphertext_field = self._gui.text(2, 14, 50, 5, W)
        self._gui.label('Binary plaintext: ', 2, 15, W)
        self._cipher_binary_field = self._gui.text(2, 16, 50, 5, W)
        # Variable to choose language
        self._lang_radio = StringVar()
        # A 2 radiobuttons to choose language
        self._en_radio = self._gui.radiobutton(1, 1, E, self._EN,
                                self._lang_radio, self._EN, self.__change_lang)
        self._ru_radio = self._gui.radiobutton(1, 2, E, self._RU,
                                self._lang_radio, self._RU, self.__change_lang)
        self._gui.button('Encrypt', 3, 2, 30, W, self.__encrypt)
        self._gui.button('Generate key', 3, 10, 30, W, self.__generate)
        self._gui.button('Decrypt', 3, 14, 30, W, self.__decrypt)
        self._gui.button('Clear', 3, 16, 30, W, self.__clear)
        # Create a 2 object of AdditiveCipher to change them when it will need
        self._en_cipher = AdditiveCipher(self._EN)
        self._ru_cipher = AdditiveCipher(self._RU)
        self._chosen_cipher = None
        # Set default radiobutton as english lang
        self._en_radio.invoke()

    def __change_lang(self) -> None:
        # Method to change language
        lang = self._lang_radio.get()
        if lang == self._EN:
            self._chosen_cipher = self._en_cipher
        else:
            self._chosen_cipher = self._ru_cipher

    def __crypt(self, data_field, bin_data_field,
                                        result_field, bin_result_field) -> None:
        # Logic of encryption and decryption
        try:
            # Clear all field which will need
            self.__flush(bin_data_field)
            self.__flush(result_field)
            self.__flush(bin_result_field)
            # Get the data
            data = data_field.get("1.0", END)[:-1]
            if data:
                # If data is set try to get the key
                input_key = self._key_field.get("1.0", END)[:-1]
                gen_key = self._gen_key_field.get("1.0", END)[:-1]
                if input_key:
                    result = self._chosen_cipher.crypt(data, input_key)
                    self._bin_input_key_field.insert(INSERT,
                                                    self._chosen_cipher.bin_key)
                elif gen_key:
                    result = self._chosen_cipher.crypt(data, gen_key)
                else:
                    result = self._chosen_cipher.crypt(data)
                    self._gen_key_field.insert(INSERT, self._chosen_cipher.key)
                    self._gen_bin_key_field.insert(INSERT,
                                                    self._chosen_cipher.bin_key)
                bin_data_field.insert(INSERT, self._chosen_cipher.bin_data)
                result_field.insert(INSERT, result)
                bin_result_field.insert(INSERT, self._chosen_cipher.bin_result)
        except ValueError:
            # Open a new window with button when we have an exception
            self.__process_exception()

    def __encrypt(self) -> None:
        # Method to call the crypt method with appropriate parameters
        self.__crypt(self._plaintext_field, self._plain_binary_field,
                        self._ciphertext_field, self._cipher_binary_field)

    def __generate(self) -> None:
        # Method to generate key
        # Clear  key fields
        self.__flush(self._gen_key_field)
        self.__flush(self._gen_bin_key_field)
        data = self._plaintext_field.get("1.0", END)[:-1]
        # Generate key from cipher object
        try:
            key = self._chosen_cipher.generate_key(data)
        except ValueError:
            self.__process_exception()
        # Also get a binary view of key
        bin_key = self._chosen_cipher.bin_key
        # Insert in the fields
        self._gen_key_field.insert(INSERT, key)
        self._gen_bin_key_field.insert(INSERT, bin_key)

    def __decrypt(self) -> None:
        # As encrypt, but with other parameters
        self.__crypt(self._ciphertext_field, self._cipher_binary_field,
                        self._plaintext_field, self._plain_binary_field)

    def __clear(self) -> None:
        # Method to clear all fields
        self.__flush(self._plaintext_field)
        self.__flush(self._plain_binary_field)
        self.__flush(self._key_field)
        self.__flush(self._bin_input_key_field)
        self.__flush(self._gen_key_field)
        self.__flush(self._gen_bin_key_field)
        self.__flush(self._ciphertext_field)
        self.__flush(self._cipher_binary_field)

    def __flush(self, field) -> None:
        # Method to clear one field
        field.delete("1.0", END)

    def __process_exception(self) -> None:
        # Method to create a new window on top of main window
        self._gui.message_box('Ошибка', 'Неверные данные')

    def __okay_button_handler(self):
        # Method to clear fields and close the top window
        self.__clear()
        self._window.destroy()
