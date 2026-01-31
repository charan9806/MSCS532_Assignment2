from __future__ import annotations
import time
import tracemalloc
import random
import csv
import os
from typing import Callable, List, Dict, Tuple

from sorts import quicksort, mergesort

# -----------------------------
# Making the lists
# -----------------------------

def make_sorted(n: int) -> List[int]:
    return list(range(n))

def make_reverse_sorted(n: int) -> List[int]:
    return list(range(n, 0, -1))

def make_random(n: int, seed: int = 42) -> List[int]:
    rng = random.Random(seed)
    return [rng.randint(0, 10**9) for _ in range(n)]

# -----------------------------
# Measuring stuff
# -----------------------------

def measure_time_and_memory(sort_fn: Callable[[List[int]], List[int]], data: List[int]) -> Tuple[float, int]:
    """
    Returns:
      how long it took, and the most memory we used
    
    We use a special tool to watch memory usage while the function runs.
    """
    # Turn on the memory watcher
    tracemalloc.start()

    # Start the stopwatch
    start = time.perf_counter()
    out = sort_fn(data)  # sort on a provided list
    end = time.perf_counter()

    # Just a quick sanity check to make sure it actually sorted it correctly.
    if out != sorted(data):
        raise ValueError(f"{sort_fn.__name__} produced incorrect result!")

    # Check what the memory usage peaked at
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return (end - start), peak

# -----------------------------
# Running the race
# -----------------------------

def run_benchmarks(
    sizes: List[int],
    repeats: int = 3,
    out_csv_path: str = "../results/results.csv"
) -> None:
    """
    Runs the race for Quick Sort and Merge Sort on different kinds of lists.
    Saves the results in a CSV file so we can look at them later.
    """

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
            base_data = make_fn(n)

            for alg_name, alg_fn in algorithms.items():
                for run in range(1, repeats + 1):
                    # IMPORTANT: give it a copy so it doesn't mess up the original list for the next run
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

    # Save all the numbers to a file
    with open(out_csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nSaved results to: {out_csv_path}")

# -----------------------------
# Making pretty charts
# -----------------------------

def summarize_and_plot(
    csv_path: str = "../results/results.csv",
    out_time_plot: str = "../results/time_plot.png",
    out_mem_plot: str = "../results/memory_plot.png"
) -> None:
    """
    Creates:
      - a table printed right here
      - two pictures (plots) of the time and memory usage
    
    Uses matplotlib to draw the pictures.
    """
    import pandas as pd
    import matplotlib.pyplot as plt

    df = pd.read_csv(csv_path)

    # Group the runs together and take the average
    agg = (
        df.groupby(["algorithm", "dataset", "n"], as_index=False)
          .agg(time_sec_mean=("time_sec", "mean"),
               peak_mem_mean=("peak_mem_bytes", "mean"))
    )

    # Save the averaged numbers to a file too, just in case we need them
    agg_out_path = os.path.join(os.path.dirname(csv_path), "results_aggregated.csv")
    agg.to_csv(agg_out_path, index=False)
    print(f"Saved aggregated table to: {agg_out_path}\n")

    # Show a little preview of the data
    print("Aggregated Results (mean over runs):")
    print(agg.head(20).to_string(index=False))

    # -------- Time plot --------
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

    # -------- Memory plot --------
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

# -----------------------------
# Main
# -----------------------------

if __name__ == "__main__":
    # Pick some list sizes. Not too big or it takes forever.
    sizes = [200, 500, 1000, 2000, 5000]

    run_benchmarks(sizes=sizes, repeats=3, out_csv_path="../results/results.csv")
    summarize_and_plot(
        csv_path="../results/results.csv",
        out_time_plot="../results/time_plot.png",
        out_mem_plot="../results/memory_plot.png"
    )
