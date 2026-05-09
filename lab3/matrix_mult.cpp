#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>

using namespace std;
using namespace chrono;

void readMatrices(const string& filename, vector<vector<double>>& A, vector<vector<double>>& B, int& N) {
    ifstream fin(filename);
    fin >> N;
    A.assign(N, vector<double>(N));
    B.assign(N, vector<double>(N));
    for (int i = 0; i < N; ++i)
        for (int j = 0; j < N; ++j)
            fin >> A[i][j];
    for (int i = 0; i < N; ++i)
        for (int j = 0; j < N; ++j)
            fin >> B[i][j];
}

void writeMatrix(const string& filename, const vector<vector<double>>& C) {
    ofstream fout(filename);
    int N = C.size();
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j)
            fout << C[i][j] << " ";
        fout << endl;
    }
}

void multiply(const vector<vector<double>>& A, const vector<vector<double>>& B, vector<vector<double>>& C) {
    int N = A.size();
    C.assign(N, vector<double>(N, 0.0));
    for (int i = 0; i < N; ++i)
        for (int k = 0; k < N; ++k)
            for (int j = 0; j < N; ++j)
                C[i][j] += A[i][k] * B[k][j];
}

int main() {
    vector<vector<double>> A, B, C;
    int N;
    readMatrices("input.txt", A, B, N);
    
    auto start = high_resolution_clock::now();
    multiply(A, B, C);
    auto stop = high_resolution_clock::now();
    
    auto duration = duration_cast<milliseconds>(stop - start);
    cout << "Time: " << duration.count() << " ms\n";
    cout << "Problem size: " << N << " x " << N << endl;
    
    writeMatrix("output.txt", C);
    return 0;
}