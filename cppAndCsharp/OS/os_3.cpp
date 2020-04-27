#include <windows.h>
#include <tchar.h>
#include <strsafe.h>
#include <iostream>
#include <algorithm>
using namespace std;

// Заполнение массива случайными значениями
void init_arr(int n);

// Вывод всего массива
void write_arr(int n);

// Функция потока
DWORD WINAPI sum_pair(LPVOID lpParam);

// diff - разница между кол-вом элементов n и k 
int diff;
int* a;

int _tmain() {
	// n - длина массива, а также счётчик в while
	int n;
	cin >> n;

	// Инициализация массива
	init_arr(n);

	// Массив дескрипторов потоков
	HANDLE* hThreadArray = new HANDLE[n / 2];

	// k - длина подмассива равная целочисленному делению n на 2
	int k;

	// Если n равно 1, то ответ готов в 0-ом элементе
	while (n > 1) {
		k = n / 2;

		// Вычислить разницу
		diff = n - k;

		// Суммирование пар 
		for (int i = 0; i < k; i++) {
			// Создание i-ого потока
			// если n - нечётное, то разница diff тоже нечётная
			// поэтому элемент в середине массива не складывается в этом подмассиве
			hThreadArray[i] = CreateThread(
				NULL,
				0,
				sum_pair,
				(LPVOID)i,
				0,
				0
				);
		}

		// Ожидание завершения работы всех созданных потоков
		// или пока не истечёт интервал(в данном случае бесконечность)
		WaitForMultipleObjects(k, hThreadArray, TRUE, INFINITE);

		// Закрытие дескрипторов потоков
		for (int i = 0; i < k; i++)
			CloseHandle(hThreadArray[i]);

		// Вычесть из длины массива длину подмассива для суммирования
		n -= k;
		
		// Вывод промежуточного вычисления
		write_arr(n);
	}
	
	// Удаление выделенной памяти под массив дескрипторов потоков
	delete[] hThreadArray;

	cout << "sum = " << a[0];

	// Удаление выделенной памяти под массив
	delete[] a;
	return 0;
}

void init_arr(int n) {
	// Устанавливает начальное значение для генератора случайных чисел
	srand(GetTickCount64());

	// Выделение памяти под массив a
	a = new int[n];

	// Заполнение массива случайными числами от 1 до 10
	for (int i = 0; i < n; i++) {
		a[i] = rand() % 10 + 1;
		cout << a[i] << " ";
	}
	cout << endl;
}

void write_arr(int n) {
	for (int i = 0; i < n; i++)
		cout << a[i] << " ";
	cout << endl;
}

DWORD WINAPI sum_pair(LPVOID lpParam) {
	int i = (int)lpParam;

	// Сложение пары i и i + diff
	a[i] += a[i + diff];
	return 0;
}