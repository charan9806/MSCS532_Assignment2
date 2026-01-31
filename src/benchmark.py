from __future__ import annotations
import time
import tracemalloc
import random
import csv
import os
from typing import Callable, List, Dict, Tuple

# These are in a local file named sorts.py
from sorts import quicksort, mergesort

# Dataset Generators

def make_sorted(n: int) -> List[int]:
    # Best-case scenario for some algos, worst for others (like basic QuickSort)
    return list(range(n))

def make_reverse_sorted(n: int) -> List[int]:
    # Worst-case scenario usually
    return list(range(n, 0, -1))

def make_random(n: int, seed: int = 42) -> List[int]:
    # Standard random input. Fixed seed so results are reproducible.
    rng = random.Random(seed)
    return [rng.randint(0, 10**9) for _ in range(n)]

# Performance Tracking

def measure_time_and_memory(sort_fn: Callable[[List[int]], List[int]], data: List[int]) -> Tuple[float, int]:
    # Start memory tracing
    tracemalloc.start()

    # Time the function
    start = time.perf_counter()
    out = sort_fn(data)  # sort on a provided list
    end = time.perf_counter()

    # Validate correctness quickly (optional but helpful)
    if out != sorted(data):
        raise ValueError(f"{sort_fn.__name__} produced incorrect result!")

    # Capture peak memory
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return (end - start), peak

# Benchmark runner

def run_benchmarks(
    sizes: List[int],
    repeats: int = 3,
    out_csv_path: str = "../results/results.csv"
) -> None:
   
   # Make sure the folder exists so we don't crash on file write
    os.makedirs(os.path.dirname(out_csv_path), exist_ok=True)

    algorithms: Dict[str, Callable[[List[int]], List[int]]] = {
        "quicksort_random_pivot": quicksort,
        "mergesort": mergesort,
    }

    datasets: Dict[str, Callable[[int], List[int]]] = {
        "sorted": make_sorted,
        "reverse_sorted": make_reverse_sorted,
        "random": make_random,
    }

    rows = []
    for n in sizes:
        for dataset_name, make_fn in datasets.items():
            # Generate the base data once for this size/type
            base_data = make_fn(n)

            for alg_name, alg_fn in algorithms.items():
                for run in range(1, repeats + 1):
                    # IMPORTANT: pass a copy so each run sees the same input
                    data = list(base_data)

                    elapsed, peak_mem = measure_time_and_memory(alg_fn, data)

                    rows.append({
                        "algorithm": alg_name,
                        "dataset": dataset_name,
                        "n": n,
                        "run": run,
                        "time_sec": elapsed,
                        "peak_mem_bytes": peak_mem,
                    })
                    print(f"n={n:6d} | {dataset_name:13s} | {alg_name:22s} | run={run} | time={elapsed:.6f}s | mem={peak_mem}")

    # Write CSV
    with open(out_csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nSaved results to: {out_csv_path}")

# Plotting and table summary

def summarize_and_plot(
    csv_path: str = "../results/results.csv",
    out_time_plot: str = "../results/time_plot.png",
    out_mem_plot: str = "../results/memory_plot.png"
) -> None:

    import pandas as pd
    import matplotlib.pyplot as plt

    df = pd.read_csv(csv_path)

    # Aggregate mean over runs
    agg = (
        df.groupby(["algorithm", "dataset", "n"], as_index=False)
          .agg(time_sec_mean=("time_sec", "mean"),
               peak_mem_mean=("peak_mem_bytes", "mean"))
    )

    # Save aggregated table for easy copy into report
    agg_out_path = os.path.join(os.path.dirname(csv_path), "results_aggregated.csv")
    agg.to_csv(agg_out_path, index=False)
    print(f"Saved aggregated table to: {agg_out_path}\n")

    # Print a small table preview
    print("Aggregated Results (mean over runs):")
    print(agg.head(20).to_string(index=False))

    # Time plot
    plt.figure()
    for (alg, dataset), sub in agg.groupby(["algorithm", "dataset"]):
        # plot each line separately
        sub_sorted = sub.sort_values("n")
        plt.plot(sub_sorted["n"], sub_sorted["time_sec_mean"], label=f"{alg} | {dataset}")
    plt.xlabel("n")
    plt.ylabel("mean time (sec)")
    plt.title("Sorting Time vs Input Size")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_time_plot, dpi=200)

    #Memory plot
    plt.figure()
    for (alg, dataset), sub in agg.groupby(["algorithm", "dataset"]):
        sub_sorted = sub.sort_values("n")
        plt.plot(sub_sorted["n"], sub_sorted["peak_mem_mean"], label=f"{alg} | {dataset}")
    plt.xlabel("n")
    plt.ylabel("mean peak memory (bytes)")
    plt.title("Peak Memory vs Input Size")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_mem_plot, dpi=200)

    print(f"\nSaved plots:\n- {out_time_plot}\n- {out_mem_plot}")

# Main

if __name__ == "__main__":
    # Choose sizes that won't blow recursion/time in Python.
    # You can increase, but if you do, consider using iterative / in-place variants.
    sizes = [200, 500, 1000, 2000, 5000]

    run_benchmarks(sizes=sizes, repeats=3, out_csv_path="../results/results.csv")
    summarize_and_plot(
        csv_path="../results/results.csv",
        out_time_plot="../results/time_plot.png",
        out_mem_plot="../results/memory_plot.png"
    )
