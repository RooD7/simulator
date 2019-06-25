from enum import Enum

class Artesao(object):

    def __init__(self, specialist=False, ociosity=True, id=0):
        self.__id = id
        self.__ociosity = ociosity
        self.__specialist = specialist
        
    def set_id(self, id):
        self.__id = id

    def set_ociosity(self, ociosity):
        self.__id = ociosity

    def get_id(self):
        return self.__id
    
    def get_ociosity(self):
        return self.__ociosity

    def isSpecialist(self):
        return self.__specialist
