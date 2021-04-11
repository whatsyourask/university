from typing import List, Tuple
import re
import string
import random


class AdditiveCipher:
    """Class which perform XOR or Additive encryption and decryption"""
    __EN_ALPH_LEN = 26
    __RU_ALPH_LEN = 33
    __ALPH_ONE_CHR = 6
    def __init__(self, lang: str) -> None:
        # Constructor
        self.__create_trans_table(lang)
        self.__alph_len = len(self.__alphabet)

    def __create_trans_table(self, lang: str) -> None:
        # Create translate table
        if lang == 'en':
            self.__alphabet = string.ascii_uppercase
        if lang == 'ru':
            self.__alphabet = self.__load_alphabet('А', self.__RU_ALPH_LEN - 1)
            # Put an additional russian letter to alphabet
            letter_index = self.__alphabet.index('Ж')
            self.__alphabet = self.__alphabet[:letter_index] + 'Ё' \
                                                + self.__alphabet[letter_index:]
        self.__chosen_lang = lang
        self.__alphabet += string.digits
        self.__alphabet += string.punctuation[:64 - len(self.__alphabet)]

    def __load_alphabet(self, first_letter: str, alph_len: int) -> str:
        # Method to generate russian alphabet
        first_num = ord(first_letter)
        return ''.join([chr(char_num) for char_num in range(first_num,
                                                    first_num + alph_len)])

    def crypt(self, data: str, key: str=None) -> str:
        # Method to encrypt or decrypt data with key
        self.__language_validation(data, key)
        data = data.upper()
        if key:
            result = self.__crypt_with_key(data, key)
        else:
            result = self.__crypt_without_key(data)
        return result

    def __crypt_with_key(self, data: str, key: str) -> str:
        key = key.upper()
        # If key is shorter than data then you need to expand it
        key = self.__modify_key(data, key)
        # Start the main algorithm
        result = self.__crypto_algorithm(data, key)
        return result

    def __language_validation(self, data: str, key: str=None) -> None:
        # Validate that data and choosen language are equal
        # Compile to regex patterns
        # For english, russian and punctuation
        en_lang = re.compile('[a-zA-Z]')
        punct = re.compile(f'[{re.escape(string.punctuation)}\s]')
        ru_lang = re.compile('[а-яА-Я]')
        print(self.__chosen_lang)
        print(punct.findall(data))
        print(not ru_lang.findall(data))
        # Rules to validate
        en_rules = [self.__chosen_lang == 'en',
            (not ru_lang.findall(data)) or punct.findall(data)]
        ru_rules = [self.__chosen_lang == 'ru',
            (not en_lang.findall(data)) or punct.findall(data)]
        if key is not None:
            # If we have the key then also validate it
            en_rules.append((not ru_lang.findall(key)) or punct.findall(key))
            ru_rules.append((not en_lang.findall(key)) or punct.findall(key))
        print(all(en_rules))
        print(all(ru_rules))
        if all(en_rules) and all(ru_rules):
            print('raise?')
            raise ValueError

    def __modify_key(self, data: str, key: str) -> str:
        # Addition of the key
        key_len = len(key)
        data_len = len(data)
        if key_len != data_len:
            count = data_len // key_len
            mod = data_len % key_len
            key = key * count + key[:mod]
        return key

    def __crypto_algorithm(self, data: str, key: str) -> str:
        # Main algorithm to encrypt or decrypt data
        result = []
        # Lists to store binary view of data, key, and result
        self.__bin_data = []
        self.__bin_key = []
        self.__bin_result = []
        for data, key in zip(data, key):
            data_ind = self.__alphabet.index(data)
            self.__bin_data.append(self.__to_binary(data_ind))
            key_ind = self.__alphabet.index(key)
            self.__bin_key.append(self.__to_binary(key_ind))
            result_ind = data_ind ^ key_ind
            self.__bin_result.append(self.__to_binary(result_ind))
            result.append(self.__alphabet[result_ind])
        result = ''.join(result)
        self.__bin_data = '|'.join(self.__bin_data)
        self.__bin_key = '|'.join(self.__bin_key)
        self.__bin_result = '|'.join(self.__bin_result)
        return result

    def __crypt_without_key(self, data: str) -> str:
        # Method to crypt without key
        # Create a new key
        key = self.__create_key(len(data))
        # Save it within the field
        self.__key = key
        # Execute the algorithm
        return self.__crypto_algorithm(data, key)

    def __create_key(self, key_len: int) -> str:
        # Generation of the key
        half = key_len // 2
        zeros = '0' * half * self.__ALPH_ONE_CHR
        ones = '1' * (key_len - half) * self.__ALPH_ONE_CHR
        key = list(zeros + ones)
        random.shuffle(key)
        key_parts = []
        for i in range(0, len(key), self.__ALPH_ONE_CHR):
            key_parts.append(''.join(key[i: i + self.__ALPH_ONE_CHR]))
        binary_view = key_parts.copy()
        key = []
        for part in key_parts:
            result_ind = int(''.join(part), 2)
            key.append(self.__alphabet[result_ind])
        self.__bin_key = '|'.join(binary_view)
        return ''.join(key)

    def __to_binary(self, number: int) -> str:
        # Convert to binary view
        return str(bin(number))[2:]

    @property
    def key(self) -> str:
        return self.__key

    @property
    def bin_key(self) -> str:
        return self.__bin_key

    @property
    def bin_data(self) -> str:
        return self.__bin_data

    @property
    def bin_result(self) -> str:
        return self.__bin_result

    def generate_key(self, data: str) -> str:
        # Generate key without execution of main crypt algorithm
        self.__language_validation(data)
        key_len = len(data)
        return self.__create_key(key_len)
