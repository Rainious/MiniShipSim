from dataclasses import dataclass

@dataclass
class ControlCommand:
    target_rudder: float = 0.0
    target_speed: float = 0.0