from typing import List
import re
import string
import random


class AdditiveCipher:
    __EN_ALPH_LEN = 26
    __RU_ALPH_LEN = 33
    __ALPH_ONE_CHR = 6
    ENCRYPT_MODE = 0
    DECRYPT_MODE = 1
    def __init__(self, lang: str, letter_case: str) -> None:
        self.__create_trans_table(lang)
        self.__chosen_case = letter_case
        self.__alph_len = len(self.__alphabet)

    def __create_trans_table(self, lang: str) -> None:
        if lang == 'en':
            self.__alphabet = self.__load_alphabet('A', self.__EN_ALPH_LEN)
        if lang == 'ru':
            self.__alphabet = self.__load_alphabet('А', self.__RU_ALPH_LEN - 1)
            letter_index = self.__alphabet.index('Ж')
            self.__alphabet.insert(letter_index, 'Ё')
        self.__chosen_lang = lang
        self.__alphabet.extend([str(num) for num in range(0, 10)])
        # self.__alphabet += string.punctuation[:64 - len(self.__alphabet)]
        # print(self.__alphabet)
        # print(len(self.__alphabet))

    def __load_alphabet(self, first_letter: str, alph_len: int) -> List:
        first_num = ord(first_letter)
        return [chr(char_num) for char_num in range(first_num,
                                                    first_num + alph_len)]

    def crypt(self, plaintext: str, keyword: str=None,
                mode=ENCRYPT_MODE) -> str:
        #print(f'plaintext = {plaintext}\n')
        self.__punctuation_validation(plaintext, keyword)
        self.__language_validation(plaintext, keyword)
        self.__case_validation(plaintext, keyword)
        to_lower = False
        if plaintext.islower():
            plaintext = plaintext.upper()
            to_lower = True
        if keyword:
            ciphertext = self.__crypt_with_keyword(plaintext, keyword, mode)
        else:
            ciphertext = self.__crypt_without_keyword(plaintext, mode)
        if to_lower:
            ciphertext = ciphertext.lower()
        return ciphertext

    def __crypt_with_keyword(self, plaintext: str, keyword: str, mode) -> str:
        if keyword.islower():
            keyword = keyword.upper()
        keyword = self.__modify_keyword(plaintext, keyword)
        ciphertext = self.__crypto_algorithm(plaintext, keyword, mode)
        return ciphertext

    def __punctuation_validation(self, plaintext: str, keyword: str) -> None:
        no_punct = re.compile(f'[{re.escape(string.punctuation)}\s]')
        in_plaintext = no_punct.findall(plaintext)
        in_keyword = no_punct.findall(keyword) if keyword is not None else False
        if in_plaintext or in_keyword:
            raise ValueError

    def __language_validation(self, plaintext: str, keyword: str) -> None:
        #print(plaintext)
        en_lang = re.compile('[a-zA-Z]')
        ru_lang = re.compile('[а-яА-Я]')
        en_rules = [self.__chosen_lang == 'en',
                    not ru_lang.findall(plaintext)]
        ru_rules = [self.__chosen_lang == 'ru',
                    not en_lang.findall(plaintext)]
        if keyword:
            en_rules.append(not ru_lang.findall(keyword))
            ru_rules.append(not en_lang.findall(keyword))
        if all(en_rules) and all(ru_rules):
            raise ValueError

    def __case_validation(self, plaintext: str, keyword: str) -> None:
        plain_upper_or_digit = [plaintext.isupper(), plaintext.isdigit()]
        plain_upper = [self.__chosen_case == 'upper', any(plain_upper_or_digit)]
        plain_lower_or_digit = [plaintext.islower(), plaintext.isdigit()]
        plain_lower = [self.__chosen_case == 'lower', any(plain_lower_or_digit)]
        if keyword:
            key_upper_or_digit = [keyword.isupper(), keyword.isdigit()]
            key_upper = [all(plain_upper), any(key_upper_or_digit)]
            key_lower_or_digit = [keyword.islower(), keyword.isdigit()]
            key_lower = [all(plain_lower), any(key_lower_or_digit)]
            check_case = [all(key_upper), all(key_lower)]
        else:
            check_case = [all(plain_lower), all(plain_upper)]
        if not any(check_case):
            raise ValueError

    def __modify_keyword(self, plaintext: str, keyword: str) -> str:
        keyword_len = len(keyword)
        plaintext_len = len(plaintext)
        if keyword_len != plaintext_len:
            count = plaintext_len // keyword_len
            mod = plaintext_len % keyword_len
            keyword = keyword * count + keyword[:mod]
        return keyword

    def __crypto_algorithm(self, plaintext: str, keyword: str, mode: int) -> str:
        ciphertext = []
        # print('plain = ', plaintext)
        # print(len(plaintext))
        # print('keyword = ', keyword)
        # print(len(keyword))
        # print(self.__alph_len)
        for plain, key in zip(plaintext, keyword):
            plain_ind = self.__alphabet.index(plain) + 1
            key_ind = self.__alphabet.index(key) + 1
            # print(plain_ind)
            # print(key_ind)
            if not mode:
                cipher = (plain_ind + key_ind) % self.__alph_len
            else:
                cipher = (plain_ind - key_ind + self.__alph_len) % self.__alph_len
            if not cipher:
                cipher = self.__alph_len
            # print('cipher = ', cipher)
            ciphertext.append(self.__alphabet[cipher - 1])
        ciphertext = ''.join(ciphertext)
        #print(ciphertext)
        return ciphertext

    def __crypt_without_keyword(self, plaintext: str, mode: int) -> str:
        keyword = self.__create_keyword(len(plaintext))
        self.__key_validation(keyword)

    def __create_keyword(self, plaintext_len: int) -> List:
        half = plaintext_len // 2
        zeros = '0' * half * self.__ALPH_ONE_CHR
        ones = '1' * (plaintext_len - half) * self.__ALPH_ONE_CHR
        keyword = list(zeros + ones)
        print(keyword)
        random.shuffle(keyword)
        print(keyword)
        return keyword

    def __key_validation(self, keyword: List) -> str:
        keyword_parts = []
        for i in range(0, len(keyword), self.__ALPH_ONE_CHR):
            keyword_parts.append(keyword[i: i + self.__ALPH_ONE_CHR])
        for part in keyword_parts:
            num = int(''.join(part), 2)
            print(num)
