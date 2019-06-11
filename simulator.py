import vaso as Vaso
import inputFile as InputFile
import const as Const
import fel as Fel
import filaVaso as FilaVaso
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
	vasos = FilaVaso.FilaVaso()

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
				# coloca vaso na fila de preparacao da forma]
				vasos.insert_vaso('PREPARACAO_FORMA',time_system)
		else:
			# coloca vaso na fila de preparacao da forma
			vasos.insert_vaso('PREPARACAO_FORMA',time_system)
			

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
				# Fazer massa - fazer_massa
				DCA_fazer_massa()
			# SE pouca pedra (-25%)
			elif (pedra < 25):
				################### aloca o artesao para coleta de pedra
				# Coletar pedra - coleta_pedra
				DCA_coleta_pedra()
			# SE vaso na fila de envernizacao geral
			elif ( vasos.search_vaso('ENVERNIZACAO_GERAL') ):
				# desenfilera vaso da fila envernizacao geral
				v = vasos.remove_vaso('ENVERNIZACAO_GERAL')
				################### aloca o artesao para envernizacao
				# Envernizacao Geral - envernizacao_geral()
				DCA_envernizacao_geral()
			# SE vaso na fila de impermeabilizacao interna
			elif ( vasos.search_vaso('IMPERMEABILIZACAO_INTERNA') ):
				# desenfilera vaso da fila impermeabilizacao interna
				v = vasos.remove_vaso('IMPERMEABILIZACAO_INTERNA')
				################### aloca o artesao para impermeabilizacao
				# Impermeabilizacao Interna - impermeabilizacao_interna()
				DCA_impermeabilizacao_interna()
			# SE vaso na fila de limpeza acabamento boca
			elif ( vasos.search_vaso('LIMPEZA_ACABAMENTO_BOCA') ):
				# desenfilera vaso da fila limpeza acabamento boca
				v = vasos.remove_vaso('LIMPEZA_ACABAMENTO_BOCA')
				################### aloca o artesao para limpeza
				# limpeza acabamento boca - limpeza_acabamento_boca()
				DCA_limpeza_acabamento_boca()
			# SE vaso na fila de preparacao boca
			elif ( vasos.search_vaso('PREPARACAO_BOCA') ):
				# desenfilera vaso da fila preparacao boca
				v = vasos.remove_vaso('PREPARACAO_BOCA')
				################### aloca o artesao para preparacao
				# preparacao boca - preparacao_boca()
				DCA_preparacao_boca()
			# SE vaso na fila de preparacao boca
			elif ( vasos.search_vaso('ACABAMENTO_BASE') ):
				# desenfilera vaso da fila limpeza acabamento base
				v = vasos.remove_vaso('ACABAMENTO_BASE')
				################### aloca o artesao para limpeza
				# limpeza acabamento base - limpeza_acabamento_base()
				DCA_limpeza_acabamento_base()
			# SE vaso na fila inicial
			elif ( vasos.search_vaso('PREPARACAO_FORMA') ):
				# desenfilera vaso da fila inicial
				v = vasos.remove_vaso('PREPARACAO_FORMA')
				################### aloca o artesao para fila inicial
				# fila inicial - preparacao_forma()
				DCA_preparacao_forma()
			else:
				################### libera artesao
				pass

		rand = np.random.triangular(7,10,14)
		# Evento: atualiza tempos do sistema
		fel.insert_Fel('LIMPEZA_ACABAMENTO_BASE',time_system + rand)

	################### Existe uma fila entre essas 2 atividades

	def DCA_limpeza_acabamento_base(self):
		if haveSpecialist():
			spec = getSpecialist()
			# sorteia tempo de limpeza acabamento base
			rand = np.random.triangular(5,8,11)
			# Evento: atualiza tempos do sistema
			fel.insert_Fel('LIMPEZA_ACABAMENTO_BASE',time_system + rand)
		elif haveArtisan():
			spec = getArtisan()
			rand = np.random.triangular(5,8,11)
			# Evento: atualiza tempos do sistema
			fel.insert_Fel('LIMPEZA_ACABAMENTO_BASE',time_system + rand)
		else:
			vasos.insert_vaso('LIMPEZA_ACABAMENTO_BASE',time_system)

	def DCA_secagem_base(self):
		#################### SE recurso alocado atual == artesao
		if ( 1 ):
			# SE pouca massa (-25%)
			if (massa < 25):
				################### aloca o artesao para preparacao da massa
				# Fazer massa - fazer_massa
				DCA_fazer_massa()
			# SE pouca pedra (-25%)
			elif (pedra < 25):
				################### aloca o artesao para coleta de pedra
				# Coletar pedra - coleta_pedra
				DCA_coleta_pedra()
			# SE vaso na fila de envernizacao geral
			elif ( vasos.search_vaso('ENVERNIZACAO_GERAL') ):
				# desenfilera vaso da fila envernizacao geral
				v = vasos.remove_vaso('ENVERNIZACAO_GERAL')
				################### aloca o artesao para envernizacao
				# Envernizacao Geral - envernizacao_geral()
				DCA_envernizacao_geral()
			# SE vaso na fila de impermeabilizacao interna
			elif ( vasos.search_vaso('IMPERMEABILIZACAO_INTERNA') ):
				# desenfilera vaso da fila impermeabilizacao interna
				v = vasos.remove_vaso('IMPERMEABILIZACAO_INTERNA')
				################### aloca o artesao para impermeabilizacao
				# Impermeabilizacao Interna - impermeabilizacao_interna()
				DCA_impermeabilizacao_interna()
			# SE vaso na fila de limpeza acabamento boca
			elif ( vasos.search_vaso('LIMPEZA_ACABAMENTO_BOCA') ):
				# desenfilera vaso da fila limpeza acabamento boca
				v = vasos.remove_vaso('LIMPEZA_ACABAMENTO_BOCA')
				################### aloca o artesao para limpeza
				# limpeza acabamento boca - limpeza_acabamento_boca()
				DCA_limpeza_acabamento_boca()
			# SE vaso na fila de preparacao boca
			elif ( vasos.search_vaso('PREPARACAO_BOCA') ):
				# desenfilera vaso da fila preparacao boca
				v = vasos.remove_vaso('PREPARACAO_BOCA')
				################### aloca o artesao para preparacao
				# preparacao boca - preparacao_boca()
				DCA_preparacao_boca()
			# SE vaso na fila de limpeza acabamento base
			elif ( vasos.search_vaso('LIMPEZA_ACABAMENTO_BASE') ):
				# desenfilera vaso da fila limpeza acabamento base
				v = vasos.remove_vaso('LIMPEZA_ACABAMENTO_BASE')
				################### aloca o artesao para limpeza
				# limpeza acabamento base - limpeza_acabamento_base()
				DCA_limpeza_acabamento_base()
			# SE vaso na fila inicial
			elif ( vasos.search_vaso('PREPARACAO_FORMA') ):
				# desenfilera vaso da fila inicial
				v = vasos.remove_vaso('PREPARACAO_FORMA')
				################### aloca o artesao para fila inicial
				# fila inicial - preparacao_forma()
				DCA_preparacao_forma()
			else:
				################### libera artesao
				pass

		rand = np.random.triangular(4,12,24)
		# Evento: atualiza tempos do sistema
		fel.insert_Fel('SECAGEM_BASE',time_system + rand)

	################### Existe uma fila entre essas 2 atividades

	def DCA_preparacao_boca(self):
		if haveSpecialist():
			spec = getSpecialist()
			# sorteia tempo de preparacao da boca
			rand = np.random.triangular(7,10,14)
			# Evento: atualiza tempos do sistema
			fel.insert_Fel('PREPARACAO_BOCA',time_system + rand)
		elif haveArtisan():
			spec = getArtisan()
			rand = np.random.triangular(7,10,14)
			# Evento: atualiza tempos do sistema
			fel.insert_Fel('PREPARACAO_BOCA',time_system + rand)
		else:
			vasos.insert_vaso('PREPARACAO_BOCA',time_system)

	def DCA_acabamento_inicial_boca(self):
		rand = np.random.triangular(3,5,8)
		# Evento: atualiza tempos do sistema
		fel.insert_Fel('ACABAMENTO_INICIAL_BOCA',time_system + rand)

	def DCA_secagem_acabamento_boca(self):
		#################### SE recurso alocado atual == artesao
		if ( 1 ):
			# SE pouca massa (-25%)
			if (massa < 25):
				################### aloca o artesao para preparacao da massa
				# Fazer massa - fazer_massa
				DCA_fazer_massa()
			# SE pouca pedra (-25%)
			elif (pedra < 25):
				################### aloca o artesao para coleta de pedra
				# Coletar pedra - coleta_pedra
				DCA_coleta_pedra()
			# SE vaso na fila de envernizacao geral
			elif ( vasos.search_vaso('ENVERNIZACAO_GERAL') ):
				# desenfilera vaso da fila envernizacao geral
				v = vasos.remove_vaso('ENVERNIZACAO_GERAL')
				################### aloca o artesao para envernizacao
				# Envernizacao Geral - envernizacao_geral()
				DCA_envernizacao_geral()
			# SE vaso na fila de impermeabilizacao interna
			elif ( vasos.search_vaso('IMPERMEABILIZACAO_INTERNA') ):
				# desenfilera vaso da fila impermeabilizacao interna
				v = vasos.remove_vaso('IMPERMEABILIZACAO_INTERNA')
				################### aloca o artesao para impermeabilizacao
				# Impermeabilizacao Interna - impermeabilizacao_interna()
				DCA_impermeabilizacao_interna()
			# SE vaso na fila de limpeza acabamento boca
			elif ( vasos.search_vaso('LIMPEZA_ACABAMENTO_BOCA') ):
				# desenfilera vaso da fila limpeza acabamento boca
				v = vasos.remove_vaso('LIMPEZA_ACABAMENTO_BOCA')
				################### aloca o artesao para limpeza
				# limpeza acabamento boca - limpeza_acabamento_boca()
				DCA_limpeza_acabamento_boca()
			# SE vaso na fila de preparacao boca
			elif ( vasos.search_vaso('PREPARACAO_BOCA') ):
				# desenfilera vaso da fila preparacao boca
				v = vasos.remove_vaso('PREPARACAO_BOCA')
				################### aloca o artesao para preparacao
				# preparacao boca - preparacao_boca()
				DCA_preparacao_boca()
			# SE vaso na fila de limpeza acabamento base
			elif ( vasos.search_vaso('LIMPEZA_ACABAMENTO_BASE') ):
				# desenfilera vaso da fila limpeza acabamento base
				v = vasos.remove_vaso('LIMPEZA_ACABAMENTO_BASE')
				################### aloca o artesao para limpeza
				# limpeza acabamento base - limpeza_acabamento_base()
				DCA_limpeza_acabamento_base()
			# SE vaso na fila inicial
			elif ( vasos.search_vaso('PREPARACAO_FORMA') ):
				# desenfilera vaso da fila inicial
				v = vasos.remove_vaso('PREPARACAO_FORMA')
				################### aloca o artesao para fila inicial
				# fila inicial - preparacao_forma()
				DCA_preparacao_forma()
			else:
				################### libera artesao
				pass

		rand = np.random.triangular(8,10,13)
		# Evento: atualiza tempos do sistema
		fel.insert_Fel('SECAGEM_ACABAMENTO_BOCA',time_system + rand)

	def DCA_limpeza_acabamento_boca(self):
		if haveSpecialist():
			spec = getSpecialist()
			# sorteia tempo de preparacao da boca
			rand = np.random.triangular(6,7,10)
			# Evento: atualiza tempos do sistema
			fel.insert_Fel('LIMPEZA_ACABAMENTO_BOCA',time_system + rand)
		elif haveArtisan():
			spec = getArtisan()
			rand = np.random.triangular(6,7,10)
			# Evento: atualiza tempos do sistema
			fel.insert_Fel('LIMPEZA_ACABAMENTO_BOCA',time_system + rand)
		else:
			vasos.insert_vaso('LIMPEZA_ACABAMENTO_BOCA',time_system)

	def DCA_secagem_boca(self):
		#################### SE recurso alocado atual == artesao
		if ( 1 ):
			# SE pouca massa (-25%)
			if (massa < 25):
				################### aloca o artesao para preparacao da massa
				# Fazer massa - fazer_massa
				DCA_fazer_massa()
			# SE pouca pedra (-25%)
			elif (pedra < 25):
				################### aloca o artesao para coleta de pedra
				# Coletar pedra - coleta_pedra
				DCA_coleta_pedra()
			# SE vaso na fila de envernizacao geral
			elif ( vasos.search_vaso('ENVERNIZACAO_GERAL') ):
				# desenfilera vaso da fila envernizacao geral
				v = vasos.remove_vaso('ENVERNIZACAO_GERAL')
				################### aloca o artesao para envernizacao
				# Envernizacao Geral - envernizacao_geral()
				DCA_envernizacao_geral()
			# SE vaso na fila de impermeabilizacao interna
			elif ( vasos.search_vaso('IMPERMEABILIZACAO_INTERNA') ):
				# desenfilera vaso da fila impermeabilizacao interna
				v = vasos.remove_vaso('IMPERMEABILIZACAO_INTERNA')
				################### aloca o artesao para impermeabilizacao
				# Impermeabilizacao Interna - impermeabilizacao_interna()
				DCA_impermeabilizacao_interna()
			# SE vaso na fila de limpeza acabamento boca
			elif ( vasos.search_vaso('LIMPEZA_ACABAMENTO_BOCA') ):
				# desenfilera vaso da fila limpeza acabamento boca
				v = vasos.remove_vaso('LIMPEZA_ACABAMENTO_BOCA')
				################### aloca o artesao para limpeza
				# limpeza acabamento boca - limpeza_acabamento_boca()
				DCA_limpeza_acabamento_boca()
			# SE vaso na fila de preparacao boca
			elif ( vasos.search_vaso('PREPARACAO_BOCA') ):
				# desenfilera vaso da fila preparacao boca
				v = vasos.remove_vaso('PREPARACAO_BOCA')
				################### aloca o artesao para preparacao
				# preparacao boca - preparacao_boca()
				DCA_preparacao_boca()
			# SE vaso na fila de limpeza acabamento base
			elif ( vasos.search_vaso('LIMPEZA_ACABAMENTO_BASE') ):
				# desenfilera vaso da fila limpeza acabamento base
				v = vasos.remove_vaso('LIMPEZA_ACABAMENTO_BASE')
				################### aloca o artesao para limpeza
				# limpeza acabamento base - limpeza_acabamento_base()
				DCA_limpeza_acabamento_base()
			# SE vaso na fila inicial
			elif ( vasos.search_vaso('PREPARACAO_FORMA') ):
				# desenfilera vaso da fila inicial
				v = vasos.remove_vaso('PREPARACAO_FORMA')
				################### aloca o artesao para fila inicial
				# fila inicial - preparacao_forma()
				DCA_preparacao_forma()
			else:
				################### libera artesao
				pass

		rand = np.random.triangular(3,8,12)
		# Evento: atualiza tempos do sistema
		fel.insert_Fel('SECAGEM_BOCA',time_system + rand)
