#include <windows.h>
#include <iostream>
#include <tchar.h>
#include <strsafe.h>
#include <queue>
using namespace std;

// Инициализация потоков
void thread_init(HANDLE* hThreadArray, int count, LPTHREAD_START_ROUTINE address);

// Функция потока парикмахера
DWORD WINAPI barber_activity(LPVOID lp_param);

// Функция потока клиента
DWORD WINAPI client_activity(LPVOID lp_param);

int clients_count;
int haircuts_count;
int barbers_count;
int couch_seats;
int all_seats;

HANDLE free_wait_seats;
HANDLE free_service_seats;

struct Number {
	int number;
	HANDLE h;
};

queue<Number> wait_room;
queue<Number> service_room;

int _tmain() {
	// Ввести кол-во клиентов
	cout << "Write clients count: ";
	cin >> clients_count;
	// Ввести кол-во стрижек для одного клиента
	cout << "Write haircuts count: ";
	cin >> haircuts_count;
	// Ввести кол-во парикмахеров
	cout << "Write barbers count: ";
	cin >> barbers_count;
	// Ввести кол-во мест на диване
	cout << "Write seats on the couch count: ";
	cin >> couch_seats;
	// Общее кол-во мест в парикмахерской
	// Кол-во номерков равно общему кол-ву мест в парикмахерской
	all_seats = couch_seats + barbers_count;
	// Создать стол с номерками
	for (int i = 0; i < all_seats; i++) {
		Number n;
		n.number = i;
		n.h = CreateMutex(NULL, FALSE, NULL);
		wait_room.push(n);
	}
	// Инициализировать массив дескрипторов потоков парикмахеров
	HANDLE* hBarberArray = new HANDLE[barbers_count];
	// Создать семафор для входа в зал обслуживания
	free_service_seats = CreateSemaphore(NULL, barbers_count, barbers_count, NULL);
	// Инициализировать потоки парикмахеров
	thread_init(hBarberArray, barbers_count, barber_activity);
	// Инициализировать массив дескрипторов потоков клиентов
	HANDLE* hClientArray = new HANDLE[clients_count];
	// Создать семафор для входа в зал ожидания
	free_wait_seats = CreateSemaphore(NULL, couch_seats, couch_seats, NULL);
	// Инициализировать потоки клиентов
	thread_init(hClientArray, clients_count, client_activity);
	// Ожидать завершения работы всех созданных потоков
	// или пока не истечёт интервал(в данном случае бесконечность)
	WaitForMultipleObjects(clients_count, hClientArray, TRUE, INFINITE);
	// Закрыть дескрипторы потоков и мьютексов
	for (int i = 0; i < clients_count; i++) {
		CloseHandle(hClientArray[i]);
	}
	/*for (int i = 0; i < all_seats; i++) {
		HANDLE number = wait_room.front();
		CloseHandle(number);
		wait_room.pop();
	}*/
	//CloseHandle(free_wait_seats);
	//CloseHandle(free_service_seats);
	delete[] hClientArray;
	return 0;
}

void thread_init(HANDLE* hThreadArray, int count, LPTHREAD_START_ROUTINE address) {
	for (int handle = 0; handle < count; handle++) {
		hThreadArray[handle] = CreateThread(
			NULL,
			0,
			address,
			(LPVOID)handle,
			0,
			0
			);
	}
}

DWORD WINAPI barber_activity(LPVOID lp_param){
	int barber_number = (int)lp_param + 1;
	// Бесконечный цикл
	while (true) {
		bool empty = service_room.empty();
		printf("%d\n", empty);
		if(!empty) {
			printf("Barber %d is ready\n", barber_number);
			// Ждать пока на столике в зале ожидания появятся номерки
			// Взять номерок
			Number n = service_room.front();
			service_room.pop();
			WaitForSingleObject(n.h, INFINITE);
			// Стрижка
			printf("Barber %d haircuts a client with number %d\n", barber_number, n.number);
			srand(GetTickCount64() + barber_number);
			int haircut_time = (rand() % 3 + 1) * 1000;
			Sleep(haircut_time);
			// Известить клиента, что стрижка окончена
			ReleaseMutex(n.h);
			//// Подождать пока клиент освободит кресло
			//WaitForSingleObject(free_service_seats, INFINITE);
			// Положить номерок на стол в комнате ожидания
			wait_room.push(n);
			//// Известить нового клиента, что кресло свободно
			//ReleaseSemaphore(free_service_seats, 1, NULL);
		}
	}
	return 0;
}

DWORD WINAPI client_activity(LPVOID lp_param) {
	int client_number = (int)lp_param + 1;
	// Цикл по кол-ву стрижек, что должен сделать клиент
	for (int haircut = 0; haircut < haircuts_count; haircut++) {
		bool hair_is_done = false;
		// Если стрижка не сделана, крутиться в цикле
		while (!hair_is_done) {
			// Посмотреть есть ли места в парикмахерской
			DWORD empty_seat = WaitForSingleObject(free_wait_seats, (rand() % 3 + 1) * 1000);
			Number n;
			switch (empty_seat)
			{
			case WAIT_OBJECT_0:
				// Если места есть
				// Взять номерок
				n = wait_room.front();
				wait_room.pop();
				printf("Client %d in waiting room\n", client_number);
				// Ждать извещения о стрижке
				// Занять место в зале обслуживания, если есть свободные места
				WaitForSingleObject(free_service_seats, INFINITE);
				printf("Client %d sits in chair\n", client_number);
				// Значит, место в зале ожидания освобождается
				ReleaseSemaphore(free_wait_seats, 1, NULL);
				// Положить номерок
				service_room.push(n);
				// Ждать конца стрижки
				WaitForSingleObject(n.h, INFINITE);
				// Выйти из зала
				printf("Client %d got a haircut\n", client_number);
				hair_is_done = true;
				// Покинуть кресло
				ReleaseSemaphore(free_service_seats, 1, NULL);
				//// Написать, что кресло свободно
				//printf("Service seat is free\n");
				ReleaseMutex(n.h);
				printf("Client %d EXITS\n", client_number);
				break;
			case WAIT_TIMEOUT:
				printf("Client %d, No free seats in waiting room\n", client_number);
				srand(GetTickCount64() + client_number);
				// Если мест нет
				// Уйти из парикмахерской и вернуться через 1-5 сек
				int walk_time = (rand() % 5 + 1) * 1000;
				Sleep(walk_time);
				break;
			}
		}
		// Вернуться через 1-5 секунд за новой стрижкой
		srand(GetTickCount64() + client_number);
		int walk_time = (rand() % 5 + 1) * 1000;
		Sleep(walk_time);
	}
	return 0;
}