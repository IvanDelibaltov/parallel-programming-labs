CC = mpicxx
CFLAGS = -O3 -std=c++11

all: matrix_mult_mpi

matrix_mult_mpi: src/main_mpi.cpp
	$(CC) $(CFLAGS) -o matrix_mult_mpi src/main_mpi.cpp

clean:
	rm -f matrix_mult_mpi

run:
	mpirun -np 4 ./matrix_mult_mpi data/input.txt data/input.txt data/output.txt
