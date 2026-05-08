@echo off
setlocal enabledelayedexpansion

echo ================================
echo Benchmark
echo ================================

if not exist "..\matrix_mult.exe" (
    echo Error: matrix_mult.exe not found!
    pause
    exit /b 1
)

if not exist "data" mkdir data
if not exist "..\results" mkdir ..\results

echo N,Time_sec,GFLOPS > ..\results\benchmark_results.csv

for %%N in (200 400 800 1200 1600 2000) do (
    echo.
    echo ========================================
    echo Testing N = %%N
    echo ========================================
    
    echo Generating matrices...
    python gen_matrix.py %%N data\bench_A.txt
    python gen_matrix.py %%N data\bench_B.txt
    
    echo Running multiplication...
    ..\matrix_mult.exe data\bench_A.txt data\bench_B.txt data\bench_C.txt > temp.txt
    
    :: Parse "Time: X seconds"
    for /f "tokens=2" %%T in ('findstr /c:"Time:" temp.txt') do set TIME_VAL=%%T
    
    :: Parse "Performance: X GFLOPS"  
    for /f "tokens=2" %%G in ('findstr /c:"Performance:" temp.txt') do set GFLOPS_VAL=%%G
    
    echo Time: !TIME_VAL! sec
    echo GFLOPS: !GFLOPS_VAL!
    
    echo %%N,!TIME_VAL!,!GFLOPS_VAL! >> ..\results\benchmark_results.csv
)

del temp.txt 2>nul
del data\bench_*.txt 2>nul

echo.
echo ================================
echo Benchmark completed!
echo ================================
echo.
echo Results:
type ..\results\benchmark_results.csv
echo.
pause