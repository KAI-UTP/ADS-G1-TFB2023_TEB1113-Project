import time
import subprocess
import sys

def measure_execution_time():
    """
    Measure the execution time of baseline.py with automated input
    """
    print("="*60)
    print("  BASELINE.PY EXECUTION TIME BENCHMARK")
    print("="*60 + "\n")
    
    # Automated input sequence:
    # - Queue capacity: 5
    # - Add 3 patients
    # - Serve 1 patient
    # - Display queue
    # - Exit (9)
    automated_input = """5
1
John
101
3
1
Sarah
102
4
1
Mike
103
2
2
7
9
"""
    
    print("Running baseline.py with automated input...")
    print("- Queue capacity: 5")
    print("- Adding 3 patients")
    print("- Serving 1 patient")
    print("- Displaying queue")
    print("- Exiting\n")
    
    # Start timing
    start_time = time.perf_counter()
    
    try:
        # Run baseline.py as a subprocess with automated input
        result = subprocess.run(
            [sys.executable, "baseline.py"],
            input=automated_input,
            capture_output=True,
            text=True,
            timeout=30  # 30 second timeout
        )
        
        # End timing
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        
        print("="*60)
        print(f"✓ Execution completed successfully!\n")
        print(f"Execution Time: {elapsed_time:.4f} seconds")
        print(f"Execution Time: {elapsed_time*1000:.2f} milliseconds")
        
        if elapsed_time > 60:
            minutes = int(elapsed_time // 60)
            seconds = elapsed_time % 60
            print(f"Execution Time: {minutes}m {seconds:.2f}s")
        
        print(f"\nReturn code: {result.returncode}")
        
        if result.stdout:
            print(f"\n--- PROGRAM OUTPUT ---\n{result.stdout}")
        if result.stderr:
            print(f"\n--- ERRORS ---\n{result.stderr}")
        
    except subprocess.TimeoutExpired:
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(f"✗ Execution timed out after {elapsed_time:.2f} seconds")
    except Exception as e:
        print(f"✗ Error running baseline.py: {e}")

if __name__ == "__main__":
    measure_execution_time()
