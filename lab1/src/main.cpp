#include <iostream>
#include <fstream>
#include <vector>
#include <iomanip>
#include <chrono>
#include <cmath>

using namespace std;

bool loadMatrix(const string& path, vector<vector<double>>& mat, int& size) {
    ifstream in(path);
    if (!in) {
        cerr << "Error: cannot open " << path << endl;
        return false;
    }
    in >> size;
    mat.assign(size, vector<double>(size));
    for (int i = 0; i < size; i++)
        for (int j = 0; j < size; j++)
            in >> mat[i][j];
    return true;
}

bool saveMatrix(const string& path, const vector<vector<double>>& mat, int size) {
    ofstream out(path);
    if (!out) {
        cerr << "Error: cannot create " << path << endl;
        return false;
    }
    out << size << "\n";
    out << fixed << setprecision(6);
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++)
            out << mat[i][j] << " ";
        out << "\n";
    }
    return true;
}

void multiplyMatrices(const vector<vector<double>>& A,
                      const vector<vector<double>>& B,
                      vector<vector<double>>& C,
                      int n) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            C[i][j] = 0.0;
            for (int k = 0; k < n; k++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
}

int main(int argc, char* argv[]) {
    if (argc != 4) {
        cout << "Usage: " << argv[0] << " <input_A> <input_B> <output_C>" << endl;
        return 1;
    }
    
    vector<vector<double>> A, B, C;
    int nA, nB;
    
    cout << "Reading matrices..." << endl;
    if (!loadMatrix(argv[1], A, nA)) return 1;
    if (!loadMatrix(argv[2], B, nB)) return 1;
    
    if (nA != nB) {
        cerr << "Error: matrices must have same size" << endl;
        return 1;
    }
    
    int n = nA;
    C.assign(n, vector<double>(n));
    
    cout << "Matrix size: " << n << "x" << n << endl;
    cout << "Computing..." << endl;
    
    auto start = chrono::high_resolution_clock::now();
    multiplyMatrices(A, B, C, n);
    auto end = chrono::high_resolution_clock::now();
    
    double elapsed = chrono::duration<double>(end - start).count();
    double flops = 2.0 * pow(n, 3);
    double gflops = flops / (elapsed * 1e9);
    
    cout << "Time: " << elapsed << " seconds" << endl;
    cout << "Performance: " << gflops << " GFLOPS" << endl;
    
    if (!saveMatrix(argv[3], C, n)) return 1;
    
    cout << "Result saved to " << argv[3] << endl;
    
    // Metrics for parsing by scripts
    cout << "METRIC:N:" << n << endl;
    cout << "METRIC:TIME:" << elapsed << endl;
    cout << "METRIC:GFLOPS:" << gflops << endl;
    
    return 0;
}