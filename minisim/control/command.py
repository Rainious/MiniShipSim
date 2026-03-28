from dataclasses import dataclass

@dataclass
class ControlCommand:
    rudder: float = 0.0
    speed: float = 0.0