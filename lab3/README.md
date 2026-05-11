
# Умножение матриц с распараллеливанием (MPI)

## Описание

Программа на C++ для перемножения квадратных матриц с использованием технологии MPI (Message Passing Interface). Автоматическая верификация результатов через Python (NumPy).

## Структура проекта

| Файл | Назначение |
|------|------------|
| src/main_mpi.cpp | Исходный код C++ (умножение матриц + MPI) |
| scripts/verify.py | Проверка результата через Python/NumPy |
| scripts/gen_matrix.py | Генерация тестовых матриц |
| scripts/run_test.sh | Автоматическая верификация |
| scripts/benchmark_mpi.sh | Серия экспериментов производительности |
| scripts/plot_mpi_full.py | Построение графиков |
| Makefile | Компиляция программы |
| data/ | Папка для входных/выходных файлов |
| results/ | Папка для результатов бенчмарка и графиков |

## Входные данные (матрицы)

### Формат входных файлов

Матрицы хранятся в текстовых файлах в папке data/:

- N — размер матрицы (первая строка)
- a_ij — элементы матрицы (разделены пробелами)

Создаются при помощи `scripts/gen_matrix.py` для выполнения тестов.

## Как проходят тесты и проверки

### 1. Верификация корректности (run_test.sh)

Что делает:
- Создаёт тестовые матрицы 500×500
- Запускает matrix_mult_mpi на 1, 2, 4, 8 процессах
- Сравнивает результат с эталоном (Python + NumPy)
- Выводит VERIFICATION: SUCCESS или FAILED

### 2. Тест производительности (benchmark_mpi.sh)

Что делает:
- Генерирует матрицы размеров: 200, 400, 800, 1200, 1600, 2000
- Для каждого размера запускает умножение на 1, 2, 4, 8 процессах
- Замеряет время и вычисляет метрики: GFLOPS, Speedup
- Сохраняет результаты в `results/mpi_results.csv`

### Метрики

| Метрика | Описание | Формула |
|---------|----------|---------|
| Time | Время выполнения (сек) | Замер через MPI_Wtime() |
| GFLOPS | Производительность | 2×N³ / (Time × 10⁹) |
| Speedup | Ускорение | T(1 proc) / T(N procs) |

## Как запускать

### Полный цикл (компиляция + тесты)

1. Компиляция
```bash
make
Верификация корректности

bash
cd scripts
./run_test.sh
Бенчмарк производительности

bash
./benchmark_mpi.sh
Построение графиков

bash
python3 plot_mpi_full.py
Требования
ОС: Linux (Ubuntu/Debian) или WSL2

Компилятор: g++ с поддержкой MPI

MPI: openmpi-bin, libopenmpi-dev

Python: 3.8+ с библиотеками numpy, pandas, matplotlib

Установка зависимостей (Ubuntu):

bash
sudo apt install openmpi-bin libopenmpi-dev g++ python3 python3-pip
sudo apt install python3-numpy python3-pandas python3-matplotlib
Результаты
Вывод run_test.sh
text
================================
Automated testing (MPI version)
================================

Generating test matrices (500x500)...
Generated 500x500 matrix -> data/input_A.txt
Generated 500x500 matrix -> data/input_B.txt

Test 1: Correctness check (4 processes)
----------------------------------------
Reading matrices...
Matrix size: 500x500
MPI processes: 4
Time: 0.125338 seconds
Performance: 1.99461 GFLOPS
VERIFICATION: SUCCESS
Max difference: 4.00e-11

Test 2: Different number of processes
----------------------------------------

Running on 1 processes...
Time: 0.240014 seconds
Performance: 1.04161 GFLOPS
VERIFICATION: SUCCESS

Running on 2 processes...
Time: 0.128568 seconds
Performance: 1.94449 GFLOPS
VERIFICATION: SUCCESS

Running on 4 processes...
Time: 0.125338 seconds
Performance: 1.99461 GFLOPS
VERIFICATION: SUCCESS

Running on 8 processes...
Time: 0.144256 seconds
Performance: 1.73303 GFLOPS
VERIFICATION: SUCCESS

================================
ALL TESTS HAVE BEEN PASSED SUCCESSFULLY!
================================
Процессы	Время (сек)	GFLOPS	Ускорение	Погрешность	Статус
1	0.2400	1.04	1.00×	4.00×10⁻¹¹	✅
2	0.1286	1.94	1.87×	4.00×10⁻¹¹	✅
4	0.1253	2.00	1.92×	4.00×10⁻¹¹	✅
8	0.1443	1.73	1.66×	4.00×10⁻¹¹	✅
Вывод benchmark_mpi.sh
text
================================
MPI Benchmark Suite
================================

Matrix size: 200x200
  1 processes: Time=0.01161s, GFLOPS=1.38, Speedup=1.00x
  2 processes: Time=0.00645s, GFLOPS=2.48, Speedup=1.79x
  4 processes: Time=0.00553s, GFLOPS=2.89, Speedup=2.09x
  8 processes: Time=0.00457s, GFLOPS=3.50, Speedup=2.53x

Matrix size: 400x400
  1 processes: Time=0.10076s, GFLOPS=1.27, Speedup=1.00x
  2 processes: Time=0.05570s, GFLOPS=2.30, Speedup=1.80x
  4 processes: Time=0.05515s, GFLOPS=2.32, Speedup=1.82x
  8 processes: Time=0.05204s, GFLOPS=2.46, Speedup=1.93x

Matrix size: 800x800
  1 processes: Time=2.64093s, GFLOPS=0.39, Speedup=1.00x
  2 processes: Time=2.54029s, GFLOPS=0.40, Speedup=1.03x
  4 processes: Time=1.36979s, GFLOPS=0.75, Speedup=1.92x
  8 processes: Time=1.18851s, GFLOPS=0.86, Speedup=2.22x

Matrix size: 1200x1200
  1 processes: Time=19.6261s, GFLOPS=0.18, Speedup=1.00x
  2 processes: Time=12.2062s, GFLOPS=0.28, Speedup=1.60x
  4 processes: Time=7.86652s, GFLOPS=0.44, Speedup=2.49x
  8 processes: Time=8.97945s, GFLOPS=0.38, Speedup=2.18x

Matrix size: 1600x1600
  1 processes: Time=45.9237s, GFLOPS=0.18, Speedup=1.00x
  2 processes: Time=26.4521s, GFLOPS=0.31, Speedup=1.73x
  4 processes: Time=18.8287s, GFLOPS=0.44, Speedup=2.43x
  8 processes: Time=20.0884s, GFLOPS=0.41, Speedup=2.28x

Matrix size: 2000x2000
  1 processes: Time=99.6758s, GFLOPS=0.16, Speedup=1.00x
  2 processes: Time=56.8087s, GFLOPS=0.28, Speedup=1.75x
  4 processes: Time=39.0492s, GFLOPS=0.41, Speedup=2.55x
  8 processes: Time=40.4566s, GFLOPS=0.40, Speedup=2.46x
```

## Сводные таблицы

### Время выполнения (секунды)

| N | 1 процесс | 2 процесса | 4 процесса | 8 процессов |
|---|--------|--------|--------|--------|
| 200 | 0.0116 | 0.0065 | 0.0055 | 0.0046 |
| 400 | 0.1008 | 0.0557 | 0.0552 | 0.0520 |
| 800 | 2.6409 | 2.5403 | 1.3698 | 1.1885 |
| 1200 | 19.6261 | 12.2062 | 7.8665 | 8.9795 |
| 1600 | 45.9237 | 26.4521 | 18.8287 | 20.0884 |
| 2000 | 99.6758 | 56.8087 | 39.0492 | 40.4566 |

### Производительность (GFLOPS)

| N | 1 процесс | 2 процесса | 4 процесса | 8 процессов |
|---|--------|--------|--------|--------|
| 200 | 1.38 | 2.48 | 2.89 | 3.50 |
| 400 | 1.27 | 2.30 | 2.32 | 2.46 |
| 800 | 0.39 | 0.40 | 0.75 | 0.86 |
| 1200 | 0.18 | 0.28 | 0.44 | 0.38 |
| 1600 | 0.18 | 0.31 | 0.44 | 0.41 |
| 2000 | 0.16 | 0.28 | 0.41 | 0.40 |

### Ускорение (Speedup)

| N | 2 процесса | 4 процесса | 8 процессов |
|---|--------|--------|--------|
| 200 | 1.79× | 2.09× | 2.53× |
| 400 | 1.80× | 1.82× | 1.93× |
| 800 | 1.03× | 1.92× | 2.22× |
| 1200 | 1.60× | 2.49× | 2.18× |
| 1600 | 1.73× | 2.43× | 2.28× |
| 2000 | 1.75× | 2.55× | 2.46× |

## Графики
1. Ускорение (Speedup) по размерам матрицы
<img width="1500" height="900" alt="image" src="https://github.com/user-attachments/assets/d25a6a6a-0f22-49ac-870b-d3607d1ee2dd" />


2. Производительность (GFLOPS) по размерам матрицы
<img width="1500" height="900" alt="image" src="https://github.com/user-attachments/assets/fbe61af9-9d41-4439-9f3f-af38f29f85e2" />


3. Масштабирование времени (логарифмический масштаб)
<img width="1500" height="900" alt="image" src="https://github.com/user-attachments/assets/b751f240-e54a-4986-be63-b28f938abb7e" />


4. Тепловая карта производительности (GFLOPS)
<img width="1500" height="900" alt="image" src="https://github.com/user-attachments/assets/21b5305d-f630-44e1-a3bc-51a50d72d488" />


5. Производительность vs процессы (N=1200)
<img width="1500" height="900" alt="image" src="https://github.com/user-attachments/assets/6b7c73db-619e-4949-80f2-6c3064eba8d5" />


## Анализ результатов
Верификация: Все тесты пройдены успешно. Погрешность не превышает 4×10⁻¹¹, что находится в пределах машинной точности типа double.

Ускорение: Максимальное ускорение 2.55× достигнуто на матрице 2000×2000 с 4 процессами. Для больших матриц (1200-2000) ускорение составляет 2.4-2.6× на 4 процессах.

Эффективность: На 8 процессах эффективность падает из-за накладных расходов на коммуникацию. Оптимальное количество процессов для данной вычислительной системы — 4.

Масштабируемость: Для малых матриц (200-400) накладные расходы MPI заметны, но ускорение всё равно достигает 1.8-2.5× на 8 процессах. Для больших матриц (≥800) ускорение стабилизируется на уровне 2.2-2.6×.

Производительность: Пиковая производительность 3.50 GFLOPS достигнута на матрице 200×200 с 8 процессами. Для больших матриц производительность падает до 0.40 GFLOPS из-за ограничений пропускной способности памяти (memory-bound режим).

### Вывод
MPI-реализация демонстрирует корректную работу и масштабируемость на больших матрицах. Оптимальное ускорение достигается на 4 процессах для матриц размером ≥800×800. Для матриц 2000×2000 ускорение составляет 2.55× на 4 процессах. Наибольший прирост производительности наблюдается при переходе с 1 на 2 процесса. Использование более 4 процессов на данной вычислительной системе не даёт дополнительного выигрыша из-за накладных расходов на коммуникацию и неравномерного распределения нагрузки.

Временная сложность алгоритма соответствует теоретической O(N³), что подтверждается логарифмическим графиком зависимости времени от размера матрицы.

## Требования для запуска
ОС: Linux (Ubuntu/Debian) или WSL2

Компилятор C++ с поддержкой MPI

Python 3 с библиотеками: numpy, pandas, matplotlib
