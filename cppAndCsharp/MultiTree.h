#include <iostream>
#include <stack>
#include <vector>
#include <queue>
using namespace std;

template<typename T>
class MultiTree {
	//Структура корня
	struct Node {
		T info;
		//Вектора ссылок на потомков корня
		vector <Node *> vectPoint;
		Node(T info) {
			this->info = info;
		}
	};
	Node *main_root = NULL;
public:
	MultiTree();
	void printWidth();
	void printDepth();
private:
	void Write_R(Node *root);
	void printDepth_R(Node *root);
};

//Конструктор дерева
template<typename T>
MultiTree<T>::MultiTree() {
	cout << "Write the main root info field:\t";
	T a;
	cin >> a;
	cin.ignore();
	main_root = new Node(a);
	Write_R(main_root);
}

template<typename T>
void MultiTree<T>::Write_R(Node *root) {
	int n;// кол-во потомков
	T num; // вводимые данные в инфо-поле
	int answ; // переменная для запроса на продолжение заполнения поддерева
	cout << "How many subtrees you want? ";
	cin >> n;
	cin.ignore();
	for (int j = 0; j < n; j++) {
		cout << "Write number: ";
		cin >> num;
		root->vectPoint.push_back(new Node(num));
		cout << "Do you want to continue to enter a new subtree??\nWrite 1,if YES,and 0,if NO: ";
		cin >> answ;
		// Если отвечаем 0,то ввод "ветки" поддерева закончен и перескакиваем на заполнение другой ветки
		if (answ == 0)
			cout << "Subtree is end" << endl;
		// Иначе рекурсивно начинаем ввод нового поддерева 
		else
			Write_R(root->vectPoint[j]);
	}
}

//Печать элементов с обходом в глубину
template<typename T>
void MultiTree<T>::printDepth() {
	printDepth_R(main_root);
	cout << endl;
}

// Рекурсивный метод обхода в глубину 
template<typename T>
void MultiTree<T>::printDepth_R(Node *root) {
	int len = root->vectPoint.size();
	if (len != 0) {
		// Запускаем рекурсию по элементам вектора указателей
		for (int i = 0; i < len; i++)
			printDepth_R(root->vectPoint[i]);
	}
	cout << root->info << " ";
}

//Печать элементов с обходом в ширину
template<typename T>
void MultiTree<T>::printWidth() {
	cout << main_root->info << " ";
	queue <Node *> Width;
	// Пушим корень
	Width.push(main_root);
	int len;
	while (!Width.empty()) {
		len = Width.front()->vectPoint.size();
		// Проверяем наличие потомков
		if (len != 0) {
			// Если они есть,то записываем их и пушим в очередь
			for (int i = 0; i < len; i++) {
				cout << Width.front()->vectPoint[i]->info << " ";
				Width.push(Width.front()->vectPoint[i]);
			}
		}
		// Выталкиваем с начала узел
		Width.pop();
	}
	cout << endl;
}
