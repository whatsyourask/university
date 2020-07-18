#ifndef TRAINING_CLASS_FUNCTION_IMPLEMENTATION_H
#define TRAINING_CLASS_FUNCTION_IMPLEMENTATION_H

//Print list
void list::print_list(node *head);

//Adding to the top of the list
void list::add_beg(node *head,int info);

//Delete end of list
void list::remove_end(node *head);

//Add to end of list
void list::add_end(node *head,int info);

//Print the doubly linked list from the end
void double_linked_list::print_end_list(node *head);

//Remove end of doubly linked list
void double_linked_list::delete_end_list(node *head);

//Add to end of list
void double_linked_list::add_end_list(node *head,int info);

//Printing tree elements in LMR in recursion
void bin_tree::print_tree_LMR_rec(node *main_root);

//Printing tree elements in LMR in cycle
void bin_tree::print_tree_LMR(node *main_root);

//Printing tree elements in MRL in recursion
void bin_tree::print_tree_MRL_rec(node *main_root);

//Printing tree elements in MRL in cycle
void bin_tree::print_tree_MRL(node *main_root);

//Printing tree elements in LRM in recursion
void bin_tree::print_tree_LRM_rec(node *main_root);

//Printing tree elements in LRM in cycle(I don't know yet how to implement this traversal)
void bin_tree::print_tree_LRM(node *main_root);

#endif //TRAINING_CLASS_FUNCTION_IMPLEMENTATION_H