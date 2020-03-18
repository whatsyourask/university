#ifndef TRAINING_STRUCTURES_AND_CLASSES_H
#define TRAINING_STRUCTURES_AND_CLASSES_H
#include <string>
#include <list>

struct student{
    std::string name;
    int age;
    int group;
};

class complex{
    int rm;
    int im;
public:
    complex();
};


class mobile{
    std::string brand,model;
    int price;
public:
    void print_all();
};

struct handbook{
    std::string name,phone;
};

template<typename T>
struct linked_node{
    T info;
    T *next;
    linked_node(T info,linked_node *next=NULL){
        this->info=info;
        this->next = next;
    }
};

template<typename T>
struct double_linked_node{
    T info;
    T *next;
    T *last;
    double_linked_node(T info,double_linked_node * next = NULL,double_linked_node *last = NULL){
        this->info=info;
        this->next=next;
        this->last=last;
    }
};

template<typename T>
class graph{
    struct edge{
        int begin,end;
    };
    int m; // The number of vertices of the graph
    T **matrix; // Adjacency matrix
    std::list<edge> list_of_edges;
public:
    unsigned int get_the_number_of_edges();
    bool directed();
    std::list<int> get_adjacency_list(int vertex);
    void create_matrix();
};

template<typename T>
class matrix{
    T **matr;
    unsigned int m,n;
public:
    matrix(unsigned int m,unsigned int n);
    matrix(const matrix& mat);
    matrix<T>& operator=(matrix<T>& mat);
    friend std::istream& operator>>(std::istream& str,matrix<T>& mat);
    friend std::ostream& operator<<(std::ostream& str,matrix<T>& mat);
    matrix<T> operator+(matrix<T> mat);
    void transposition();
    bool unit();
};

template<typename T>
struct tree_node {
    T info;
    tree_node *left, *right;
    unsigned char height;
    tree_node(T info) {
        this->info = info;
        left = right = NULL;
        height = 1;
    }
};

template<typename T>
class bin_tree {
    tree_node<T> *main_root = NULL;
public:
    void Add(T a);
    void Delete(T a);
    tree_node<T> Search(T a);
    friend std::ostream& operator<<(std::ostream& str, bin_tree<T>& t);
    friend std::istream& operator>>(std::istream& str, bin_tree<T>& t);
    bool operator==(bin_tree<T>& t_two);
    bool operator&&(bin_tree<T>& t_two);
    ~bin_tree();
private:
    void Destroy(tree_node<T> *root);
    void Delete(tree_node<T> *&root, T a);
    void Print_R(tree_node<T> *root,std::ostream& str);
    bool equal_in_value(tree_node<T> *root_one, tree_node<T> *root_two);
    bool equal_in_struct(tree_node<T> *root_one, tree_node<T> *root_two);
    unsigned char height(tree_node<T>* v);
    int b_factor(tree_node<T> * v);
    void fix_height(tree_node<T> *v);
    tree_node<T>* rotate_right(tree_node<T> *v);
    tree_node<T>* rotate_left(tree_node<T> *v);
    tree_node<T>* balance(tree_node<T> *v);
};

#endif