#include <string>
#include <fstream>
#include <iostream>
#include "Structures_and_Classes.h"
using namespace std;

//Enter 3 numbers or words in txt file
void write_three_words() {
    string *arr = new string[3];
    cout << "write three words or three numbers: ";
    bool check_num = false,check_char = false;
    bool mode = false;
    for (int i = 0; i < 3; i++) {
        cin >> arr[i];
        for (int j = 0; j < arr[i].length(); j++) {
            if (arr[i][j] < '0' || arr[i][j] > '9')
                check_char = true;
            else
                check_num = true;
        }
        if (check_num && check_char) {
            cout << "invalid value";
            return;
        }
        check_char = false;
        check_num = false;
    }
    string filename;
    cout<<"Write a name of file: ";
    cin>>filename;
    ofstream out(filename);
    string help_str;
    for(int i=0; i<3;i++) {
        out << arr[i] + " ";
    }
    out.close();
    delete[] arr;
}

//Reading words from a file
void read_words_from_file(){
    string filename;
    cout<<"Write a name of file: ";
    cin>>filename;
    ifstream in(filename);
    string str,help_str;
    while(!in.eof()){
        getline(in,help_str);
        str+= help_str;
        help_str = "";
    }
    cout<<str;
}

//Reading numbers from file
void read_numbers_from_file() {
    string filename;
    cout << "Write a name of file: ";
    cin >> filename;
    ifstream in(filename);
    int num;
    while (!in.eof()) {
        in >> num;
        cout << num << endl;
    }
    in.close();
}

//Reading numbers from bin. file
void read_numbers_from_binfile(){
    string filename;
    cout<<"Write a name of file: ";
    cin>>filename;
    ifstream in(filename,ios::binary);
    if(!in.is_open()){
        cout<<"Not open!";
        return;
    }
    while(in.peek()!=EOF){
        int a;
        in.read((char*)&a,sizeof(int));
        cout<<a<<" ";
    }
    in.close();
}

//Write the structure to the bin. file
void write_struct_in_binfile(handbook *data,int n){
    string filename;
    cout<<"Write a name of file: ";
    cin>>filename;
    ofstream out(filename,ios::binary);
    if(!out.is_open()){
        cout<<"Not open!";
        return;
    }
    out.write((char *)data, sizeof(handbook)*n);
    out.close();
}