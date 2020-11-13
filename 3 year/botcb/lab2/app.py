from rsa import *
from lab1.gui import *
from time import time

class Application:
    def run(self) -> None:
        # Создать все элементы
        self._create_all_elements()
        # Создать объект класса RSA
        self._rsa = RSA()
        # Запустить приложение с интерфейсом
        self._gui.start()

    def _create_all_elements(self) -> None:
        # Создание объекта интерфейса из лабораторной 1
        self._gui = GraphicUI()
        # Назначение заголовка приложения
        self._gui.set_title('Lab №2')
        # Ширина ячеек в таблице окна
        self._width = 30
        # Создание метки с текстом
        self._gui.label('p ', 1, 1, E)
        # Создание поля для переменной
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
        # Создание кнопки с передачей ей функции
        # которую она будет выполнять при нажатии
        # Переменная для хранения объекта интерфейса, где выводятся возможные e
        self._text        = None
        self._pos_e_label = None
        self._gui.button('Генерация ключей шифрования', 2, 12,
                         self._width, W, self._generate_keys_event)
        # Переменная для сохранения элемента интерфейса с предупреждением
        # о величине m
        self._m_warning = None
        self._gui.button('Зашифровать сообщение', 2, 13,
                         self._width, W, self._encrypt_message_event)
        # Переменная для сохранения элемента интерфейса с предупреждением
        # о величине c
        self._c_warning = None
        self._gui.button('Дешифровать сообщение', 2, 14,
                         self._width, W, self._decrypt_message_event)

    def _generate_keys_event(self) -> None:
        # Функция для кнопки генерации ключей
        # Достаем p и q из полей
        p = self._p_field.get()
        q = self._q_field.get()
        # Проверяем, если не нули
        if p and q:
            # Создаём объект со своими параметрами
            self._rsa = RSA(p, q)
            # Генерируем ключи
            self._rsa.generate_public_key()
            # Присваиваем все поля класса нужным полям интерфейса
            self._n_field.set(self._rsa.n)
            self._euler_f_field.set(self._rsa.euler_func)
            self._e_field.set(self._rsa.e)
            self._rsa.generate_private_key()
            self._d_field.set(self._rsa.d)
            # Берём возможные ключи из класса RSA
            e_arr = self._rsa._e_arr
        # Создаем объект интерфейса с текстом
        if self._text:
            self._text.grid_remove()
        if self._pos_e_label:
            self._pos_e_label.grid_remove()
        self._pos_e_label = self._gui.label('Возможные е', 1, 15, W)

        self._text = self._gui.text(1, 16, (self._width + 4) * 3,
                                                len(e_arr) // self._width, W, 4)
        # Заполняем его возможными ключами
        self._text.insert(INSERT, e_arr)

    def _encrypt_message_event(self) -> None:
        # Для кнопки шифрования сообщения
        # Достаем из полей m и n
        m = self._m_field.get()
        n = self._n_field.get()
        # Если m >= n то вывести предупреждение
        if m >= n:
            self._m_warning = self._gui.label('! m < n', 3, 7, W)
            return
        # Если же нет, то продолжить шифрование
        # Если до этого выводили предупреждения, то надо их убрать
        # т.к m прошло проверку
        if self._m_warning:
            # Удалить с фрейма
            self._m_warning.grid_remove()
        if self._c_warning:
            self._c_warning.grid_remove()
        # Получить текущее время
        start = time()
        # Взять ключ из поля
        e = self._e_field.get()
        # Проверяем не равны ли нулю e и n
        if n != self._rsa.n:
            self._rsa.n = n
        if e != self._rsa.e:
            self._rsa.e = e
        # Шифрование в объекте класса RSA
        c = self._rsa.encrypt(m)
        self._c_field.set(c)
        # Смотрим время после шифрования
        end = time()
        # Вычисляем время шифрования
        self._e_t_field.set(end - start)

    def _decrypt_message_event(self) -> None:
        # Полностью аналогичный метод, только разные переменные
        # Написать всё в один метод нельзя, т.к нельзя передать параметры метода
        # кнопке напрямую, мы можем взять значения только внутри функции
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
