import sys
# To import FastModularExponentiation
sys.path.insert(0, '..')
from additive_cipher.gui import *
from backend import miller_rabin_generate, RSA


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
        title = 'RSA Algorithm'
        self._gui.set_title(title)
        width = 30
        self._gui.label('Bits', 1, 1, W)
        self._bits_field, _ = self._gui.entry(StringVar(), 2, 1, width, W)
        self._gui.button('Generate', 3, 1, width, W, self._generate)
        self._gui.label('p', 1, 2, W)
        self._p_field, _ = self._gui.entry(StringVar(), 2, 2, width, W)
        self._gui.label('q', 1, 3, W)
        self._q_field, _ = self._gui.entry(StringVar(), 2, 3, width, W)
        self._gui.label('n', 1, 4, W)
        self._n_field, _ = self._gui.entry(StringVar(), 2, 4, width, W)
        self._gui.label('Euler func', 1, 5, W)
        self._euler_func_field, _ = self._gui.entry(StringVar(), 2, 5, width, W)
        self._gui.label('e', 1, 6, W)
        self._e_field, _ = self._gui.entry(StringVar(), 2, 6, width, W)
        self._gui.label('d', 1, 7, W)
        self._d_field, _ = self._gui.entry(StringVar(), 2, 7, width, W)
        self._gui.label('Cleartext', 1, 8, W)
        self._cleartext_field = self._gui.text(2, 8, width, 5, W)
        self._gui.label('Encrypted text', 1, 9, W)
        self._encrypted_field = self._gui.text(2, 9, width, 5, W)
        self._gui.button('Encrypt', 3, 9, width, W, self._encrypt)
        self._gui.label('Decrypted text', 1, 10, W)
        self._decrypted_field = self._gui.text(2, 10, width, 5, W)
        self._gui.button('Decrypt', 3, 10, width, W, self._decrypt)

    def _generate(self) -> None:
        # Method to generate necessary numbers
        try:
            # Clear the fields
            self._p_field.set('')
            self._q_field.set('')
            self._n_field.set('')
            self._euler_func_field.set('')
            self._e_field.set('')
            self._d_field.set('')
            # Get bits length
            bits_len = int(self._bits_field.get())
            # If less than eigth then raise exception
            if bits_len < 8:
                raise ValueError
            # Generate p and q by Miller Rabit test
            p = miller_rabin_generate(bits_len)
            self._p_field.set(p)
            q = miller_rabin_generate(bits_len)
            self._q_field.set(q)
            n = p * q
            self._n_field.set(n)
            euler_func = (p - 1) * (q - 1)
            self._euler_func_field.set(euler_func)
            # Generate public and private keys
            self._rsa = RSA()
            self._rsa.n = n
            self._rsa.euler_func = euler_func
            # Bits length needs to be more or equal than one third
            e = self._rsa.generate_public_key(bits_len // 3)
            self._e_field.set(e)
            d = self._rsa.generate_private_key()
            self._d_field.set(d)
        except ValueError:
            self._process_exception()

    def _encrypt(self) -> None:
        self._encrypted_field.delete("1.0", END)
        cleartext = self._cleartext_field.get("1.0", END)[:-1]
        encrypted = self._rsa.encrypt(cleartext)
        self._encrypted_field.insert(INSERT, encrypted)

    def _decrypt(self) -> None:
        self._decrypted_field.delete("1.0", END)
        encrypted = self._encrypted_field.get("1.0", END)[:-1]
        decrypted = self._rsa.decrypt(encrypted)
        self._decrypted_field.insert(INSERT, decrypted)

    def _process_exception(self) -> None:
        # Method to create a new window on top of main window
        self._gui.message_box('Ошибка', 'Неверные данные')
