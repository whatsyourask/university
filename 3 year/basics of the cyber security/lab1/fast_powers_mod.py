from typing import List, Tuple


def to_binary(b) -> List:
    binary = []
    while b != 1:
        binary.append(b % 2)
        b //= 2
    binary.append(b)
    binary.reverse()
    return binary


def fast_powers_mod(n, a, b) -> Tuple:
    binary     = to_binary(b)
    binary_str = ''.join([str(item) for item in binary])
    #print(binary_str)
    temp_arr   = [a]
    temp       = a
    for e in binary[1:]:
        temp = (a * (temp ** 2)) % n if e else (temp ** 2) % n
        temp_arr.append(temp)
    return temp, [binary, temp_arr], binary_str


def test():
    n      = 527
    a      = 24
    b      = 117
    result, _, _ = fast_powers_mod(n, a, b)
    answer = 232
    if result == answer:
        print('Passed')


if __name__=='__main__':
    test()
