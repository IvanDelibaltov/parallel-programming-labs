import subprocess
import os
import sys

def main():
    # Размеры матриц
    sizes = [200, 400, 800, 1200, 1600, 2000]
    # Количество потоков
    threads = [1, 2, 4, 8]
    
    # Создаём папку для результатов
    if not os.path.exists("../results"):
        os.makedirs("../results")
    
    # Открываем CSV файл для записи
    with open("../results/openmp_results.csv", "w") as f:
        f.write("N,Threads,Time_sec,GFLOPS\n")
        
        for n in sizes:
            print(f"\n=== Testing N={n} ===")
            
            # Генерируем матрицы
            print(f"Generating {n}x{n} matrices...")
            subprocess.run(["python", "gen_matrix.py", str(n), f"../data/bench_{n}.txt"], check=True)
            
            for t in threads:
                print(f"  Threads={t}...")
                
                # Запускаем программу с нужным количеством потоков
                env = os.environ.copy()
                env["OMP_NUM_THREADS"] = str(t)
                
                result = subprocess.run(
                    ["../matrix_mult.exe", f"../data/bench_{n}.txt", f"../data/bench_{n}.txt", "../data/out.txt"],
                    capture_output=True,
                    text=True,
                    env=env
                )
                
                # Парсим вывод
                time_val = ""
                gflops_val = ""
                for line in result.stdout.split("\n"):
                    if "Time:" in line and "seconds" in line:
                        time_val = line.split()[1]
                    if "Performance:" in line and "GFLOPS" in line:
                        gflops_val = line.split()[1]
                
                print(f"    Time={time_val} sec, GFLOPS={gflops_val}")
                f.write(f"{n},{t},{time_val},{gflops_val}\n")
    
    print("\n=== Done! Results saved to ../results/openmp_results.csv ===")
    
    # Выводим результаты
    print("\n=== Results ===")
    with open("../results/openmp_results.csv", "r") as f:
        print(f.read())

if __name__ == "__main__":
    main()