""""""

__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2016, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


class Command(object):
	pass


class CommandLoop(object):
	""""""

	def __init__(self):
		self.options = None
		self.default = None
		self.option = None
		self.message = None

	def is_option(self):
		if not self.option:
			return False
		if self.option not in self.options:
			return False

	def get_option(self):
		self.option = rs.GetString(self.message, self.default, self.options)

	def handle_option(self):
		self.handlers[self.option]()

	def loop(self):
		while True:
			self.get_option()
			if not self.is_option():
				return
			self.handle_option()


