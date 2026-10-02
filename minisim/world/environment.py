import math

class waveField:

    def __init__(self, amplitude, wavelength, speed, direction):
        self.amplitude = amplitude
        self.wavelength = wavelength
        self.speed = speed
        self.direction = direction


    def eta(self, x, y, time):
        k = 2 * math.pi / self.wavelength
        along = x * math.cos(self.direction) + y * math.sin(self.direction)
        height = self.amplitude * math.sin(k * (along - self.speed * time)) #y = A sin ( x + speed * t ) 
        return height; 