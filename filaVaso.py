from enum import Enum
import vaso as Vaso

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

class FilaVaso(object):
	def __init__(self):
		self.__fila = []
		self.id = 0

	def insert_vaso(self, name, size, time_event):
		self.__fila.append((Ativ[name],Vaso.Vaso(self.id, size, time_event)))
		self.id += 1

	def get_fila(self):
		return self.__fila

	def remove_vaso(self, name):
		for v in self.__fila:
			if v[0] == Ativ(name):
				self.__fila.remove(v)
				return v[1]
		return None

	def search_vaso(self, name):
		for v in self.__fila:
			if v[0] == Ativ[name]:
				return True
		return False