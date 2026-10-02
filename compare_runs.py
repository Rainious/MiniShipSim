"""保留旧启动方式；推荐使用 python main.py compare。"""

import sys

from main import main as run_app


def main():
    run_app(["compare", *sys.argv[1:]])


if __name__ == "__main__":
    main()
