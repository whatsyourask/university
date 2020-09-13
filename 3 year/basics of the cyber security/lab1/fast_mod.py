from typing import List


def to_binary(b) -> List:
    binary = []
    while b != 1:
        binary.append(b % 2)
        b //= 2
    binary.append(b)
    binary.reverse()
    return binary


def fast_mod_powers(n, a, b) -> int:
    binary = to_binary(b)
    temp   = a
    for e in binary[1:]:
        temp = (a * (temp ** 2)) % n if e else (temp ** 2) % n
    return temp


def test():
    n      = 527
    a      = 24
    b      = 117
    result = fast_mod_powers(n, a, b)
    answer = 232
    if result == answer:
        print('Passed')


if __name__=='__main__':
    test()
