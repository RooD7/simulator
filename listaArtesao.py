from enum import Enum
import artesao as Artesao

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
    PREPARACAO_MASSA            = 16
    PREPARACAO_PEDRA            = 17
    OCIOSO                      = 18

class ListaArtesao(object):
    def __init__(self):
        self.__lista = []
        self.id = 1

    def insert_new_artesao(self, ativ_event='OCIOSO', specialist=False, ociosity=True, time=0):
        self.__lista.append([Ativ[ativ_event], Artesao.Artesao(specialist, ociosity, id), time])
        self.id += 1

    def insert_artesao(self, ativ_event, artesao, time):
        self.__lista.append([ativ_event, artesao, time])

    def get_lista(self):
        return self.__lista

    def remove_artesao(self, id):
        for v in self.__lista:
            if v[1].get_id() == id:
                x = v[1]
                self.__lista.remove(v)
                return x
        return None

    def search_artesao(self, id):
        for v in self.__lista:
            if v[1].get_id() == id:
                return True
        return False

    def have_specialist(self, ativ_event):
        for x in self.__lista:
            if (x[1].isSpecialist()  and 
                x[0].name == 'OCIOSO'):
                return True
        return False

    def aloca_specialist(self, ativ_event, time=0):
        for x in self.__lista:
            if (x[1].isSpecialist() and x[1].get_ociosity()):
                x[0] = Ativ[ativ_event]
                x[1].set_ociosity(False)
                x[2] = time
                return x[1]
        return None

    def time_specialist(self, ativ_event, time):
        for x in self.__lista:
            if (x[0].name == ativ_event and
                x[1].isSpecialist() and
                x[2] == 0):
                x[1].set_ociosity(False)
                x[2] = time
                return x[1]
        return None

    def have_artisan(self, ativ_event):
        for x in self.__lista:
            if (not x[1].isSpecialist()  and 
                x[0].name == 'OCIOSO'):
                return True
        return False

    def aloca_artisan(self, ativ_event, time=0):
        for x in self.__lista:
            if (not x[1].isSpecialist() and x[1].get_ociosity()):
                x[0] = Ativ[ativ_event]
                x[1].set_ociosity(False)
                x[2] = time
                return x[1]
        return None

    def time_artisan(self, ativ_event, time):
        for x in self.__lista:
            if (x[0].name == ativ_event and
                not x[1].isSpecialist() and
                x[2] == 0):
                x[1].set_ociosity(False)
                x[2] = time
                return x[1]
        return None
    
    def get_artisan(self, ativ_event):
        for x in self.__lista:
            if x[0] == Ativ[ativ_event]:
                return x[1]
        return None

    def libera_artisan(self, id):
        for x in self.__lista:
            if (x[1].get_id() == id):
                x[0] = Ativ['OCIOSO']
                x[1].set_ociosity(True)
                x[2] = 0
    
    def alocados(self, time):
        for x in self.__lista:
            if (x[2] <= time):
                x[0] = Ativ['OCIOSO']
                x[1].set_ociosity(True)
                x[2] = 0

    def show(self):
        print('--- Artesoes ---')
        for v in self.__lista:
            print('AT: '+str(v[0].name)+' - ID: '+str(v[1].get_id())+' - OCIO: '+
                    str(v[1].get_ociosity())+' - SPEC: '+
                    str(v[1].isSpecialist())+' - TIME: '+str(v[2]))