"""仿真记录和结果的文件保存。"""

import csv
from pathlib import Path


def save_history_csv(history, output_path):
    if not history:
        raise ValueError("没有可保存的记录")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(history[0].keys())
    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(history)
