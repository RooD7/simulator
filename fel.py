import evento as Evento

class fel(object):
	def __init__(self):
		self.fel = []

	def insert_fel(self, name_event, time_event):
		self.fel.append(Evento.Evento(name_event,time_event))

	def remove_fel(self):
		return self.fel.pop(0)
		
	def get_fel(self):
		return self.fel