import threading
import time
import subprocess

# Use absolute paths
file1 = r"C:\Users\Ansar\eclipse-workspace\crypto_api\src\kline_data_getter_update_maybe.py"
file3 = r"C:\Users\Ansar\eclipse-workspace\crypto_api\src\kline_data_getter_update_maybe2.py"
file2 = r"C:\Users\Ansar\eclipse-workspace\crypto_api\src\graph_only_kraken.py"
file4 = r"C:\Users\Ansar\eclipse-workspace\crypto_api\src\graph_only_kraken2.py"

FILE = r"C:\Users\Ansar\eclipse-workspace\crypto_api\src\THIS_IS_REAL_ONLY_UPDATED_LATEST.py"

def run_file1():
    subprocess.run(["python", file1])

def run_file2():
    time.sleep(1)  # Wait 1 second before running file2
    subprocess.run(["python", file2])

def run_file3():
    subprocess.run(["python", file3])

def run_file4():
    time.sleep(1)  # Wait 1 second before running file4
    subprocess.run(["python", file4])

def run_FILE_with_retry():
    while True:
        try:
            time.sleep(1)  # Optional delay before starting
            subprocess.run(["python", FILE])
            break  # Exit the loop if it completes successfully
        except Exception as e:
            print(f"Error in threadF: {e}. Restarting...")

# Create threads for each file
thread1 = threading.Thread(target=run_file1)
# thread3 = threading.Thread(target=run_file3)
# thread2 = threading.Thread(target=run_file2)
# thread4 = threading.Thread(target=run_file4)

threadF = threading.Thread(target=run_FILE_with_retry)

# Start the threads
thread1.start()
threadF.start()
# thread3.start()
# thread2.start()
# thread4.start()

# Wait for all threads to complete
thread1.join()
threadF.join()
# thread3.join()
# thread2.join()
# thread4.join()
