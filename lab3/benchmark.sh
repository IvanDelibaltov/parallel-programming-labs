#!/bin/bash

echo "=========================================="
echo "MPI Benchmark Suite"
echo "=========================================="

mkdir -p results data

# Заголовки CSV
echo "N,Processes,Time_sec,GFLOPS,Speedup" > results/mpi_results.csv

# Размеры матриц
SIZES="200 400 800 1200 1600 2000"
# Количество процессов
PROCS="1 2 4 8"

for N in $SIZES; do
    echo ""
    echo "=========================================="
    echo "Matrix size: ${N}x${N}"
    echo "=========================================="
    
    # Генерация матриц
    python3 scripts/gen_matrix.py $N data/matrix_${N}.txt
    
    # База для ускорения (1 процесс)
    BASE_TIME=""
    
    for P in $PROCS; do
        echo -n "  Running with $P processes... "
        
        OUTPUT=$(mpirun -np $P ./matrix_mult_mpi data/matrix_${N}.txt data/matrix_${N}.txt data/out_${N}_${P}.txt 2>&1)
        
        TIME=$(echo "$OUTPUT" | grep "METRIC:TIME:" | cut -d: -f3)
        GFLOPS=$(echo "$OUTPUT" | grep "METRIC:GFLOPS:" | cut -d: -f3)
        
        if [ -z "$BASE_TIME" ] && [ "$P" = "1" ]; then
            BASE_TIME=$TIME
            SPEEDUP=1
        else
            SPEEDUP=$(echo "scale=2; $BASE_TIME / $TIME" | bc)
        fi
        
        echo "Time: ${TIME}s, GFLOPS: ${GFLOPS}, Speedup: ${SPEEDUP}x"
        echo "$N,$P,$TIME,$GFLOPS,$SPEEDUP" >> results/mpi_results.csv
    done
done

echo ""
echo "=========================================="
echo "Benchmark completed!"
echo "Results saved to results/mpi_results.csv"
echo "=========================================="
echo ""
echo "Results summary:"
cat results/mpi_results.csv
