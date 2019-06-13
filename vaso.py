from enum import Enum
import numpy as np

class Size(Enum):
    SMALL ='S'
    MEDIUM ='M'
    BIG ='B'

class Vaso(object):

    def __init__(self, id, size, start_time):
        self.__id = id
        # S - M - B
        self.__size = Size(size)
        self.__start_time = start_time
        self.__end_time = 0

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

    # S - M - B
    def get_size(self):
        return self.__size.value

    def getStartTime(self):
        return self.__start_time

    def getEndTime(self):
        return self.__end_time