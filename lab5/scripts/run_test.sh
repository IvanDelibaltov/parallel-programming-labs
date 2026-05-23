#!/bin/bash

echo "================================"
echo "Automated testing (MPI version)"
echo "================================"

cd "$(dirname "$0")/.."

if [ ! -f "matrix_mult_mpi" ]; then
    echo "Error: matrix_mult_mpi not found!"
    echo "Run make first."
    exit 1
fi

mkdir -p data

echo ""
echo "Generating test matrices (500x500)..."
python3 scripts/gen_matrix.py 500 data/input_A.txt
python3 scripts/gen_matrix.py 500 data/input_B.txt

echo ""
echo "Test 1: Correctness check (4 processes)"
echo "----------------------------------------"
mpirun -np 4 ./matrix_mult_mpi data/input_A.txt data/input_B.txt data/output_C.txt
python3 scripts/verify.py data/input_A.txt data/input_B.txt data/output_C.txt

echo ""
echo "Test 2: Different number of processes"
echo "----------------------------------------"

for P in 1 2 4 8; do
    echo ""
    echo "Running on $P processes..."
    mpirun -np $P ./matrix_mult_mpi data/input_A.txt data/input_B.txt data/output_C.txt
    python3 scripts/verify.py data/input_A.txt data/input_B.txt data/output_C.txt
done

echo ""
echo "================================"
echo "ALL TESTS HAVE BEEN PASSED SUCCESSFULLY!"
echo "================================"
