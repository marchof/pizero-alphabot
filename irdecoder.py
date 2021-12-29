
_TOLERANCE = 0.2

class _UnexpectedPulse(Exception):
	pass

class _Pulse(object):

	def __init__(self, durationms):
		duration = durationms / 1000.0
		delta = duration * _TOLERANCE
		self.durationmin = duration - delta
		self.durationmax = duration + delta
		
	def matches(self, actual):
		return actual >= self.durationmin and actual <= self.durationmax
		
	def expect(self, actual):
		if not self.matches(actual):
			raise _UnexpectedPulse()

_LEADING1 = _Pulse(9.0000)
_LEADING2 = _Pulse(4.5000)
_SPACE    = _Pulse(0.5625)
_BIT0     = _Pulse(0.5625)
_BIT1     = _Pulse(1.6875)


class IRDecoder(object):

	def __init__(self):
		self._state = self._protocol()
		self._state.send(None)
		
	def pulse(self, duration):
		self._state.send(duration)

	def _readbit(self):
		_SPACE.expect((yield))
		duration = (yield)
		if _BIT0.matches(duration):
			return 0
		if _BIT1.matches(duration):
			return 1
		raise _UnexpectedPulse()

	def _readbyte(self):
		value = 0
		for _ in range(0, 8):
			value = (value << 1) | (yield from self._readbit())
		return value

	def _readbyte_with_complement(self):
		value = (yield from self._readbyte())
		complement = (yield from self._readbyte())
		if value ^ complement != 0xff:
			raise _UnexpectedPulse()	
		return value

	def _protocol(self):
		while True:
			try:
				_LEADING1.expect((yield))
				_LEADING2.expect((yield))
				address = (yield from self._readbyte_with_complement())
				command = (yield from self._readbyte_with_complement())
				_SPACE.expect((yield))
				
				print("address %s, command %s" % (address, command))

						
			except _UnexpectedPulse as err:
				pass

