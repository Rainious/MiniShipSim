from minisim.ship import Ship
from minisim.simulator import Simulator
from minisim.render.plot2d import plot_trajectory
from minisim.render.plot2d import plot_state_history
from minisim.control.command import ControlCommand

import math

def main():
    ship = Ship()

    ship.state.speed = 2.0
    
    command = ControlCommand()
    
    
    sim = Simulator(ship)
    
    for i in range(30):
        if i < 10:
            command.rudder = 0
        else:
            command.rudder = 0.5
        sim.step(0.1, command)

    for item in sim.history:
        print(f"time = {item['time']:.1f}")
        print(f"x = {item['x']:.3f}")
        print(f"y = {item['y']:.3f}")
        print(f"heading = {item['heading']:.3f}")
        print(f"turn_rate = {item['turn_rate']:.3f}")
        print()
        
    plot_trajectory(sim.history)
    plot_state_history(sim.history)



if __name__ == "__main__":
    main()