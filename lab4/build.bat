@echo off
echo Compiling CUDA matrix multiplication...
nvcc -O3 -o matrix_mult_cuda.exe src/main.cu
if %errorlevel% equ 0 (
    echo Success!
) else (
    echo Failed
    pause
)