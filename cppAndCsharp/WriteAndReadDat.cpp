#include <iostream>
#include <string>
#include <fstream>
using namespace std;
void read_write_bin(string &file_name_out, int &n) {
	int *a = new int[n];
	for (int i = 0; i < n; i++) {
		cin >> a[i];
	}
	//fstream t;
	//t.flush();
	//ofstream out(file_name_out, ios::binary);
	//out.write((char *)&n, sizeof(int));  
	//out.write((char *)a, sizeof(int)*n);
	//delete[] a;
	//out.close();
	//ifstream in(file_name_out, ios::binary);
	//int k = 0;
	//in.read((char *)&k, sizeof(int));
	//cout << "k = " << k << endl;
	//int *b = new int[k];
	//in.read((char *)b, sizeof(int)*n);
	//in.close();
	fstream f(file_name_out, ios::binary|ios::in | ios::out);
	f.write((char *)&n, sizeof(int));
	f.write((char *)a, sizeof(int)*n);
	delete[] a;
	int k = 0;
	f.seekp(0, ios::beg);
	//f.flush(); //	очистка буфера
	f.read((char *)&k, sizeof(int));
	cout << " k = " << k << endl;
	int *b = new int[k];
	f.read((char *)b, sizeof(int)*k);
	f.close();
	for (int i = 0; i < k; i++) {
		cout << b[i] << " ";
	}
	delete[] b;
}
int main()
{
	string file_name_out;
	int n;
	getline(cin, file_name_out);
	cin >> n;
	cin.ignore();
	read_write_bin(file_name_out, n);
	return 0;
}
