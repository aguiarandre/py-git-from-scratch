import os
import logging


class Workspace(object):
	"""docstring for Workspace"""

	

	def __init__(self, path):
		self.path = path
		self._ignored_files = ['.', '..', '.git', '__pycache__']
	
	def _filter_ignored_files(self, files):
		"""Return a list containing the files except the files in ignored list of files"""
		return filter(lambda item: item not in self._ignored_files, files)

	def list_files(self):
		"""
		Method responsible to list all the files in a directory 
		with the exception of the files '.', '..' and '.git'
		"""	
		files = os.listdir(self.path) 
		filtered_files = self._filter_ignored_files(files)

		return list(filtered_files)

	def read_file(self, path_to_file):
		file = os.path.join(self.path, path_to_file)
		
		with open(file, 'r') as reader:
			content = reader.read()

		return content