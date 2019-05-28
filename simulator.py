import vaso as Vaso
import inputFile as InputFile

class simulator:
	vaso1 = Vaso.Vaso(10,'B',0)
	print(vaso1.get_id())

	inpFile = InputFile.InputFile()
	txt = inpFile.inputs('entrada.txt')
	for l in txt:
		if (l[0] != '#') and (l[0] != '\n'):
			print(l)
	# print(txt)

# if __name__ == '__main__':
# 	main()