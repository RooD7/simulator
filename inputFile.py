import os
import re

class InputFile(object):
	def __init__(self):
		self.lines = []

	def inputs(self, patchFile):
		if os.path.isfile(patchFile):
			file = open(patchFile,'r')
			# for l in file:
			# 	print(l)
			self.param = file.readlines()
			# print(self.param)
			file.close()
			
		else:
			self.param = None		
			print('Arquivo informado não existe!')	
			exit()

		return self.param