#include <iostream>
#include "Structures_and_Classes.h"

//Default constructor
complex::complex(){
    rm = 0;
    im = 0;
}

void mobile::print_all() {
    std::cout<<"brand: "<<brand<<std::endl<<"model: "<<model<<std::endl<<"price: "<<price;
}

//Rib counting method
template<typename T>
unsigned int graph<T>::get_the_number_of_edges() {
    unsigned int count = 0;
    for (int i = 0; i < m; i++)
        for (int j = i + 1; j < m; j++)
            if ((matrix[i][j] == matrix[j][i] != 0) ||
                (matrix[i][j] == 0 && matrix[j][i] != 0) ||
                (matrix[j][i] == 0 && matrix[i][j] != 0))
                count++;
    return count;
}

//Method of determining the type of graph
template<typename T>
bool graph<T>::directed() {
    for (int i = 0; i < m; i++)
        for (int j = i + 1; j < m; j++)
            if (matrix[i][j] != matrix[j][i])
                return true;
    return false;
}

//Method of obtaining the adjacency list
template<typename T>
std::list<int> graph<T>::get_adjacency_list(int vertex) {
    std::list<int> adjacency;
    for (int j = 0; j < m; j++)
        if (matrix[vertex-1][j] != 0)
            adjacency.push_back(j + 1);
    return adjacency;
}

//Method of creating the adjacency matrix of ribs list
template<typename T>
void graph<T>::create_matrix() {
    for (auto i:list_of_edges)
        matrix[i.begin][i.end] = matrix[i.end][i.begin] = 1;
}

//Constructor with parameters
template<typename T>
matrix<T>::matrix(unsigned int m, unsigned int n) {
    this->m = m;
    this->n = n;
    **matr = new T *[m];
    for (auto &i : matr)
        i = new T[n];
}

//Copy Constructor
template<typename T>
matrix<T>::matrix(const matrix& mat) {
    this->m = mat.m;
    this->n = mat.n;
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; i++)
            matr[i][j] = mat.matr[i][j];
}

//Overload =
template<typename T>
matrix<T>& matrix<T>::operator=(matrix<T>& mat) {
    if (this->n != mat.n || this->m != mat.m) {
        for (int i = 0; i < m; i++)
            delete[] matr[i];
        delete[] matr;
        **matr = new T *[mat.m];
        for (int i = 0; i < m; i++)
            matr[i] = new T[mat.n];
    }
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; i++)
            matr[i][j] = mat.matr[i][j];
    return *this;
}

//Overload >>
template<typename T>
std::istream& operator>>(std::istream& str,matrix<T>& mat) {
    for (int i = 0; i < mat.m; i++)
        for (int j = 0; j < mat.n; i++)
            str >> mat.matr[i][j];
    return str;
}

//Overload <<
template<typename T>
std::ostream& operator<<(std::ostream& str,matrix<T>& mat) {
    for (int i = 0; i < mat.m; i++)
        for (int j = 0; j < mat.n; i++)
            str << mat.matr[i][j]<<" ";
    str << std::endl;
    return str;
}

//Overload +
template<typename T>
matrix<T> matrix<T>::operator+(matrix<T> mat) {
    if (this->m != mat.m || this->n != mat.n)
        throw 1;
    else {
        matrix<T> res(m, n);
        for (int i = 0; i < m; i++)
            for (int j = 0; j < n; j++)
                res[i][j] = matr[i][j] + mat.matr[i][j];
        return res;
    }
}

//Method of matrix transposition
template<typename T>
void matrix<T>::transposition() {
    for (int i = 0; i < m; i++)
        for (int j = i + 1; j < n; j++) {
            T t = matr[i][j];
            matr[i][j] = matr[j][i];
            matr[j][i] = t;
        }
}

//Unit matrix
template<typename T>
bool matrix<T>::unit() {
    for (int i = 0; i < m; i++)
        for (int j = i; j < n; j++)
            if ((i == j && matr[i][j] != 1) || (i != j && matr[i][j] != 0) || (matr[i][j] != matr[j][i]))
                return false;
    return true;
}

//Destroy bin_tree
template<typename T>
bin_tree<T>::~bin_tree() {
    Destroy(main_root);
}

//Destroy recursion
template<typename T>
void bin_tree<T>::Destroy(tree_node<T> *root) {
    if (root != NULL) {
        Destroy(root->left);
        Destroy(root->right);
        delete root;
    }
}

//Add method
template<typename T>
void bin_tree<T>::Add(T a) {
    if (main_root == NULL) {
        main_root = new tree_node<T>(a);
        return;
    }
    tree_node<T> *current = main_root;
    while (1) {
        if (a < current->info) {
            if (current->left == NULL) {
                current->left = new tree_node<T>(a);
                return;
            }
            else
                current = current->left;
        }
        else if (current->right == NULL) {
            current->right = new tree_node<T>(a);
            return;
        }
        else
            current = current->right;
    }
}

//Delete method
template<typename T>
void bin_tree<T>::Delete(T a) {
    Delete(main_root, a);
}

//Delete recursion
template<typename T>
void bin_tree<T>::Delete(tree_node<T> *&root, T a) {
    if (root == NULL)
        return;
    else if (root->info > a)
        Delete(root->left, a);
    else if (root->info < a)
        Delete(root->right, a);
    else {
        tree_node<T> *current = root;
        if (root->left == NULL) {
            root = root->right;
            delete current;
        }
        else if (root->right == NULL) {
            root = root->left;
            delete current;
        }
        else {
            tree_node<T> *p = root->right;
            if (p->left == NULL) {
                p->left = current->left;
                root = p;
                delete current;
            }
            else {
                tree_node<T> *q = p->left;
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

//Search method
template<typename T>
tree_node<T> bin_tree<T>::Search(T a) {
    try {
        tree_node<T> *current = main_root;
        while (current != NULL) {
            if (a == current->info)
                return current;
            else if (a < current->info)
                current = current->left;
            else
                current = current->right;
        }
        throw 1;
    }
    catch (int error) {
        std::cout << "Not found!" << std::endl;
    }
}

//Overload <<
template<typename T>
std::ostream& operator<<(std::ostream& str, bin_tree<T>& t) {
    t.Print_R(t.main_root, str);
    return str;
}

//Recursion for overload <<
template<typename T>
void bin_tree<T>::Print_R(tree_node<T> *root,std::ostream& str) {
    if (root != NULL) {
        Print_R(root->left,str);
        std::cout << root->info << " ";
        Print_R(root->right,str);
    }
}

//Overload >>
template<typename T>
std::istream& operator>>(std::istream& str, bin_tree<T>& t) {
    int n, num;
    str >> n;
    for (int i = 0; i < n; i++) {
        str >> num;
        t.Add(num);
    }
    return str;
}

//Overload ==
template<typename T>
bool bin_tree<T>::operator==(bin_tree<T>& t_two) {
    return equal_in_value(this->main_root, t_two.main_root);
}

//Recursion for overload ==
template<typename T>
bool bin_tree<T>::equal_in_value(tree_node<T> *root_one, tree_node<T> *root_two) {
    return (root_one != NULL && root_two != NULL &&
           root_one->info == root_two->info &&
           equal_in_value(root_one->left, root_two->left) &&
           equal_in_value(root_one->right, root_two->right))|| (root_one == NULL && root_two == NULL);
}

//Overload && (Are trees equivalent or not?)
template<typename T>
bool bin_tree<T>::operator&&(bin_tree<T>& t_two) {
    return equal_in_struct(this->main_root, t_two.main_root);
}

//Recursion for overload &&
template<typename T>
bool bin_tree<T>::equal_in_struct(tree_node<T> *root_one, tree_node<T> *root_two) {
    return (root_one != NULL && root_two != NULL &&
           equal_in_struct(root_one->left, root_two->left) &&
           equal_in_struct(root_one->right, root_two->right))|| (root_one == NULL && root_two == NULL);
}

//Method of calculating the height of the node
template<typename T>
unsigned char bin_tree<T>::height(tree_node<T>* v){
    return v ? v->height : 0;
}

//Method that calculates the difference between the heights of descendants
template<typename T>
int bin_tree<T>::b_factor(tree_node<T> * v){
    return height(v->right)-height(v->left);
}

//Method restoring the correct values for the node
template<typename T>
void bin_tree<T>::fix_height(tree_node<T> *v) {
    unsigned char h_l = height(v->left);
    unsigned char h_r = height(v->right);
    v->height =(h_l>h_r? h_l:h_r)+1;
}

//Rotate...
template<typename T>
tree_node<T>* bin_tree<T>::rotate_right(tree_node<T> *v) {
    tree_node<T>* h_v = v->left;
    v->left = h_v->right;
    h_v->right = v;
    fix_height(v);
    fix_height(h_v);
    return h_v;
}

//Rotate...
template<typename T>
tree_node<T>* bin_tree<T>::rotate_left(tree_node<T> *v) {
    tree_node<T>* h_v = v->right;
    v->right = h_v->left;
    h_v->left = v;
    fix_height(v);
    fix_height(h_v);
    return h_v;
}

//The basic method of balancing a tree with checking the condition of height difference and making a turn
template<typename T>
tree_node<T>* bin_tree<T>::balance(tree_node<T> *v){
    fix_height(v);
    if(b_factor(v)==2){
        if (b_factor(v->right)<0)
            v->right=rotate_right(v->right);
        return rotate_left(v);
    }else if (b_factor(v)==-2){
        if (b_factor(v->left)>0)
            v->left=rotate_left(v->left);
        return rotate_right(v);
    }
    return v;
}
