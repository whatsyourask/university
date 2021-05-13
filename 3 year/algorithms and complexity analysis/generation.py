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


def generate_half_sorted(generate_func: callable, length: int, place: float) -> list:
    array = generate_func(length)
    part = int(length * place)
    first_part = array[:part]
    second_part = array[part:]
    return sorted(first_part) + second_part


def generate_half_sorted_numbers(length: int, percent: float) -> list:
    return generate_half_sorted(generate_numbers, length, percent)


def generate_half_sorted_integers(length: int, percent: float) -> list:
    return generate_half_sorted(generate_integers, length, percent)


def generate_half_sorted_strings(length: int, percent: float) -> list:
    return generate_half_sorted(generate_strings, length, percent)


def generate_half_sorted_dates(length: int, percent: float) -> list:
    return generate_half_sorted(generate_dates, length, percent)


def generate_reversed_sorted(generate_func: callable, length: int) -> list:
    array = generate_func(length)
    array.sort()
    return array

def generate_reversed_sorted_numbers(length: int) -> list:
    return generate_reversed_sorted(generate_numbers, length)


def generate_reversed_sorted_integers(length: int) -> list:
    return generate_reversed_sorted(generate_integers, length)


def generate_reversed_sorted_strings(length: int) -> list:
    return generate_reversed_sorted(generate_strings, length)


def generate_reversed_sorted_dates(length: int) -> list:
    return generate_reversed_sorted(generate_dates, length)


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
    percent = 0.8
    half_sorted_numbers = generate_half_sorted_numbers(50, percent)
    print(half_sorted_numbers)
    half_sorted_integers = generate_half_sorted_integers(50, percent)
    print(half_sorted_integers)
    half_sorted_strings = generate_half_sorted_strings(50, percent)
    print(half_sorted_strings)
    half_sorted_dates = generate_half_sorted_dates(50, percent)
    print(half_sorted_dates)


if __name__=='__main__':
    main()
