import vaso as Vaso
import inputFile as InputFile
import const as Const
import fel as Fel
import artesao as Artesao
import numpy as np

class simulator:
	# vaso1 = Vaso.Vaso(10,'B',0)
	# print(vaso1.get_id())

	time_system = 0
	massa 		= 100
	pedra		= 100
	artesoes 	= []
	uso_esp_sec	= 0

	inpFile = InputFile.InputFile()

	CONST 	= Const.Const()
	CONST 	= inpFile.inputs('entrada.txt')
	# print(CONST.get_G_TSM())
	fel = Fel.Fel()

	# Cria os artesoes e especialistas do sistema
	for i in range(CONST.get_NUM_ART()):
		artesoes.append(Artesao.Artesao())
	for i in range(CONST.get_NUM_ESP()):
		artesoes.append(Artesao.Artesao(True))

	def haveSpecialist(self):
		for x in artesoes:
			if (x.isSpecialist() and x.getOciosity()):
				return True
		return False
				
	def getSpecialist(self):
		for x in artesoes:
			if (x.isSpecialist() and x.getOciosity()):
				x.setOciosity(False)
				return x
		return None

	def haveArtisan(self):
		for x in artesoes:
			if (not x.isSpecialist() and x.getOciosity()):
				return True
		return False

	def getArtisan(self):
		for x in artesoes:
			if (not x.isSpecialist() and x.getOciosity()):
				x.setOciosity(False)
				return x
		return None

	def DCA_preparacao_forma(self):
		# espaco de secagem
		if (uso_esp_sec < CONST.get_esp_sec()):
			# massa suficiente
			if (massa > 0):				
				if haveSpecialist():
					spec = getSpecialist()
					# sorteia tempo de preparacao da forma
					rand = np.random.triangular(2,4,6)
					# Evento: atualiza tempos do sistema
					fel.insert_Fel('PREPARACAO_BASE',time_system + rand)
				elif haveArtisan():
					spec = getArtisan()
					rand = np.random.triangular(2,4,6)
					# Evento: atualiza tempos do sistema
					fel.insert_Fel('PREPARACAO_BASE',time_system + rand)
			else:
				################### coloca vaso na fila de preparacao da forma]
				pass
		else:
			################### coloca vaso na fila de preparacao da forma
			pass

	def DCA_preparacao_base(self):
		rand = np.random.triangular(15,40,120)
		# Evento: atualiza tempos do sistema
		fel.insert_Fel('ACABAMENTO_INICIAL_BASE',time_system + rand)

	def DCA_acabamento_inicial_base(self):
		rand = np.random.triangular(2,5,8)
		# Evento: atualiza tempos do sistema
		fel.insert_Fel('SECAGEM_ACABAMENTO_BASE',time_system + rand)

	def DCA_secagem_acabamento_base(self):
		#################### SE recurso alocado atual == artesao
		if ( 1 ):
			# SE pouca massa (-25%)
			if (massa < 25):
				################### aloca o artesao para preparacao da massa
				################### Fazer massa - fazer_massa
				pass
			# SE pouca pedra (-25%)
			elif (pedra < 25):
				################### aloca o artesao para coleta de pedra
				################### Coletar pedra - coleta_pedra
				pass
			#################### SE vaso na fila de envernizacao geral
			elif ( 1 ):
				################### desenfilera vaso da fila envernizacao geral
				################### aloca o artesao para envernizacao
				################### Envernizacao Geral - envernizacao_geral()
				pass
			#################### SE vaso na fila de impermeabilizacao interna
			elif ( 1 ):
				################### desenfilera vaso da fila impermeabilizacao interna
				################### aloca o artesao para impermeabilizacao
				################### Impermeabilizacao Interna - impermeabilizacao_interna()
				pass
			#################### SE vaso na fila de limpeza acabamento boca
			elif ( 1 ):
				################### desenfilera vaso da fila limpeza acabamento boca
				################### aloca o artesao para limpeza
				################### limpeza acabamento boca - limpeza_acabamento_boca()
				pass
			#################### SE vaso na fila de preparacao boca
			elif ( 1 ):
				################### desenfilera vaso da fila preparacao boca
				################### aloca o artesao para preparacao
				################### preparacao boca - preparacao_boca()
				pass
			#################### SE vaso na fila de preparacao boca
			elif ( 1 ):
				################### desenfilera vaso da fila limpeza acabamento base
				################### aloca o artesao para limpeza
				################### limpeza acabamento base - limpeza_acabamento_base()
				pass
			#################### SE vaso na fila inicial
			elif ( 1 ):
				################### desenfilera vaso da fila inicial
				################### aloca o artesao para fila inicial
				################### fila inicial - preparacao_forma()
				pass
			else:
				################### libera artesao
				pass

		rand = np.random.triangular(7,10,14)
		# Evento: atualiza tempos do sistema
		fel.insert_Fel('LIMPEZA_ACABAMENTO_BASE',time_system + rand)