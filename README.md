# MiniShipSim

MiniShipSim is a Python ship maneuvering simulation project that starts from a minimal 2D prototype and gradually evolves toward a more modular and expressive simulator.

At its current stage, the project focuses on building a runnable simulation core rather than a physically accurate ship model. It already supports:

- an **offline scripted simulation** with matplotlib plots;
- a **pygame real-time keyboard demo** for interactive steering experiments.

The long-term goal is to keep improving the structure, control flow, and physical modeling step by step, so that this project can gradually grow from a small prototype into a clearer ship maneuvering simulation framework.

---

## Current Status

MiniShipSim is still an early-stage prototype, but the main loop is already working:

- scripted rudder / target-speed inputs can drive offline runs;
- simulation history can be recorded and visualized;
- a real-time pygame demo can steer the ship interactively;
- the project already has a core package structure (`state`, `ship`, `simulator`, `control`, `render`) that can be extended later.

In short: **the project is no longer just a single test script — it is becoming a small simulation project with a usable core loop.**

---

## Implemented Features

### Core State and Simulation
- **Ship state** stored in `ShipState`
  - `x`, `y`
  - `speed`
  - `heading`
  - `turn_rate`
  - `rudder`
  - `target_speed`
- **Simplified ship dynamics** in `Ship.step(...)`
  - speed approaches `target_speed` through a first-order response;
  - turn rate evolves from rudder input with damping;
  - heading is integrated from turn rate;
  - position is integrated from speed and heading.
- **Simulator with history recording**
  - accepts a `ControlCommand` each step;
  - applies control inputs before state update;
  - records simulation history over time.

### Offline Simulation
- **Offline runner** in `main.py`
- **Scripted control inputs** in `minisim/control/scripts.py`
- **Matplotlib output**
  - `tra.png` — trajectory plot
  - `state.png` — state history plot

### Real-Time Demo
- **pygame keyboard demo** in `examples/realtime_keyboard.py`
- Keyboard control of rudder and target speed
- Ship drawn as a triangle
- Live trajectory trail
- HUD showing:
  - current rudder
  - current speed
  - current target speed

---

## Project Structure

```text
MiniShipSim/
├── main.py                         # Offline simulation entry point
├── requirements.txt
├── README.md
├── data/                           # Reserved for future data/config files
├── examples/
│   ├── realtime_keyboard.py        # Pygame real-time demo entry point
│   └── demo_turning.py             # Placeholder
└── minisim/                        # Core package
    ├── __init__.py
    ├── state.py                    # ShipState dataclass
    ├── ship.py                     # Ship dynamics
    ├── simulator.py                # Simulation loop + history recording
    ├── config.py                   # Reserved for future configuration
    ├── control/
    │   ├── __init__.py
    │   ├── command.py              # ControlCommand dataclass
    │   └── scripts.py              # Predefined offline rudder / target-speed scripts
    ├── render/
    │   ├── __init__.py
    │   └── plot2d.py               # Matplotlib plotting helpers
    ├── physics/                    # Placeholder modules
    │   ├── __init__.py
    │   ├── drag.py
    │   ├── propulsion.py
    │   └── steering.py
    └── world/
        ├── __init__.py
        └── environment.py          # Placeholder
```

---

## Installation

Create a virtual environment if you want, then install dependencies:

```bash
pip install -r requirements.txt
```

Current runtime dependencies are intentionally minimal.

> Notes:
> - `pygame` may require additional system packages on some Linux environments.
> - If you only want to run the offline simulation, `matplotlib` is the key dependency.

---

## Run the Offline Simulation

From the repository root:

```bash
python main.py
```

What it currently does:
1. runs a scripted offline simulation;
2. prints recorded state history to the console;
3. generates:
   - `tra.png` — trajectory plot
   - `state.png` — state history plot

At the moment, the default `main.py` setup runs:

- `dt = 0.1`
- `steps = 45`
- `rudder_straight`
- `target_speed_straight`

You can change the selected control scripts in `main.py` to try different offline experiments.

---

## Run the Real-Time Keyboard Demo

From the repository root:

```bash
python examples/realtime_keyboard.py
```

### Keyboard Controls

| Key | Action |
|---|---|
| ← Left | Decrease rudder |
| → Right | Increase rudder |
| ↑ Up | Increase target speed |
| ↓ Down | Decrease target speed |
| No left/right input | Rudder gradually returns toward 0 |

The pygame window currently shows:
- the ship as a triangle,
- its trajectory trail,
- current rudder,
- current speed,
- current target speed.

This mode is currently a lightweight interactive demo rather than a polished simulation UI.

---

## Example Output

The repository root currently contains example output images generated by the offline simulation:

- `tra.png` — trajectory plot
- `state.png` — state history plot

These are **generated runtime outputs**, not source assets.  
Running `main.py` may overwrite them.

---

## Current Model Notes

The current model is intentionally simple:

- `rudder` acts as a control input;
- `target_speed` acts as a commanded speed target;
- `speed` is a simulated response that gradually approaches `target_speed`;
- `turn_rate`, `heading`, `x`, and `y` are evolved step by step from the current state.

This means the project is already moving beyond “directly set speed and position,” but it is still far from a realistic ship dynamics model.

---

## Current Limitations

MiniShipSim is still a prototype. Important limitations at the moment include:

- The physics model is highly simplified and not intended to be physically accurate.
- Command naming for target speed is now unified as `target_speed` across the control path.
- `minisim/physics/`, `minisim/world/`, `minisim/config.py`, and `examples/demo_turning.py` are still placeholders.
- Offline output images are still saved into the repository root.
- In plotting, control application time and recorded state time are not yet fully separated, so command transitions may appear slightly shifted.
- The real-time pygame mode is a demo, not yet a full simulation application.

---

## Roadmap Direction

The project is gradually moving toward:

- clearer separation between command, state, and physics;
- richer offline experiment workflows;
- more complete ship / environment modeling;
- better visualization and control structure;
- a more modular ship maneuvering simulator rather than a single prototype script.

This roadmap is directional, not a claim that all of these features already exist.

---

## License

No license file is included yet.

If this repository is intended to stay public, adding a license such as **MIT** would make reuse and collaboration much clearer.

---

## Suggested GitHub About

**Description**  
A Python ship maneuvering simulation project, evolving from a minimal 2D prototype toward a more modular and expressive simulator.

**Topics**  
`python`, `simulation`, `ship`, `maneuvering`, `2d`, `pygame`, `matplotlib`, `control`