from enum import Enum

class Type(Enum):
    SMALL ='S'
    MEDIUM ='M'
    BIG ='B'

class Vaso(object):

    def __init__(self, id, Type, start_time):
        self.__id = id
        self.__Type = Type
        self.__start_time = start_time
        self.__end_time = 0

    def setId(self, id):
        self.__id = id

    def setType(self, type):
        self.__type = type

    def setStartTime(self, start_time):
        self.__start_time = start_time

    def setEndTime(self, end_time):
        self.__end_time = end_time

    def get_id(self):
        return self.__id

    def getType(self):
        return self.__type

    def getStartTime(self):
        return self.__start_time

    def getEndTime(self):
        return self.__end_time