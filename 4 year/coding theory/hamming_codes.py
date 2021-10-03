from random import choice, choices
from bitarray import bitarray


def binary(char: int) -> tuple:
    bits = bitarray()
    bits.frombytes(char.encode())
    bits = list(bits)
    return bits[:8], bits[8:]


def check_digits(seq: list) -> None:
    # Вычисляем c1, c2, c4, c8, c13
    c0 = seq[2] + seq[4] + seq[6] + seq[8] + seq[10]
    c1 = seq[2] + seq[5] + seq[6] + seq[9] + seq[10]
    c3 = seq[4] + seq[5] + seq[6] + seq[11]
    c7 = seq[8] + seq[9] + seq[10] + seq[11]
    seq[0] = c0 % 2
    seq[1] = c1 % 2
    seq[3] = c3 % 2
    seq[7] = c7 % 2
    c12 = sum(seq[:-1]) % 2
    seq[12] = c12


def encode(char: list) -> list:
    length = 13
    # Создаём последовательность из 13 нулей
    temp_seq = [0] * length
    # Копируем m разряды в эту последовательность
    temp_seq[2], temp_seq[4], temp_seq[5], temp_seq[6] = char[:4]
    temp_seq[8], temp_seq[9], temp_seq[10], temp_seq[11] = char[4:]
    # Вычисляем проверочные разряды
    check_digits(temp_seq)
    return temp_seq


def encode_alphabet(binary_alphabet: list) -> list:
    # Кодируем все буквы
    encoded_alphabet = []
    for char in binary_alphabet:
        # Кодируем 1 символ
        # Переводим код ASCII в бинарную последовательность
        bin_seq1, bin_seq2 = binary(char)
        encoded_seq1 = encode(bin_seq1)
        encoded_seq2 = encode(bin_seq2)
        print(f'\t{char} -> {"".join(map(str, encoded_seq1))}{"".join(map(str, encoded_seq2))}')
        encoded_alphabet.append(encoded_seq1)
        encoded_alphabet.append(encoded_seq2)
    print()
    return encoded_alphabet


def invert_bit(char: list, ind: int) -> None:
    # Инвертируем 1 бит
    char[ind] = 0 if char[ind] == 1 else 1


def check_n_correct(char: list) -> str:
    # Проверка на ошибки и исправление
    length = 13
    # Временная переменная из 13 битов
    temp_seq = [0] * length
    # Копируем m разряды
    temp_seq[2], temp_seq[4], temp_seq[5], temp_seq[6] = char[2], char[4], char[5], char[6]
    temp_seq[8], temp_seq[9], temp_seq[10], temp_seq[11] = char[8], char[9], char[10], char[11]
    # Вычисляем проверочные разряды
    check_digits(temp_seq)
    # Сразу сравниваем входную последовательность и временную
    correct1 = temp_seq == char
    # Если не равны, то ищем ошибки
    if not correct1:
        # Складываем проверочные разряды
        checksum = 0
        for i in [0, 1, 3, 7, 12]:
            if temp_seq[i] != char[i]:
                checksum += i + 1
        # Вычисляем индекс ошибки
        ind = (checksum - 1) % length
        # Корректируем бит в обоих последовательностях
        invert_bit(temp_seq, ind)
        invert_bit(char, ind)
        # Снова вычисляем проверочные биты для временной последовательности
        check_digits(temp_seq)
        # Сравниваем последовательности
        # Если равны, то была 1 ошибка, иначе две
        correct2 = char == temp_seq
    char = ''.join(map(str, char))
    if correct1:
        print(f'\t0 ошибок для {char}')
    elif correct2:
        print(f'\t1 ошибка для {char}')
    else:
        print(f'\tБольше 1 ошибки для {char}')
    return char


def decode(char1: str, char2: str) -> str:
    # Декодирование обратно в символ
    bin_seq1 = [0] * 8
    bin_seq1[:4] = char1[2], char1[4], char1[5], char1[6]
    bin_seq1[4:] = char1[8], char1[9], char1[10], char1[11]
    bin_seq2 = [0] * 8
    bin_seq2[:4] = char2[2], char2[4], char2[5], char2[6]
    bin_seq2[4:] = char2[8], char2[9], char2[10], char2[11]
    bin_seq = list(map(int, bin_seq1 + bin_seq2))
    return bitarray(bin_seq).tobytes().decode()


def decode_alphabet(encoded_alphabet: list) -> None:
    # Декодирование
    for i in range(0, len(encoded_alphabet) - 1, 2):
        # Проверка ошибок в коде и исправление
        char1 = check_n_correct(encoded_alphabet[i])
        char2 = check_n_correct(encoded_alphabet[i + 1])
        try:
            char = decode(char1, char2)
            print(f'\tСимвол после декодирования - {char}')
        except UnicodeDecodeError:
            print('\tНевозможно декодировать')
    print()


def spoil_one_time(encoded_seq: list) -> None:
    # Выбираем 1 бит инвертируем
    ind = choice([2,4,5,6,8,9,10,11])
    invert_bit(encoded_seq, ind)


def spoil_two_times(encoded_seq: list) -> None:
    # Случайно выбираем 2 бита и инвертируем
    ind, ind2 = choices([2,4,5,6,8,9,10,11], k=2)
    invert_bit(encoded_seq, ind)
    invert_bit(encoded_seq, ind2)


def spoil_alphabet(encoded_alphabet: list, spoil_func) -> list:
    # Портим биты в каждой букве
    spoiled_alphabet = []
    for char in encoded_alphabet:
        # в зависимости от переданной функции, портим либо 1 бит, либо 2
        spoil_func(char)
        print(f'\t{"".join(map(str, char))}')
        spoiled_alphabet.append(char)
    print()
    return spoiled_alphabet


def get_uniq(alphabet: list) -> list:
    uniq_rows = []
    length = len(alphabet)
    for i in range(length):
        equal = False
        for j in range(i + 1, length):
            if alphabet[i] == alphabet[j]:
                equal = True
        if not equal:
            uniq_rows.append(alphabet[i])
    return uniq_rows


def min_distance(encoded_alphabet: list):
    uniq_rows = get_uniq(encoded_alphabet)
    min_d = 13
    length = len(uniq_rows)
    for i in range(length):
        for j in range(i + 1, length):
            temp_d = 13
            for k in range(len(uniq_rows[i])):
                if uniq_rows[i][k] == uniq_rows[j][k]:
                    temp_d -= 1
            if temp_d < min_d:
                min_d = temp_d
    print(min_d)


def main():
    alphabet = 'ЛМНОП'
    print('Режим кодирования:\n')
    encoded_alphabet = encode_alphabet(alphabet)
    print('Режим декодирования:\n')
    decode_alphabet(encoded_alphabet)
    print('Внос 1 ошибки:\n')
    spoiled_alphabet = spoil_alphabet(encoded_alphabet, spoil_one_time)
    print('Режим декодирования:\n')
    decode_alphabet(spoiled_alphabet)
    print('Внос 2 ошибок:\n')
    spoiled_alphabet = spoil_alphabet(encoded_alphabet, spoil_two_times)
    print('Режим декодирования:\n')
    decode_alphabet(spoiled_alphabet)
    min_distance(encoded_alphabet)


if __name__=='__main__':
    main()
