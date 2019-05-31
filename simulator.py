import vaso as Vaso
import inputFile as InputFile
import const as Const
import fel as Fel

class simulator:
	# vaso1 = Vaso.Vaso(10,'B',0)
	# print(vaso1.get_id())
	time_system = 0

	inpFile = InputFile.InputFile()

	CONST 	= Const.Const()
	CONST 	= inpFile.inputs('entrada.txt')
	# print(CONST.get_G_TSM())

	fel = Fel.Fel()