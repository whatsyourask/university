#include <iostream>
#include <queue>
#include <vector>
#include <string>
using namespace std;

template<typename T>
class graph {
	int m; // The number of vertices of the graph
	T **matrix; // Adjacency matrix
	void create_matrix(int m);
public:
	graph(int m = 0);
	graph(const graph& g);
	~graph();
	void write_matrix();
	vector<int> search_way(int v1, int v2);
	graph<int> min_frame_tree();
	void print_matrix();
};

// Graph constructor with transmitted m
template<typename T>
graph<T>::graph(int m) {
    if (m == 0) {
        cout << "Write a count of vertex: ";
        cin >> m;
		cin.ignore();
    }
    create_matrix(m);
}

template<typename T>
graph<T>::graph(const graph& g) {
	m = g.m;
	matrix = new T*[m];
	for (int i = 0; i < m; i++)
		matrix[i] = new T[m];
	for (int i = 0; i < m; i++)
		for (int j = 0; j < m; j++)
			matrix[i][j] = g.matrix[i][j];
}

// Private method of allocating memory for adjacency matrix
template<typename T>
void graph<T>::create_matrix(int m) {
	this->m = m;
	matrix = new T*[m];
	for (int i = 0; i < m; i++)
		matrix[i] = new T[m];
	for (int i = 0; i < m; i++)
		for (int j = 0; j < m; j++)
			matrix[i][j] = 0;
}

template<typename T>
void graph<T>::print_matrix() {
    for(int i=0;i<m;i++) {
        for (int j = 0; j < m; j++)
            cout << matrix[i][j]<<" ";
        cout<<endl;
    }
}

// Private adjacency matrix input method
template<typename T>
void graph<T>::write_matrix() {
	if (!is_same<T, bool>::value) {
		int way;
		for (int i = 0; i < m; i++) {
			cout << "Write edge length for " << i + 1 << " vertex,if vertex is no way to another vertex, write 0:	";
			for (int j = 0; j < m; j++) {
				cin >> way;
				matrix[i][j] = way;
			}
		}
	}else{
		string ways;
		int n = 0;
		for (int i = 0; i < m; i++) {
			cout << "write vertices that have a path from " << i + 1 << " vertex	";
			getline(cin, ways);
			int length = ways.length();
			for (int j = 0; j < length; j++)
				if (ways[j] == ' ' || j == length - 1) {
					matrix[i][atoi(ways.substr(j - n, n + 1).c_str()) - 1] = 1;
					n = 0;
				}
				else
					n++;
		}
	}
}

// Adjacency matrix destructor
template<typename T>
graph<T>::~graph() {
	for (int i = 0; i < m; i++) 
		delete[] matrix[i];
	delete[] matrix;
}

// Method for finding the shortest path from one vertex to another
template<typename T>
vector<int> graph<T>::search_way(int v1, int v2) {
	vector<int> processed; // The status vector of the graph's top (0 - not processed, 1 - visited, 2 - processed)
	vector<int> ways, prevs; // The vector of paths for each vertex from v1 and the vector of vertices of which came in the i-th
	queue<int> processing; // Vertex processing queue
	int node, elem, min, ind=NULL, check;
	// Fill status vector and paths with zeros
	for (int i = 0; i < m; i++) {
		processed.push_back(0);
		ways.push_back(0);
		prevs.push_back(v1 - 1);
	}
	// Push in the queue starting vertex
	processing.push(v1-1);
	while (!processing.empty()) {
		// Set at least the upper limit of the int
		min = INT_FAST32_MAX;
		// Take out the first element of the queue
		node = processing.front();
		for (int i = 0; i < m; i++) {
			elem = matrix[node][i];
			// If there is a path, then it is not zero
			if (elem != 0) {
				// If the top is not processed, then we push into the queue and mark as visited
				if (processed[i] == 0)
					processed[i] = 1;
				// Check whether the sum of the previous distance and the current is less than the other path to the i-th vertex, or add the path 1 time
				if (elem + ways[node] < ways[i] || ways[i] == 0) {
					ways[i] = elem + ways[node];
					// Push the top from which we come to the current
					prevs[i] = node;
				}
			}
		}
		// Note that the vertex is processed
		processed[node] = 2;
		check = 0;
		// Looking for raw vertices
		for (int i = 0; i < m && check == 0; i++)
			if (processed[i] != 2)
				check = 1;
		// If there are raw, then do the following:
		if (check) {
			/* We are looking for a minimum in the cycle among the current calculated paths,
			   we select only those vertices that are visited, but not processed, and the path of which is not 0 */
			for (int i = 0; i < m; i++)
				if (ways[i] != 0 && ways[i] < min && processed[i] == 1) {
					min = ways[i];
					ind = i;
					processing.push(ind);
				}
			// We push the minimum
		}
		processing.pop();
	}
//	if (!is_same<T,bool>::value)
//        cout << "short way = " << ways[v2 - 1] << endl;
//	// Print the path from the desired vertex to the initial
//	cout <<"Way:"<< v2;
	int need = v2 - 1;
	vector<int> result;
	while (need != v1 - 1) {
		need = prevs[need];
		result.push_back(need);
//		cout << "<-" << need + 1;
	}
	result.pop_back();
	return result;
}

// Search a minimal frame tree in graph
template<typename T>
graph<int> graph<T>::min_frame_tree() {
	// Edge struct with begin,end and length
    struct edge {
		int begin, end;
		int length;
        edge(int begin, int end, int length) {
            this->begin = begin;
            this->end = end;
            this->length = length;
        };
    };
	// Edges vector
    vector<edge> edges;
	// Fill vector with edges
    for (int i = 0; i < m - 1; i++)
        for (int j = i + 1; j < m; j++)
            if (matrix[i][j]!=0)
                edges.push_back(edge(i, j, matrix[i][j]));
    int size = edges.size();
	// Sort vector ascending
    for (int i = 0; i < size - 1; i++)
        for (int j = i + 1; j < size; j++)
            if (edges[i].length > edges[j].length) {
                edge e = edges[i];
                edges[i] = edges[j];
                edges[j] = e;
            }
	// Result frame in graph
    graph<int> result_g(m);
    int j = 0;
	// Variable to exit the cycle
    bool check_way;
	// Edges are 1 less than vertices
    for (int i=0; i < m - 1; i++) {
        check_way = false;
		// Run the cycle until we paint a pair of vertices.
        while (!check_way) {
			// Using the Dijkstra algorithm, look for the current shortest path
			// The algorithm had to be slightly modified to return the path vector
            vector<int> way = result_g.search_way(edges[j].begin + 1, edges[j].end + 1);
            if (way.empty()) {
                result_g.matrix[edges[j].begin][edges[j].end] = 
					result_g.matrix[edges[j].end][edges[j].begin] = edges[j].length;
                check_way = true;
            }
            j++;
        }
    }
	// For check
	result_g.print_matrix();
	return result_g;
}