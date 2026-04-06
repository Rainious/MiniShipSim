import math
from minisim.state import ShipState

class Ship:
    
    def __init__(self):
        self.state = ShipState()
        
        
    def speed_cal(self, dt):
        k = 0.3
        speed_dot = k * (self.state.target_speed - self.state.speed)
        self.state.speed = self.state.speed + dt * speed_dot
        
        
    def heading_cal(self, dt):
        turn_accel = 1.5 * self.state.rudder - 0.8 * self.state.turn_rate
        self.state.turn_rate = self.state.turn_rate + dt * turn_accel
        self.state.heading = self.state.heading + dt * self.state.turn_rate
        
        
    def pos_cal(self, dt):
        vx = self.state.speed * math.cos(self.state.heading)
        vy = self.state.speed * math.sin(self.state.heading)

        self.state.x = self.state.x + dt * vx
        self.state.y = self.state.y + dt * vy
        

    def step(self, dt):
        
        self.speed_cal(dt)
        self.heading_cal(dt)
        self.pos_cal(dt)


        