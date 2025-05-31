#implementation of concurrency with threading
from flask import Flask, render_template, request
import threading

app = Flask(__name__)

result = {"sum": 0}

def compute_sum(start, end, result_dict):
    total = 0
    for n in range(start, end + 1):
        total += 1 / (n ** 2)
    result_dict["sum"] = round(total, 6)  # for clean display

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            i = int(request.form['i'])
            j = int(request.form['j'])

            if i <= 0 or j <= 0 or i > j:
                return render_template('index.html', error="Invalid input. Ensure 0 < i ≤ j.")

            thread_result = {}
            t = threading.Thread(target=compute_sum, args=(i, j, thread_result))
            t.start()
            t.join()

            return render_template('index.html', result=thread_result["sum"], i=i, j=j)

        except ValueError:
            return render_template('index.html', error="Please enter valid integers.")

    return render_template('index.html')
if __name__ == "__main__":
    app.run(debug=True)

