class Blob(object):
	"""docstring for Blob"""
	def __init__(self, data):
		self.data = data
		self.object_id = None
	
	@property
	def type(self):
		return "blob"

	@property
	def to_s(self):
		return self.data