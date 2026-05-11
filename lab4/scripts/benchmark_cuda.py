#!/usr/bin/env python3
import subprocess
import os
import sys

os.makedirs("../results", exist_ok=True)

sizes = [200, 400, 800, 1200, 1600, 2000]
block_sizes = [16, 32]  # threads per block

with open("../results/cuda_results.csv", "w") as f:
    f.write("N,BlockSize,Time_sec,GFLOPS\n")
    
    for N in sizes:
        print(f"\n=== Testing N={N} ===")
        subprocess.run(["python", "gen_matrix.py", str(N), f"../data/matrix_{N}.txt"], check=True)
        
        for bs in block_sizes:
            print(f"  Block size={bs}x{bs}...")
            env = os.environ.copy()
            env["CUDA_BLOCK_SIZE"] = str(bs)
            
            result = subprocess.run(
                [f"../matrix_mult_cuda.exe", f"../data/matrix_{N}.txt", f"../data/matrix_{N}.txt", f"../data/out_{N}.txt"],
                capture_output=True, text=True, env=env
            )
            
            time_val = ""
            gflops_val = ""
            for line in result.stdout.split("\n"):
                if "METRIC:TIME:" in line:
                    time_val = line.split(":")[2]
                if "METRIC:GFLOPS:" in line:
                    gflops_val = line.split(":")[2]
            
            print(f"    Time={time_val}s, GFLOPS={gflops_val}")
            f.write(f"{N},{bs},{time_val},{gflops_val}\n")

print("\n=== Done! Results saved to ../results/cuda_results.csv ===")