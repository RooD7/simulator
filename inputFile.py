import os
import re
import const as Const

class InputFile(object):
	def __init__(self):
		self.lines = []
		self.CONST = Const.Const()

	def inputs(self, patchFile):
		if os.path.isfile(patchFile):
			file = open(patchFile,'r')
			for l in file:
				if (l[0] != '#') and (l[0] != '\n'):
					result = re.match('(G TSM )(.{1,20})', l)
					if result:
						self.CONST.set_G_TSM(int(result.group(2)))
						#print(l)
					result = re.match('(num_art )(.{1,20})', l)
					if result:
						self.CONST.set_NUM_ART(int(result.group(2)))
						#print(l)
					result = re.match('(num_esp )(.{1,20})', l)
					if result:
						self.CONST.set_NUM_ESP(int(result.group(2)))
						#print(l)
					result = re.match('(esp_sec )(.{1,20})', l)
					if result:
						self.CONST.set_ESP_SEC(int(result.group(2)))
						#print(l)
					result = re.match('(uso_espaco )(.{1,20}) (.{1,20}) (.{1,20})', l)
					if result:
						self.CONST.set_USO_ESP(int(result.group(2)), 
												int(result.group(3)), 
												int(result.group(4)))
						#print(l)
					result = re.match('(qtd_massa )(.{1,20})', l)
					if result:
						self.CONST.set_QTD_MASSA(int(result.group(2)))
						#print(l)
					result = re.match('(uso_massa )(.{1,20}) (.{1,20}) (.{1,20})', l)
					if result:
						self.CONST.set_USO_MASSA(int(result.group(2)), 
												int(result.group(3)), 
												int(result.group(4)))
						#print(l)
					result = re.match('(qtd_massa_max )(.{1,20})', l)
					if result:
						self.CONST.set_QTD_MASSA_MAX(int(result.group(2)))
						#print(l)
					result = re.match('(qtd_pedra )(.{1,20})', l)
					if result:
						self.CONST.set_QTD_PEDRA(int(result.group(2)))
						#print(l)
					result = re.match('(uso_pedra )(.{1,20}) (.{1,20}) (.{1,20})', l)
					if result:
						self.CONST.set_USO_PEDRA(int(result.group(2)), 
												int(result.group(3)), 
												int(result.group(4)))
						#print(l)
					result = re.match('(qtd_pedra_max )(.{1,20})', l)
					if result:
						self.CONST.set_QTD_PEDRA_MAX(int(result.group(2)))
						#print(l)
					result = re.match('(probs )(.{1,20}) (.{1,20}) (.{1,20})', l)
					if result:
						self.CONST.set_PROBS(float(result.group(2)), 
											float(result.group(3)), 
											float(result.group(4)))
						#print(l)
					result = re.match('(tam_ped )(.{1,20}) (.{1,20}) (.{1,20})', l)
					if result:
						self.CONST.set_TAM_PED(int(result.group(2)), 
											   int(result.group(3)), 
											   int(result.group(4)))
						#print(l)
					result = re.match('(freq_ped )(.{1,20}) (.{1,20}) (.{1,20})', l)
					if result:
						self.CONST.set_FREQ_PED(int(result.group(2)), 
												int(result.group(3)), 
												int(result.group(4)))
						#print(l)
					result = re.match('(prep_massa )(.{1,20}) (.{1,20}) (.{1,20})', l)
					if result:
						self.CONST.set_PREP_MASSA(int(result.group(2)), 
												  int(result.group(3)), 
												  int(result.group(4)))
						#print(l)
					result = re.match('(prep_pedra )(.{1,20}) (.{1,20}) (.{1,20})', l)
					if result:
						self.CONST.set_PREP_PEDRA(int(result.group(2)), 
												  int(result.group(3)), 
												  int(result.group(4)))
						#print(l)
					result = re.match('(prep_form )(.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20})', l)
					if result:
						self.CONST.set_PREP_FORM(int(result.group(2)), 
												 int(result.group(3)), 
												 int(result.group(4)), 
												 int(result.group(5)), 
												 int(result.group(6)),
												 int(result.group(7)), 
												 int(result.group(8)), 
												 int(result.group(9)), 
												 int(result.group(10)))
						#print(l)
					result = re.match('(prep_base )(.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20})', l)
					if result:
						self.CONST.set_PREP_BASE(int(result.group(2)), 
												 int(result.group(3)), 
												 int(result.group(4)), 
												 int(result.group(5)), 
												 int(result.group(6)),
												 int(result.group(7)), 
												 int(result.group(8)), 
												 int(result.group(9)), 
												 int(result.group(10)))
						#print(l)
					result = re.match('(prep_ini_base )(.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20})', l)
					if result:
						self.CONST.set_PREP_INI_BASE(int(result.group(2)), 
													int(result.group(3)), 
													int(result.group(4)), 
													int(result.group(5)), 
													int(result.group(6)),
													int(result.group(7)), 
													int(result.group(8)), 
													int(result.group(9)), 
													int(result.group(10)))
						#print(l)
					result = re.match('(sec_acab )(.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20})', l)
					if result:
						self.CONST.set_SEC_ACAB(int(result.group(2)), 
												 int(result.group(3)), 
												 int(result.group(4)), 
												 int(result.group(5)), 
												 int(result.group(6)),
												 int(result.group(7)), 
												 int(result.group(8)), 
												 int(result.group(9)), 
												 int(result.group(10)))
						#print(l)
					result = re.match('(limp_acab_base )(.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20})', l)
					if result:
						self.CONST.set_LIMP_ACAB_BASE(int(result.group(2)), 
												 int(result.group(3)), 
												 int(result.group(4)), 
												 int(result.group(5)), 
												 int(result.group(6)),
												 int(result.group(7)), 
												 int(result.group(8)), 
												 int(result.group(9)), 
												 int(result.group(10)))
						#print(l)
					result = re.match('(sec_base )(.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20})', l)
					if result:
						self.CONST.set_SEC_BASE(int(result.group(2)), 
												 int(result.group(3)), 
												 int(result.group(4)), 
												 int(result.group(5)), 
												 int(result.group(6)),
												 int(result.group(7)), 
												 int(result.group(8)), 
												 int(result.group(9)), 
												 int(result.group(10)))
						#print(l)
					result = re.match('(prep_boca )(.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20})', l)
					if result:
						self.CONST.set_PREP_BOCA(int(result.group(2)), 
												 int(result.group(3)), 
												 int(result.group(4)), 
												 int(result.group(5)), 
												 int(result.group(6)),
												 int(result.group(7)), 
												 int(result.group(8)), 
												 int(result.group(9)), 
												 int(result.group(10)))
						#print(l)
					result = re.match('(acab_ini_boca )(.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20})', l)
					if result:
						self.CONST.set_ACAB_INI_BOCA(int(result.group(2)), 
												 int(result.group(3)), 
												 int(result.group(4)), 
												 int(result.group(5)), 
												 int(result.group(6)),
												 int(result.group(7)), 
												 int(result.group(8)), 
												 int(result.group(9)), 
												 int(result.group(10)))
						#print(l)
					result = re.match('(sec_acab_boca )(.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20})', l)
					if result:
						self.CONST.set_SEC_ACAB_BOCA(int(result.group(2)), 
												 int(result.group(3)), 
												 int(result.group(4)), 
												 int(result.group(5)), 
												 int(result.group(6)),
												 int(result.group(7)), 
												 int(result.group(8)), 
												 int(result.group(9)), 
												 int(result.group(10)))
						#print(l)
					result = re.match('(limp_acab_boca )(.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20})', l)
					if result:
						self.CONST.set_LIMP_ACAB_BOCA(int(result.group(2)), 
												 int(result.group(3)), 
												 int(result.group(4)), 
												 int(result.group(5)), 
												 int(result.group(6)),
												 int(result.group(7)), 
												 int(result.group(8)), 
												 int(result.group(9)), 
												 int(result.group(10)))
						#print(l)
					result = re.match('(sec_boca )(.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20})', l)
					if result:
						self.CONST.set_SEC_BOCA(int(result.group(2)), 
												 int(result.group(3)), 
												 int(result.group(4)), 
												 int(result.group(5)), 
												 int(result.group(6)),
												 int(result.group(7)), 
												 int(result.group(8)), 
												 int(result.group(9)), 
												 int(result.group(10)))
						#print(l)
					result = re.match('(imp_interna )(.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20})', l)
					if result:
						self.CONST.set_IMP_INTERNA(int(result.group(2)), 
												 int(result.group(3)), 
												 int(result.group(4)), 
												 int(result.group(5)), 
												 int(result.group(6)),
												 int(result.group(7)), 
												 int(result.group(8)), 
												 int(result.group(9)), 
												 int(result.group(10)))
						#print(l)
					result = re.match('(sec_interna )(.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20})', l)
					if result:
						self.CONST.set_SEC_INTERNA(int(result.group(2)), 
												 int(result.group(3)), 
												 int(result.group(4)), 
												 int(result.group(5)), 
												 int(result.group(6)),
												 int(result.group(7)), 
												 int(result.group(8)), 
												 int(result.group(9)), 
												 int(result.group(10)))
						#print(l)
					result = re.match('(env_geral )(.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20})', l)
					if result:
						self.CONST.set_ENV_GERAL(int(result.group(2)), 
												 int(result.group(3)), 
												 int(result.group(4)), 
												 int(result.group(5)), 
												 int(result.group(6)),
												 int(result.group(7)), 
												 int(result.group(8)), 
												 int(result.group(9)), 
												 int(result.group(10)))
						#print(l)
					result = re.match('(sec_final )(.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20}) (.{1,20})', l)
					if result:
						self.CONST.set_SEC_FINAL(int(result.group(2)), 
												 int(result.group(3)), 
												 int(result.group(4)), 
												 int(result.group(5)), 
												 int(result.group(6)),
												 int(result.group(7)), 
												 int(result.group(8)), 
												 int(result.group(9)), 
												 int(result.group(10)))
						#print(l)
					result = re.match('(.{1,30})(.txt)', l)
					if result:
						self.CONST.set_ARQ_LOG(l)
						#print(l)
			file.close()
			
		else:
			self.CONST = None		
			#print('Arquivo informado nao existe!')
			exit()

		return self.CONST

	def get_CONST(self):
		return self.CONST