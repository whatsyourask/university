from rsa import *
from lab1.gui import *
from time import time

class Application:
    def run(self) -> None:
        self._create_all_elements()
        self._rsa = RSA()
        self._gui.start()

    def _create_all_elements(self) -> None:
        self._gui = GraphicUI()
        self._gui.set_title('Lab №2')
        self._width = 30
        self._gui.label('p ', 1, 1, E)
        self._p_field, _ = self._gui.entry(IntVar(), 2, 1, self._width, W)
        self._gui.label('q ', 1, 2, E)
        self._q_field, _ = self._gui.entry(IntVar(), 2, 2, self._width, W)
        self._gui.label('n = p * q ', 1, 3, E)
        self._n_field, _ = self._gui.entry(IntVar(), 2, 3, self._width, W)
        self._gui.label('ф. Эйлера: e_f = (p - 1) * (q - 1) ', 1, 4, W)
        self._euler_f_field, _ = self._gui.entry(IntVar(), 2, 4, self._width, W)
        self._gui.label('Публичный ключ e ', 1, 5, E)
        self._e_field, _ = self._gui.entry(IntVar(), 2, 5, self._width, W)
        self._gui.label(' e <= n, HOД(e_f(n), e) = 1', 3, 5, W)
        self._gui.label('Приватный ключ d ', 1, 6, E)
        self._d_field, _ = self._gui.entry(IntVar(), 2, 6, self._width, W)
        self._gui.label(' e ^ d mod e_f(n) = 1', 3, 6, W)
        self._gui.label('Сообщение m ', 1, 7, E)
        self._m_field, _ = self._gui.entry(IntVar(), 2, 7, self._width, W, 3)
        self._gui.label('Шифрованное c ', 1, 8, E)
        self._c_field, _ = self._gui.entry(IntVar(), 2, 8, self._width, W, 3)
        self._gui.label('Дешифрованное m ', 1, 9, E)
        self._d_m_field, _ = self._gui.entry(IntVar(), 2, 9, self._width, W, 3)
        self._gui.label('Время шифрования ', 1, 10, E)
        self._e_t_field, _ = self._gui.entry(IntVar(), 2, 10,
                                             self._width, W)
        self._gui.label('Время дешифрования ', 1, 11, E)
        self._d_t_field, _ = self._gui.entry(IntVar(), 2, 11,
                                             self._width, W)
        self._gui.button('Генерация ключей шифрования', 2, 12,
                         self._width, W, self._generate_keys_event)
        self._m_warning = None
        self._gui.button('Зашифровать сообщение', 2, 13,
                         self._width, W, self._encrypt_message_event)
        self._c_warning = None
        self._gui.button('Дешифровать сообщение', 2, 14,
                         self._width, W, self._decrypt_message_event)

    def _generate_keys_event(self) -> None:
        p = self._p_field.get()
        q = self._q_field.get()
        if p and q:
            self._rsa = RSA(p, q)
            self._rsa.generate_public_key()
            self._n_field.set(self._rsa.n)
            self._euler_f_field.set(self._rsa.euler_func)
            self._e_field.set(self._rsa.e)
            self._rsa.generate_private_key()
            self._d_field.set(self._rsa.d)

    def _encrypt_message_event(self) -> None:
        m = self._m_field.get()
        n = self._n_field.get()
        if m >= n:
            self._m_warning = self._gui.label('! m < n', 3, 7, W)
            return
        if self._m_warning:
            self._m_warning.grid_remove()
        if self._c_warning:
            self._c_warning.grid_remove()
        start = time()
        e = self._e_field.get()
        if n != self._rsa.n:
            self._rsa.n = n
        if e != self._rsa.e:
            self._rsa.e = e
        c = self._rsa.encrypt(m)
        self._c_field.set(c)
        end = time()
        self._e_t_field.set(end - start)

    def _decrypt_message_event(self) -> None:
        c = self._c_field.get()
        n = self._n_field.get()
        if c >= n:
            self._c_warning = self._gui.label('! c < n', 3, 8, W)
            return
        if self._m_warning:
            self._m_warning.grid_remove()
        if self._c_warning:
            self._c_warning.grid_remove()
        start = time()
        d = self._d_field.get()
        if n != self._rsa.n:
            self._rsa.n = n
        if d != self._rsa.d:
            self._rsa.d = d
        d_m = self._rsa.decrypt(c)
        self._d_m_field.set(d_m)
        end = time()
        self._d_t_field.set(end - start)
