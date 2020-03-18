#ifndef TRAINING_FILES_H
#define TRAINING_FILES_H
#include "Structures_and_Classes.h"

//Enter 3 numbers or words in txt file
void write_three_words();

//Reading words from a file
void read_words_from_file();

//Reading numbers from file
void read_numbers_from_file();

//Reading numbers from bin. file
void read_numbers_from_binfile();

//Write the structure to the bin. file
void write_struct_in_binfile(handbook *data);

#endif //TRAINING_FILES_H