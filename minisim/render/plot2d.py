import matplotlib.pyplot as plt

def plot_trajectory(history):
	xs = []
	ys = []
	
	for item in history:
		xs.append(item["x"])
		ys.append(item["y"])
		
	plt.figure()
	plt.plot(xs, ys)
	plt.xlabel("x")
	plt.ylabel("y")
	plt.title("Ship Trajectory")
	plt.axis("equal")
	plt.grid(True)
	plt.savefig("tra.png", dpi=150)
	plt.show()