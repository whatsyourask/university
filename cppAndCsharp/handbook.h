#include <iostream>
#include <string>
#include <fstream>
using namespace std;

//структура данных о человеке(номер и имя)
struct human {
	string name, phone_number;
};

//класс телефонного справочника
class handbook {
	int n;
	human *book;
public:
	handbook(int n);
	~handbook();
	friend istream& operator>>(istream& str, handbook& directory);
	friend ostream& operator<<(ostream& str, handbook& directory);
	void writeDat(string &file_name);
	void readDat(string &file_name);
	void writeTxt(string &file_name);
	void readTxt(string &file_name);
	string search(string &name);
	void add(string &name, string &phone);
	void remove(int &i);
	human get(int &i);
	human operator[](int &i);
};

//конструктор
handbook::handbook(int n) {
	this->n = n;
	book = new human[n];
}

//деструктор
handbook::~handbook() {
	delete[] book;
}

//перегрузка оператора ввода
istream& operator>>(istream& str, handbook& directory) {
	for (int i = 0; i < directory.n; i++)
		str >> directory.book[i].name >> directory.book[i].phone_number;
	return str;
}

//перегрузка оператора вывода
ostream& operator<<(ostream& str, handbook& directory) {
	for (int i = 0; i < directory.n; i++)
		str << "[" << i + 1 << "] " << directory.book[i].name << " " << directory.book[i].phone_number << endl;
	return str;
}

//метод записи в дат файл
void handbook::writeDat(string &file_name) {
	ofstream out(file_name, ios::binary | ios::trunc);
	out.write((char *)&n, sizeof(int));
	out.write((char *)book, sizeof(human)*n);
	out.close();
}

//метод чтения из дат файла
void handbook::readDat(string &file_name) {
	ifstream in(file_name, ios::binary);
	int k;
	in.read((char *)&k, sizeof(int));
	human *copy_of_the_book = new human[k];
	in.read((char *)copy_of_the_book, sizeof(human)*k);
	in.close();
	for (int i = 0; i < k; i++)
		cout << "[" << i << "] " << copy_of_the_book[i].name << " " << copy_of_the_book[i].phone_number << endl;
	delete[] copy_of_the_book;
}

//метод записи в текстовый файл
void handbook::writeTxt(string &file_name) {
	ofstream out(file_name);
	out << n << " " << "\n";
	for (int i = 0; i < n; i++) {
		out << book[i].name << " " << book[i].phone_number;
		out << "\n";
	}
	out.close();
}

//метод чтения из текстового файла
void handbook::readTxt(string &file_name) {
	ifstream in(file_name);
	int k;
	in >> k;
	human *copy_of_the_book = new human[k];
	for (int i = 0; i < k; i++) {
		in >> copy_of_the_book[i].name;
		in >> copy_of_the_book[i].phone_number;
	}
	in.close();
	for (int i = 0; i < k; i++)
		cout << "[" << i << "] " << copy_of_the_book[i].name << " " << copy_of_the_book[i].phone_number << endl;
	delete[] copy_of_the_book;
}

//поиск номера по имени
string handbook::search(string &name) {
	int i;
	bool searching = false;
	for (i = 0; i < n&&searching == false; i++)
		if (book[i].name == name)
			searching = true;
	return book[i - 1].phone_number;
}

//добавить номер и имя
void handbook::add(string &name, string &phone) {
	n++;
	human *copy_of_the_book = new human[n];
	for (int i = 0; i < n - 1; i++) {
		copy_of_the_book[i].name = book[i].name;
		copy_of_the_book[i].phone_number = book[i].phone_number;
	}
	copy_of_the_book[n - 1].name = name;
	copy_of_the_book[n - 1].phone_number = phone;
	this->book = copy_of_the_book;
}

//удалить номер и имя с индексом i
void handbook::remove(int &i) {
	n--;
	human *copy_of_the_book = new human[n];
	for (int j = 0, q = 0; j < n;) {
		if (q != i - 1) {
			copy_of_the_book[j].name = book[q].name;
			copy_of_the_book[j].phone_number = book[q].phone_number;
			j++;
		}
		q++;
	}
	this->book = copy_of_the_book;
}

//метод получения номера и имени по индексу i
human handbook::get(int &i) {
	human info;
	info.name = book[i - 1].name;
	info.phone_number = book[i - 1].phone_number;
	return info;
}

//перегрузка оператора [] с использованием функции get 
human handbook::operator[](int &i) {
	return get(i);
}