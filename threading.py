import threading

# Example function that simulates processing a value.
def generate_response(value):
    # Replace with your actual logic.
    return f"Processed {value}"

# Function that uses the results after all threads have finished.
def finalize(results):
    print("All threads have finished. Final results:")
    for result in results:
        print(result)

def main():
    # List of values to process.
    values = [1, 2, 3, 4, 5]

    # This list will collect the results.
    results = []
    
    # A lock to ensure that appending to results is thread-safe.
    results_lock = threading.Lock()
    
    # List to keep track of threads.
    threads = []
    
    # Worker function that each thread will execute.
    def worker(value):
        response = generate_response(value)
        with results_lock:
            results.append(response)
    
    # Create and start a thread for each value.
    for value in values:
        thread = threading.Thread(target=worker, args=(value,))
        thread.start()
        threads.append(thread)
    
    # Wait for all threads to complete.
    for thread in threads:
        thread.join()
    
    # Once all threads are done, call the finalize function.
    finalize(results)

if __name__ == '__main__':
    main()
