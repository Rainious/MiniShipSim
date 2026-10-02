"""当前实际使用的仿真配置。"""

import math
from dataclasses import dataclass
from pathlib import Path


DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parents[1] / "outputs"


@dataclass
class SimulationConfig:
    dt: float = 0.1
    steps: int = 200

    def __post_init__(self):
        if not math.isfinite(self.dt) or self.dt <= 0:
            raise ValueError("dt 必须是有限的正数")
        if self.steps < 0:
            raise ValueError("steps 不能小于 0")
