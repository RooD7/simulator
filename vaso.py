from enum import Enum

class Type(Enum):
    SMALL ='S'
    MEDIUM ='M'
    BIG ='B'

class Vaso(object):

    def __init__(self, id, Type, start_time):
        self.id = id
        self.Type = Type
        self.start_time = start_time
        self.end_time = 0

    def setId(self, id):
        self.id = id

    def setType(self, type):
        self.type = type

    def setStartTime(self, start_time):
        self.start_time = start_time

    def setEndTime(self, end_time):
        self.end_time = end_time

    def get_id(self):
        return self.id

    def getType(self):
        return self.type

    def getStartTime(self):
        return self.start_time

    def getEndTime(self):
        return self.end_time