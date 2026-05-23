#!/bin/bash
#SBATCH --job-name=mpi_lab3_tests
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --time=01:00:00
#SBATCH --output=tests_output.out
#SBATCH --error=tests_error.err

module load intel/mpi4
module load intel/icc18

cd $SLURM_SUBMIT_DIR

python3 scripts/gen_matrix.py 500 data/input_A.txt
python3 scripts/gen_matrix.py 500 data/input_B.txt

for P in 1 2 4 8; do
    srun -n $P ./matrix_mult_mpi data/input_A.txt data/input_B.txt data/output_C.txt
done

python3 scripts/verify.py data/input_A.txt data/input_B.txt data/output_C.txt

echo "Tests completed!"