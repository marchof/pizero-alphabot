from typing import NamedTuple
import time
from RPi import GPIO

from irdecoder import IRDecoder


class IOWiring(object):
	"""Functional mapping of the IO ports"""	
	
	class WheelWiring(NamedTuple):
		forward: int
		reverse: int
		speed: int
		frequency: int

	def __init__(self):
		# general
		self.pinmode = GPIO.BCM 

		# wheels
		self.leftWheel = IOWiring.WheelWiring(13, 12, 6, 500)
		self.rightWheel = IOWiring.WheelWiring(21, 20, 26, 500)
		
		# IR sensor
		self.ir = 17


class AlphaBot(object):
	"""All sensors and actors of the AlphaBot2"""

	class Wheel(object):
		"""Controller for a single wheel"""
	
		def __init__(self, wiring):
			self.wiring = wiring
			GPIO.setup((wiring.forward, wiring.reverse, wiring.speed), GPIO.OUT)
			GPIO.output((wiring.forward, wiring.reverse, wiring.speed), GPIO.LOW)
			self.pwm = GPIO.PWM(wiring.speed, wiring.frequency)
		
		def spin(self, speed):
			directions = [GPIO.HIGH, GPIO.LOW]
			if speed < 0: directions.reverse()
			GPIO.output((self.wiring.forward, self.wiring.reverse), directions)
			self.pwm.start(abs(speed))

	def __init__(self, iowiring = IOWiring()):
		self.iowiring = iowiring
		
		GPIO.setmode(iowiring.pinmode)
		GPIO.setwarnings(False)

		self.leftWheel  = AlphaBot.Wheel(iowiring.leftWheel)		
		self.rightWheel = AlphaBot.Wheel(iowiring.rightWheel)		

