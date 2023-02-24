import io
from flask import Flask, send_file
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import argparse
import numpy as np
import subprocess

app = Flask(__name__)

def parse_opt() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Script to plot data from mpi_label_histo"
    )
    parser.add_argument(
        "--file-path",
        type=str,
        action="store",
        required=True,
        help="File to open with histogram data"
    )
    return parser.parse_args()

def create_plot(file_path):
    with open(file_path) as infile:
        file_data = infile.readlines()
        list_data = file_data[0].split(' ')[:-1]

    np_data = np.array(list_data, dtype=int)
    classes = [ i for i in range(len(np_data)) ]

    fig = Figure()
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)
    ax.bar(classes, np_data)
    ax.set_title("Histogram of classes")
    ax.set_xlabel("Objects of interest (Classes)")
    ax.set_ylabel("Number of occurrences in dataset")
    canvas.draw()
    return fig

@app.route('/')
def plot():
    opt = parse_opt()
    fig = create_plot(opt.file_path)

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return send_file(io.BytesIO(output.getvalue()), mimetype='image/png')

if __name__ == '__main__':
    subprocess.call("ls -al", shell=True)
    app.run(debug=True, host="0.0.0.0")
