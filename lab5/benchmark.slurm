#!/bin/bash
#SBATCH --job-name=mpi_lab3_benchmark
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --time=02:00:00
#SBATCH --output=benchmark_%j.out
#SBATCH --error=benchmark_%j.err

module load intel/mpi4
module load intel/icc18

cd $SLURM_SUBMIT_DIR

mkdir -p results
echo "N,Procs,Time,GFLOPS,Speedup" > results/mpi_results.csv

for N in 200 400 800 1000; do
    python3 scripts/gen_matrix.py $N data/bench_A.txt
    python3 scripts/gen_matrix.py $N data/bench_B.txt
    
    srun -n 1 ./matrix_mult_mpi data/bench_A.txt data/bench_B.txt data/bench_C.txt > /tmp/out.txt
    BASE_TIME=$(grep "METRIC:TIME:" /tmp/out.txt | cut -d: -f3)
    
    for P in 1 2 4 8; do
        srun -n $P ./matrix_mult_mpi data/bench_A.txt data/bench_B.txt data/bench_C.txt > /tmp/out.txt
        TIME=$(grep "METRIC:TIME:" /tmp/out.txt | cut -d: -f3)
        GFLOPS=$(grep "METRIC:GFLOPS:" /tmp/out.txt | cut -d: -f3)
        SPEEDUP=$(echo "scale=2; $BASE_TIME / $TIME" | bc)
        echo "$N,$P,$TIME,$GFLOPS,$SPEEDUP" >> results/mpi_results.csv
    done
done