"""保留旧启动方式；推荐使用 python main.py keyboard。"""

import sys
from pathlib import Path

# 支持从任意工作目录直接运行这个旧示例入口。
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from minisim.interactive import main


if __name__ == "__main__":
    main()
