from __future__ import annotations

class Ring:
    def __init__(self, n: int, num: int) -> None:
        self._n   = n
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

    def _euclid_algorithm(self) -> int:
        a = self._n
        b = self._num
        # To save divs or a/b
        div_arr = []
        a_arr   = [a]
        b_arr   = [b]
        mod_arr = []
        while True:
            mod = a % b
            mod_arr.append(mod)
            div = a // b
            div_arr.append(div)
            if not mod:
                break
            a = b
            b = mod
            a_arr.append(a)
            b_arr.append(b)
        div_arr[-1] = None
        return a_arr, b_arr, mod_arr, div_arr

    def invert(self) -> Ring:
        # Find a invert of current num
        a_arr, b_arr, mod_arr, div_arr = self._euclid_algorithm()
        x = 0
        y = 1
        x_arr = [x]
        y_arr = [y]
        copy_div_arr = div_arr[:]
        copy_div_arr.pop()
        while copy_div_arr:
            last = copy_div_arr.pop()
            x, y = y, x - y * last
            x_arr.append(x)
            y_arr.append(y)
        print(len(a_arr))
        print(len(b_arr))
        print(len(mod_arr))
        print(len(div_arr))
        print(len(x_arr))
        print(len(y_arr))
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
    c = a.invert()
    print(f'invert of {a.num} = {c.num}')
    c = a / b
    print(f'{a.num} / {b.num} = {c.num}')


if __name__=='__main__':
    test()
