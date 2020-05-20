#include <windows.h>
#include <iostream>
#include <tchar.h>
#include <strsafe.h>
using namespace std;

#define BUF_SIZE 255

// Функция для всех философов
void philosophers();
// Функция активности философов
DWORD WINAPI activity(LPVOID lp_param);

int ph_count;
int iterations;

HANDLE semaphore;
HANDLE* hMutexArray;

int _tmain() {
	// Ввести кол-во философов count
	cout << "Write phylosophers count: ";
	cin >> ph_count;
	// Ввести кол-во проходов цикла философа iterations
	cout << "Write iteration count: ";
	cin >> iterations;
	philosophers();
	return 0;
}

void philosophers() {
	// Создать массив дескрипторов потоков размера ph_count
	HANDLE* hThreadArray = new HANDLE[ph_count];
	// Создать массив дескрипторов мьютексов размера ph_count
	hMutexArray = new HANDLE[ph_count];
	// Создать семафор с начальным значением ph_count - 1 
	semaphore = CreateSemaphore(
		NULL,
		ph_count - 1,
		ph_count - 1,
		NULL
		);
	// цикл по каждому философу
	int handle = 0;
	while (handle < ph_count) {
		// Создать i-ый мьютекс,
		// не позволяя наследовать процесс, 
		// не позволяя процессу владеть мьютексом, 
		// без имени
		hMutexArray[handle] = CreateMutex(NULL, FALSE, NULL);
		// Создать потоки для философов
		// Передать функцию обеда для философа
		hThreadArray[handle] = CreateThread(
			NULL,
			0,
			activity,
			(LPVOID)handle,
			0,
			0
			);
		handle++;
	}
	// Ожидать завершения работы всех созданных потоков
	// или пока не истечёт интервал(в данном случае бесконечность)
	WaitForMultipleObjects(handle, hThreadArray, TRUE, INFINITE);
	// Закрыть дескрипторы потоков и мьютексов
	for (int i = 0; i < handle; i++) {
		CloseHandle(hThreadArray[i]);
		CloseHandle(hMutexArray[i]);
	}
	// Очистить память
	delete[] hThreadArray;
	delete[] hMutexArray;
}

DWORD WINAPI activity(LPVOID lp_param) {
	// Номер философа для определения места и палочек
	int philosoph_number = (int)lp_param;
	int left_stick = philosoph_number;
	// Философ берёт правую палочку у соседа справа,
	// для последнего философа в массиве, сосед справа это 0 философ
	int right_stick;
	right_stick	= (philosoph_number != ph_count - 1) ? philosoph_number + 1 : 0;
	srand(GetTickCount64() + philosoph_number);
	// цикл по кол-ву необходимых обедов для 1 философа
	for (int dinner = 0; dinner < iterations; dinner++) {
		// Кол-во символов, записанных в строку
		int write_char_count = 0;
		// Размышление философа
		int think_time = (rand() % 5 + 1);
		// Печать сообщения, что философ размышляет
		printf("%d's thinking\n", philosoph_number);
		Sleep(think_time);
		bool try_to_have_lunch = true;
		DWORD wait_result;
		// Обед
		while (try_to_have_lunch) {
			// Попытаться войти в семафор(взять стул, например)
			wait_result = WaitForSingleObject(semaphore, INFINITE);
			// Если вошёл(сел за стол)
			if (wait_result == WAIT_OBJECT_0) {
				// Поток ожидает получение мьютекса левой палочки
				WaitForSingleObject(hMutexArray[left_stick], INFINITE);
				// Печать сообщения, что философ взял левую палочку
				printf("%d took left stick\n", philosoph_number);
				// Поток ожидает получение мьютекса правой палочки
				WaitForSingleObject(hMutexArray[right_stick], INFINITE);
				// Печать сообщения, что философ взял правую палочку
				printf("%d took right stick\n", philosoph_number);
				// Начать обедать, если обе палочки свободны
				try_to_have_lunch = false;
				int lunch_time = (rand() % 3 + 1);
				// Печать сообщения, что философ ест
				printf("%d's eating\n", philosoph_number);
				Sleep(lunch_time);
				// Освобождение потока от мьютекса левой палочки
				ReleaseMutex(hMutexArray[left_stick]);
				// Освобождение потока от мьютекса правой палочки
				ReleaseMutex(hMutexArray[right_stick]);
				ReleaseSemaphore(
					semaphore,	  // дескриптор семафора
					1,            // увеличить счетчик семафора на 1
					NULL		  // Предыдущее значение не нужно
					);
			}
			// Если не вошёл в семафор
			// Ждать пока освободится семафор(стул)
			// т.е. переход к следующей итерации
		}
	}
	return 0;
}