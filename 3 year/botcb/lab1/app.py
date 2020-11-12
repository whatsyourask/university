from gui import *
from ring import Ring
from euler import euler_func
from fast_powers_mod import fast_powers_mod, List, Tuple


class Application:
    """Класс с реализацией основной логики приложения"""
    def run(self) -> None:
        # Создание всех необходимых элементов интерфейса и запуск цикла интерфейса
        self._create_all_elements()
        # Для хранения значений в таблицах промежуточных вычислений
        self._fields  = None
        # Для хранения объектов-ячеек таблиц
        self._entries = None
        # Для хранения объектов меток и обозначений столбцов для таблиц
        self._table_first_entries = []
        # Отобразить интерфейс
        self._gui.start()

    def _create_all_elements(self) -> None:
        # Создание объекта интерфейса
        self._gui = GraphicUI()
        # Заголовок программы
        self._gui.set_title('Lab №1')
        # Ширина элементов интерфейса
        self._width   = 8
        # Ставим метку для n
        self._gui.label('n ', 1, 1, W)
        # Создаём поле для ввода n
        self._n_field, _ = self._gui.entry(IntVar(), 2, 1, self._width, W)
        # Для a
        self._gui.label('a ', 1, 2, W)
        self._a_field, _ = self._gui.entry(IntVar(), 2, 2, self._width, W)
        # Для b
        self._gui.label('b ', 1, 3, W)
        self._b_field, _ = self._gui.entry(IntVar(), 2, 3, self._width, W)
        # Для результата
        self._gui.label('Результат ', 1, 4, W)
        self._result_field, _ = self._gui.entry(IntVar(), 2, 4,self._width, W)
        # Создание кнопок с операциями
        self._gui.button('+', 1, 5, self._width, W, self._addition)
        self._gui.button('-', 2, 5, self._width, W, self._substraction)
        self._gui.button('*', 3, 5, self._width, W, self._multiplication)
        self._gui.button('/', 4, 5, self._width, W, self._division)
        # Позиция таблицы для промежуточных вычислений при нахождении обратного
        self._invert_table_pos = [1, 7]
        self._gui.button('Обратн а', 1, 6, self._width, W, self._invert)
        self._gui.button('ф. Эйлера', 2, 6, self._width, W,
                                                    self._calculate_euler_func)
        # Позиция таблицы для промежуточных вычисления
        # при быстром возведении в степень по модулю
        self._mod_table_pos = [1, 7]
        self._gui.button('Мод', 3, 6, self._width, W, self._mod_powers)

    def _get_all(self) -> Tuple:
        # Взять все значения из полей для n, a, b
        n = self._n_field.get()
        # Создать объект для a и b
        a = Ring(n, self._a_field.get())
        b = Ring(n, self._b_field.get())
        return n, a, b

    def _addition(self) -> None:
        # Метод, что мы передаем в кнопку, чтобы указать ей
        # на выполнение именно этого метода при её нажатии
        n, a, b = self._get_all()
        # Проверяем на 0
        if n and (a.num or b.num):
            c = a + b
            # Меняем значение поля результата
            self._result_field.set(c.num)

    def _substraction(self) -> None:
        # Аналогично методу _addition()
        n, a, b = self._get_all()
        if n and (a.num or b.num):
            c = a - b
            self._result_field.set(c.num)

    def _multiplication(self) -> None:
        n, a, b = self._get_all()
        if n and (a.num or b.num):
            c = a * b
            self._result_field.set(c.num)

    def _division(self) -> None:
        n, a, b = self._get_all()
        if n and a.num and b.num:
            c = a / b
            self._result_field.set(c.num)

    def _invert(self) -> None:
        n = self._n_field.get()
        # Создаем объект для a
        a = Ring(n, self._a_field.get())
        if n and a.num:
            # Находим обратное и промежуточные результаты
            c, arr = a.invert()
            # Переворачиваем матрицу для удобства таблицы
            arr = self._reverse_matrix(arr)
            self._result_field.set(c.num)
            # Проверяем были ли созданы таблицы до этого
            if self._entries:
                # Если да, убираем их с интерфейса
                self._destroy_previous_entries()
            _ = self._gui.label('Таблица расширенного алгоритма Евклида',
                                self._invert_table_pos[0],
                                self._invert_table_pos[1],
                                W,
                                4)
            # Кладём метку в массив объектов интерфейса,
            # чтобы потом можно было по ним же их и удалить с фрейма
            self._table_first_entries.append(_)
            # Двигаем позицию вниз
            self._invert_table_pos[1] += 1
            # Создаем ячейки таблицы с обозначением A, B, A mod B, A / B, x, y
            self._a_entry = self._create_column_label('A',
                                                      self._invert_table_pos,
                                                      0)
            self._b_entry = self._create_column_label('B',
                                                      self._invert_table_pos,
                                                      0)
            self._mod_entry = self._create_column_label('A mod B',
                                                      self._invert_table_pos,
                                                      0)
            self._div_entry = self._create_column_label('A / B',
                                                      self._invert_table_pos,
                                                      0)
            self._x_entry = self._create_column_label('x',
                                                      self._invert_table_pos,
                                                      0)
            self._y_entry = self._create_column_label('y',
                                                      self._invert_table_pos,
                                                      0)
            # Двигаем позицию, для создания самой таблицы
            self._invert_table_pos[0] -= 6
            self._invert_table_pos[1] += 1
            # Создаем таблицу
            self._create_table(arr, self._invert_table_pos)
            # Сбросить позицию для таблицы, чтобы при новом создании,
            # она создавалась на том же месте
            self._invert_table_pos = [1, 7]

    def _reverse_matrix(self, arr) -> List:
        # Транспонировать матрицу
        rows    = len(arr)
        columns = len(arr[0])
        # Создать список пустых списков
        new_arr = [[] for i in range(columns)]
        for row in range(rows):
            for column in range(columns):
                new_arr[column].append(arr[row][column])
        return new_arr

    def _destroy_previous_entries(self) -> None:
        # Уничтожение всей предыдущей таблицы
        rows    = len(self._entries)
        columns = len(self._entries[0])
        for row in range(rows):
            for column in range(columns):
                # Берём элемент матрицы, что является объектом элемента интерфейса
                self._entries[row][column].grid_remove()
        # Аналогично, только для списка
        for entries in self._table_first_entries:
            entries.grid_remove()

    def _create_column_label(self, text, table_pos, direction):
        # Создать обозначения для колонки в таблице
        table_field, _ = self._gui.entry(StringVar(),
                    table_pos[0], table_pos[1],
                    self._width + 1, W)
        self._table_first_entries.append(_)
        table_field.set(text)
        table_pos[direction] += 1
        return table_field

    def _mod_powers(self) -> None:
        # Взять все значения без создания объектов Ring
        n = self._n_field.get()
        a = self._a_field.get()
        b = self._b_field.get()
        if n and a and b:
            # Получить результаты быстрого возведения в степень по модулю
            c, arr = fast_powers_mod(n, a, b)
            self._result_field.set(c)
            # Аналогично с _invert
            if self._entries:
                self._destroy_previous_entries()
            _ = self._gui.label('Таблица с разрядами b и основаниями a',
                                self._mod_table_pos[0],
                                self._mod_table_pos[1],
                                W,
                                4)
            self._table_first_entries.append(_)
            self._mod_table_pos[1] += 1
            self._e_entry = self._create_column_label('e',
                                                      self._mod_table_pos,
                                                      1)
            self._m_entry = self._create_column_label('m',
                                                      self._mod_table_pos,
                                                      0)
            self._mod_table_pos[1] -= 1
            self._create_table(arr, self._mod_table_pos)
            # Сбросить позицию для таблицы, чтобы при новом создании,
            # она создавалась на том же месте
            self._mod_table_pos = [1, 7]

    def _create_table(self, arr, position: Tuple[int, int]):
        # Поставить ячейки таблицы на фрейм интерфейса
        # Обновить интерфейс
        self._gui.update()
        rows          = len(arr)
        columns       = len(arr[0])
        # Список для полей таблицы
        self._fields  = [columns * [None] for row in range(rows)]
        # Список для объектов ячеек
        self._entries = [columns * [None] for row in range(rows)]
        for row in range(rows):
            for column in range(columns):
                # Создание ячейки
                self._fields[row][column], self._entries[row][column] = self._gui.entry(IntVar(),
                                                position[0] + column,
                                                position[1] + row,
                                                self._width + 1,
                                                W)
                # Заполнить ячейку
                self._fields[row][column].set(arr[row][column])

    def _calculate_euler_func(self) -> None:
        n = self._n_field.get()
        if n:
            # Подсчитать функцию эйлера и заполнить поле
            result = euler_func(n)
            self._result_field.set(result)
