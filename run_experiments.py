import time
import random
import statistics
import matplotlib.pyplot as plt
import argparse


def bubble_sort(arr):
    n = len(arr)
    A = arr.copy()
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if A[j] > A[j + 1]:
                A[j], A[j + 1] = A[j + 1], A[j]
                swapped = True
        if not swapped:
            break
    return A


def insertion_sort(arr):
    A = arr.copy()
    for i in range(1, len(A)):
        key = A[i]
        j = i - 1
        while j >= 0 and key < A[j]:
            A[j + 1] = A[j]
            j -= 1
        A[j + 1] = key
    return A


def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    A = arr.copy()
    _quick_sort_inplace(A, 0, len(A) - 1)
    return A


def _quick_sort_inplace(arr, low, high):
    if low < high:
        pi = _partition(arr, low, high)
        _quick_sort_inplace(arr, low, pi - 1)
        _quick_sort_inplace(arr, pi + 1, high)


def _partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def selection_sort(arr):
    A = arr.copy()
    n = len(A)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if A[j] < A[min_idx]:
                min_idx = j
        A[i], A[min_idx] = A[min_idx], A[i]
    return A


def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    A = arr.copy()
    _merge_sort_inplace(A, 0, len(A) - 1)
    return A

def _merge_sort_inplace(arr, l, r):
    if l < r:
        m = l + (r - l) // 2
        _merge_sort_inplace(arr, l, m)
        _merge_sort_inplace(arr, m + 1, r)
        _merge(arr, l, m, r)

def _merge(arr, l, m, r):
    n1 = m - l + 1
    n2 = r - m
    L = arr[l:m+1]
    R = arr[m+1:r+1]
    i = 0
    j = 0
    k = l
    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1
    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1


def run_experiment(algorithms, sizes, num_trials, experiment_type='random', noise_percent=0, filename='result1.png', title='Runtime Comparison'):
    results_mean = {name: [] for name in algorithms}
    results_std = {name: [] for name in algorithms}

    print(f"Starting {title} (this might take a minute or two)...")

    for size in sizes:
        print(f"Testing array size: {size}")
        times = {name: [] for name in algorithms}

        for trial in range(num_trials):
            if experiment_type == 'random':
                arr = [random.randint(0, 100000) for _ in range(size)]
            elif experiment_type == 'nearly_sorted':
                arr = list(range(1, size + 1))
                num_swaps = int(size * (noise_percent / 100.0) / 2)
                for _ in range(num_swaps):
                    i, j = random.randint(0, size - 1), random.randint(0, size - 1)
                    arr[i], arr[j] = arr[j], arr[i]

            for name, func in algorithms.items():
                start_time = time.time()
                func(arr)
                end_time = time.time()
                times[name].append(end_time - start_time)

        for name in algorithms:
            mean_time = statistics.mean(times[name])
            std_time = statistics.stdev(times[name]) if num_trials > 1 else 0.0
            results_mean[name].append(mean_time)
            results_std[name].append(std_time)

    plt.figure(figsize=(10, 6))

    for name in algorithms:
        mean_times = results_mean[name]
        std_times = results_std[name]

        plt.plot(sizes, mean_times, marker='o', label=name)

        lower_bound = [max(0, m - s) for m, s in zip(mean_times, std_times)]
        upper_bound = [m + s for m, s in zip(mean_times, std_times)]
        plt.fill_between(sizes, lower_bound, upper_bound, alpha=0.2)

    plt.title(title)
    plt.xlabel('Array size (n)')
    plt.ylabel('Runtime (seconds)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)

    plt.savefig(filename)
    print(f"Experiment finished. Results saved to {filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Sorting Algorithms Experiments")
    parser.add_argument("-a", "--algorithms", type=int, nargs='+', help="Algorithms to compare (1=Bubble, 2=Selection, 3=Insertion, 4=Merge, 5=Quick)")
    parser.add_argument("-s", "--sizes", type=int, nargs='+', help="Array sizes")
    parser.add_argument("-e", "--experiment", type=int, help="Experiment type (1=Nearly sorted 5% noise, 2=Nearly sorted 20% noise)")
    parser.add_argument("-r", "--repetitions", type=int, help="Number of repetitions")
    
    args = parser.parse_args()

    ALL_ALGORITHMS = {
        1: ("Bubble Sort", bubble_sort),
        2: ("Selection Sort", selection_sort),
        3: ("Insertion Sort", insertion_sort),
        4: ("Merge Sort", merge_sort),
        5: ("Quick Sort", quick_sort)
    }

    if any([args.algorithms, args.sizes, args.experiment is not None, args.repetitions]):
        # Run CLI mode
        algos_to_run = {}
        if args.algorithms:
            for a_id in args.algorithms:
                if a_id in ALL_ALGORITHMS:
                    name, func = ALL_ALGORITHMS[a_id]
                    algos_to_run[name] = func
        else:
            algos_to_run = {name: func for name, func in ALL_ALGORITHMS.values()}
            
        sizes = args.sizes if args.sizes else [100, 500, 1000]
        num_trials = args.repetitions if args.repetitions else 5
        
        experiment_type = 'random'
        noise_percent = 0
        title = 'Runtime Comparison (Custom CLI)'
        filename = 'result_cli.png'
        
        if args.experiment == 1:
            experiment_type = 'nearly_sorted'
            noise_percent = 5
            title = 'Runtime Comparison (5% Noise)'
            filename = 'result_cli_5_noise.png'
        elif args.experiment == 2:
            experiment_type = 'nearly_sorted'
            noise_percent = 20
            title = 'Runtime Comparison (20% Noise)'
            filename = 'result_cli_20_noise.png'
            
        print("\n--- Running Custom CLI Experiment ---")
        run_experiment(algos_to_run, sizes, num_trials, experiment_type=experiment_type, noise_percent=noise_percent, filename=filename, title=title)
        
    else:
        # Default homework behavior if no arguments provided
        default_algorithms = {
            "Bubble Sort": bubble_sort,
            "Insertion Sort": insertion_sort,
            "Quick Sort": quick_sort
        }
        default_sizes = [100, 500, 1000, 1500, 2000, 2500, 3000]
        
        print("--- Part A & B: Random Arrays ---")
        run_experiment(default_algorithms, default_sizes, 5, experiment_type='random', filename='result1.png', title='Runtime Comparison (Random Arrays)')
        
        print("\n--- Part C: Nearly Sorted Arrays (20% Noise) ---")
        run_experiment(default_algorithms, default_sizes, 5, experiment_type='nearly_sorted', noise_percent=20, filename='result2.png', title='Runtime Comparison (20% Noise)')

