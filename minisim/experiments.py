"""组织实验：运行、统计、保存与显示。"""

from pathlib import Path
import math

from minisim.config import DEFAULT_OUTPUT_DIR
from minisim.control.command import ControlCommand
from minisim.control.scripts import (
    rudder_s_turn,
    rudder_straight,
    speed_ramp,
    target_speed_straight,
)
from minisim.metrics import summary
from minisim.ship import Ship
from minisim.simulator import Simulator
from minisim.storage import save_history_csv
from minisim.world.environment import waveField


def run_offline_sim(dt, steps, target_rudder_script, target_speed_script):
    """共享的离线运行函数；每次创建一艘新船。"""
    ship = Ship()
    command = ControlCommand()
    wave = waveField(
        amplitude=0.15,
        wavelength=8.0,
        speed=1.0,
        direction=math.pi / 4,
    )
    sim = Simulator(ship, wave)
    sim.update_pose()
    sim.record()

    for i in range(steps):
        command.target_rudder = target_rudder_script(i)
        command.target_speed = target_speed_script(i)
        sim.step(dt, command)

    return sim


def print_summary(result, name):
    print(f"[{name}]")
    print(f"total distance = {result['total_distance']:.3f}")
    print(f"total time = {result['total_time']:.3f}")
    print(f"average speed = {result['average_speed']:.3f}")


def run_experiment(config, target_rudder_script=rudder_s_turn,
                   target_speed_script=target_speed_straight,
                   output_dir=None, show=True, verbose=False):
    from minisim.render.plot2d import plot_state_history, plot_trajectory

    if output_dir is None:
        output_dir = DEFAULT_OUTPUT_DIR / "offline"
    output_dir = Path(output_dir)

    sim = run_offline_sim(config.dt, config.steps,
                          target_rudder_script, target_speed_script)
    result = summary(sim.history)
    save_history_csv(sim.history, output_dir / "simulation_history.csv")
    save_history_csv([result], output_dir / "run_summary.csv")
    print_summary(result, "offline")

    if verbose:
        for item in sim.history:
            print(item)

    plot_trajectory(sim.history, output_dir / "tra.png", show=show)
    plot_state_history(sim.history, output_dir / "state.png", show=show)
    return sim


def compare_experiments(config, cases=None, output_dir=None, show=True):
    from minisim.render.plot2d import plot_compare_trajs

    if cases is None:
        cases = [
            ("straight", rudder_straight, target_speed_straight),
            ("s_turn", rudder_s_turn, speed_ramp),
        ]
    if not cases:
        raise ValueError("至少需要一个实验方案")
    if output_dir is None:
        output_dir = DEFAULT_OUTPUT_DIR / "compare"
    output_dir = Path(output_dir)

    summaries = []
    runs = []
    for name, rudder_script, speed_script in cases:
        sim = run_offline_sim(config.dt, config.steps,
                              rudder_script, speed_script)
        runs.append((name, sim.history))
        result = summary(sim.history)
        result["case"] = name
        summaries.append(result)
        print_summary(result, name)

    save_history_csv(summaries, output_dir / "comparison.csv")
    plot_compare_trajs(runs, output_dir / "comparison.png", show=show)
    return runs, summaries
