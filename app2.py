#implementing concurrency with parallelism
from flask import Flask, render_template, request
import threading
from multiprocessing import Pool, Manager
import time
import math

app = Flask(__name__)

# Function to be run in parallel processes
def partial_sum(start, end):
    total = 0
    for n in range(start, end + 1):
        total += 1 / (n ** 2)
    return total

# Threaded logger (just for effect)
def log_progress():
    for i in range(3):
        print(f"[Logger Thread] Working... ({i+1})")
        time.sleep(1)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            i = int(request.form['i'])
            j = int(request.form['j'])

            if i <= 0 or j <= 0 or i > j:
                return render_template('index.html', error="Invalid input. Ensure 0 < i ≤ j.")

            # Start logging thread
            logger_thread = threading.Thread(target=log_progress)
            logger_thread.start()

            # Split into chunks for parallel processing
            num_chunks = 4
            chunk_size = math.ceil((j - i + 1) / num_chunks)
            ranges = [(i + k * chunk_size, min(i + (k + 1) * chunk_size - 1, j)) for k in range(num_chunks)]

            # Run chunks in parallel
            with Pool(processes=num_chunks) as pool:
                results = pool.starmap(partial_sum, ranges)

            total_sum = round(sum(results), 6)

            logger_thread.join()

            return render_template('index.html', result=total_sum, i=i, j=j)

        except ValueError:
            return render_template('index.html', error="Please enter valid integers.")

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
