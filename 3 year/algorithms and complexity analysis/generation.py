from random import randrange, randint, choice
from string import ascii_letters, digits, punctuation
from datetime import datetime, timedelta


def generate_numbers(length: int) -> list:
    return generate(length, randrange, 0, 9)


def generate_integers(length: int) -> list:
    return generate(length, randint, -10000, 10000)


def generate_strings(length: int) -> list:
    return generate(length, generate_string, 10, 100)


def generate(length: int, func: callable, *args: list) -> list:
    return [func(*args) for _ in range(length)]


def generate_string(from_length: int, to_length: int) -> str:
    return ''.join(choice(ascii_letters + digits + punctuation) for i in range(randrange(from_length, to_length)))


def generate_dates(length: int) -> list:
    start = datetime.strptime('1/1/2020 1:30 PM', '%m/%d/%Y %I:%M %p')
    end = datetime.strptime('1/1/2021 4:50 AM', '%m/%d/%Y %I:%M %p')
    return generate(length, generate_date, start, end)


def generate_date(start, end):
    delta = end - start
    secs_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(secs_delta)
    return start + timedelta(seconds=random_second)


def main():
    numbers = generate_numbers(50)
    print(numbers)
    integers = generate_integers(500)
    print(integers)
    string = generate_string(10, 100)
    print(string)
    strings = generate_strings(50)
    print(strings)
    dates = generate_dates(100)
    print(dates)


if __name__=='__main__':
    main()
