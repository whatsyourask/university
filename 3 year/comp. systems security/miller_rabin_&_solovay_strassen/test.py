from backend import MillerRabin, SolovayStrassen, legendre_symbol
import unittest


class TestMillerRabin(unittest.TestCase):
    def test1(self) -> None:
        self.__validate_method(13214124123, 10, False)

    def test2(self) -> None:
        self.__validate_method(1321412412321341234123213412343, 423, False)

    def test_equal_2(self) -> None:
        self.__check_raise(2, 10)

    def test_less_than_2(self) -> None:
        self.__check_raise(-5, 10)

    def __check_raise(self, n: int, k: int) -> None:
        self.assertRaises(ValueError, MillerRabin.test, n, k)

    def __validate_method(self, n: int, k: int, answer: bool) -> None:
        self.assertEqual(MillerRabin.test(n, k), answer)


class TestLegenreSymbol(unittest.TestCase):
    def test1(self) -> None:
        self.__validate_method(30, 23, -1)

    def __validate_method(self, a: int, p: int, answer: int) -> None:
        self.assertEqual(legendre_symbol(a, p), answer)
