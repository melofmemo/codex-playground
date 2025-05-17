import os
from datetime import datetime
from zoneinfo import ZoneInfo

def main():
    os.makedirs("results", exist_ok=True)
    now = datetime.now(ZoneInfo("Asia/Seoul"))
    with open(os.path.join("results", "now.txt"), "w") as f:
        f.write(now.isoformat() + "\n")

if __name__ == "__main__":
    main()
