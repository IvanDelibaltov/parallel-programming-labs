@echo off
setlocal enabledelayedexpansion

echo ================================
echo OpenMP Benchmark
echo ================================
echo.

if not exist "matrix_mult.exe" (
    echo Error: matrix_mult.exe not found!
    pause
    exit /b 1
)

if not exist "data" mkdir data
if not exist "results" mkdir results

echo N,Threads,Time_sec,GFLOPS > results\openmp_results.csv

for %%N in (200 400 800 1200 1600 2000) do (
    echo.
    echo ========================================
    echo Matrix size: %%N x %%N
    echo ========================================
    
    echo Generating matrices...
    python scripts\gen_matrix.py %%N data\bench_A.txt
    python scripts\gen_matrix.py %%N data\bench_B.txt
    
    for %%T in (1 2 4 8) do (
        echo Running with %%T threads...
        set OMP_NUM_THREADS=%%T
        matrix_mult.exe data\bench_A.txt data\bench_B.txt data\bench_C.txt > temp.txt
        
        for /f "tokens=2" %%L in ('findstr "METRIC:TIME:" temp.txt') do set time_val=%%L
        for /f "tokens=2" %%G in ('findstr "METRIC:GFLOPS:" temp.txt') do set gflops_val=%%G
        
        echo %%N,%%T,!time_val!,!gflops_val! >> results\openmp_results.csv
    )
)

del temp.txt 2>nul
del data\bench_*.txt 2>nul

echo.
echo ================================
echo Benchmark completed!
echo Results saved to results\openmp_results.csv
echo ================================
type results\openmp_results.csv
pause