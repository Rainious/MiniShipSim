import math
from minisim.state import ShipState

class Ship:
    def __init__(self):
        self.state = ShipState()

    def step(self , dt):
        self.state.heading = self.state.heading + dt * self.state.turn_rate

        vx = self.state.speed * math.cos(self.state.heading)
        vy = self.state.speed * math.sin(self.state.heading)

        self.state.x = self.state.x + dt * vx
        self.state.y = self.state.y + dt * vy