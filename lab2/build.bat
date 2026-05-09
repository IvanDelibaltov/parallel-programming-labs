@echo off
echo Compiling with OpenMP...
g++ -O3 -std=c++11 -fopenmp -o matrix_mult.exe src/main.cpp
if %errorlevel% equ 0 (
    echo Success!
) else (
    echo Failed
    pause
)