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

    A = read_matrix(sys.argv[1])
    B = read_matrix(sys.argv[2])
    C = read_matrix(sys.argv[3])

    C_ref = np.dot(A, B)
    max_diff = np.max(np.abs(C - C_ref))

    print(f"Max difference: {max_diff}")

    if max_diff < 1e-6:
        print("VERIFICATION: SUCCESS")
        sys.exit(0)
    else:
        print("VERIFICATION: FAILED")
        sys.exit(1)

if __name__ == "__main__":
    main()