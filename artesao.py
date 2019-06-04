from enum import Enum

class Artesao(object):

    # id = 0

    def __init__(self, specialist=False, ociosity=True):
        # id += 1
        # self.__id = id
        self.__ociosity = ociosity
        self.__specialist = specialist

    # def setId(self, id):
    #     self.__id = id

    def setOciosity(self, ociosity):
        self.__ociosity = ociosity

    # def getId(self):
    #     return self.__id

    def getOciosity(self):
        return self.__ociosity
    
    def isSpecialist(self):
        return self.__specialist
