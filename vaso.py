from enum import Enum

class Size(Enum):
    SMALL ='S'
    MEDIUM ='M'
    BIG ='B'

class Vaso(object):

    def __init__(self, id, start_time):
        self.__id = id
        # chamar aqui a funcao que sorteia o size do vaso
        self.__size = Size[size]
        self.__start_time = start_time
        self.__end_time = 0

    # criar aqui a funcao que sorteia o size do vaso
    
    def setId(self, id):
        self.__id = id

    # def setSize(self, size):
    #     self.__size = Size

    def setStartTime(self, start_time):
        self.__start_time = start_time

    def setEndTime(self, end_time):
        self.__end_time = end_time

    def get_id(self):
        return self.__id

    def getSize(self):
        return self.__size

    def getStartTime(self):
        return self.__start_time

    def getEndTime(self):
        return self.__end_time