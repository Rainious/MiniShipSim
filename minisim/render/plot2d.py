import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pathlib import Path
import math
from minisim.config import DEFAULT_OUTPUT_DIR


def _finish_plot(output_path, show):
	output_path = Path(output_path)
	output_path.parent.mkdir(parents=True, exist_ok=True)
	try:
		plt.savefig(output_path, dpi=150)
		if show:
			plt.show()
	finally:
		plt.close()

def plot_trajectory(history, output_path=DEFAULT_OUTPUT_DIR / "offline" / "tra.png", show=True):
	xs = []
	ys = []
	
	for item in history:
		xs.append(item["x"])
		ys.append(item["y"])
	
	plt.figure()
	plt.plot(xs, ys, label="trajectory")
	plt.plot(xs[0], ys[0], "go", label="start")
	plt.plot(xs[-1], ys[-1], "ro", label="end")

	plt.xlabel("x")
	plt.ylabel("y")
	plt.title("Ship Trajectory")
	plt.axis("equal")
	plt.grid(True)
	plt.legend()
	_finish_plot(output_path, show)

#TODO:
#command is applied at step start, while state is recorded at step end.
#This can make control signal tansitions appear shifted in plots.
def plot_state_history(history, output_path=DEFAULT_OUTPUT_DIR / "offline" / "state.png", show=True):
	ts = []
	headings = []
	turn_rates = []
	rudders = []
	speeds = []
	speed_accels = []
	target_speeds = []
	target_rudders = []
	
	for item in history:
		ts.append(item["time"])
		headings.append(item["heading"])
		turn_rates.append(item["turn_rate"])
		rudders.append(item["rudder"])
		speeds.append(item["speed"])
		speed_accels.append(item["speed_accel"])
		target_speeds.append(item["target_speed"])
		target_rudders.append(item["target_rudder"])

	plt.figure()
	plt.plot(ts, headings, label="heading")
	plt.plot(ts, turn_rates, label="turn_rate")
	plt.step(ts, rudders, where="post", label="rudder")
	plt.step(ts, speeds, where ="post", label="speed")
	plt.step(ts, speed_accels, where ="post", label="speed_accel")
	plt.step(ts, target_rudders, where="post", label="t_rudder")
	plt.step(ts, target_speeds, where ="post", label="t_speed")

	plt.xlabel("time")
	plt.ylabel("value")
	plt.title("State History")
	plt.grid(True)
	plt.legend()
	_finish_plot(output_path, show)

def plot_compare_trajs(runs, output_path=DEFAULT_OUTPUT_DIR / "compare" / "comparison.png", show=True):
	plt.figure()

	for name, history in runs:
		xs = [item['x'] for item in history]
		ys = [item['y'] for item in history]
		plt.plot(xs, ys, label = name)

	plt.xlabel("x")
	plt.ylabel("y")
	plt.title("Trajectory Comparison")
	plt.axis("equal")
	plt.grid(True)
	plt.legend()
	_finish_plot(output_path, show)

def _draw_hull_frame(axes, vertices, faces, pose=None, wave=None):
	heave = 0.0 if pose is None else pose["z"]
	pitch = 0.0 if pose is None else pose["pitch"]
	roll = 0.0 if pose is None else pose["roll"]

	for f in faces:
		xs = []
		ys = []
		zs = []
		for index in f:
			x, y, z = vertices[index]
			px = x * math.cos(pitch) - z * math.sin(pitch)
			pz = x * math.sin(pitch) + z * math.cos(pitch)
			ry = y * math.cos(roll) - pz * math.sin(roll)
			rz = y * math.sin(roll) + pz * math.cos(roll)
			xs.append(px)
			ys.append(ry)
			zs.append(rz + heave)
		xs.append(xs[0])
		ys.append(ys[0])
		zs.append(zs[0])
		axes[0].plot(xs, zs, color = "black", linewidth = 0.5)
		axes[1].plot(ys, zs, color = "black", linewidth = 0.5)

	xmax = max(vertex[0] for vertex in vertices)
	xmin = min(vertex[0] for vertex in vertices)
	ymax = max(vertex[1] for vertex in vertices)
	ymin = min(vertex[1] for vertex in vertices)

	if pose is not None and wave is not None:
		heading = pose["heading"]
		water_xs_0 = []
		water_zs_0 = []
		water_xs_1 = []
		water_zs_1 = []

		for i in range(41):
			local_x = xmin + (xmax - xmin) * i / 40
			local_y = ymin + (ymax - ymin) * i / 40

			world_x_0 = pose["x"] + local_x * math.cos(heading)
			world_y_0 = pose["y"] + local_x * math.sin(heading)
			world_x_1 = pose["x"] - local_y * math.sin(heading)
			world_y_1 = pose["y"] + local_y * math.cos(heading)

			wheight_0 = wave.eta(world_x_0, world_y_0, pose["time"])
			water_zs_0.append(wheight_0)
			water_xs_0.append(local_x)
			wheight_1 = wave.eta(world_x_1, world_y_1, pose["time"])
			water_zs_1.append(wheight_1)
			water_xs_1.append(local_y)

		axes[0].plot(water_xs_0, water_zs_0, color = 'c', linewidth = 0.4)
		axes[1].plot(water_xs_1, water_zs_1, color = 'c', linewidth = 0.4)

	axes[0].set_title("Side View")
	axes[0].set_xlabel("x (m)")
	axes[0].set_ylabel("z (m)")

	axes[1].set_title("Stern View")
	axes[1].set_xlabel("y (m)")
	axes[1].set_ylabel("z (m)")

	for ax in axes:
		ax.set_aspect("equal", adjustable="box")
		ax.grid(True)


def plot_hull_views(vertices, faces, output_path, show = True, pose = None, wave = None):
	fig, axes = plt.subplots(1, 2, figsize = (10, 4))

	_draw_hull_frame(axes, vertices, faces, pose, wave)

	if pose is not None:
		fig.suptitle(f't = {pose["time"]:.1f} s')

	fig.tight_layout()
	_finish_plot(output_path, show)

def animate_hull_views(vertices, faces, history, wave = None):
	if len(history) < 2:
		raise ValueError("当前记录不足两条")

	fig, axes = plt.subplots(1, 2, figsize = (10, 4))
	interval_ms = (history[1]["time"] - history[0]["time"]) * 1000

	radius = max(math.sqrt(x * x + y * y + z * z) for x, y, z in vertices)
	heaves = [pose["z"] for pose in history]
	margin = 0.2

	horizontal_limit = radius + margin
	zmin = min(heaves) - radius - margin
	zmax = max(heaves) + radius + margin

	def update(frame_index):
		for ax in axes:
			ax.clear()

		pose = history[frame_index]
		_draw_hull_frame(axes, vertices, faces, pose, wave)
		for ax in axes:
			ax.set_xlim(-horizontal_limit, horizontal_limit)
			ax.set_ylim(zmin, zmax)
		fig.suptitle(f't = {pose["time"]:.1f} s')

	animation = FuncAnimation(fig, update, frames = len(history), interval = interval_ms, repeat = False)

	fig.tight_layout()
	plt.show()
