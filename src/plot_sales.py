import os
import csv
import sys

# Ensure local src directory is on path so our minimal matplotlib is found
sys.path.insert(0, os.path.dirname(__file__))
import matplotlib.pyplot as plt  # type: ignore

# Paths
DATA_PATH = os.path.join('data', 'sales.csv')
REPORTS_DIR = 'reports'
IMAGE_FILE = os.path.join(REPORTS_DIR, 'sales.png')
HTML_FILE = os.path.join(REPORTS_DIR, 'report.html')


def read_sales(path):
    dates = []
    sales = []
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            dates.append(row['month'])
            sales.append(float(row['sales']))
    return dates, sales


def main():
    # Read data
    months, values = read_sales(DATA_PATH)

    # Ensure reports directory exists
    os.makedirs(REPORTS_DIR, exist_ok=True)

    # Create bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(values)
    plt.tight_layout()

    # Save plot
    plt.savefig(IMAGE_FILE)
    plt.close()

    # Create HTML report
    with open(HTML_FILE, 'w') as f:
        f.write("<html><body>\n")
        f.write("<h1>Sales Report</h1>\n")
        f.write('<img src="sales.png" alt="Sales chart">\n')
        f.write("</body></html>\n")

    print(f"Report generated: {HTML_FILE}")


if __name__ == '__main__':
    main()
