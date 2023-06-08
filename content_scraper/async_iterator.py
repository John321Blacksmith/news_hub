import asyncio



class AsyncIterator:
	def __init__(self, seq):
		self._sequence = seq
		self._index = 0

	def __aiter__(self):
		return self

	# the __next__ asynchronous method
	# is always a coroutine
	async def __anext__(self):
		if self._index < len(self._sequence):
			value = self._sequence[self._index]
			self._index += 1
			return value
		else:
			raise StopAsyncIteration

