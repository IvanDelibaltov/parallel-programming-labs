@echo off
setlocal enabledelayedexpansion

echo ================================
echo Verification Test
echo ================================

if not exist "..\matrix_mult.exe" (
    echo Error: matrix_mult.exe not found!
    echo Please run build.bat first from the lab1 folder.
    pause
    exit /b 1
)

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: Python not found!
    pause
    exit /b 1
)

if not exist "data" mkdir data

echo.
echo [Test 1] Small matrix (3x3)
echo ----------------------------------------

echo 3 > data\test_A.txt
echo 1 2 3 >> data\test_A.txt
echo 4 5 6 >> data\test_A.txt
echo 7 8 9 >> data\test_A.txt

echo 3 > data\test_B.txt
echo 9 8 7 >> data\test_B.txt
echo 6 5 4 >> data\test_B.txt
echo 3 2 1 >> data\test_B.txt

..\matrix_mult.exe data\test_A.txt data\test_B.txt data\test_C.txt

python verify.py data\test_A.txt data\test_B.txt data\test_C.txt
if %errorlevel% neq 0 (
    echo.
    echo VERIFICATION FAILED!
    pause
    exit /b 1
)

echo.
echo [Test 2] Medium matrix (100x100)
echo ----------------------------------------

python gen_matrix.py 100 data\test_A.txt
python gen_matrix.py 100 data\test_B.txt

..\matrix_mult.exe data\test_A.txt data\test_B.txt data\test_C.txt

python verify.py data\test_A.txt data\test_B.txt data\test_C.txt
if %errorlevel% neq 0 (
    echo.
    echo VERIFICATION FAILED!
    pause
    exit /b 1
)

echo.
echo [Test 3] Large matrix (500x500)
echo ----------------------------------------

python gen_matrix.py 500 data\test_A.txt
python gen_matrix.py 500 data\test_B.txt

..\matrix_mult.exe data\test_A.txt data\test_B.txt data\test_C.txt

python verify.py data\test_A.txt data\test_B.txt data\test_C.txt
if %errorlevel% neq 0 (
    echo.
    echo VERIFICATION FAILED!
    pause
    exit /b 1
)

echo.
echo ================================
echo ALL VERIFICATION TESTS PASSED!
echo ================================
pause