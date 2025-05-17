import pandas as pd
from pathlib import Path

DATA_FILE = Path('data') / 'sales.csv'
RESULTS_DIR = Path('results')
OUTPUT_FILE = RESULTS_DIR / 'sales_summary.txt'


def main() -> None:
    # Load the CSV data using pandas
    df = pd.read_csv(DATA_FILE)

    # Calculate basic statistics
    total_sales = df['sales'].sum()
    mean_sales = df['sales'].mean()
    max_sales = df['sales'].max()
    min_sales = df['sales'].min()

    summary_lines = [
        f'Total sales: {total_sales}',
        f'Mean sales: {mean_sales}',
        f'Max sales: {max_sales}',
        f'Min sales: {min_sales}',
    ]

    # Ensure the results directory exists
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    # Write summary to file
    OUTPUT_FILE.write_text('\n'.join(summary_lines) + '\n')

    # Also print summary to stdout
    for line in summary_lines:
        print(line)


if __name__ == '__main__':
    main()
