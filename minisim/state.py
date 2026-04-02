from dataclasses import dataclass

@dataclass
class ShipState:
    x: float = 0.0
    y: float = 0.0
    speed: float = 0.0
    heading: float = 0.0
    turn_rate: float = 0.0
    rudder: float = 0.0
    target_speed: float = 0.0