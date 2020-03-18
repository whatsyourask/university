#include <iostream>
#include <string>
using namespace std;

template<typename T>
struct Node {
	T info;
	Node *left, *right;
	Node(T info) {
		this->info = info;
		left = right = NULL;
	}
};

template<typename T>
class BinTree {
	Node<T> *main_root = NULL;
public:
	void Add(T a);
	void Delete(T a);
	Node<T> Search(T a);
	template<typename T> friend ostream& operator<<(ostream& str, BinTree<T>& t);
    	template<typename T> friend istream& operator>>(istream& str, BinTree<T>& t);
	bool operator==(BinTree<T>& t_two);
	bool operator&&(BinTree<T>& t_two);
	~BinTree();
private:
	void Destroy(Node<T> *root);
	void Delete(Node<T> *&root, T a);
	void Print_R(Node<T> *root,ostream& str);
	bool equal_in_value(Node<T> *root_one, Node<T> *root_two);
	bool equal_in_struct(Node<T> *root_one, Node<T> *root_two);
};

// Äåñòðóêòîð äåðåâà
template<typename T>
BinTree<T>::~BinTree() {
	Destroy(main_root);
}

// Ðåêóðñèâíûé ìåòîä óäàëåíèÿ äåðåâà
template<typename T>
void BinTree<T>::Destroy(Node<T> *root) {
	if (root != NULL) {
		Destroy(root->left);
		Destroy(root->right);
		delete root;
	}
}

// Ìåòîä äîáàâëåíèÿ óçëà
template<typename T>
void BinTree<T>::Add(T a) {
	// Åñëè êîðåíü ïóñòîé,äîáàâëÿåì òóäà
	if (main_root == NULL) {
		main_root = new Node<T>(a);
		return;
	}
	// Èíà÷å
	Node<T> *current = main_root;
	// Çàïóñêàåì áåñêîíå÷íûé öèêë
	while (1) {
		if (a < current->info) {
			if (current->left == NULL) {
				current->left = new Node<T>(a);
				return;
			}
			else
				current = current->left;
		}
		else if (current->right == NULL) {
			current->right = new Node<T>(a);
			return;
		}
		else
			current = current->right;
	}
}

// Ìåòîä óäàëåíèÿ óçëà
template<typename T>
void BinTree<T>::Delete(T a) {
	Delete(main_root, a);
}

// Ïðèâàòíûé ìåòîä óäàëåíèÿ óçëà
template<typename T>
void BinTree<T>::Delete(Node<T> *&root, T a) {
	// Åñëè òàêîãî óçëà íåò,âûõîäèì
	if (root == NULL)
		return;
	// Èùåì íóæíûé óçåë
	else if (root->info > a)
		Delete(root->left, a);
	else if (root->info < a)
		Delete(root->right, a);
	// Íàøëè
	else {
		Node<T> *current = root;
		// Ïðîâåðÿåì ïîòîìêîâ,åñëè íåò îäíîãî,òî ñîñåäíåãî ïðèâÿçûâàåì ê óçëó,êîòîðûé óäàëÿåì
		if (root->left == NULL) {
			root = root->right;
			delete current;
		}
		else if (root->right == NULL) {
			root = root->left;
			delete current;
		}
		// Åñëè åñòü îáà ïîòîìêà ðàññìàòðèâàåì 2 ñëó÷àÿ
		else {
			Node<T> *p = root->right;
			// Åñëè ó ïðàâîãî ïîòîìêà íåò ëåâîãî ïîòîìêà,òî ïðèâÿçûâàåì ê íåìó ëåâîãî ïîòîìêà óäàëÿåìîãî óçëà 
			if (p->left == NULL) {
				p->left = current->left;
				root = p;
				delete current;
			}
			/*Èíà÷å åñëè ó ïðàâîãî ïîòîìêà åñòü ëåâûé ïîòîìîê,
			ñïóñêàåìñÿ ïî ëåâîìó ïîääåðåâó ïðàâîãî ïîòîìêà ïîòîìêà äî òåõ ïîð,
			ïîêà íå íàéäåì ó ïðîõîäèìîãî ïîòîìêà ïóñòîå ìåñòî ñëåâà
			Çàòåì âñòàâëÿåì â óäàëÿåìûé óçåë íàéäåííîãî ïîòîìêà,à ê åãî ðîäèòåëþ ñëåâà ïðèâÿçûâàåì åãî ïðàâîãî ïîòîìêà */
			else {
				Node<T> *q = p->left;
				while (q->left != NULL) {
					q = q->left;
					p = p->left;
				}
				root->info = q->info;
				p->left = q->right;
				delete q;
			}
		}
	}
}

//Node BinTree::Search(T a){} ïîä÷åðêèâàåò Node è Search,êîãäà ñòðóêòóðà â êëàññå îïðåäåëåíà,à íå çà åãî ïðåäåëàìè

// Ìåòîä ïîèñêà ïî çíà÷åíèþ
template<typename T>
Node<T> BinTree<T>::Search(T a) {
	// Ïûòàåìñÿ íàéòè íóæíûé óçåë
	try {
		Node<T> *current = main_root;
		while (current != NULL) {
			if (a == current->info)
				return current;
			else if (a < current->info)
				current = current->left;
			else
				current = current->right;
		}
		// Åñëè íå íàøëè,âûáðàñûâàåì èñêëþ÷åíèå
		throw 1;
	}
	catch (int error) {
		cout << "Not found!" << endl;
	}
}

// Ïåðåãðóçêà îïåðàòîðà âûâîäà
template<typename T>
ostream& operator<<(ostream& str, BinTree<T>& t) {
	t.Print_R(t.main_root, str);
	return str;
}

// Ðåêóðñèâíûé ìåòîä ïå÷àòè óçëîâ
template<typename T>
void BinTree<T>::Print_R(Node<T> *root,ostream& str) {
	if (root != NULL) {
		Print_R(root->left,str);
		cout << root->info << " ";
		Print_R(root->right,str);
	}
}

// Ïåðåãðóçêà îïåðàòîðà ââîäà
template<typename T>
istream& operator>>(istream& str, BinTree<T>& t) {
	int n, num;
	str >> n;
	for (int i = 0; i < n; i++) {
		str >> num;
		t.Add(num);
	}
	return str;
}

// Ïåðåãðóçêà îïåðàòîðà ==
template<typename T>
bool BinTree<T>::operator==(BinTree<T>& t_two) {
	return equal_in_value(this->main_root, t_two.main_root);
}

// Ðåêóðñèâíûé ìåòîä ñðàâíèâàíèÿ çíà÷åíèé óçëîâ 2 äåðåâüåâ
template<typename T>
bool BinTree<T>::equal_in_value(Node<T> *root_one, Node<T> *root_two) {
	return root_one != NULL && root_two != NULL &&
		root_one->info == root_two->info &&
		equal_in_value(root_one->left, root_two->left) &&
		equal_in_value(root_one->right, root_two->right)|| root_one == NULL && root_two == NULL;
}

// Ïåðåãðóçêà îïåðàòîðà &&
template<typename T>
bool BinTree<T>::operator&&(BinTree<T>& t_two) {
	return equal_in_struct(this->main_root, t_two.main_root);
}

// Ðåêóðñèâíûé ìåòîä ñðàâíèâàíèÿ ñòðóêòóð 2 äåðåâüåâ
template<typename T>
bool BinTree<T>::equal_in_struct(Node<T> *root_one, Node<T> *root_two) {
	return root_one != NULL && root_two != NULL &&
		equal_in_struct(root_one->left, root_two->left) &&
		equal_in_struct(root_one->right, root_two->right)|| root_one == NULL && root_two == NULL;
}