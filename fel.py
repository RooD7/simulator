import evento as Evento

class Fel(object):
	def __init__(self):
		self.__fel = []
		self.id = 0

	def insert_fel(self, name_event, time_event):
		self.__fel.append(Evento.Evento(self.id, name_event,time_event))
		self.id += 1
		
	def remove_fel(self):
		return self.__fel.pop(0)

	def get_fel(self):
		return self.__fel