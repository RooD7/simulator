class Const(object):
	
	G_TSM 			= None
	NUM_ART 		= None
	NUM_ESP			= None
	ESP_SEC			= None
	USO_ESP			= None
	QTD_MASSA		= None
	USO_MASSA		= None
	QTD_MASSA_MAX	= None
	QTD_PEDRA		= None
	USO_PEDRA		= None
	QTD_PEDRA_MAX	= None
	PROBS			= []
	TAM_PED 		= []
	FREQ_PED 		= []
	PREP_PEDRA		= []
	PREP_MASSA		= []
	PREP_FORM 		= []
	PREP_BASE 		= []
	PREP_INI_BASE 	= []
	SEC_ACAB		= []		
	LIMP_ACAB_BASE	= []
	SEC_BASE		= []
	PREP_BOCA		= []
	ACAB_INI_BOCA	= []
	SEC_ACAB_BOCA	= []
	LIMP_ACAB_BOCA	= []
	SEC_BOCA		= []
	IMP_INTERNA		= []
	SEC_INTERNA		= []
	ENV_GERAL		= []
	SEC_FINAL 		= []
	ARQ_LOG			= None

	def __init__(self):
		pass

	def set_G_TSM(self, x):
		self.__G_TSM = x

	def set_NUM_ART(self, x):
		self.__NUM_ART = x

	def set_NUM_ESP(self, x):
		self.__NUM_ESP = x

	def set_ESP_SEC(self, x):
		self.__ESP_SEC = x
	
	def set_USO_ESP(self, x, y, z):
		self.__USO_ESP = [x, y, z]

	def set_QTD_MASSA(self, x):
		self.__QTD_MASSA = x

	def set_USO_MASSA(self, x, y, z):
		self.__USO_MASSA = [x, y, z]

	def set_QTD_MASSA_MAX(self, x):
		self.__QTD_MASSA_MAX = x

	def set_QTD_PEDRA(self, x):
		self.__QTD_PEDRA = x

	def set_USO_PEDRA(self, x, y, z):
		self.__USO_PEDRA = [x, y, z]

	def set_QTD_PEDRA_MAX(self, x):
		self.__QTD_PEDRA_MAX = x

	def set_PROBS(self, x, y, z):
		self.__PROBS = [x, y, z]

	def set_TAM_PED(self, x, y, z):
		self.__TAM_PED = [x, y, z]

	def set_FREQ_PED(self, x, y, z):
		self.__FREQ_PED = [x, y, z]

	def set_PREP_PEDRA(self, x, y, z):
		self.__PREP_PEDRA = [x, y, z]

	def set_PREP_MASSA(self, x, y, z):
		self.__PREP_MASSA = [x, y, z]

	def set_PREP_FORM(self, s1, s2, s3, m1, m2, m3, b1, b2, b3):
		self.__PREP_FORM = [[s1,s2,s3],[m1,m2,m3],[b1,b2,b3]]

	def set_PREP_BASE(self, s1, s2, s3, m1, m2, m3, b1, b2, b3):
		self.__PREP_BASE = [[s1,s2,s3],[m1,m2,m3],[b1,b2,b3]]

	def set_PREP_INI_BASE(self, s1, s2, s3, m1, m2, m3, b1, b2, b3):
		self.__PREP_INI_BASE = [[s1,s2,s3],[m1,m2,m3],[b1,b2,b3]]

	def set_SEC_ACAB(self, s1, s2, s3, m1, m2, m3, b1, b2, b3):
		self.__SEC_ACAB = [[s1,s2,s3],[m1,m2,m3],[b1,b2,b3]]

	def set_LIMP_ACAB_BASE(self, s1, s2, s3, m1, m2, m3, b1, b2, b3):
		self.__LIMP_ACAB_BASE = [[s1,s2,s3],[m1,m2,m3],[b1,b2,b3]]

	def set_SEC_BASE(self, s1, s2, s3, m1, m2, m3, b1, b2, b3):
		self.__SEC_BASE = [[s1,s2,s3],[m1,m2,m3],[b1,b2,b3]]

	def set_PREP_BOCA(self, s1, s2, s3, m1, m2, m3, b1, b2, b3):
		self.__PREP_BOCA = [[s1,s2,s3],[m1,m2,m3],[b1,b2,b3]]

	def set_ACAB_INI_BOCA(self, s1, s2, s3, m1, m2, m3, b1, b2, b3):
		self.__ACAB_INI_BOCA = [[s1,s2,s3],[m1,m2,m3],[b1,b2,b3]]

	def set_SEC_ACAB_BOCA(self, s1, s2, s3, m1, m2, m3, b1, b2, b3):
		self.__SEC_ACAB_BOCA = [[s1,s2,s3],[m1,m2,m3],[b1,b2,b3]]

	def set_LIMP_ACAB_BOCA(self, s1, s2, s3, m1, m2, m3, b1, b2, b3):
		self.__LIMP_ACAB_BOCA = [[s1,s2,s3],[m1,m2,m3],[b1,b2,b3]]

	def set_SEC_BOCA(self, s1, s2, s3, m1, m2, m3, b1, b2, b3):
		self.__SEC_BOCA = [[s1,s2,s3],[m1,m2,m3],[b1,b2,b3]]

	def set_IMP_INTERNA(self, s1, s2, s3, m1, m2, m3, b1, b2, b3):
		self.__IMP_INTERNA = [[s1,s2,s3],[m1,m2,m3],[b1,b2,b3]]

	def set_SEC_INTERNA(self, s1, s2, s3, m1, m2, m3, b1, b2, b3):
		self.__SEC_INTERNA = [[s1,s2,s3],[m1,m2,m3],[b1,b2,b3]]

	def set_ENV_GERAL(self, s1, s2, s3, m1, m2, m3, b1, b2, b3):
		self.__ENV_GERAL = [[s1,s2,s3],[m1,m2,m3],[b1,b2,b3]]	

	def set_SEC_FINAL(self, s1, s2, s3, m1, m2, m3, b1, b2, b3):
		self.__SEC_FINAL = [[s1,s2,s3],[m1,m2,m3],[b1,b2,b3]]	

	def set_ARQ_LOG(self, x):
		self.__ARQ_LOG = x

	def get_G_TSM(self):
		return self.__G_TSM

	def get_NUM_ART(self):
		return self.__NUM_ART

	def get_NUM_ESP(self):
		return self.__NUM_ESP

	def get_ESP_SEC(self):
		return self.__ESP_SEC

	def get_USO_ESP(self, x):
		if x == 'S':
			return self.__USO_ESP[0]
		elif x == 'M':
			return self.__USO_ESP[1]
		elif x == 'B':
			return self.__USO_ESP[2]

	def get_QTD_MASSA(self):
		return self.__QTD_MASSA

	def get_USO_MASSA(self, x):
		if x == 'S':
			return self.__USO_MASSA[0]
		elif x == 'M':
			return self.__USO_MASSA[1]
		elif x == 'B':
			return self.__USO_MASSA[2]

	def get_QTD_MASSA_MAX(self):
		return self.__QTD_MASSA_MAX

	def get_QTD_PEDRA(self):
		return self.__QTD_PEDRA

	def get_USO_PEDRA(self, x):
		if x == 'S':
			return self.__USO_PEDRA[0]
		elif x == 'M':
			return self.__USO_PEDRA[1]
		elif x == 'B':
			return self.__USO_PEDRA[2]

	def get_QTD_PEDRA_MAX(self):
		return self.__QTD_PEDRA_MAX

	def get_PROBS(self):
		return self.__PROBS

	def get_TAM_PED(self):
		return self.__TAM_PED

	def get_FREQ_PED(self):
		return self.__FREQ_PED

	def get_PREP_PEDRA(self):
		return self.__PREP_PEDRA
	
	def get_PREP_MASSA(self):
		return self.__PREP_MASSA

	def get_PREP_FORM(self, x):
		if x == 'S':
			return self.__PREP_FORM[0]
		elif x == 'M':
			return self.__PREP_FORM[1]
		elif x == 'B':
			return self.__PREP_FORM[2]

	def get_PREP_BASE(self, x):
		if x == 'S':
			return self.__PREP_BASE[0]
		elif x == 'M':
			return self.__PREP_BASE[1]
		elif x == 'B':
			return self.__PREP_BASE[2]

	def get_PREP_INI_BASE(self, x):
		if x == 'S':
			return self.__PREP_INI_BASE[0]
		elif x == 'M':
			return self.__PREP_INI_BASE[1]
		elif x == 'B':
			return self.__PREP_INI_BASE[2]

	def get_SEC_ACAB(self, x):
		if x == 'S':
			return self.__SEC_ACAB[0]
		elif x == 'M':
			return self.__SEC_ACAB[1]
		elif x == 'B':
			return self.__SEC_ACAB[2]

	def get_LIMP_ACAB_BASE(self, x):
		if x == 'S':
			return self.__LIMP_ACAB_BASE[0]
		elif x == 'M':
			return self.__LIMP_ACAB_BASE[1]
		elif x == 'B':
			return self.__LIMP_ACAB_BASE[2]

	def get_SEC_BASE(self, x):
		if x == 'S':
			return self.__SEC_BASE[0]
		elif x == 'M':
			return self.__SEC_BASE[1]
		elif x == 'B':
			return self.__SEC_BASE[2]

	def get_PREP_BOCA(self, x):
		if x == 'S':
			return self.__PREP_BOCA[0]
		elif x == 'M':
			return self.__PREP_BOCA[1]
		elif x == 'B':
			return self.__PREP_BOCA[2]

	def get_ACAB_INI_BOCA(self, x):
		if x == 'S':
			return self.__ACAB_INI_BOCA[0]
		elif x == 'M':
			return self.__ACAB_INI_BOCA[1]
		elif x == 'B':
			return self.__ACAB_INI_BOCA[2]

	def get_SEC_ACAB_BOCA(self, x):
		if x == 'S':
			return self.__SEC_ACAB_BOCA[0]
		elif x == 'M':
			return self.__SEC_ACAB_BOCA[1]
		elif x == 'B':
			return self.__SEC_ACAB_BOCA[2]

	def get_LIMP_ACAB_BOCA(self, x):
		if x == 'S':
			return self.__LIMP_ACAB_BOCA[0]
		elif x == 'M':
			return self.__LIMP_ACAB_BOCA[1]
		elif x == 'B':
			return self.__LIMP_ACAB_BOCA[2]

	def get_SEC_BOCA(self, x):
		if x == 'S':
			return self.__SEC_BOCA[0]
		elif x == 'M':
			return self.__SEC_BOCA[1]
		elif x == 'B':
			return self.__SEC_BOCA[2]

	def get_IMP_INTERNA(self, x):
		if x == 'S':
			return self.__IMP_INTERNA[0]
		elif x == 'M':
			return self.__IMP_INTERNA[1]
		elif x == 'B':
			return self.__IMP_INTERNA[2]

	def get_SEC_INTERNA(self, x):
		if x == 'S':
			return self.__SEC_INTERNA[0]
		elif x == 'M':
			return self.__SEC_INTERNA[1]
		elif x == 'B':
			return self.__SEC_INTERNA[2]

	def get_ENV_GERAL(self, x):
		if x == 'S':
			return self.__ENV_GERAL[0]
		elif x == 'M':
			return self.__ENV_GERAL[1]
		elif x == 'B':
			return self.__ENV_GERAL[2]

	def get_SEC_FINAL(self, x):
		if x == 'S':
			return self.__SEC_FINAL[0]
		elif x == 'M':
			return self.__SEC_FINAL[1]
		elif x == 'B':
			return self.__SEC_FINAL[2]

	def get_ARQ_LOG(self):
		return self.__ARQ_LOG