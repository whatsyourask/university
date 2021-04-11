import unittest
from backend import AdditiveCipher


class TestBackend(unittest.TestCase):
    """Class to test AdditiveCipher crypt method"""
    def test_crypt_smaller_key(self):
        self.__check('HELLOWORLDZZZZZ1231231232', 'HELLO', 'en',
                        'KEY SMALLER THAN data')

    def test_crypt_bigger_key(self):
        self.__check('HELLOWORLD', 'HELLOWORLD12312312312', 'en',
                        'KEY BIGGER THAN data')

    def test_crypt_en_upper(self):
        self.__check('HELLOWORLD111', 'WORLDHELLO222', 'en',  'EN UPPER')

    def test_crypt_en_lower(self):
        self.__check('helloworld111', 'worldhello222', 'en',  'EN LOWER')

    def test_crypt_ru_upper(self):
        self.__check('ПРИВЕТМИР111', 'МИРПРИВЕТ222', 'ru',  'RU UPPER')

    def test_crypt_ru_lower(self):
        self.__check('приветмир111', 'мирпривет222', 'ru',  'RU LOWER')

    def test_crypt_with_punctuation(self):
        self.__check('привет,мир!', 'мир,привет&', 'ru',
                            'ALL WITH PUNCTUATION')

    def test_crypt_data_with_punct(self):
        self.__check_raise('привет, мир!', 'мирпривет111', 'ru',
                            'data WITH PUNCTUATION')

    def test_crypt_different_lang(self):
        self.__check_raise('HELLOWORLD', 'WORLDHELLO', 'ru',
                            'DIFFERENT LANG')

    def test_crypt_ru_with_en(self):
        self.__check_raise('приветмир111', 'helloworld11', 'ru',
                            'RU WITH EN')

    def test_crypt_en_with_ru(self):
        self.__check_raise('helloworld11', 'приветмир111', 'en',
                            'EN WITH RU')

    def test_crypt_punct_n_lang(self):
        self.__check_raise('привет, мир111', 'hello, world11', 'ru',
                            'PUNCTUATION & LANGUAGE')

    def test_crypt_different_cases(self):
        self.__check('HELLOWORLD111' , 'worldhello222', 'en',
                            'CASES ARE NOT EQUALS')

    def test_crypt_ruslan(self):
        self.__check('Z9', '99', 'en',  'RUSLAN TEST')

    def test_crypt_without_key(self):
        self.__check('HELLOWORLDHELLOWORLD', None, 'en',
                        'WITHOUT KEY')

    def test_crypt_valid_punct_lang(self):
        self.__check('./.,/,/.,/../,', None, 'ru', 'PUNCTUATION + LANG')

    def test_crypt_valid_punct_diff_lang_from_chosen(self):
        self.__check('./././sa././.sa/dfas/./.', None, 'en',
                        'DIFF LANG FROM CHOSEN + PUNCTUATION')
                        
    def test_generate_key_with_diff_lang(self):
        cipher = AdditiveCipher('ru')
        self.assertRaises(ValueError, cipher.generate_key, 'asdfsadfsad')
        print('\n[+] GENERATE KEY WITH DIFF LANG')

    def __check(self, data: str, key: str, lang: str, log_message:str) -> None:
        # Main method of tests
        answer = self.__execute_crypt(data, key, lang)
        answer = answer.lower()
        data = data.lower()
        self.assertEqual(answer, data)
        print('\n[+] ' + log_message)

    def __execute_crypt(self, data: str, key: str, lang: str) -> str:
        # Method to exectu all needed operations with the object
        cipher = AdditiveCipher(lang)
        ciphertext = cipher.crypt(data, key)
        if not key:
            key = cipher.key
        answer = cipher.crypt(ciphertext, key)
        return answer

    def __check_raise(self, data: str, key: str, lang: str,
                                                    log_message: str) -> None:
        # Method with different assert that will check if there was an exception
        self.assertRaises(ValueError, self.__execute_crypt, data, key, lang)
        print('\n[+] ' + log_message)
