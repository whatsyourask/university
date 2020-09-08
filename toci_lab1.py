class Ring:
    def __init__(self, n, num):
        self._n = n
        self._num = num

    @property
    def num(self):
        return self._num

    @num.setter
    def num(self, num):
        self._num = num

    def __add__(self, other):
        return Ring(self._n, (self._num + other.num) % self._n)

    def __sub__(self, other):
        if other.num < 0:
            other.num += self._n
        return Ring(self._n, (self._num - other.num) % self._n)

    def __mul__(self, other):
        return Ring(self._n, (self._num * other.num) % self._n)

    def _lines_count(self):
        a = self._n
        b = self._num
        lines_count = 1
        while True:
            mod = a % b
            if not mod:
                break
            a = b
            b = mod
            lines_count += 1
        return lines_count

    def invert(self):
        self._lines_count()


def some_code():
    a = Ring(26, 22)
    b = Ring(26, 15)
    c = a + b
    print(f'{a.num} + {b.num} = {c.num}')
    c = a - b
    print(f'{a.num} - {b.num} = {c.num}')
    c = a * b
    print(f'{a.num} * {b.num} = {c.num}')
    b.invert()


some_code()
