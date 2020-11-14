import numpy as np
from PIL import Image


def get_total_entropy(array) -> int:
    # Подсчёт всех уникальных элементов в массиве
    elements, count = np.unique(array, return_counts=True)
    print(f'elements = {elements}')
    print(f'each element count = {count}')
    # Подсчёт всех элементов в массиве
    all_count = np.sum(count)
    print(f'elements count = {all_count}')
    # Оценка вероятности каждого элемента
    p = count / all_count
    print(f'each element probability = {p}')
    # Энтропия элемента
    entropy = - np.sum(p * np.log2(p))
    print(f'one element entropy = {entropy}')
    # Общая энтропия
    total_entropy = entropy * all_count
    return total_entropy


def main():
    # Беру текст из файла
    text = np.array(list(open('book.txt', 'r').read()))
    print('\tBook:')
    # Считаю общую энтропию книги
    book_entropy = get_total_entropy(text)
    print(f'entropy = {book_entropy}')
    # Беру пиксели из изображения
    image = np.array(Image.open('image.jpg'), dtype='uint8')
    print('\n\tImage:')
    # Считаю общую энтропию изображения
    image_entropy = get_total_entropy(image)
    print(f'entropy = {image_entropy}')
    # Вывожу их отношение
    print(f'Book entropy / Image entropy = {book_entropy / image_entropy}')


main()
