#include <windows.h>
#include <tchar.h>
#include <strsafe.h>
#include <iostream>
using namespace std;

#define BUF_SIZE 255

// Кол-во строк, столбцов, кол-во частей результирующего вектора
int rows, columns, q;

// Указатели для матрицы, вектора, результирующего вектора
int** matrix, * vector, * result_vector;

// Выделение памяти и заполнение матрицы
void init_matrix();

// Заполнение вектора и вывод в консоль
void init_vector(int *v, int rows);

// Заполнение вектора нулями
void set_zeros(int *v, int rows);

// Указатель на массив дескрипторов мьютексов
HANDLE* hMutexArray;

// Функция потока
DWORD WINAPI multiplication(LPVOID lpParam);

// Вывод результата
void write_result_vector();

// Удаление матрицы
void delete_matrix();

int _tmain() {
	srand(GetTickCount64());
	cout << "write n ";
	cin >> rows;
	cout << "write m ";
	cin >> columns;
	cout << "write q ";
	cin >> q;

	// Выделение памяти и инициализация матрицы случайными значениями
	init_matrix();

	// Выделение памяти для вектора
	vector = new int[columns];

	// Инициализация вектора случайными значениям и вывод
	cout << "vector" << endl;
	init_vector(vector, columns);
	cout << endl;

	// Выделение памяти для результирующего вектора
	result_vector = new int[rows];

	// Инициализация вектора нулями
	set_zeros(result_vector, rows);

	// Выделение памяти для массива дескрипторов мьютексов
	hMutexArray = new HANDLE[q];

	for (int i = 0; i < q; i++)
		// Создание i-ого мьютекса,
		// не позволяя наследовать процесс, 
		// не позволяя процессу владеть мьютексом, 
		// без имени
		hMutexArray[i] = CreateMutex(NULL, FALSE, NULL);

	// Кол-во потоков и блоков
	int thread_count = q * q;

	// Выделение памяти для вектора дескрипторов потоков
	HANDLE* hThreadArray = new HANDLE[thread_count];

	// Создание потоков
	for (int i = 0; i < thread_count; i++)
		hThreadArray[i] = CreateThread(
			NULL,
			0,
			multiplication,
			(LPVOID)i,
			0,
			0
			);

	// Ожидание завершения работы всех созданных потоков
	// или пока не истечёт интервал(в данном случае бесконечность)
	WaitForMultipleObjects(thread_count, hThreadArray, TRUE, INFINITE);

	// Закрытие дескрипторов потоков
	for (int i = 0; i < thread_count; i++)
		CloseHandle(hThreadArray[i]);

	// Закрытие дескрипторов мьютексов
	for (int i = 0; i < q; i++)
		CloseHandle(hMutexArray[i]);

	// Вывод результирующего вектора
	write_result_vector();

	delete_matrix();
	delete[] vector;
	delete[] result_vector;
	delete[] hMutexArray;
	delete[] hThreadArray;
 	return 0;
}

void init_matrix() {
	// Выделение памяти под каждый указатель на строку
	matrix = new int* [rows];

	// Выделение памяти под каждую строку, и заполнение этой строки случайными числами, и вывод в консоль
	cout << "matrix" << endl;
	for (int i = 0; i < rows; i++) {
		matrix[i] = new int[columns];
		init_vector(matrix[i], columns);
	}
	cout << endl;
}

void init_vector(int *v, int rows) {
	// Заполнение вектора случайными числами и вывод в консоль
	for (int i = 0; i < rows; i++){
		v[i] = rand() % 10 + 1;
		cout << v[i] << " ";
	}
	cout << endl;
}

void set_zeros(int *v,int rows) {
	// Заполнение вектора нулями
	for (int i = 0; i < rows; i++)
		v[i] = 0;
}

DWORD WINAPI multiplication(LPVOID lpParam) {
	char msgBuf[BUF_SIZE];

	// Индекс блока, что обрабатывается в потоке
	int block_index = (int)lpParam;

	// Размеры строк и столбцов блока
	int block_rows = rows / q;
	int block_columns = columns / q;

	// Вектор, для промежуточных вычислений
	int* temp_vector = new int[block_rows];

	// Инициализация нулями для суммирования в вектор промежуточных вычислений
	set_zeros(temp_vector, block_rows);

	// Начало итерации по строке и столбцу
	int row_start = block_index / q * block_rows;
	int column_start = block_index % q * block_columns;

	// Конец итерации по строке и столбцу
	int row_end = row_start + block_rows;
	int column_end = column_start + block_columns;

	// Умножение блока на часть вектора
	for (int i = row_start; i < row_end; i++)
		for (int j = column_start; j < column_end; j++)
			temp_vector[i - row_start] += matrix[i][j] * vector[j];

	// Кол-во байт, записанных в строку
	int write_char_count;

	// Выводим вектор, что вычислил поток и плюсуем его в результирующий вектор
	write_char_count = sprintf_s(msgBuf, BUF_SIZE, "Block (%d, %d)\n", block_index / q, block_index % q);
	for (int i = row_start; i < row_end; i++) {
		write_char_count += sprintf_s(msgBuf + write_char_count, BUF_SIZE - write_char_count, "%d (index: %d) ", temp_vector[i - row_start], i);
	}
	sprintf_s(msgBuf + write_char_count, BUF_SIZE - write_char_count, "\n");

	// Вывод получившейся строки в консоль
	printf("%s", msgBuf);

	// Поток ожидает получение мьютекса
	WaitForSingleObject(hMutexArray[block_index / q], INFINITE);
	
	// Запись в результирующий вектор
	for (int i = row_start; i < row_end; i++) {
		result_vector[i] += temp_vector[i - row_start];
	}

	// Освобождение потока от мьютекса
	ReleaseMutex(hMutexArray[block_index / q]);

	delete[] temp_vector;
	return 0;
}

void write_result_vector() {
	cout << endl << "result_vector" << endl;
	for (int i = 0; i < rows; i++)
		cout << result_vector[i] << " ";
}

void delete_matrix() {
	for (int i = 0; i < rows; i++)
		delete[] matrix[i];
	delete[] matrix;
}