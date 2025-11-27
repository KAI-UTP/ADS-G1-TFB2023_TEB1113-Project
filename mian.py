import os
import sys


def run_baseline() -> None:
    cmd = f'"{sys.executable}" baseline.py'
    os.system(cmd)


def run_optimized() -> None:
    cmd = f'"{sys.executable}" optimized.py'
    os.system(cmd)


def run_time_test() -> None:
    cmd = f'"{sys.executable}" time_test.py'
    os.system(cmd)


def run_benchmark_combine() -> None:
    """
    Runs benchmark_combine.py, which tests enqueue and dequeue
    separately for both baseline and optimized systems.
    """
    cmd = f'"{sys.executable}" benchmark_combine.py'
    os.system(cmd)


def main() -> None:
    while True:
        print("\n=== Hospital Triage System Launcher ===")
        print(" 1. Run Baseline FCFS demo")
        print(" 2. Run Optimized Priority Queue demo")
        print(" 3. Run Simple Benchmark (time_test.py)")
        print(" 4. Run Combined Benchmark (benchmark_combine.py)")
        print(" 5. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            run_baseline()
        elif choice == "2":
            run_optimized()
        elif choice == "3":
            run_time_test()
        elif choice == "4":
            run_benchmark_combine()
        elif choice == "5":
            print("Exiting launcher.")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()
