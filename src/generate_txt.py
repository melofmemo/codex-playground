import os
from datetime import datetime

def main():
    os.makedirs("results", exist_ok=True)
    with open(os.path.join("results", "now.txt"), "w") as f:
        f.write(datetime.now().isoformat() + "\n")

if __name__ == "__main__":
    main()
