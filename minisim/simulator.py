import math
class Simulator:
	def __init__(self, ship, wave = None):
		self.ship = ship
		self.wave = wave
		self.time = 0.0
		self.history = []

	def wave_height_at(self, local_x, local_y):
		s = self.ship.state
		world_x = s.x + local_x * math.cos(s.heading) - local_y * math.sin(s.heading)
		world_y = s.y + local_x * math.sin(s.heading) + local_y * math.cos(s.heading)
		return self.wave.eta(world_x, world_y, self.time)	

	def update_pose(self):
		s = self.ship.state
		if self.wave is None:
			s.z = 0.0
			s.pitch = 0.0
			s.roll = 0.0
			return
		s.z = self.wave_height_at(0, 0)
		#四个采样点：船头2.0, 0 船尾-2.0, 0 左侧0, 0.75 右侧0, -0.75
		porth = self.wave_height_at(0, 0.75)
		starboardh = self.wave_height_at(0, -0.75)
		bowh = self.wave_height_at(2.0, 0)
		sternh = self.wave_height_at(-2.0, 0)

		s.pitch = math.atan2(bowh - sternh, 4.0)
		s.roll = math.atan2(porth - starboardh, 1.5)
		
	def record(self):
		s = self.ship.state
		self.history.append(
			{
				"time": self.time,
				"x": s.x,
				"y": s.y,
				"z": s.z,
				"speed": s.speed,
				"speed_accel": s.speed_accel,
				"heading": s.heading,
				"pitch": s.pitch,
				"roll" : s.roll,
				"turn_rate": s.turn_rate,
				"rudder": s.rudder,
				"target_speed": s.target_speed,
				"target_rudder": s.target_rudder,
			}
		
		)

	def apply_command(self, command):
		self.ship.state.target_rudder = command.target_rudder
		self.ship.state.target_speed = command.target_speed
	
		
	def step(self, dt, command=None):
		if command is not None:
			self.apply_command(command)

		self.ship.step(dt)#使用ship的step方法更新ship的状态
		self.time = self.time + dt
		self.update_pose()
		self.record()
		
	def run(self, dt, steps, command=None):
		if command is not None:
			self.apply_command(command)

		self.update_pose()
		self.record()
		for _ in range(steps):
			self.step(dt, command)