import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Читаем результаты
df = pd.read_csv('results/mpi_results.csv')

# Создаём сводные таблицы
time_pivot = df.pivot(index='N', columns='Processes', values='Time_sec')
gflops_pivot = df.pivot(index='N', columns='Processes', values='GFLOPS')
speedup_pivot = df.pivot(index='N', columns='Processes', values='Speedup')

# График 1: Ускорение
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
for proc in [2, 4, 8]:
    plt.plot(speedup_pivot.index, speedup_pivot[proc], 'o-', label=f'{proc} processes')
plt.plot([200, 2000], [1, 1], 'k--', alpha=0.5)
plt.plot([200, 2000], [8, 8], 'k--', alpha=0.3, label='Ideal 8x')
plt.xlabel('Matrix size N')
plt.ylabel('Speedup')
plt.title('MPI Speedup vs Matrix Size')
plt.legend()
plt.grid(True, alpha=0.3)

# График 2: Время выполнения (логарифмический)
plt.subplot(1, 2, 2)
for proc in [1, 2, 4, 8]:
    plt.loglog(time_pivot.index, time_pivot[proc], 'o-', label=f'{proc} processes')
plt.xlabel('Matrix size N (log scale)')
plt.ylabel('Time (seconds, log scale)')
plt.title('MPI Execution Time vs Matrix Size')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('results/mpi_plots.png', dpi=150)
print("Графики сохранены в results/mpi_plots.png")

# График 3: Тепловая карта GFLOPS
plt.figure(figsize=(10, 6))
im = plt.imshow(gflops_pivot.values, cmap='YlOrRd', aspect='auto')
plt.colorbar(im, label='GFLOPS')
plt.xticks(range(len(gflops_pivot.columns)), [f'{p} proc' for p in gflops_pivot.columns])
plt.yticks(range(len(gflops_pivot.index)), [f'N={n}' for n in gflops_pivot.index])
plt.title('MPI Performance (GFLOPS) Heatmap')
for i in range(len(gflops_pivot.index)):
    for j in range(len(gflops_pivot.columns)):
        plt.text(j, i, f'{gflops_pivot.values[i, j]:.2f}', ha='center', va='center')
plt.tight_layout()
plt.savefig('results/mpi_heatmap.png', dpi=150)
print("Тепловая карта сохранена в results/mpi_heatmap.png")

print("\n=== Сводная таблица ускорения ===")
print(speedup_pivot.to_string())
