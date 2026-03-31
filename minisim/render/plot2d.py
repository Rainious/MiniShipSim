import matplotlib.pyplot as plt

def plot_trajectory(history):
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
	plt.savefig("tra.png", dpi=150)
	plt.show()
	plt.close

#TODO:
#command is applied at step start, while state is recorded at step end.
#This can make control signal tansitions appear shifted in plots.
def plot_state_history(history):
	ts = []
	headings = []
	turn_rates = []
	rudders = []
	speeds = []
	
	for item in history:
		ts.append(item["time"])
		headings.append(item["heading"])
		turn_rates.append(item["turn_rate"])
		rudders.append(item["rudder"])
		speeds.append(item["speed"])

	plt.figure()
	plt.plot(ts, headings, label="heading")
	plt.plot(ts, turn_rates, label="turn_rate")
	plt.step(ts, rudders, where="post", label="rudder")
	plt.step(ts, speeds, where ="post", label="speed")

	plt.xlabel("time")
	plt.ylabel("value")
	plt.title("State History")
	plt.grid(True)
	plt.legend()
	plt.savefig("state.png", dpi=150)
	plt.show()
	plt.close()