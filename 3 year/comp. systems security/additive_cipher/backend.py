from typing import List
import re
import string


class AdditiveCipher:
    __EN_ALPH_LEN = 26
    __RU_ALPH_LEN = 33
    def __init__(self, lang: str) -> None:
        self.__create_trans_table(lang)

    def __create_trans_table(self, lang: str) -> None:
        if lang == 'en':
            self.__alphabet = self.__load_alphabet('A', self.__EN_ALPH_LEN)
        if lang == 'ru':
            self.__alphabet = self.__load_alphabet('А', self.__RU_ALPH_LEN - 1)
            letter_index = self.__alphabet.index('Ж')
            self.__alphabet.insert(letter_index, 'Ё')
        self.__chosen_lang = lang
        self.__alphabet.extend([str(num) for num in range(0, 10)])

    def __load_alphabet(self, first_letter: str, alph_len: int) -> List:
        first_num = ord(first_letter)
        return [chr(char_num) for char_num in range(first_num,
                                                    first_num + alph_len)]

    def crypt(self, plaintext: str, keyword: str=None) -> str:
        print(f'plaintext = {plaintext}\n')
        self.__valid_punctutation(plaintext, keyword)
        self.__valid_language(plaintext, keyword)
        self.__valid_case(plaintext, keyword)
        to_lower = False
        if plaintext.islower():
            plaintext = plaintext.upper()
            to_lower = True
        if keyword:
            ciphertext = self.__crypt_with_keyword(plaintext, keyword)
        else:
            ciphertext = self.__crypt_without_keyword(plaintext)
        if to_lower:
            ciphertext = ciphertext.lower()
        return ciphertext

    def __crypt_with_keyword(self, plaintext: str, keyword: str) -> str:
        if keyword.islower():
            keyword = keyword.upper()
        keyword = self.__modify_keyword(plaintext, keyword)
        ciphertext = self.__crypto_algorithm(plaintext, keyword)
        return ciphertext

    def __valid_punctutation(self, plaintext: str, keyword: str) -> None:
        no_punct = re.compile(f'[{re.escape(string.punctuation)}\s]')
        in_plaintext = no_punct.findall(plaintext)
        in_keyword = no_punct.findall(keyword) if keyword is not None else False
        if in_plaintext or in_keyword:
            raise ValueError

    def __valid_language(self, plaintext: str, keyword: str) -> None:
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

    def __valid_case(self, plaintext: str, keyword: str) -> None:
        if keyword:
            not_equals = [plaintext.isupper() and keyword.islower(),
                          plaintext.islower() and keyword.isupper()]
        else:
            not_equals = [plaintext.isupper(), ]
        if any(not_equals):
            raise ValueError

    def __modify_keyword(self, plaintext: str, keyword: str) -> str:
        keyword_len = len(keyword)
        plaintext_len = len(plaintext)
        if keyword_len != plaintext_len:
            count = plaintext_len // keyword_len
            mod = plaintext_len % keyword_len
            keyword = keyword * count + keyword[:mod]
        return keyword

    def __crypto_algorithm(self, plaintext: str, keyword: str) -> str:
        ciphertext = []
        for plain, key in zip(plaintext, keyword):
            cipher = self.__alphabet.index(plain) ^ self.__alphabet.index(key)
            ciphertext.append(self.__alphabet[cipher])
        ciphertext = ''.join(ciphertext)
        return ciphertext

    def __crypt_without_keyword(self, plaintext: str) -> str:
        keyword = self.__create_keyword(len(plaintext))

    def __create_keyword(self, plaintext_len: int) -> str:
        half = plaintext_len // 2
        keyword = '0' * half + '1' * (plaintext_len - half)
        print(keyword)
