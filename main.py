from minisim.ship import Ship
from minisim.simulator import Simulator
from minisim.render.plot2d import plot_trajectory, plot_state_history
from minisim.control.command import ControlCommand
from minisim.control.scripts import rudder_step_script, speed_step_script, rudder_s_turn_script, rudder_straight, target_speed_straight

def run_offline_sim(dt, steps, rudder_script, speed_script):
    
    ship = Ship()

    command = ControlCommand()
    
    sim = Simulator(ship)
    
    sim.record()
    
    for i in range(steps):
        command.rudder = rudder_script(i)
        command.t_speed = speed_script(i)
        sim.step(dt, command)
        
    return sim
        
        
def show_results(sim):
    
    for item in sim.history:
        print(f"time = {item['time']:.1f}")
        print(f"x = {item['x']:.3f}")
        print(f"y = {item['y']:.3f}")
        print(f"heading = {item['heading']:.3f}")
        print(f"turn_rate = {item['turn_rate']:.3f}")
        print(f"rudder = {item['rudder']:.3f}")
        print(f"speed = {item['speed']:.3f}")
        print()
        
    plot_trajectory(sim.history)
    plot_state_history(sim.history)
    



def main():
    

    dt = 0.1
    steps = 45
    
    sim = run_offline_sim(dt, steps, rudder_straight, target_speed_straight)
    
    show_results(sim)
    
    





if __name__ == "__main__":
    main()