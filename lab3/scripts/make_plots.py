import matplotlib.pyplot as plt
import numpy as np

# Твои данные
N = [200, 400, 800, 1200, 1600, 2000]
time = [0.016, 0.153, 1.619, 11.510, 30.077, 75.127]
gflops = [1.00, 0.84, 0.63, 0.30, 0.27, 0.21]

# Теоретическая кривая O(N³), масштабируем под первую точку
N_theory = np.linspace(200, 2000, 100)
time_theory = time[0] * (N_theory / N[0]) ** 3

# Рисуем первый график: время от N
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(N, time, 'o-', linewidth=2, markersize=8, label='Measured')
plt.plot(N_theory, time_theory, '--', linewidth=2, label='O(N³) theoretical')
plt.xlabel('Matrix size N', fontsize=12)
plt.ylabel('Time (seconds)', fontsize=12)
plt.title('Execution Time vs Matrix Size', fontsize=14)
plt.legend()
plt.grid(True, alpha=0.3)

# Рисуем второй график: GFLOPS от N
plt.subplot(1, 2, 2)
plt.plot(N, gflops, 's-', linewidth=2, markersize=8, color='red')
plt.xlabel('Matrix size N', fontsize=12)
plt.ylabel('Performance (GFLOPS)', fontsize=12)
plt.title('Performance vs Matrix Size', fontsize=14)
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('../results/plots.png', dpi=150)
print("Графики сохранены в results/plots.png")
plt.show()