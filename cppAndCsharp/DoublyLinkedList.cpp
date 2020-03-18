#include <iostream>
using namespace std;

//двусвязный список
class list {
	struct Node {
		int info;//инф.поле
		Node *next;//указатель на следующий элемент
		Node *last;//указатель на предыдущий элемент
		//конструктор
		Node(int a, Node *next = NULL,Node *last = NULL) {
			info = a;
			this->next = next;
			this->last = last;
		}
	};
	Node *head = NULL;//указатель на начало списка
	Node *tail = NULL;//указатель на конец списка
public:
	~list();
	void Add(int a, int i);
	void AddBeg(int a);
	void AddEnd(int a);
	void Remove(int i);
	int Get(int i);
	friend ostream& operator<<(ostream& str, list& list);
	friend istream& operator>>(istream& str, list& list);
	int operator[](int i);
	void ReverseList();
};

//деструктор
list:: ~list() {
	while (head != NULL) {
		Remove(0);
	}
}

//метод добавления по индексу
void list::Add(int a, int i) {
	//создать первый элемент
	if (i == 0) {
		head = new Node(a, head);
		if (head->next != NULL) {
			head->next->last = head;
		}
		return;
	}
	//ошибка
	if (i < 0) {
		cout << "[ERROR]";
		return;
	}
	Node *current = head;
	for (int j = 0; current != NULL && j != i - 1; j++, current = current->next);//пробег по списку
	if (current != NULL) {
		current->next = new Node(a, current->next,current);
		if (current->next->next == NULL)
			tail = current->next;
		else
			current->next->next->last = current->next;
	}
}

//метод добавления в начало
void list::AddBeg(int a) {
	Add(a, 0);
}

//метод добавления в конец
void list::AddEnd(int a) {
	if (head == NULL) {
		head = new Node(a, head);
		tail = head;
	}
	else {
		Node *current = head;
		while (current->next != NULL) {
			current = current->next;
		}
		current->next = new Node(a, current->next, current);
		tail = current->next;
	}
}

//метод удаления
void list::Remove(int i) {
	//ошибка
	if (head == NULL || i < 0) {
		cout << "[ERROR]";
		return;
	}
	//удаляем первый
	if (i == 0) {
		Node *p = head;
		head = p->next;
		if (head != NULL) {
			head->last = NULL;
		} else {
			tail = head;
		}
		delete p;
		return;
	}
	Node *current = head;
	for (int j = 0; current->next != NULL && j != i - 1; j++, current = current->next);
	//проверка на существование
	if (current->next != NULL) {
		Node *p = current->next;
		current->next = p->next;
		p->next->last = current;
		delete p;
	}
}

//метод получения элемента списка по индексу
int list::Get(int i) {
	Node *current = head;
	for (int j = 0; current != NULL && j != i - 1; j++, current = current->next);
	if (current != NULL) {
		return current->info;
	}
}

int list::operator[](int i) {
	return Get(i);
}

//перегрузка оператора <<
ostream& operator<<(ostream& str, list& list) {
	//если начало списка ноль,то список пуст
	if (list.head == NULL) {
		str << "List is empty" << endl;
		return str;
	}
	else {
		for (list::Node *current = list.head; current != NULL; current = current->next) {
			str << current->info << " ";
		}
		return str;
	}
}

//перегрузка оператора >>
istream& operator>>(istream& str, list& list) {
	int n, a;
	str >> n;
	for (int i = 0; i < n; i++) {
		str >> a;
		list.AddEnd(a);
	}
	return str;
}

//метод переворота списка
void list::ReverseList() {
	Node *current = head, *temp = NULL;
	while (current != NULL) {
		temp = current->last;
		current->last = current->next;
		current->next = temp;
		current = current->last;
	}
	if (temp!=NULL)
		head = temp->last;
}

int main() {
		list one;
		cin >> one;
		//one.ReverseList();
		cout << one << endl;
		one.Add(55, 3);
		cout << one << endl;
		one.AddBeg(66);
		cout << one << endl;
		one.Remove(3);
		cout << one << endl;
		one.AddEnd(44);
		cout << one << endl;
		one.ReverseList();
		cout << one << endl;
		cout << one[3] << endl;
		cout << one << endl;
	system("pause");
	return 0;
}