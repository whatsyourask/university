#include <iostream>
using namespace std;

//структура координат точки
struct point {
	int x, y;
};

//класс прямая
class line {
	point one;
	point two;
public:
	line();
	line(int x1, int y1, int x2, int y2);
	bool crossing_lines(line second);
	~line();
	friend ostream& operator<<(ostream& str, line& first);
	friend istream& operator>>(istream& str, line& first);
};

//конструктор
line::line(){}

//конструктор копирования
line::line(const line& first) {
	one.x = first.one.x;
	one.y = first.one.y;
	two.x = first.two.x;
	two.y = first.two.y;
}

line::line(int x1, int y1, int x2, int y2) {
	this->one.x = x1;
	this->one.y = y1;
	this->two.x = x2;
	this->two.y = y2;
}
//деструктор
line::~line() {}

//метод определения пересечений прямых по 2 точкам
bool line::crossing_lines(line second) {
	int dx_k1 = (two.x - one.x), dx_k2 = (second.two.x - second.one.x);
	int dy_k1 = (two.y - one.y), dy_k2 = (second.two.y - second.one.y);
	if ((dy_k1 != 0 && dy_k2 != 0)) {
		int k1 = dx_k1 / dy_k1;
		int k2 = dx_k2 / dy_k2;
		if (k1 == k2)
			return false;
		else
			return true;
	}
	else if ((dy_k1 == 0 && dy_k2 != 0) || (dy_k2 == 0 && dy_k1 != 0))
		return true;
	else
		return false;
}

//перегрузка <<
ostream& operator<<(ostream& str, line& first) {
	str << first.one.x << " " << first.one.y << endl << first.two.x << " " << first.two.y << endl;
	return str;
}

//перегрузка >>
istream& operator>>(istream& str, line& first) {
	str >> first.one.x >> first.one.y >> first.two.x >> first.two.y;
	return str;
}

int main()
{
	line first;
	cin >> first;
	line second;
	cin >> second;
	cout << "cross = " << first.crossing_lines(second) << endl;
	system("pause");
	return 0;
}