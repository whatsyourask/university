from __future__ import annotations

class Ring:
    def __init__(self, n: int, num: int) -> None:
        self._n = n
        self._num = num

    @property
    def num(self) -> int:
        return self._num

    @num.setter
    def num(self, num: int) -> None:
        self._num = num

    def __add__(self, other: Ring) -> Ring:
        # + operator overload
        return Ring(self._n, (self._num + other.num) % self._n)

    def __sub__(self, other: Ring) -> Ring:
        # - operator overload
        if other.num < 0:
            other.num += self._n
        return Ring(self._n, (self._num - other.num) % self._n)

    def __mul__(self, other: Ring) -> Ring:
        # * operator overload
        return Ring(self._n, (self._num * other.num) % self._n)

    def _lines_count(self) -> int:
        # Compute lines count
        a = self._n
        b = self._num
        lines_count = 0
        # To save divs or a/b
        self._divs = []
        while True:
            mod = a % b
            div = a // b
            self._divs.append(div)
            if not mod:
                break
            a = b
            b = mod
            lines_count += 1
        self._divs.pop()
        return lines_count

    def invert(self) -> Ring:
        # Find a invert of current num
        count = self._lines_count()
        x = 0
        y = 1
        while self._divs:
            temp = x
            x = y
            last = self._divs.pop()
            y = temp - y * last
        return Ring(self._n, y)

    def __truediv__(self, other: Ring) -> Ring:
        # / operator overload
        invert_other = other.invert()
        return self.__mul__(invert_other)


def test():
    # Method to test class
    a = Ring(26, 22)
    b = Ring(26, 15)
    c = a + b
    print(f'{a.num} + {b.num} = {c.num}')
    c = a - b
    print(f'{a.num} - {b.num} = {c.num}')
    c = a * b
    print(f'{a.num} * {b.num} = {c.num}')
    c = b.invert()
    print(f'invert of {b.num} = {c.num}')
    c = b.invert()
    print(f'invert of {b.num} = {c.num}')
    c = a / b
    print(f'{a.num} / {b.num} = {c.num}')


if __name__=='__main__':
    test()
