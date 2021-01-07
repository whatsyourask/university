from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from typing import List, Dict, Tuple


def get_image(filename: str):
    # Берём пиксели из изображения
    image = np.array(Image.open(filename), dtype='uint8')
    return image


def quantization(matrix) -> List:
    # Квантование по формуле
    # Берём центральную строку
    center_pixs = matrix[len(matrix) // 2]
    # Квантуем
    center_pixs = np.round(center_pixs / 20) * 20
    return center_pixs


def syms_frequencies_in_pixels_seq(center_pixs: List) -> Dict:
    # Находим уникальные символы/пиксели
    uniq_syms        = np.unique(center_pixs)
    syms_frequencies = {}
    syms_count       = len(center_pixs)
    center_pixs      = list(center_pixs)
    for uniq_sym in uniq_syms:
        # Считаем кол-во уникального пикселя в последовательности
        count     = center_pixs.count(uniq_sym)
        # Находим частоту
        frequency = count / syms_count
        # Кладём в словарь, где пиксель - ключ, частота - значение
        syms_frequencies[uniq_sym] = frequency
    return syms_frequencies


class Node:
    """Класс для узла дерева"""
    def __init__(self, sym_freq: Tuple(float, float),
                                     left: Node=None, right: Node=None) -> None:
        # sym_freq - кортеж (символ, частота)
        # left, right - ссылки на дочерние узлы
        self.sym_freq = sym_freq
        self.left     = left
        self.right    = right


class Tree:
    """Класс дерева с обходом в глубину для взятия всех кодов Хаффмана"""
    def __init__(self, root: Node) -> None:
        # Получаем корень дерева
        self._main_root = root

    def get_paths(self) -> Dict:
        # Находим все пути
        # Словарь, где пиксель - ключ, путь - значение
        self._paths = {}
        # Переменная для сохранения промежуточного пути
        self._path  = []
        self._walk_in_depth(self._main_root)
        return self._paths

    def _walk_in_depth(self, root: Node) -> None:
        # Обход в глубину
        if root.left:
            self._path.append('0')
            self._walk_in_depth(root.left)
        if root.right:
            self._path.append('1')
            self._walk_in_depth(root.right)
        # Т.к. при создании узлов, некоторые не имеют пикселя в поле syms_freq
        # то нам они не нужны в результате
        if root.sym_freq[0]:
            # Соединить элементы пути в строку и засунуть в словарь
            self._paths[root.sym_freq[0]] = ''.join(self._path)
        # Убрать последний элемент пути,
        # т.к. мы возвращаемся на предыдущий узел для продолжения обхода
        self._path = self._path[:-1]


def create_huffman_codes(syms_frequencies: Dict) -> Dict:
    # Создание кодов Хаффмана
    # Сортируем по убыванию
    descend_frequencies = sorted(syms_frequencies.items(),
                               key=lambda item: item[1],
                               reverse=True)
    # Создаем для каждого элемента новый узел без потомков в стэк
    stack = [Node(item) for item in descend_frequencies]
    # Пока в стэке не останется последний
    while len(stack) != 1:
        # Достаём левый узел, т.е. самый маленький по значению частоты
        left         = stack.pop()
        # Правый
        right        = stack.pop()
        # Вычисляем новое значение в узле
        new          = left.sym_freq[1] + right.sym_freq[1]
        # Создаем новый объект узла с потомками, из которых он сформирован
        node         = Node((None, new), left, right)
        # Кладём его в стэк
        stack.append(node)
        # Снова сортируем по убыванию
        stack.sort(key=lambda item: item.sym_freq[1], reverse=True)
    # Создаем дерево от единственного элемента в стэке, что является корневым
    tree  = Tree(stack[0])
    # Находим пути в дереве или коды
    codes = tree.get_paths()
    return codes


def encode(sequence: List, codes: Dict) -> str:
    # Кодируем последовательность
    encoded = []
    for item in sequence:
        # Для каждого элемента последовательности находим соответствующий код
        encoded.append(codes[item])
    return encoded


def estimate(codes: Dict, syms_frequencies: Dict, count: int) -> Tuple:
    # Оценка качества кодирования
    # Берём из словаря только частоты
    frequencies = list(syms_frequencies.values())
    # Вычисляем энтропию
    entropy = - np.sum(frequencies * np.log2(frequencies))
    # Вычисляем среднюю длину кода
    mean_length = 0
    for symbol in syms_frequencies.keys():
        # Для каждого символа берём его частоту
        #  и умножаем на длину соответствующего кода
        mean_length += syms_frequencies[symbol] * len(codes[symbol])
    # Вычисляем относительную избыточность
    rel_redundancy = (1 - entropy / mean_length)
    return entropy, mean_length, rel_redundancy


def main():
    filename = 'parrot.gif'
    image    = get_image(filename)
    print(f'Picture size = {image.shape}')
    print(f'Pixel value max = {np.max(image)}')
    center_pixs = quantization(image)
    print(f'Center pixels = {center_pixs}')
    syms_frequencies = syms_frequencies_in_pixels_seq(center_pixs)
    print(f'Frequency as "symbol: frequency" = {syms_frequencies}')
    codes = create_huffman_codes(syms_frequencies)
    print(f'Huffman codes as "symbol: code" = {codes}')
    encoded = encode(center_pixs, codes)
    print(f'Encoded sequence = {"".join(encoded)}')
    entropy, mean_length, rel_redundancy = estimate(codes,
                                                    syms_frequencies,
                                                    len(center_pixs))
    print(f'Entropy = {entropy}')
    print(f'Mean length = {mean_length}')
    print(f'Relative redundancy = {rel_redundancy}')


main()
