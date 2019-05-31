class Const(object):
	
	G_TSM 			= None
	NUM_ART 		= None
	NUM_ESP			= None
	ESP_SEC			= None
	PROBS			= []
	TAM_PED 		= []
	FREQ_PED 		= None
	PREP_FORM 		= []
	PREP_BASE 		= []
	PREP_INI_BASE 	= []
	SEC_ACAB		= []		
	LIMP_ACAB		= []
	SEC_BAS			= []
	PREP_BOCA		= []
	AVAB_INI_BOCA	= []
	SEC_ACAB_BOCA	= []
	LIMP_ACAB_BOCA	= []
	SEC_BOCA		= []
	IMP_INTERNA		= []
	SEC_INTERNA		= []
	ENV_GERAL		= []
	SEC_FINAL 		= []

	def __init__(self):
		pass

	def set_G_TSM(self, x):
		self.G_TSM = x

	def set_NUM_ART(self, x):
		self.NUM_ART = x

	def set_NUM_ESP(self, x):
		self.NUM_ESP = x

	def set_ESP_SEC(self, x):
		self.ESP_SEC = x

	def set_PROBS(self, x, y, z):
		self.PROBS = [x,y,z]

	def set_TAM_PED(self, x, y, z):
		self.TAM_PED = [x,y,z]

	def set_FREQ_PED(self, x):
		self.FREQ_PED = x

	def set_PREP_FORM(self, x, y, z):
		self.PREP_FORM = [x,y,z]

	def set_PREP_BASE(self, x, y, z):
		self.PREP_BASE = [x,y,z]

	def set_PREP_INI_BASE(self, x, y, z):
		self.PREP_INI_BASE = [x,y,z]

	def set_SEC_ACAB(self, x, y, z):
		self.SEC_ACAB = [x,y,z]

	def set_LIMP_ACAB(self, x, y, z):
		self.LIMP_ACAB = [x,y,z]

	def set_SEC_BAS(self, x, y, z):
		self.SEC_BAS = [x,y,z]

	def set_PREP_BOCA(self, x, y, z):
		self.PREP_BOCA = [x,y,z]

	def set_AVAB_INI_BOCA(self, x, y, z):
		self.AVAB_INI_BOCA = [x,y,z]

	def set_SEC_ACAB_BOCA(self, x, y, z):
		self.SEC_ACAB_BOCA = [x,y,z]

	def set_LIMP_ACAB_BOCA(self, x, y, z):
		self.LIMP_ACAB_BOCA = [x,y,z]

	def set_SEC_BOCA(self, x, y, z):
		self.SEC_BOCA = [x,y,z]

	def set_IMP_INTERNA(self, x, y, z):
		self.IMP_INTERNA = [x,y,z]

	def set_SEC_INTERNA(self, x, y, z):
		self.SEC_INTERNA = [x,y,z]

	def set_ENV_GERAL(self, x, y, z):
		self.ENV_GERAL = [x,y,z]	

	def set_SEC_FINAL(self, x, y, z):
		self.SEC_FINAL = [x,y,z]	

	def get_G_TSM(self):
		return self.G_TSM

	def get_NUM_ART(self):
		return self.NUM_ART

	def get_NUM_ESP(self):
		return self.NUM_ESP

	def get_ESP_SEC(self):
		return self.ESP_SEC

	def get_PROBS(self):
		return self.PROBS

	def get_TAM_PED(self):
		return self.TAM_PED

	def get_FREQ_PED(self):
		return self.FREQ_PED

	def get_PREP_FORM(self):
		return self.PREP_FORM

	def get_PREP_BASE(self):
		return self.PREP_BASE

	def get_PREP_INI_BASE(self):
		return self.PREP_INI_BASE

	def get_SEC_ACAB(self):
		return self.SEC_ACAB

	def get_LIMP_ACAB(self):
		return self.LIMP_ACAB

	def get_SEC_BAS(self):
		return self.SEC_BAS

	def get_PREP_BOCA(self):
		return self.PREP_BOCA

	def get_AVAB_INI_BOCA(self):
		return self.AVAB_INI_BOCA

	def get_SEC_ACAB_BOCA(self):
		return self.SEC_ACAB_BOCA

	def get_SEC_BOCA(self):
		return self.SEC_BOCA

	def get_SEC_INTERNA(self):
		return self.SEC_INTERNA

	def get_ENV_GERAL(self):
		return self.ENV_GERAL

	def get_SEC_FINAL(self):
		return self.SEC_FINAL