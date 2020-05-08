#include <windows.h>
#include <tchar.h>
#include <strsafe.h>
#include <iostream>
#include <algorithm>
using namespace std;

// Заполнить массив случайными числами
void set_random_arr();

// Блочная сортировка
void block_sort(int p);

// Сортировка каждого блока по отдельности
void sort_each_block(int size_block);

// Функция потока
DWORD WINAPI sort_in_thread(LPVOID lp_param);

// Вывод массива
void print_arr();

// Тестирование на правильность
void test(int count, int p);

int* arr;
int n;
int block_size;

int _tmain() {
	cout << "Write n: ";
	cin >> n;
	int p;
	cout << "Write p: ";
	cin >> p;
	arr = new int[n];
	int test_count = 10;
	test(test_count, p);
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

void block_sort(int p) {
	// Если n не больше p, то поменять p, вычисляя половину от n
	if (n <= p) p = (n % 2 == 0) ? n / 2 : n / 2 + 1;

	// Если n не делится без остатка на p, дополнить его
	int new_n = n;
	while (new_n % p) new_n++;

	// Найти размер блока
	block_size = new_n / p;

	// Отсортировать каждый блок отдельно
	sort_each_block(block_size);

	// Выделение памяти под массив дескрипторов потоков
	HANDLE* hThreadArray = new HANDLE[p];

	// Цикл по шагам
	for (int step = 0; step < 2*p; step++) {
		cout << "step: " << step << endl;
		// Цикл по четно-нечётным линиям
		int handle = 0;
		for (int line = (step % 2) * block_size/2; line < n && line + block_size < new_n; line += block_size) {
			hThreadArray[handle] = CreateThread(
				NULL,
				0,
				sort_in_thread,
				(LPVOID)line,
				0,
				0
				);
			handle++;
			cout << "\tline: " << line << endl;
		}
		// Ожидание завершения работы всех созданных потоков
		// или пока не истечёт интервал(в данном случае бесконечность)
		WaitForMultipleObjects(handle, hThreadArray, TRUE, INFINITE);
		
		// Закрытие дескрипторов потоков
		for (int i = 0; i < handle; i++)
			CloseHandle(hThreadArray[i]);
	}
	// Удаление выделенной памяти под массив дескрипторов потоков
	delete[] hThreadArray;
}

void sort_each_block(int block_size) {
	// Сортировать блоки до последнего блока
	int i;
	for (i = 0; i + block_size < n; i += block_size) {
		sort(arr + i, arr + i + block_size);
	}
	// Последний блок отдельно
	sort(arr + i, arr + n);
}

DWORD WINAPI sort_in_thread(LPVOID lp_param) {
	int ind = (int)lp_param;

	// Вычисление длины блока
	// если это последний блок и он не равен block_size, то вычислить его длину как разницу длины массива и индекса первого элемента блока
	int length = (ind + block_size > n) ? n - ind : block_size;

	// Сортировка блока
	sort(arr + ind, arr + ind + length);
	return 0;
}

void print_arr() {
	// Вывод массива
	for (int i = 0; i < n; i++) {
		cout << arr[i] << " ";
	}
	cout << endl;
}

void test(int count, int p) {
	for (int new_p = p; new_p < count; new_p++) {
		cout << "p = " << new_p << endl;
		set_random_arr();
		block_sort(new_p);
		print_arr();
	}
}
