#include <iostream>
#include <vector>
#include <fstream>
#include <algorithm>

int get_command(){
    int command;
    std::cin>>command;
    std::cin.ignore();
    return command;
}

int get_value(){
    int value;
    std::cout<<"write the value: ";
    std::cin>>value;
    return value;
}

std::string get_filename(){
    std::cout<<"write the file name: ";
    std::string filename;
    std::getline(std::cin,filename);
    return filename;
}

void storage() {
    std::cout << "=========Command List=========\n"
                 "[ 1 ]:Show storage.\n"
                 "[ 2 ]:Add to begin of storage.\n"
                 "[ 3 ]:Add to end of storage.\n"
                 "[ 4 ]:Delete by position.\n"
                 "[ 5 ]:Write storage in file.\n"
                 "[ 6 ]:Read storage from file.\n"
                 "[ 7 ]:Sort storage.\n"
                 "[ 0 ]:Exit.\n";
    std::vector<int> v;
    //Command to enter the cycle
    int command = -1;
    int value;
    std::string filename;
    while (command != 0) {
        //Get the right team
        command = get_command();
        switch (command) {
            case 0: {
                std::cout << "Exit...\n";
                break;
            }
            case 1: {
                if (!v.size())
                    std::cout << "Storage is empty.\n";
                else {
                    std::cout << "STORAGE: ";
                    for (auto cell:v)
                        std::cout << "[" << cell << "] ";
                    std::cout << "\n";
                }
                break;
            }
            case 2: {
                value = get_value();
                if (v.size()) {
                    auto iter = v.begin(); //For method 'insert(iterator, value)'
                    v.insert(iter, value);
                } else
                    v.push_back(value);
                std::cout << "Added to begin of storage.\n";
                break;
            }
            case 3: {
                value = get_value();
                v.push_back(value);
                std::cout << "Added to end of storage.\n";
                break;
            }
            case 4: {
                int position;
                std::cout << "write the position: ";
                std::cin >> position;
                auto iter = v.begin(); //For method 'erase(iterator)'
                v.erase(iter + position - 1);
                std::cout << "Deleted by position from storage.\n";
                break;
            }
            case 5: {
                filename = get_filename();
                std::ofstream out(filename);
                if (!out.is_open())
                    std::cout << "File not open.\n";
                else {
                    for (auto cell:v)
                        out << cell << " ";
                    out.close();
                    std::cout << "Wrote storage in file.\n";
                }
                break;
            }
            case 6: {
                filename = get_filename();
                std::ifstream in(filename);
                if (!in.is_open())
                    std::cout << "File not open.\n";
                else {
                    int num;
                    while (in>>num) {
                        v.push_back(num);
                    }
                    in.close();
                    std::cout << "Read storage out file.\n";
                }
                break;
            }
            case 7: {
                std::sort(v.begin(), v.end());
                std::cout << "Storage sorted.\n";
                break;
            }
            default: {
                std::cout << "[ERROR]:INCORRECT VALUE!!!\n";
                break;
            }
        }
    }
}