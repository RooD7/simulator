from enum import Enum

class Ativ(Enum): 
    CHEGADA_PEDIDO				=  0
    PREPARACAO_FORMA            =  1
    PREPARACAO_BASE             =  2
    ACABAMENTO_INICIAL_BASE     =  3
    SECAGEM_ACABAMENTO_BASE     =  4
    LIMPEZA_ACABAMENTO_BASE     =  5
    SECAGEM_BASE                =  6
    PREPARACAO_BOCA             =  7
    ACABAMENTO_INICIAL_BOCA     =  8
    SECAGEM_ACABAMENTO_BOCA     =  9
    LIMPEZA_ACABAMENTO_BOCA     = 10
    SECAGEM_BOCA                = 11
    IMPERMEABILIZACAO_INTERNA   = 12
    SECAGEM_INTERNA             = 13
    ENVERNIZACAO_GERAL          = 14
    SECAGEM_ENVERNIZACAO        = 15

class Evento(object):

    def __init__(self, id, ativ_event, time_event):
        self.__id_event   = id
        self.__ativ_event = Ativ[ativ_event]
        self.__time_event = time_event

    def set_ativ_event(self, ativ_event):
        self.__ativ_event = ativ_event

    def set_time_event(self, time_event):
        self.__time_event = time_event

    def get_id_event(self):
        return self.__id_event

    def get_ativ_event(self):
        return self.__ativ_event

    def get_time_event(self):
        return self.__time_event