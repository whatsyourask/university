import unittest
from backend import AdditiveCipher


class TestBackend(unittest.TestCase):
    # def test_crypt_smaller_key(self):
    #     self.__check('HELLOWORLDZZZZZ1231231232', 'HELLO', 'en', 'upper',
    #                     'KEY SMALLER THAN PLAINTEXT')
    #
    # def test_crypt_bigger_key(self):
    #     self.__check('HELLOWORLD', 'HELLOWORLD12312312312', 'en', 'upper',
    #                     'KEY BIGGER THAN PLAINTEXT')
    #
    # def test_crypt_en_upper(self):
    #     self.__check('HELLOWORLD111', 'WORLDHELLO222', 'en', 'upper', 'EN UPPER')
    #
    # def test_crypt_en_lower(self):
    #     self.__check('helloworld111', 'worldhello222', 'en', 'lower', 'EN LOWER')
    #
    # def test_crypt_ru_upper(self):
    #     self.__check('ПРИВЕТМИР111', 'МИРПРИВЕТ222', 'ru', 'upper', 'RU UPPER')
    #
    # def test_crypt_ru_lower(self):
    #     self.__check('приветмир111', 'мирпривет222', 'ru', 'lower', 'RU LOWER')
    #
    # def test_crypt_with_punctuation(self):
    #     self.__check_raise('привет,мир!', 'мир,привет&', 'ru', 'lower',
    #                         'ALL WITH PUNCTUATION')
    #
    # def test_crypt_plaintext_with_punct(self):
    #     self.__check_raise('привет, мир!', 'мирпривет111', 'ru', 'lower',
    #                         'PLAINTEXT WITH PUNCTUATION')
    #
    # def test_crypt_different_lang(self):
    #     self.__check_raise('HELLOWORLD', 'WORLDHELLO', 'ru', 'upper',
    #                         'DIFFERENT LANG')
    #
    # def test_crypt_ru_with_en(self):
    #     self.__check_raise('приветмир111', 'helloworld11', 'ru', 'lower',
    #                         'RU WITH EN')
    #
    # def test_crypt_en_with_ru(self):
    #     self.__check_raise('helloworld11', 'приветмир111', 'en', 'lower',
    #                         'EN WITH RU')
    #
    # def test_crypt_punct_n_lang(self):
    #     self.__check_raise('привет, мир111', 'hello, world11', 'ru', 'lower',
    #                         'PUNCTUATION & LANGUAGE')
    #
    # def test_crypt_different_cases(self):
    #     self.__check_raise('HELLOWORLD111' , 'worldhello222', 'en', 'upper',
    #                         'CASES ARE NOT EQUALS')
    #
    # def test_crypt_ruslan(self):
    #     self.__check('Z9', '99', 'en', 'upper', 'RUSLAN TEST')

    # def test_crypt_without_keyword_differ_case(self):
    #     self.__check_raise('HELLOasdfdsaf', None, 'en', 'upper',
    #                         'WITHOUT KEYWORD AND DIFFERENT LANG')

    def test_crypt_without_keyword(self):
        self.__check('HELLOWORLDHELLOWORLD', None, 'en', 'upper',
                        'WITHOUT KEYWORD')

    def __check(self, plaintext: str, keyword: str, lang: str, letter_case: str,
                 log_message:str):
        answer = self.__execute_method(plaintext, keyword, lang, letter_case)
        self.assertEqual(answer, plaintext)
        print('\n[+] ' + log_message)

    def __execute_method(self, plaintext: str, keyword: str, lang: str,
                            letter_case: str) -> str:
        cipher = AdditiveCipher(lang, letter_case)
        ciphertext = cipher.crypt(plaintext, keyword)
        answer = cipher.crypt(ciphertext, keyword, AdditiveCipher.DECRYPT_MODE)
        return answer

    def __check_raise(self, plaintext: str, keyword: str, lang: str,
                        letter_case: str, log_message: str):
        self.assertRaises(ValueError, self.__execute_method, plaintext, keyword,
                            lang, letter_case)
        print('\n[+] ' + log_message)
