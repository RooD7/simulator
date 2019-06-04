import evento as Evento

class Fel(object):
	def __init__(self):
		self.__fel = []

	def insert_fel(self, name_event, time_event):
		self.__fel.append(Evento.Evento(name_event,time_event))

	def remove_fel(self):
		return self.__fel.pop(0)

	def get_fel(self):
		return self.__fel