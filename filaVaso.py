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
	PREPARACAO_MASSA            = 16
	PREPARACAO_PEDRA            = 17
	FIM							= 18

class FilaVaso(object):
	def __init__(self):
		self.__fila = []
		self.id = 1

	def insert_new_vaso(self, name, size, time):
		self.__fila.append((Ativ[name],Vaso.Vaso(self.id, size, time)))
		self.id += 1
	
	def insert_vaso(self, name, vaso):
		self.__fila.append((Ativ[name], vaso)) 

	def get_fila(self):
		return self.__fila

	def remove_vaso(self, name):
		for v in self.__fila:
			if v[0] == Ativ[name]:
				x = v[1]
				self.__fila.remove(v)
				return x
		return None

	def search_vaso(self, name):
		for v in self.__fila:
			# print('$$$ '+v[0].name+' '+name)
			if v[0].name == name:
				return True
		return False

	def show(self):
		print('--- Vasos ---')
		for v in self.__fila:
			print('AT: '+v[0].name+' - ID: '+str(v[1].get_id())+' - S: '+v[1].get_size()+' - TI: '+
					str(v[1].getStartTime())+' - TE: '+str(v[1].getEndTime())+' - TF: '+
					str(v[1].getCompletionTime()))