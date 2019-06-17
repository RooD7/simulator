import vaso as Vaso
import inputFile as InputFile
import const as Const
import fel as fel
import filaVaso as FilaVaso
import artesao as Artesao
import numpy as np

fel = fel.Fel()
vasos = FilaVaso.FilaVaso()

inpFile = InputFile.InputFile()

CONST = Const.Const()
CONST = inpFile.inputs('entrada.txt')

time_system = 0
massa = CONST.get_QTD_MASSA()
pedra = CONST.get_QTD_PEDRA()
pouca_massa = 250
pouca_pedra = 250
artesoes = []
uso_esp_sec = 0


# DCA_chegada_pedido()

def haveSpecialist():
	for x in artesoes:
		if (x.isSpecialist() and x.getOciosity()):
			return True
	return False


def getSpecialist():
	for x in artesoes:
		if (x.isSpecialist() and x.getOciosity()):
			x.setOciosity(False)
			return x
	return None


def haveArtisan():
	for x in artesoes:
		if (not x.isSpecialist() and x.getOciosity()):
			return True
	return False


def getArtisan():
	for x in artesoes:
		if (not x.isSpecialist() and x.getOciosity()):
			x.setOciosity(False)
			return x
	return None


# def randomTime(, evento, vaso):
# 	param = vaso.get_size()
# 	rand = np.random.triangular(2,4,6)

################### resolver essa porra de sorteio 0.4 - 0.4 - 0.2
# def probSizeVaso():
# 	x = CONST.get_PROBS()
# 	rand = np.random.triangular(x[0],x[1],x[2])
# 	# return

def DCA_fazer_massa():
	massa = CONST.get_QTD_MASSA_MAX


def DCA_coleta_pedra():
	pedra = CONST.get_QTD_PEDRA_MAX


def DCA_chegada_pedido():
	print('inicio - CHEGADA_PEDIDO')
	# frequencia de chegada de pedidos
	# tamanho do pedido (seguindo a probabilidade do CONST)
	x = CONST.get_TAM_PED()
	rand = np.random.triangular(x[0], x[1], x[2])
	################### remover
	size = 'S'
	# serao feitos 'rand' pedidos
	for r in range(0, int(rand)):
		vasos.insert_vaso('CHEGADA_PEDIDO', size, time_system)
	################### tamanho (S - M - B) de cada vazo do pedido (seguindo a proporcao do CONST)]
	DCA_preparacao_forma()
	print('fim - CHEGADA_PEDIDO')

################### Existe uma fila entre essas 2 atividades

def DCA_preparacao_forma():
	print('inicio - PREPARACAO_FORMA')
	# espaco de secagem
	if (uso_esp_sec < CONST.get_ESP_SEC()):
		# massa suficiente
		if (massa > pouca_massa):
			if haveSpecialist():
				spec = getSpecialist()
				# sorteia tempo de preparacao da forma
				x = getSizeVaso(vaso.get_size())
				rand = np.random.triangular(x[0], x[1], x[2])
				# rand = np.random.triangular(2, 4, 6)
				# Evento: atualiza tempos do sistema
				fel.insert_fel('PREPARACAO_BASE', time_system + rand)
			elif haveArtisan():
				spec = getArtisan()
				x = getSizeVaso(vaso.get_size())
				rand = np.random.triangular(x[0], x[1], x[2])
				# rand = np.random.triangular(2, 4, 6)
				# Evento: atualiza tempos do sistema
				fel.insert_fel('PREPARACAO_BASE', time_system + rand)
		else:
			# coloca vaso na fila de preparacao da forma]
			vasos.insert_vaso('PREPARACAO_FORMA', time_system)
	else:
		# coloca vaso na fila de preparacao da forma
		vasos.insert_vaso('PREPARACAO_FORMA', time_system)
	DCA_preparacao_base()
	print('fim - PREPARACAO_FORMA')


def DCA_preparacao_base():
	print('inicio - PREPARACAO_BASE')
	x = getSizeVaso(vaso.get_size())
	rand = np.random.triangular(x[0], x[1], x[2])
	# rand = np.random.triangular(15, 40, 120)
	# Evento: atualiza tempos do sistema
	fel.insert_fel('ACABAMENTO_INICIAL_BASE', time_system + rand)
	DCA_acabamento_inicial_base()
	print('fim - PREPARACAO_BASE')


def DCA_acabamento_inicial_base():
	print('inicio - ACABAMENTO_INICIAL_BASE')
	x = getSizeVaso(vaso.get_size())
	rand = np.random.triangular(x[0], x[1], x[2])
	# rand = np.random.triangular(2, 5, 8)
	# Evento: atualiza tempos do sistema
	fel.insert_fel('SECAGEM_ACABAMENTO_BASE', time_system + rand)
	DCA_secagem_acabamento_base()
	print('fim - ACABAMENTO_INICIAL_BASE')


def DCA_secagem_acabamento_base():
	print('inicio - SECAGEM_ACABAMENTO_BASE')
	#################### SE recurso alocado atual == artesao
	if (1):
		# SE pouca massa (-25%)
		if (massa < pouca_massa):
			################### aloca o artesao para preparacao da massa
			# Fazer massa - fazer_massa
			DCA_fazer_massa()
		# SE pouca pedra (-25%)
		elif (pedra < pouca_pedra):
			################### aloca o artesao para coleta de pedra
			# Coletar pedra - coleta_pedra
			DCA_coleta_pedra()
		# SE vaso na fila de envernizacao geral
		elif (vasos.search_vaso('ENVERNIZACAO_GERAL')):
			# desenfilera vaso da fila envernizacao geral
			v = vasos.remove_vaso('ENVERNIZACAO_GERAL')
			################### aloca o artesao para envernizacao
			# Envernizacao Geral - envernizacao_geral()
			DCA_envernizacao_geral()
		# SE vaso na fila de impermeabilizacao interna
		elif (vasos.search_vaso('IMPERMEABILIZACAO_INTERNA')):
			# desenfilera vaso da fila impermeabilizacao interna
			v = vasos.remove_vaso('IMPERMEABILIZACAO_INTERNA')
			################### aloca o artesao para impermeabilizacao
			# Impermeabilizacao Interna - impermeabilizacao_interna()
			DCA_impermeabilizacao_interna()
		# SE vaso na fila de limpeza acabamento boca
		elif (vasos.search_vaso('LIMPEZA_ACABAMENTO_BOCA')):
			# desenfilera vaso da fila limpeza acabamento boca
			v = vasos.remove_vaso('LIMPEZA_ACABAMENTO_BOCA')
			################### aloca o artesao para limpeza
			# limpeza acabamento boca - limpeza_acabamento_boca()
			DCA_limpeza_acabamento_boca()
		# SE vaso na fila de preparacao boca
		elif (vasos.search_vaso('PREPARACAO_BOCA')):
			# desenfilera vaso da fila preparacao boca
			v = vasos.remove_vaso('PREPARACAO_BOCA')
			################### aloca o artesao para preparacao
			# preparacao boca - preparacao_boca()
			DCA_preparacao_boca()
		# SE vaso na fila de preparacao boca
		elif (vasos.search_vaso('ACABAMENTO_INICIAL_BASE')):
			# desenfilera vaso da fila limpeza acabamento base
			v = vasos.remove_vaso('ACABAMENTO_INICIAL_BASE')
			################### aloca o artesao para limpeza
			# limpeza acabamento base - limpeza_acabamento_base()
			DCA_limpeza_acabamento_base()
		# SE vaso na fila inicial
		elif (vasos.search_vaso('PREPARACAO_FORMA')):
			# desenfilera vaso da fila inicial
			v = vasos.remove_vaso('PREPARACAO_FORMA')
			################### aloca o artesao para fila inicial
			# fila inicial - preparacao_forma()
			DCA_preparacao_forma()
		else:
			################### libera artesao
			pass

	x = getSizeVaso(vaso.get_size())
	rand = np.random.triangular(x[0], x[1], x[2])
	# rand = np.random.triangular(7, 10, 14)
	# Evento: atualiza tempos do sistema
	fel.insert_fel('LIMPEZA_ACABAMENTO_BASE', time_system + rand)
	DCA_limpeza_acabamento_base()
	print('fim - SECAGEM_ACABAMENTO_BASE')


################### Existe uma fila entre essas 2 atividades

def DCA_limpeza_acabamento_base():
	print('inicio - LIMPEZA_ACABAMENTO_BASE')
	if haveSpecialist():
		spec = getSpecialist()
		# sorteia tempo de limpeza acabamento base
		x = getSizeVaso(vaso.get_size())
		rand = np.random.triangular(x[0], x[1], x[2])
		# rand = np.random.triangular(5, 8, 11)
		# Evento: atualiza tempos do sistema
		fel.insert_fel('LIMPEZA_ACABAMENTO_BASE', time_system + rand)
	elif haveArtisan():
		spec = getArtisan()
		x = getSizeVaso(vaso.get_size())
		rand = np.random.triangular(x[0], x[1], x[2])
		# rand = np.random.triangular(5, 8, 11)
		# Evento: atualiza tempos do sistema
		fel.insert_fel('LIMPEZA_ACABAMENTO_BASE', time_system + rand)
	else:
		vasos.insert_vaso('LIMPEZA_ACABAMENTO_BASE', time_system)
	DCA_secagem_base()
	print('fim - LIMPEZA_ACABAMENTO_BASE')


def DCA_secagem_base():
	print('inicio - SECAGEM_BASE')
	#################### SE recurso alocado atual == artesao
	if (1):
		# SE pouca massa (-25%)
		if (massa < pouca_massa):
			################### aloca o artesao para preparacao da massa
			# Fazer massa - fazer_massa
			DCA_fazer_massa()
		# SE pouca pedra (-25%)
		elif (pedra < pouca_pedra):
			################### aloca o artesao para coleta de pedra
			# Coletar pedra - coleta_pedra
			DCA_coleta_pedra()
		# SE vaso na fila de envernizacao geral
		elif (vasos.search_vaso('ENVERNIZACAO_GERAL')):
			# desenfilera vaso da fila envernizacao geral
			v = vasos.remove_vaso('ENVERNIZACAO_GERAL')
			################### aloca o artesao para envernizacao
			# Envernizacao Geral - envernizacao_geral()
			DCA_envernizacao_geral()
		# SE vaso na fila de impermeabilizacao interna
		elif (vasos.search_vaso('IMPERMEABILIZACAO_INTERNA')):
			# desenfilera vaso da fila impermeabilizacao interna
			v = vasos.remove_vaso('IMPERMEABILIZACAO_INTERNA')
			################### aloca o artesao para impermeabilizacao
			# Impermeabilizacao Interna - impermeabilizacao_interna()
			DCA_impermeabilizacao_interna()
		# SE vaso na fila de limpeza acabamento boca
		elif (vasos.search_vaso('LIMPEZA_ACABAMENTO_BOCA')):
			# desenfilera vaso da fila limpeza acabamento boca
			v = vasos.remove_vaso('LIMPEZA_ACABAMENTO_BOCA')
			################### aloca o artesao para limpeza
			# limpeza acabamento boca - limpeza_acabamento_boca()
			DCA_limpeza_acabamento_boca()
		# SE vaso na fila de preparacao boca
		elif (vasos.search_vaso('PREPARACAO_BOCA')):
			# desenfilera vaso da fila preparacao boca
			v = vasos.remove_vaso('PREPARACAO_BOCA')
			################### aloca o artesao para preparacao
			# preparacao boca - preparacao_boca()
			DCA_preparacao_boca()
		# SE vaso na fila de limpeza acabamento base
		elif (vasos.search_vaso('LIMPEZA_ACABAMENTO_BASE')):
			# desenfilera vaso da fila limpeza acabamento base
			v = vasos.remove_vaso('LIMPEZA_ACABAMENTO_BASE')
			################### aloca o artesao para limpeza
			# limpeza acabamento base - limpeza_acabamento_base()
			DCA_limpeza_acabamento_base()
		# SE vaso na fila inicial
		elif (vasos.search_vaso('PREPARACAO_FORMA')):
			# desenfilera vaso da fila inicial
			v = vasos.remove_vaso('PREPARACAO_FORMA')
			################### aloca o artesao para fila inicial
			# fila inicial - preparacao_forma()
			DCA_preparacao_forma()
		else:
			################### libera artesao
			pass

	x = getSizeVaso(vaso.get_size())
	rand = np.random.triangular(x[0], x[1], x[2])
	# rand = np.random.triangular(4, 12, 24)
	# Evento: atualiza tempos do sistema
	fel.insert_fel('SECAGEM_BASE', time_system + rand)
	DCA_preparacao_boca()
	print('fim - SECAGEM_BASE')


################### Existe uma fila entre essas 2 atividades

def DCA_preparacao_boca():
	print('inicio - PREPARACAO_BOCA')
	if haveSpecialist():
		spec = getSpecialist()
		# sorteia tempo de preparacao da boca
		x = getSizeVaso(vaso.get_size())
		rand = np.random.triangular(x[0], x[1], x[2])
		# rand = np.random.triangular(7, 10, 14)
		# Evento: atualiza tempos do sistema
		fel.insert_fel('PREPARACAO_BOCA', time_system + rand)
	elif haveArtisan():
		spec = getArtisan()
		x = getSizeVaso(vaso.get_size())
		rand = np.random.triangular(x[0], x[1], x[2])
		# rand = np.random.triangular(7, 10, 14)
		# Evento: atualiza tempos do sistema
		fel.insert_fel('PREPARACAO_BOCA', time_system + rand)
	else:
		vasos.insert_vaso('PREPARACAO_BOCA', time_system)
	DCA_acabamento_inicial_boca()
	print('fim - PREPARACAO_BOCA')


def DCA_acabamento_inicial_boca():
	print('inicio - ACABAMENTO_INICIAL_BOCA')
	x = getSizeVaso(vaso.get_size())
	rand = np.random.triangular(x[0], x[1], x[2])
	# rand = np.random.triangular(3, 5, 8)
	# Evento: atualiza tempos do sistema
	fel.insert_fel('ACABAMENTO_INICIAL_BOCA', time_system + rand)
	DCA_secagem_acabamento_boca()
	print('fim - ACABAMENTO_INICIAL_BOCA')


def DCA_secagem_acabamento_boca():
	print('inicio - SECAGEM_ACABAMENTO_BOCA')
	#################### SE recurso alocado atual == artesao
	if (1):
		# SE pouca massa (-25%)
		if (massa < pouca_massa):
			################### aloca o artesao para preparacao da massa
			# Fazer massa - fazer_massa
			DCA_fazer_massa()
		# SE pouca pedra (-25%)
		elif (pedra < pouca_pedra):
			################### aloca o artesao para coleta de pedra
			# Coletar pedra - coleta_pedra
			DCA_coleta_pedra()
		# SE vaso na fila de envernizacao geral
		elif (vasos.search_vaso('ENVERNIZACAO_GERAL')):
			# desenfilera vaso da fila envernizacao geral
			v = vasos.remove_vaso('ENVERNIZACAO_GERAL')
			################### aloca o artesao para envernizacao
			# Envernizacao Geral - envernizacao_geral()
			DCA_envernizacao_geral()
		# SE vaso na fila de impermeabilizacao interna
		elif (vasos.search_vaso('IMPERMEABILIZACAO_INTERNA')):
			# desenfilera vaso da fila impermeabilizacao interna
			v = vasos.remove_vaso('IMPERMEABILIZACAO_INTERNA')
			################### aloca o artesao para impermeabilizacao
			# Impermeabilizacao Interna - impermeabilizacao_interna()
			DCA_impermeabilizacao_interna()
		# SE vaso na fila de limpeza acabamento boca
		elif (vasos.search_vaso('LIMPEZA_ACABAMENTO_BOCA')):
			# desenfilera vaso da fila limpeza acabamento boca
			v = vasos.remove_vaso('LIMPEZA_ACABAMENTO_BOCA')
			################### aloca o artesao para limpeza
			# limpeza acabamento boca - limpeza_acabamento_boca()
			DCA_limpeza_acabamento_boca()
		# SE vaso na fila de preparacao boca
		elif (vasos.search_vaso('PREPARACAO_BOCA')):
			# desenfilera vaso da fila preparacao boca
			v = vasos.remove_vaso('PREPARACAO_BOCA')
			################### aloca o artesao para preparacao
			# preparacao boca - preparacao_boca()
			DCA_preparacao_boca()
		# SE vaso na fila de limpeza acabamento base
		elif (vasos.search_vaso('LIMPEZA_ACABAMENTO_BASE')):
			# desenfilera vaso da fila limpeza acabamento base
			v = vasos.remove_vaso('LIMPEZA_ACABAMENTO_BASE')
			################### aloca o artesao para limpeza
			# limpeza acabamento base - limpeza_acabamento_base()
			DCA_limpeza_acabamento_base()
		# SE vaso na fila inicial
		elif (vasos.search_vaso('PREPARACAO_FORMA')):
			# desenfilera vaso da fila inicial
			v = vasos.remove_vaso('PREPARACAO_FORMA')
			################### aloca o artesao para fila inicial
			# fila inicial - preparacao_forma()
			DCA_preparacao_forma()
		else:
			################### libera artesao
			pass

	x = getSizeVaso(vaso.get_size())
	rand = np.random.triangular(x[0], x[1], x[2])
	# rand = np.random.triangular(8, 10, 13)
	# Evento: atualiza tempos do sistema
	fel.insert_fel('SECAGEM_ACABAMENTO_BOCA', time_system + rand)
	DCA_limpeza_acabamento_boca()
	print('fim - SECAGEM_ACABAMENTO_BOCA')


def DCA_limpeza_acabamento_boca():
	print('inicio - LIMPEZA_ACABAMENTO_BOCA')
	if haveSpecialist():
		spec = getSpecialist()
		# sorteia tempo de preparacao da boca
		x = getSizeVaso(vaso.get_size())
		rand = np.random.triangular(x[0], x[1], x[2])
		# rand = np.random.triangular(6, 7, 10)
		# Evento: atualiza tempos do sistema
		fel.insert_fel('LIMPEZA_ACABAMENTO_BOCA', time_system + rand)
	elif haveArtisan():
		spec = getArtisan()
		x = getSizeVaso(vaso.get_size())
		rand = np.random.triangular(x[0], x[1], x[2])
		# rand = np.random.triangular(6, 7, 10)
		# Evento: atualiza tempos do sistema
		fel.insert_fel('LIMPEZA_ACABAMENTO_BOCA', time_system + rand)
	else:
		vasos.insert_vaso('LIMPEZA_ACABAMENTO_BOCA', time_system)
	DCA_secagem_boca()
	print('fim - LIMPEZA_ACABAMENTO_BOCA')


def DCA_secagem_boca():
	print('inicio - SECAGEM_BOCA')
	#################### SE recurso alocado atual == artesao
	if (1):
		# SE pouca massa (-25%)
		if (massa < pouca_massa):
			################### aloca o artesao para preparacao da massa
			# Fazer massa - fazer_massa
			DCA_fazer_massa()
		# SE pouca pedra (-25%)
		elif (pedra < pouca_pedra):
			################### aloca o artesao para coleta de pedra
			# Coletar pedra - coleta_pedra
			DCA_coleta_pedra()
		# SE vaso na fila de envernizacao geral
		elif (vasos.search_vaso('ENVERNIZACAO_GERAL')):
			# desenfilera vaso da fila envernizacao geral
			v = vasos.remove_vaso('ENVERNIZACAO_GERAL')
			################### aloca o artesao para envernizacao
			# Envernizacao Geral - envernizacao_geral()
			DCA_envernizacao_geral()
		# SE vaso na fila de impermeabilizacao interna
		elif (vasos.search_vaso('IMPERMEABILIZACAO_INTERNA')):
			# desenfilera vaso da fila impermeabilizacao interna
			v = vasos.remove_vaso('IMPERMEABILIZACAO_INTERNA')
			################### aloca o artesao para impermeabilizacao
			# Impermeabilizacao Interna - impermeabilizacao_interna()
			DCA_impermeabilizacao_interna()
		# SE vaso na fila de limpeza acabamento boca
		elif (vasos.search_vaso('LIMPEZA_ACABAMENTO_BOCA')):
			# desenfilera vaso da fila limpeza acabamento boca
			v = vasos.remove_vaso('LIMPEZA_ACABAMENTO_BOCA')
			################### aloca o artesao para limpeza
			# limpeza acabamento boca - limpeza_acabamento_boca()
			DCA_limpeza_acabamento_boca()
		# SE vaso na fila de preparacao boca
		elif (vasos.search_vaso('PREPARACAO_BOCA')):
			# desenfilera vaso da fila preparacao boca
			v = vasos.remove_vaso('PREPARACAO_BOCA')
			################### aloca o artesao para preparacao
			# preparacao boca - preparacao_boca()
			DCA_preparacao_boca()
		# SE vaso na fila de limpeza acabamento base
		elif (vasos.search_vaso('LIMPEZA_ACABAMENTO_BASE')):
			# desenfilera vaso da fila limpeza acabamento base
			v = vasos.remove_vaso('LIMPEZA_ACABAMENTO_BASE')
			################### aloca o artesao para limpeza
			# limpeza acabamento base - limpeza_acabamento_base()
			DCA_limpeza_acabamento_base()
		# SE vaso na fila inicial
		elif (vasos.search_vaso('PREPARACAO_FORMA')):
			# desenfilera vaso da fila inicial
			v = vasos.remove_vaso('PREPARACAO_FORMA')
			################### aloca o artesao para fila inicial
			# fila inicial - preparacao_forma()
			DCA_preparacao_forma()
		else:
			################### libera artesao
			pass

	x = getSizeVaso(vaso.get_size())
	rand = np.random.triangular(x[0], x[1], x[2])
	# rand = np.random.triangular(3, 8, 12)
	# Evento: atualiza tempos do sistema
	fel.insert_fel('SECAGEM_BOCA', time_system + rand)
	DCA_impermeabilizacao_interna()
	print('fim - SECAGEM_BOCA')


################### Existe uma fila entre essas 2 atividades

def DCA_impermeabilizacao_interna():
	print('inicio - IMPERMEABILIZACAO_INTERNA')
	if haveArtisan():
		spec = getArtisan()
		# sorteia tempo de preparacao da boca
		x = getSizeVaso(vaso.get_size())
		rand = np.random.triangular(x[0], x[1], x[2])
		# rand = np.random.triangular(3, 5, 8)
		# Evento: atualiza tempos do sistema
		fel.insert_fel('IMPERMEABILIZACAO_INTERNA', time_system + rand)
	else:
		vasos.insert_vaso('IMPERMEABILIZACAO_INTERNA', time_system)
	DCA_secagem_interna()
	print('fim - IMPERMEABILIZACAO_INTERNA')


def DCA_secagem_interna():
	print('inicio - SECAGEM_INTERNA')
	# SE pouca massa (-25%)
	if (massa < pouca_massa):
		################### aloca o artesao para preparacao da massa
		# Fazer massa - fazer_massa
		DCA_fazer_massa()
	# SE pouca pedra (-25%)
	elif (pedra < pouca_pedra):
		################### aloca o artesao para coleta de pedra
		# Coletar pedra - coleta_pedra
		DCA_coleta_pedra()
	# SE vaso na fila de envernizacao geral
	elif (vasos.search_vaso('ENVERNIZACAO_GERAL')):
		# desenfilera vaso da fila envernizacao geral
		v = vasos.remove_vaso('ENVERNIZACAO_GERAL')
		################### aloca o artesao para envernizacao
		# Envernizacao Geral - envernizacao_geral()
		DCA_envernizacao_geral()
	# SE vaso na fila de impermeabilizacao interna
	elif (vasos.search_vaso('IMPERMEABILIZACAO_INTERNA')):
		# desenfilera vaso da fila impermeabilizacao interna
		v = vasos.remove_vaso('IMPERMEABILIZACAO_INTERNA')
		################### aloca o artesao para impermeabilizacao
		# Impermeabilizacao Interna - impermeabilizacao_interna()
		DCA_impermeabilizacao_interna()
	# SE vaso na fila de limpeza acabamento boca
	elif (vasos.search_vaso('LIMPEZA_ACABAMENTO_BOCA')):
		# desenfilera vaso da fila limpeza acabamento boca
		v = vasos.remove_vaso('LIMPEZA_ACABAMENTO_BOCA')
		################### aloca o artesao para limpeza
		# limpeza acabamento boca - limpeza_acabamento_boca()
		DCA_limpeza_acabamento_boca()
	# SE vaso na fila de preparacao boca
	elif (vasos.search_vaso('PREPARACAO_BOCA')):
		# desenfilera vaso da fila preparacao boca
		v = vasos.remove_vaso('PREPARACAO_BOCA')
		################### aloca o artesao para preparacao
		# preparacao boca - preparacao_boca()
		DCA_preparacao_boca()
	# SE vaso na fila de limpeza acabamento base
	elif (vasos.search_vaso('LIMPEZA_ACABAMENTO_BASE')):
		# desenfilera vaso da fila limpeza acabamento base
		v = vasos.remove_vaso('LIMPEZA_ACABAMENTO_BASE')
		################### aloca o artesao para limpeza
		# limpeza acabamento base - limpeza_acabamento_base()
		DCA_limpeza_acabamento_base()
	# SE vaso na fila inicial
	elif (vasos.search_vaso('PREPARACAO_FORMA')):
		# desenfilera vaso da fila inicial
		v = vasos.remove_vaso('PREPARACAO_FORMA')
		################### aloca o artesao para fila inicial
		# fila inicial - preparacao_forma()
		DCA_preparacao_forma()
	else:
		################### libera artesao
		pass

	x = getSizeVaso(vaso.get_size())
	rand = np.random.triangular(x[0], x[1], x[2])
	# rand = np.random.triangular(6, 8, 10)
	# Evento: atualiza tempos do sistema
	fel.insert_fel('SECAGEM_INTERNA', time_system + rand)
	DCA_envernizacao_geral()
	print('fim - SECAGEM_INTERNA')


################### Existe uma fila entre essas 2 atividades

def DCA_envernizacao_geral():
	print('inicio - ENVERNIZACAO_GERAL')
	if haveArtisan():
		spec = getArtisan()
		# sorteia tempo de preparacao da boca
		x = getSizeVaso(vaso.get_size())
		rand = np.random.triangular(x[0], x[1], x[2])
		# rand = np.random.triangular(10, 18, 25)
		# Evento: atualiza tempos do sistema
		fel.insert_fel('ENVERNIZACAO_GERAL', time_system + rand)
	else:
		vasos.insert_vaso('ENVERNIZACAO_GERAL', time_system)
	DCA_secagem_envernizacao()
	print('fim - ENVERNIZACAO_GERAL')


def DCA_secagem_envernizacao():
	print('inicio - SECAGEM_ENVERNIZACAO')
	# SE pouca massa (-25%)
	if (massa < pouca_massa):
		################### aloca o artesao para preparacao da massa
		# Fazer massa - fazer_massa
		DCA_fazer_massa()
	# SE pouca pedra (-25%)
	elif (pedra < pouca_pedra):
		################### aloca o artesao para coleta de pedra
		# Coletar pedra - coleta_pedra
		DCA_coleta_pedra()
	# SE vaso na fila de envernizacao geral
	elif (vasos.search_vaso('ENVERNIZACAO_GERAL')):
		# desenfilera vaso da fila envernizacao geral
		v = vasos.remove_vaso('ENVERNIZACAO_GERAL')
		################### aloca o artesao para envernizacao
		# Envernizacao Geral - envernizacao_geral()
		DCA_envernizacao_geral()
	# SE vaso na fila de impermeabilizacao interna
	elif (vasos.search_vaso('IMPERMEABILIZACAO_INTERNA')):
		# desenfilera vaso da fila impermeabilizacao interna
		v = vasos.remove_vaso('IMPERMEABILIZACAO_INTERNA')
		################### aloca o artesao para impermeabilizacao
		# Impermeabilizacao Interna - impermeabilizacao_interna()
		DCA_impermeabilizacao_interna()
	# SE vaso na fila de limpeza acabamento boca
	elif (vasos.search_vaso('LIMPEZA_ACABAMENTO_BOCA')):
		# desenfilera vaso da fila limpeza acabamento boca
		v = vasos.remove_vaso('LIMPEZA_ACABAMENTO_BOCA')
		################### aloca o artesao para limpeza
		# limpeza acabamento boca - limpeza_acabamento_boca()
		DCA_limpeza_acabamento_boca()
	# SE vaso na fila de preparacao boca
	elif (vasos.search_vaso('PREPARACAO_BOCA')):
		# desenfilera vaso da fila preparacao boca
		v = vasos.remove_vaso('PREPARACAO_BOCA')
		################### aloca o artesao para preparacao
		# preparacao boca - preparacao_boca()
		DCA_preparacao_boca()
	# SE vaso na fila de limpeza acabamento base
	elif (vasos.search_vaso('LIMPEZA_ACABAMENTO_BASE')):
		# desenfilera vaso da fila limpeza acabamento base
		v = vasos.remove_vaso('LIMPEZA_ACABAMENTO_BASE')
		################### aloca o artesao para limpeza
		# limpeza acabamento base - limpeza_acabamento_base()
		DCA_limpeza_acabamento_base()
	# SE vaso na fila inicial
	elif (vasos.search_vaso('PREPARACAO_FORMA')):
		# desenfilera vaso da fila inicial
		v = vasos.remove_vaso('PREPARACAO_FORMA')
		################### aloca o artesao para fila inicial
		# fila inicial - preparacao_forma()
		DCA_preparacao_forma()
	else:
		################### libera artesao
		pass

	print('FINAL')
	x = getSizeVaso(vaso.get_size())
	rand = np.random.triangular(x[0], x[1], x[2])
	# rand = np.random.triangular(18, 20, 22)
	# Evento: atualiza tempos do sistema
	fel.insert_fel('SECAGEM_ENVERNIZACAO', time_system + rand)
	print('fim - SECAGEM_ENVERNIZACAO')

for i in range(CONST.get_NUM_ART()):
	artesoes.append(Artesao.Artesao())
for i in range(CONST.get_NUM_ESP()):
	artesoes.append(Artesao.Artesao(True))

DCA_chegada_pedido()