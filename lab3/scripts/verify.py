#!/usr/bin/env python3
import sys
import numpy as np

def read_matrix(filename):
    with open(filename, 'r') as f:
        n = int(f.readline().strip())
        matrix = []
        for _ in range(n):
            row = list(map(float, f.readline().strip().split()))
            matrix.append(row)
        return np.array(matrix)

def main():
    if len(sys.argv) != 4:
        print("Usage: python verify.py <input_A> <input_B> <output_C>")
        sys.exit(1)

    file_a = sys.argv[1]
    file_b = sys.argv[2]
    file_c = sys.argv[3]

    print("Reading matrices...")
    A = read_matrix(file_a)
    B = read_matrix(file_b)
    C = read_matrix(file_c)

    print(f"Matrix A shape: {A.shape}")
    print(f"Matrix B shape: {B.shape}")
    print(f"Matrix C shape: {C.shape}")

    print("Calculating reference result...")
    C_ref = np.dot(A, B)

    print("Comparing results...")
    max_diff = np.max(np.abs(C - C_ref))
    
    print(f"Max difference: {max_diff}")

    tolerance = 1e-6
    if max_diff < tolerance:
        print("VERIFICATION: SUCCESS")
        sys.exit(0)
    else:
        print("VERIFICATION: FAILED")
        sys.exit(1)

if __name__ == "__main__":
    main()