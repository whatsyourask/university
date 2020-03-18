#include <stack>

//Print list
void list::print_list(node *head){
    if (head == NULL){
        std::cout<<"List is empty!"<<endl;
        return;
    }else{
        for(list::node *current = head;current!=NULL;current=current->next)
            std::cout<<current.info<<" ";
    }
}

//Adding to the top of the list
void list::add_beg(node *head,int info){
    head = new node(info,head);
}

//Delete end of list
void list::remove_end(node *head){
    for(list::node* current = head;current->next!=NULL;current=current->next);
    current=NULL;
}

//Add to end of list
void list::add_end(node *head,int info){
    for(list::Node *current=head;current!=NULL;current=current->next);
    current=new node(info,current->next);
}

//Print the doubly linked list from the end
void double_linked_list::print_end_list(node *head){
    for(list::node *current = head;current->next!=NULL;current=current->next);
    for(;current->last!=NULL;current=current->last)
        cout<<current->info<<" ";
}

//Remove end of doubly linked list
void double_linked_list::delete_end_list(node *head){
    for(list::node *current = head;current->next!=NULL;current=current->next);
    current->last->next = NULL;
    current->last = NULL;
    tail=tail->last;
}

//Add to end of list
void double_linked_list::add_end_list(node *head,int info){
    if (head == NULL) {
        head = new node(a, head);
        tail = head;
    }
    else {
        node *current = head;
        while (current->next != NULL) {
            current = current->next;
        }
        current->next = new node(a, current->next, current);
        tail = current->next;
    }
}

//Printing tree elements in LMR in recursion
void bin_tree::print_tree_LMR_rec(node *main_root){
    aux_print_LMR(main_root);
    cout<<endl;
}

void bin_tree::aux_print_LMR(node *root){
    if (root != NULL){
        aux_print_LMR(root->left);
        cout<<root->info<<" ";
        aux_print_LMR(root->right);
    }
}

//Printing tree elements in LMR in cycle
void bin_tree::print_tree_LMR(node *main_root) {
    stack < node * > st;
    node *current = main_root;
    while (!st.empty() || current != NULL) {
        while (current != NULL) {
            st.push(current);
            current = current->left;
        }
        current = st.top();
        st.pop();
        cout << current->info << " ";
        current = current->right;
    }
}

//Printing tree elements in MRL in recursion
void bin_tree::print_tree_MRL_rec(node *main_root){
    aux_print_MRL(main_root);
    cout<<endl;
}

void bin_tree::aux_print_MRL(node *root){
    if (root != NULL){
        cout<<root->info<<" ";
        aux_print_LMR(root->right);
        aux_print_LMR(root->left);
    }
}

//Printing tree elements in MRL in cycle
void bin_tree::print_tree_MRL(node *main_root){
    stack<node *> st;
    node * current = main_root;
    while(!st.empty() || current!=NULL) {
        while (current != NULL) {
            cout << current->info << " ";
            st.push(current);
            current = current->right;
        }
        current = st.top();
        st.pop();
        current = current->left;
    }
}

//Printing tree elements in LRM in recursion
void bin_tree::print_tree_LRM_rec(node *main_root){
    aux_print_LRM(main_root);
    cout<<endl;
}

void bin_tree::aux_print_LRM(node *root){
    if (root != NULL){
        aux_print_LMR(root->left);
        aux_print_LMR(root->right);
        cout<<root->info<<" ";
    }
}

//Printing tree elements in LRM in cycle(I don't know yet how to implement this traversal)
void bin_tree::print_tree_LRM(node *main_root){
    stack<node *> st;
    node * current = main_root;
    while(!st.empty() || current!=NULL) {
        while (current != NULL) {
            st.push(current);
            current = current->left;
        }
        current = st.top();
        st.pop();
        current = current->right;
        cout << current->info << " ";
    }
}