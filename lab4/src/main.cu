#include <stdio.h>
#include <stdlib.h>
#include <cuda_runtime.h>
#include <math.h>

// Ядро умножения матриц (блочно-строковое)
__global__ void matrixMulKernel(float* A, float* B, float* C, int n) {
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;
    
    if (row < n && col < n) {
        float sum = 0.0f;
        for (int k = 0; k < n; k++) {
            sum += A[row * n + k] * B[k * n + col];
        }
        C[row * n + col] = sum;
    }
}

// Чтение матрицы из файла
float* readMatrix(const char* filename, int* n) {
    FILE* f = fopen(filename, "r");
    if (!f) return NULL;
    fscanf(f, "%d", n);
    float* mat = (float*)malloc((*n) * (*n) * sizeof(float));
    for (int i = 0; i < (*n) * (*n); i++) {
        fscanf(f, "%f", &mat[i]);
    }
    fclose(f);
    return mat;
}

// Запись матрицы в файл
void writeMatrix(const char* filename, float* mat, int n) {
    FILE* f = fopen(filename, "w");
    if (!f) return;
    fprintf(f, "%d\n", n);
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            fprintf(f, "%.6f ", mat[i * n + j]);
        }
        fprintf(f, "\n");
    }
    fclose(f);
}

int main(int argc, char* argv[]) {
    if (argc != 4) {
        printf("Usage: %s <input_A> <input_B> <output_C>\n", argv[0]);
        return 1;
    }
    
    int n;
    float *h_A, *h_B, *h_C;
    float *d_A, *d_B, *d_C;
    
    // Чтение матриц на хосте
    h_A = readMatrix(argv[1], &n);
    h_B = readMatrix(argv[2], &n);
    if (!h_A || !h_B) {
        printf("Error reading matrices\n");
        return 1;
    }
    h_C = (float*)malloc(n * n * sizeof(float));
    
    printf("Matrix size: %dx%d\n", n, n);
    
    // Выделение памяти на устройстве
    cudaMalloc(&d_A, n * n * sizeof(float));
    cudaMalloc(&d_B, n * n * sizeof(float));
    cudaMalloc(&d_C, n * n * sizeof(float));
    
    // Копирование данных на устройство
    cudaMemcpy(d_A, h_A, n * n * sizeof(float), cudaMemcpyHostToDevice);
    cudaMemcpy(d_B, h_B, n * n * sizeof(float), cudaMemcpyHostToDevice);
    
    // Конфигурация сетки и блоков
    dim3 threadsPerBlock(16, 16);
    dim3 numBlocks((n + 15) / 16, (n + 15) / 16);
    
    // Таймер
    cudaEvent_t start, stop;
    cudaEventCreate(&start);
    cudaEventCreate(&stop);
    
    cudaEventRecord(start);
    matrixMulKernel<<<numBlocks, threadsPerBlock>>>(d_A, d_B, d_C, n);
    cudaEventRecord(stop);
    cudaEventSynchronize(stop);
    
    float elapsed_ms;
    cudaEventElapsedTime(&elapsed_ms, start, stop);
    float elapsed_sec = elapsed_ms / 1000.0f;
    
    // Копирование результата обратно на хост
    cudaMemcpy(h_C, d_C, n * n * sizeof(float), cudaMemcpyDeviceToHost);
    
    // Расчёт GFLOPS
    float flops = 2.0f * pow(n, 3);
    float gflops = flops / (elapsed_sec * 1e9f);
    
    printf("Time: %.4f seconds\n", elapsed_sec);
    printf("Performance: %.2f GFLOPS\n", gflops);
    
    // Запись результата
    writeMatrix(argv[3], h_C, n);
    printf("Result saved to %s\n", argv[3]);
    
    printf("METRIC:N:%d\n", n);
    printf("METRIC:TIME:%.4f\n", elapsed_sec);
    printf("METRIC:GFLOPS:%.2f\n", gflops);
    
    // Очистка
    cudaFree(d_A);
    cudaFree(d_B);
    cudaFree(d_C);
    free(h_A);
    free(h_B);
    free(h_C);
    
    return 0;
}