# -*- coding: utf-8 -*-

"""Controller for a PCA9685 IC which allows to PWM control 16 channels

Implemented according to the data sheet:
https://www.nxp.com/docs/en/data-sheet/PCA9685.pdf
"""

import smbus

class PCA9685:

	CLOCK_FREQ   = 25000000.0
	CYCLE_TICKS  = 4096
      
	REG_MODE1    = 0x00
	REG_LED0     = 0x06 
	REG_PRESCALE = 0xFE
	
	MODE1_SLEEP  = 1 << 4
	
	def __init__(self, busnumber, address):
		self._address = address
		self._bus = smbus.SMBus(busnumber)
		
	def setFrequency(self, freq):
		"""Sets the frequency in Hz between 24 and 1526 Hz"""
		self._frequency = freq
		prescale = round(PCA9685.CLOCK_FREQ / (PCA9685.CYCLE_TICKS * freq)) - 1
		# Frequency can only be changed when in sleep mode
		self.writeMode1(PCA9685.MODE1_SLEEP)
		self._writeByte(PCA9685.REG_PRESCALE, prescale)
		# Disabler sleep mode to activate output
		self.writeMode1(0)

	def setOnOffPosition(self, channel, on, off):
		"""
		Sets the on/off triggers for a given channel
		
		:param channel: index of the channel (0-15)
		:param on: the position in the duty cycle when the LED is switched on (0-4095)
		:param off: the position in the duty cycle when the LED is switched off (0-4095)
		"""
		basereg = PCA9685.REG_LED0 + 4 * channel
		self._writeByte(basereg + 0, on & 0xFF)
		self._writeByte(basereg + 1, on >> 8)
		self._writeByte(basereg + 2, off & 0xFF)
		self._writeByte(basereg + 3, off >> 8)

	def setOnDuration(self, channel, duration):
		"""
		Sets the absolute on duration per cycle
		
		:param channel: index of the channel (0-15)
		:param on: the on-time for every cycle in microseconds
		"""
		off = round((PCA9685.CYCLE_TICKS * duration * self._frequency) /  1000000.0)
		self.setOnOffPosition(channel, 0, off)

	def writeMode1(self, value):
		self._writeByte(PCA9685.REG_MODE1, value)

	def _writeByte(self, reg, value):
		return self._bus.write_byte_data(self._address, reg, value)

