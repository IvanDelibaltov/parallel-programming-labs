#include <iostream>
#include <fstream>
#include <vector>
#include <iomanip>
#include <cmath>
#include <mpi.h>

using namespace std;

bool readMatrix(const string& filename, vector<double>& mat, int& n) {
    ifstream file(filename);
    if (!file) {
        cerr << "Error: cannot open " << filename << endl;
        return false;
    }
    file >> n;
    mat.resize(n * n);
    for (int i = 0; i < n * n; i++) {
        file >> mat[i];
    }
    return true;
}

bool writeMatrix(const string& filename, const vector<double>& mat, int n) {
    ofstream file(filename);
    if (!file) {
        cerr << "Error: cannot create " << filename << endl;
        return false;
    }
    file << n << "\n";
    file << fixed << setprecision(6);
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            file << mat[i * n + j] << " ";
        }
        file << "\n";
    }
    return true;
}

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);
    
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    
    if (argc != 4) {
        if (rank == 0) {
            cout << "Usage: mpirun -np N ./matrix_mult_mpi <A> <B> <C>" << endl;
        }
        MPI_Finalize();
        return 1;
    }
    
    int n;
    vector<double> A, B, C;
    
    // Rank 0 reads matrices
    if (rank == 0) {
        cout << "Reading matrices..." << endl;
        readMatrix(argv[1], A, n);
        readMatrix(argv[2], B, n);
        C.resize(n * n);
        cout << "Matrix size: " << n << "x" << n << endl;
        cout << "MPI processes: " << size << endl;
    }
    
    // Broadcast n to all processes
    MPI_Bcast(&n, 1, MPI_INT, 0, MPI_COMM_WORLD);
    
    // Resize vectors on all processes
    if (rank != 0) {
        A.resize(n * n);
        B.resize(n * n);
        C.resize(n * n);
    }
    
    // Broadcast matrices to all processes
    MPI_Bcast(A.data(), n * n, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Bcast(B.data(), n * n, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    
    // Calculate row distribution
    int rows_per_proc = n / size;
    int remainder = n % size;
    
    int start_row = rank * rows_per_proc + min(rank, remainder);
    int local_rows = rows_per_proc + (rank < remainder ? 1 : 0);
    int end_row = start_row + local_rows;
    
    // Local result for this process's rows
    vector<double> local_C(local_rows * n, 0.0);
    
    // Start timing
    double start_time = MPI_Wtime();
    
    // Multiply
    for (int i = start_row; i < end_row; i++) {
        for (int j = 0; j < n; j++) {
            double sum = 0.0;
            for (int k = 0; k < n; k++) {
                sum += A[i * n + k] * B[k * n + j];
            }
            local_C[(i - start_row) * n + j] = sum;
        }
    }
    
    double end_time = MPI_Wtime();
    double local_time = end_time - start_time;
    double max_time;
    MPI_Reduce(&local_time, &max_time, 1, MPI_DOUBLE, MPI_MAX, 0, MPI_COMM_WORLD);
    
    // Gather results to rank 0
    if (rank == 0) {
        // Copy own rows first
        for (int i = start_row; i < end_row; i++) {
            for (int j = 0; j < n; j++) {
                C[i * n + j] = local_C[(i - start_row) * n + j];
            }
        }
        
        // Receive from other processes
        for (int p = 1; p < size; p++) {
            int p_rows = rows_per_proc + (p < remainder ? 1 : 0);
            int p_start = p * rows_per_proc + min(p, remainder);
            vector<double> temp(p_rows * n);
            MPI_Recv(temp.data(), p_rows * n, MPI_DOUBLE, p, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            for (int i = 0; i < p_rows; i++) {
                for (int j = 0; j < n; j++) {
                    C[(p_start + i) * n + j] = temp[i * n + j];
                }
            }
        }
        
        double elapsed = max_time;
        double flops = 2.0 * pow(n, 3);
        double gflops = flops / (elapsed * 1e9);
        
        cout << "Time: " << elapsed << " seconds" << endl;
        cout << "Performance: " << gflops << " GFLOPS" << endl;
        
        writeMatrix(argv[3], C, n);
        cout << "Result saved to " << argv[3] << endl;
        
        cout << "METRIC:N:" << n << endl;
        cout << "METRIC:TIME:" << elapsed << endl;
        cout << "METRIC:PROC:" << size << endl;
        cout << "METRIC:GFLOPS:" << gflops << endl;
    } else {
        MPI_Send(local_C.data(), local_rows * n, MPI_DOUBLE, 0, 0, MPI_COMM_WORLD);
    }
    
    MPI_Finalize();
    return 0;
}
