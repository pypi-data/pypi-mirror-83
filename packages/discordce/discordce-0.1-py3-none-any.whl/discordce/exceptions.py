class CacheNotFound(Exception):
	def __init__(self, message):
		print(message)
		super().__init__(message)