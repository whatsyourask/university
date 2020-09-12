def gcd(a, b) -> int:
    while b:
        a, b = b, a % b
    return a


def euler_func(n) -> int:
    temp = n - 1
    count = 0
    while temp:
        if not gcd(n, temp) - 1:
            count += 1
        temp -= 1
    return count


def test():
    n = 1000
    result = euler_func(n)
    answer = 400
    if answer == result:
        print('Passed')


if __name__=='__main__':
    test()
