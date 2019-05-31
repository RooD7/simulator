class Evento(object):

    id = 0

    def __init__(self, name_event, time_event):
        id += 1
        self.id_event   = id
        self.name_event = name_event
        self.time_event = time_event

    def set_name_event(self, name_event):
        self.name_event = name_event

    def set_time_event(self, time_event):
        self.time_event = time_event

    def get_id_event(self):
        return self.id_event

    def get_name_event(self):
        return self.name_event

    def get_time_event(self):
        return self.time_event