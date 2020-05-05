#include <windows.h>
#include <tchar.h>
#include <strsafe.h>
#include <iostream>
using namespace std;

#define BUF_SIZE 255

// Заполнить массив случайными числами
void set_random_arr();

// Сортирующая сеть
void sorting_network();

// Вывод массива
void print_arr();

// Функция потока
DWORD WINAPI exchange(LPVOID lp_param);

int* arr;
int n;

// Структура индексов линий, на которых расположено сравнивающее устройство 
struct LineInd{
	int begin;
	int end;
};

int _tmain() {
	cout << "Write n: ";
	cin >> n;
	arr = new int[n];
	set_random_arr();
	sorting_network();
	print_arr();
	delete[] arr;
	return 0;
}

void set_random_arr() {
	// Устанавливает начальное значение для генератора случайных чисел
	srand(GetTickCount64());

	// Заполнение массива случайными числами от 1 до 15
	for (int i = 0; i < n; i++) {
		arr[i] = rand() % 15 + 1;
		cout << arr[i] << " ";
	}
	cout << endl;
}

void sorting_network() {
	// Вычисление ближайшей степени двойки k+1, где 2^(k+1)>n
	int add_to_degree;
	for (add_to_degree = 2; add_to_degree < n; add_to_degree *= 2) {}
	int lines_count = add_to_degree;

	// Максимальное возможное кол-во потоков в сети
	int threads_count = n / 2;

	// Выделение памяти для массива дескрипторов потоков
	HANDLE* hThreadArray = new HANDLE[threads_count];

	// Выделение памяти для массива структур, что передаются для конкретного потока в его функцию
	LineInd* lineIndArr = new LineInd[threads_count];

	// Цикл по фазам слияния
	for (int phase = 1; phase < lines_count; phase += phase) {
		cout << "Phase: " << phase << "\n";

		// Вычисление удвоенной фазы для проверки на четность-нечетность линий, где расположено устройство
		int double_phase = (phase + phase);

		// Цикл по длинам сравнивающих устройств, возможных в текущей фазе
		for (int length = phase; length > 0; length /= 2) {
			cout << "\tComparator length: " << length << "\n";

			// Цикл по сравнивающим устройствам одинаковой длины,
			for (int number = 0; number < length && number + length % phase + length < n; number++) {
				cout << "\t\tComparator number: " << number << "\n";

				// Индекс нового потока в массиве дескрипторов потоков
				int handle = 0;

				// Цикл, что идёт по чётным или нечётным линиям в зависимости от длины устройства и фазы,
				// на которых есть сравнивающее устройство
				for (int line = length % phase; line + number + length < n; line += length + length) {
					// Вычисление индексов линии, где начало и конец устройства
					int begin = line + number;
					int end = begin + length;

					// Вычисление целого от начала и конца устройства, для проверки того, что начало и конец принадлежат одному устройству
					if (begin / double_phase == end / double_phase) {
						// Если линии совпадают, то создать поток и передать ему данные для сравнения
						lineIndArr[handle].begin = begin;
						lineIndArr[handle].end = end;
						hThreadArray[handle] = CreateThread(
							NULL,
							0,
							exchange,
							(LPVOID)&lineIndArr[handle],
							0,
							0
							);
						handle++;
					}
				}
				// Ожидание завершения работы всех созданных потоков
				// или пока не истечёт интервал(в данном случае бесконечность)
				WaitForMultipleObjects(handle, hThreadArray, TRUE, INFINITE);

				// Закрытие дескрипторов потоков
				for (int i = 0; i < handle; i++)
					CloseHandle(hThreadArray[i]);
			}
		}
	}
	// Удаление выделенной памяти под массив дескрипторов потоков
	delete[] hThreadArray;

	// Удаление выделенной памяти под массив структур
	delete[] lineIndArr;
}

void print_arr() {
	// Вывод массива
	for (int i = 0; i < n; i++) {
		cout << arr[i] << " ";
	}
}

DWORD WINAPI exchange(LPVOID lp_param) {
	LineInd* indexes = (LineInd*)lp_param;

	// Перестановка значений элементов, если наверх сравнивающего устройства пришло большее число, чем вниз
	if (arr[indexes->begin] > arr[indexes->end]) {
		int temp = arr[indexes->begin];
		arr[indexes->begin] = arr[indexes->end];
		arr[indexes->end] = temp;
	}

	// Массив для строки в консоль
	char msgBuf[BUF_SIZE];

	// Вывод индексов линии, где конец и начало устройства
	sprintf_s(msgBuf, BUF_SIZE, "\t\t\tExchange: %d, %d\n", indexes->begin, indexes->end);

	// Вывод получившейся строки в консоль
	printf("%s", msgBuf);
	return 0;
}