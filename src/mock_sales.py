"""Generate random daily sales data for Jan-Mar 2025."""

from pathlib import Path
from datetime import date, timedelta
import csv
import random

def date_range(start: date, end: date):
    """Yield each day between start and end inclusive."""
    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)


def main() -> None:
    """Create a CSV with random daily sales between Jan and Mar 2025."""

    start_day = date(2025, 1, 1)
    end_day = date(2025, 3, 31)

    rows = []
    for day in date_range(start_day, end_day):
        rows.append({"date": day.isoformat(), "sales": random.randint(100, 500)})

    # Ensure the data directory exists
    output_path = Path("data")
    output_path.mkdir(parents=True, exist_ok=True)
    csv_file = output_path / "sales.csv"
    with csv_file.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "sales"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved {len(rows)} records to {csv_file}")

if __name__ == "__main__":
    main()
