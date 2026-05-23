#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

os.makedirs('results/plots', exist_ok=True)

# Твои данные (без N=1000)
data = {
    'N': [200, 400, 800, 1200, 1600, 2000],
    '1': [0.0116924, 0.10722, 2.54558, 19.3862, 46.326, 100.105],
    '2': [0.00593263, 0.0547996, 2.19319, 11.1421, 24.1711, 52.7054],
    '4': [0.00839583, 0.0599097, 1.00712, 7.91369, 17.4493, 35.9874],
    '8': [0.00807923, 0.0436008, 1.24024, 8.03484, 24.8959, 37.9266]
}

df = pd.DataFrame(data)
df = df.set_index('N')

# Расчёт GFLOPS и Speedup
for p in ['1', '2', '4', '8']:
    df[f'GFLOPS_{p}'] = 2 * df.index**3 / (df[p] * 1e9)
    df[f'Speedup_{p}'] = df['1'] / df[p]

# График 1: Speedup
plt.figure(figsize=(10, 6))
for p in ['2', '4', '8']:
    plt.plot(df.index, df[f'Speedup_{p}'], 'o-', label=f'{p} processes', linewidth=2, markersize=8)
plt.plot([200, 2000], [1, 1], 'k--', alpha=0.5)
plt.plot([200, 2000], [2, 2], 'k:', alpha=0.3)
plt.plot([200, 2000], [4, 4], 'k:', alpha=0.3)
plt.plot([200, 2000], [8, 8], 'k:', alpha=0.3)
plt.xlabel('Matrix size N', fontsize=12)
plt.ylabel('Speedup', fontsize=12)
plt.title('MPI Speedup vs Matrix Size', fontsize=14)
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('results/plots/01_speedup.png', dpi=150)
plt.close()
print("✅ 01_speedup.png")

# График 2: GFLOPS
plt.figure(figsize=(10, 6))
for p in ['1', '2', '4', '8']:
    plt.plot(df.index, df[f'GFLOPS_{p}'], 's-', label=f'{p} processes', linewidth=2, markersize=8)
plt.xlabel('Matrix size N', fontsize=12)
plt.ylabel('Performance (GFLOPS)', fontsize=12)
plt.title('MPI Performance vs Matrix Size', fontsize=14)
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('results/plots/02_gflops.png', dpi=150)
plt.close()
print("✅ 02_gflops.png")

# График 3: Log-log время
plt.figure(figsize=(10, 6))
for p in ['1', '2', '4', '8']:
    plt.loglog(df.index, df[p], 'o-', label=f'{p} processes', linewidth=2, markersize=8)
n_ref = np.array([200, 2000])
t_ref = df.loc[200, '1']
t_curve = t_ref * (n_ref / 200)**3
plt.loglog(n_ref, t_curve, 'k--', linewidth=2, label='O(N³) reference')
plt.xlabel('Matrix size N (log scale)', fontsize=12)
plt.ylabel('Time (seconds, log scale)', fontsize=12)
plt.title('MPI Scaling with Matrix Size (Log-Log)', fontsize=14)
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('results/plots/03_time_loglog.png', dpi=150)
plt.close()
print("✅ 03_time_loglog.png")

# График 4: Heatmap GFLOPS
plt.figure(figsize=(10, 6))
gflops_matrix = np.array([df[f'GFLOPS_{p}'].values for p in ['1', '2', '4', '8']]).T
im = plt.imshow(gflops_matrix, cmap='YlOrRd', aspect='auto')
plt.colorbar(im, label='GFLOPS')
plt.xticks(range(4), ['1 proc', '2 procs', '4 procs', '8 procs'])
plt.yticks(range(len(df.index)), [f'N={n}' for n in df.index])
plt.title('MPI Performance Heatmap (GFLOPS)', fontsize=14)
for i in range(len(df.index)):
    for j in range(4):
        plt.text(j, i, f'{gflops_matrix[i, j]:.2f}', ha='center', va='center', fontsize=9)
plt.tight_layout()
plt.savefig('results/plots/04_heatmap.png', dpi=150)
plt.close()
print("✅ 04_heatmap.png")

# График 5: Combined для N=1200 (вместо 1000)
plt.figure(figsize=(10, 6))
procs = [1, 2, 4, 8]
times = [df.loc[1200, '1'], df.loc[1200, '2'], df.loc[1200, '4'], df.loc[1200, '8']]
gflops_1200 = [df.loc[1200, 'GFLOPS_1'], df.loc[1200, 'GFLOPS_2'], df.loc[1200, 'GFLOPS_4'], df.loc[1200, 'GFLOPS_8']]

ax1 = plt.gca()
ax1.plot(procs, times, 'o-', color='blue', linewidth=2, markersize=8, label='Time (sec)')
ax1.set_xlabel('Number of processes', fontsize=12)
ax1.set_ylabel('Time (seconds)', color='blue', fontsize=12)
ax1.tick_params(axis='y', labelcolor='blue')

ax2 = ax1.twinx()
ax2.plot(procs, gflops_1200, 's-', color='green', linewidth=2, markersize=8, label='GFLOPS')
ax2.set_ylabel('Performance (GFLOPS)', color='green', fontsize=12)
ax2.tick_params(axis='y', labelcolor='green')

plt.title('MPI Performance vs Processes (N=1200)', fontsize=14)
plt.grid(True, alpha=0.3)
plt.savefig('results/plots/05_combined_n1200.png', dpi=150)
plt.close()
print("✅ 05_combined_n1200.png")

print("\n✅ Все графики сохранены в results/plots/")
