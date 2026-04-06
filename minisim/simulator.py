class Simulator:
	def __init__(self, ship):
		self.ship = ship
		self.time = 0.0
		self.history = []
		
	def record(self):
		s = self.ship.state
		self.history.append(
			{
				"time": self.time,
				"x": s.x,
				"y": s.y,
				"speed": s.speed,
				"heading": s.heading,
				"turn_rate": s.turn_rate,
				"rudder": s.rudder,
			}
		
		)

	def apply_command(self, command):
		self.ship.state.rudder = command.rudder
		self.ship.state.target_speed = command.target_speed
	
		
	def step(self, dt, command=None):
		if command is not None:
			self.apply_command(command)

		self.ship.step(dt)#使用ship的step方法更新ship的状态
		self.time = self.time + dt
		self.record()
		
	def run(self, dt, steps, command=None):
		if command is not None:
			self.apply_command(command)

		self.record()
		for _ in range(steps):
			self.step(dt, command)