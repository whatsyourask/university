#include "pch.h"
#include <iostream>
#include <fstream>
#include <string>
#include <cstring>
using namespace std;
void read_write_Txt(string &file_name_in,string &file_name_out,int &n) {
	ifstream in(file_name_in);
	ofstream out(file_name_out);
	string h_str, substr;
	//in.eof();
	int i, j;
	while (!in.eof()) {
		getline(in, h_str);
		int len = h_str.length();
		int count = (len+n-1)/ n;
		for (i = 0, j = 0; i < count-1; j += n, i++) {
			substr = h_str.substr(j,n);
			out << substr;
			out << '\n';
		}
		substr = h_str.substr(j);
		out << substr;
		out << '\n';
	}
	in.close();
	out.close();
}
int main()
{
	string file_name_in, file_name_out;
	int n;
	getline(cin, file_name_in);
	getline(cin, file_name_out);
	cin >> n;
	read_write_Txt(file_name_in,file_name_out,n);
	return 0;
}
