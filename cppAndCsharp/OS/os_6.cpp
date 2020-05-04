#include <windows.h>
#include <tchar.h>
#include <strsafe.h>
#include <iostream>
#include <algorithm>
using namespace std;

#define BUF_SIZE 255

// Заполнить массив случайными числами
void set_random_arr();

// Блочная сортировка
void block_sort();

// Сортировка каждого блока по отдельности
void sort_each_block(int size_block);

// Функция потока
DWORD WINAPI exchanges_sorting(LPVOID lp_param);

// Вывод массива
void print_arr();

int* arr;
int n;
int p;
int block_size;

int _tmain() {
	cout << "Write n: ";
	cin >> n;
	// Если n не больше p, то поменять p, вычисляя половину от n
	if (n <= p)
		p = (n % 2 == 0) ? n / 2 : n / 2 + 1;
	arr = new int[n];
	set_random_arr();
	cout << "Write p: ";
	cin >> p;
	block_sort();
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

void block_sort() {
	// Если n не делится без остатка на p, дополнить его
	int new_n;
	for (new_n = n; new_n % p != 0; new_n++);

	// Найти размер блока
	block_size = new_n / p / 2;

	// Отсортировать каждый блок отдельно
	sort_each_block(block_size);
	
	// Выделение памяти под массив дескрипторов потоков
	HANDLE* hThreadArray = new HANDLE[p];

	// Цикл по шагам
	for (int step = 0; step < 2 * p; step++) {
		// Цикл по четно-нечётным линиям пока, 
		int handle = 0;
		for (int line = (step % 2) * block_size; line + block_size < n; line += 2 * block_size) {
			hThreadArray[handle] = CreateThread(
				NULL,
				0,
				exchanges_sorting,
				(LPVOID)line,
				0,
				0
				);
			handle++;
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
	for (int i = 0; i < n; i += block_size)
		sort(arr + i, arr + i + block_size);
}

DWORD WINAPI exchanges_sorting(LPVOID lp_param) {
	int ind = (int)lp_param;

	// Создание 2 указателей на начала 2 блоков в исходном массива
	int* p_block1 = arr + ind;
	int* p_block2 = arr + ind + block_size;

	// Выделение памяти под временный массив для обмена
	int* temp = new int[block_size * 2];

	// Установка указателей на элементы блоков в исходном массиве
	for (int i = 0; i < block_size; i++) {
		temp[i] = p_block1[i];
		temp[i + block_size] = p_block2[i];
	}
	
	// Сортировка временного массива
	sort(temp, temp + 2 * block_size);

	// Возвращение элементов блоков в отсортированном порядке
	for (int i = 0; i < block_size; i++) {
		p_block1[i] = temp[i];
		p_block2[i] = temp[i + block_size];
	}
	return 0;
}


void print_arr() {
	// Вывод массива
	for (int i = 0; i < n; i++) {
		cout << arr[i] << " ";
	}
	cout << endl;
}