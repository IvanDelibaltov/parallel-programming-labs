import matplotlib.pyplot as plt
import pandas as pd

# Читаем результаты
df = pd.read_csv('../results/openmp_results.csv')

# Создаём сводные таблицы
time_pivot = df.pivot(index='N', columns='Threads', values='Time_sec')
speedup_pivot = time_pivot[1] / time_pivot

# График 1: Время
plt.figure(figsize=(12,5))
plt.subplot(1,2,1)
for t in [1,2,4,8]:
    plt.plot(time_pivot.index, time_pivot[t], 'o-', label=f'{t} threads')
plt.xlabel('Matrix size N')
plt.ylabel('Time (seconds)')
plt.title('Execution Time vs Matrix size')
plt.legend()
plt.grid(True, alpha=0.3)

# График 2: Ускорение
plt.subplot(1,2,2)
for t in [2,4,8]:
    plt.plot(speedup_pivot.index, speedup_pivot[t], 's-', label=f'{t} threads')
plt.plot([200,2000], [1,1], 'k--', alpha=0.5)
plt.xlabel('Matrix size N')
plt.ylabel('Speedup')
plt.title('Speedup vs Matrix size')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('../images/omp_plots.png', dpi=150)
print("Графики сохранены в images/omp_plots.png")