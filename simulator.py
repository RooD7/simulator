import vaso as Vaso
import inputFile as InputFile
import const as Const
import fel as fel
import filaVaso as FilaVaso
import artesao as Artesao
import numpy as np

class simulator2(object):

    def __init__(self):
        self.fel = fel.Fel()
        self.vasos = FilaVaso.FilaVaso()

        inpFile = InputFile.InputFile()

        self.CONST = Const.Const()
        self.CONST = inpFile.inputs('entrada.txt')

        self.time_system = 0
        self.massa = self.CONST.get_QTD_MASSA()
        self.pedra = self.CONST.get_QTD_PEDRA()
        self.pouca_massa = 250
        self.pouca_pedra = 250
        self.artesoes = []
        self.uso_esp_sec = 0
        self.vaso = None
        self.artesao = None


    def haveSpecialist(self):
        for x in self.artesoes:
            if (x.isSpecialist() and x.getOciosity()):
                return True
        return False


    def getSpecialist(self):
        for x in self.artesoes:
            if (x.isSpecialist() and x.getOciosity()):
                x.setOciosity(False)
                return x
        return None


    def haveArtisan(self):
        for x in self.artesoes:
            if (not x.isSpecialist() and x.getOciosity()):
                return True
        return False


    def getArtisan(self):
        for x in self.artesoes:
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

    def DCA_fazer_massa(self):
        self.massa = self.CONST.get_QTD_MASSA_MAX


    def DCA_coleta_pedra(self):
        self.pedra = self.CONST.get_QTD_PEDRA_MAX


    def DCA_chegada_pedido(self):
        print('inicio - CHEGADA_PEDIDO')
        # frequencia de chegada de pedidos
        # tamanho do pedido (seguindo a probabilidade do CONST)
        x = self.CONST.get_TAM_PED()
        rand = np.random.triangular(x[0], x[1], x[2])
        ################### remover
        size = 'S'
        # serao feitos 'rand' pedidos
        for r in range(0, int(rand)):
            self.vasos.insert_new_vaso('PREPARACAO_FORMA', size, self.time_system)
        ################### tamanho (S - M - B) de cada vazo do pedido (seguindo a proporcao do CONST)]
        #for r in range(0, len(vasos.get_fila())):
        #	DCA_preparacao_forma()
        self.DCA_preparacao_forma()
        print('fim - CHEGADA_PEDIDO')

    ################### Existe uma fila entre essas 2 atividades

    def DCA_preparacao_forma(self):
        print('inicio - PREPARACAO_FORMA')
        if self.vasos.search_vaso('PREPARACAO_FORMA'):
            vaso = self.vasos.remove_vaso('PREPARACAO_FORMA')
            # espaco de secagem
            if (self.uso_esp_sec < self.CONST.get_ESP_SEC()):
                # massa suficiente
                if (self.massa > self.pouca_massa):
                    if self.haveSpecialist():
                        spec = self.getSpecialist()
                        # sorteia tempo de preparacao da forma
                        x = self.CONST.get_PREP_FORM(vaso.get_size())
                        rand = np.random.triangular(x[0], x[1], x[2])
                        # rand = np.random.triangular(2, 4, 6)
                        # Evento: atualiza tempos do sistema
                        self.fel.insert_fel('PREPARACAO_BASE', self.time_system + int(rand))
                        self.vasos.insert_vaso('PREPARACAO_BASE', vaso)
                    elif self.haveArtisan():
                        spec = self.getArtisan()
                        x = self.CONST.get_PREP_FORM(vaso.get_size())
                        rand = np.random.triangular(x[0], x[1], x[2])
                        # rand = np.random.triangular(2, 4, 6)
                        # Evento: atualiza tempos do sistema
                        self.fel.insert_fel('PREPARACAO_BASE', self.time_system + int(rand))
                        self.vasos.insert_vaso('PREPARACAO_BASE', vaso)
                else:
                    # coloca vaso na fila de preparacao da forma
                    self.vasos.insert_vaso('PREPARACAO_FORMA', vaso)
            else:
                # coloca vaso na fila de preparacao da forma
                self.vasos.insert_vaso('PREPARACAO_FORMA', vaso)
        print('fim - PREPARACAO_FORMA')
        self.DCA_preparacao_base()


    def DCA_preparacao_base(self):
        print('inicio - PREPARACAO_BASE')
        if self.vasos.search_vaso('PREPARACAO_BASE'):
            vaso = self.vasos.remove_vaso('PREPARACAO_BASE')
            x = self.CONST.get_PREP_BASE(vaso.get_size())
            rand = np.random.triangular(x[0], x[1], x[2])
            # rand = np.random.triangular(15, 40, 120)
            # Evento: atualiza tempos do sistema
            self.vasos.insert_vaso('ACABAMENTO_INICIAL_BASE', vaso)
            self.fel.insert_fel('ACABAMENTO_INICIAL_BASE', self.time_system + int(rand))
        print('fim - PREPARACAO_BASE')
        self.DCA_acabamento_inicial_base()

    def DCA_acabamento_inicial_base(self):
        print('inicio - ACABAMENTO_INICIAL_BASE')
        if self.vasos.search_vaso('ACABAMENTO_INICIAL_BASE'):
            vaso = self.vasos.remove_vaso('ACABAMENTO_INICIAL_BASE')
            x = self.CONST.get_ACAB_INI_BOCA(vaso.get_size())
            rand = np.random.triangular(x[0], x[1], x[2])
            # rand = np.random.triangular(2, 5, 8)
            # Evento: atualiza tempos do sistema
            self.vasos.insert_vaso('SECAGEM_ACABAMENTO_BASE', vaso)
            self.fel.insert_fel('SECAGEM_ACABAMENTO_BASE', self.time_system + int(rand))
        print('fim - ACABAMENTO_INICIAL_BASE')
        self.DCA_secagem_acabamento_base()


    def DCA_secagem_acabamento_base(self):
        print('inicio - SECAGEM_ACABAMENTO_BASE')
        if self.vasos.search_vaso('SECAGEM_ACABAMENTO_BASE'):
            vaso = self.vasos.remove_vaso('SECAGEM_ACABAMENTO_BASE')
            #################### SE recurso alocado atual == artesao
            if (1):
                # SE pouca massa (-25%)
                if (self.massa < self.pouca_massa):
                    ################### aloca o artesao para preparacao da massa
                    # Fazer massa - fazer_massa
                    self.DCA_fazer_massa()
                # SE pouca pedra (-25%)
                elif (self.pedra < self.pouca_pedra):
                    ################### aloca o artesao para coleta de pedra
                    # Coletar pedra - coleta_pedra
                    self.DCA_coleta_pedra()
                # SE vaso na fila de envernizacao geral
                elif (self.vasos.search_vaso('ENVERNIZACAO_GERAL')):
                    # desenfilera vaso da fila envernizacao geral
                    ################### v = self.vasos.remove_vaso('ENVERNIZACAO_GERAL')
                    ################### aloca o artesao para envernizacao
                    # Envernizacao Geral - envernizacao_geral()
                    self.DCA_envernizacao_geral()
                # SE vaso na fila de impermeabilizacao interna
                elif (self.vasos.search_vaso('IMPERMEABILIZACAO_INTERNA')):
                    # desenfilera vaso da fila impermeabilizacao interna
                    ################### v = self.vasos.remove_vaso('IMPERMEABILIZACAO_INTERNA')
                    ################### aloca o artesao para impermeabilizacao
                    # Impermeabilizacao Interna - impermeabilizacao_interna()
                    self.DCA_impermeabilizacao_interna()
                # SE vaso na fila de limpeza acabamento boca
                elif (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BOCA')):
                    # desenfilera vaso da fila limpeza acabamento boca
                    ################### v = self.vasos.remove_vaso('LIMPEZA_ACABAMENTO_BOCA')
                    ################### aloca o artesao para limpeza
                    # limpeza acabamento boca - limpeza_acabamento_boca()
                    self.DCA_limpeza_acabamento_boca()
                # SE vaso na fila de preparacao boca
                elif (self.vasos.search_vaso('PREPARACAO_BOCA')):
                    # desenfilera vaso da fila preparacao boca
                    ################### v = self.vasos.remove_vaso('PREPARACAO_BOCA')
                    ################### aloca o artesao para preparacao
                    # preparacao boca - preparacao_boca()
                    self.DCA_preparacao_boca()
                # SE vaso na fila de preparacao boca
                elif (self.vasos.search_vaso('ACABAMENTO_INICIAL_BASE')):
                    # desenfilera vaso da fila limpeza acabamento base
                    ################### v = self.vasos.remove_vaso('ACABAMENTO_INICIAL_BASE')
                    ################### aloca o artesao para limpeza
                    # limpeza acabamento base - limpeza_acabamento_base()
                    self.DCA_limpeza_acabamento_base()
                # SE vaso na fila inicial
                elif (self.vasos.search_vaso('PREPARACAO_FORMA')):
                    # desenfilera vaso da fila inicial
                    ################### v = self.vasos.remove_vaso('PREPARACAO_FORMA')
                    ################### aloca o artesao para fila inicial
                    # fila inicial - preparacao_forma()
                    self.DCA_preparacao_forma()
                else:
                    ################### libera artesao
                    pass
            else:
                # SE vaso na fila de limpeza acabamento boca
                if (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BOCA')):
                    # desenfilera vaso da fila limpeza acabamento boca
                    ################### v = self.vasos.remove_vaso('LIMPEZA_ACABAMENTO_BOCA')
                    ################### aloca o artesao para limpeza
                    # limpeza acabamento boca - limpeza_acabamento_boca()
                    self.DCA_limpeza_acabamento_boca()
                # SE vaso na fila de preparacao boca
                elif (self.vasos.search_vaso('PREPARACAO_BOCA')):
                    # desenfilera vaso da fila preparacao boca
                    ################### v = self.vasos.remove_vaso('PREPARACAO_BOCA')
                    ################### aloca o artesao para preparacao
                    # preparacao boca - preparacao_boca()
                    self.DCA_preparacao_boca()
                # SE vaso na fila de preparacao boca
                elif (self.vasos.search_vaso('ACABAMENTO_INICIAL_BASE')):
                    # desenfilera vaso da fila limpeza acabamento base
                    ################### v = self.vasos.remove_vaso('ACABAMENTO_INICIAL_BASE')
                    ################### aloca o artesao para limpeza
                    # limpeza acabamento base - limpeza_acabamento_base()
                    self.DCA_limpeza_acabamento_base()
                # SE vaso na fila inicial
                elif (self.vasos.search_vaso('PREPARACAO_FORMA')):
                    # desenfilera vaso da fila inicial
                    ################### v = self.vasos.remove_vaso('PREPARACAO_FORMA')
                    ################### aloca o artesao para fila inicial
                    # fila inicial - preparacao_forma()
                    self.DCA_preparacao_forma()

            x = self.CONST.get_SEC_ACAB(vaso.get_size())
            rand = np.random.triangular(x[0], x[1], x[2])
            # rand = np.random.triangular(7, 10, 14)
            # Evento: atualiza tempos do sistema
            self.vasos.insert_vaso('LIMPEZA_ACABAMENTO_BASE', vaso)
            self.fel.insert_fel('LIMPEZA_ACABAMENTO_BASE', self.time_system + int(rand))
        print('fim - SECAGEM_ACABAMENTO_BASE')
        self.DCA_limpeza_acabamento_base()

    ################### Existe uma fila entre essas 2 atividades

    def DCA_limpeza_acabamento_base(self):
        print('inicio - LIMPEZA_ACABAMENTO_BASE')
        if self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BASE'):
            vaso = self.vasos.remove_vaso('LIMPEZA_ACABAMENTO_BASE')
            if self.haveSpecialist():
                spec = self.getSpecialist()
                # sorteia tempo de limpeza acabamento base
                x = self.CONST.get_LIMP_ACAB_BASE(vaso.get_size())
                rand = np.random.triangular(x[0], x[1], x[2])
                # rand = np.random.triangular(5, 8, 11)
                # Evento: atualiza tempos do sistema
                self.vasos.insert_vaso('SECAGEM_BASE', vaso)
                self.fel.insert_fel('SECAGEM_BASE', self.time_system + int(rand))
            elif self.haveArtisan():
                spec = self.getArtisan()
                x = self.CONST.get_LIMP_ACAB_BASE(vaso.get_size())
                rand = np.random.triangular(x[0], x[1], x[2])
                # rand = np.random.triangular(5, 8, 11)
                # Evento: atualiza tempos do sistema
                self.vasos.insert_vaso('SECAGEM_BASE', vaso)
                self.fel.insert_fel('SECAGEM_BASE', self.time_system + int(rand))
            else:
                self.vasos.insert_vaso('LIMPEZA_ACABAMENTO_BASE', vaso)
        print('fim - LIMPEZA_ACABAMENTO_BASE')
        self.DCA_secagem_base()


    def DCA_secagem_base(self):
        print('inicio - SECAGEM_BASE')
        if self.vasos.search_vaso('SECAGEM_BASE'):
            vaso = self.vasos.remove_vaso('SECAGEM_BASE')
            #################### SE recurso alocado atual == artesao
            if (1):
                # SE pouca massa (-25%)
                if (self.massa < self.pouca_massa):
                    ################### aloca o artesao para preparacao da massa
                    # Fazer massa - fazer_massa
                    self.DCA_fazer_massa()
                # SE pouca pedra (-25%)
                elif (self.pedra < self.pouca_pedra):
                    ################### aloca o artesao para coleta de pedra
                    # Coletar pedra - coleta_pedra
                    self.DCA_coleta_pedra()
                # SE vaso na fila de envernizacao geral
                elif (self.vasos.search_vaso('ENVERNIZACAO_GERAL')):
                    # desenfilera vaso da fila envernizacao geral
                    ################### v = self.vasos.remove_vaso('ENVERNIZACAO_GERAL')
                    ################### aloca o artesao para envernizacao
                    # Envernizacao Geral - envernizacao_geral()
                    self.DCA_envernizacao_geral()
                # SE vaso na fila de impermeabilizacao interna
                elif (self.vasos.search_vaso('IMPERMEABILIZACAO_INTERNA')):
                    # desenfilera vaso da fila impermeabilizacao interna
                    ################### v = self.vasos.remove_vaso('IMPERMEABILIZACAO_INTERNA')
                    ################### aloca o artesao para impermeabilizacao
                    # Impermeabilizacao Interna - impermeabilizacao_interna()
                    self.DCA_impermeabilizacao_interna()
                # SE vaso na fila de limpeza acabamento boca
                elif (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BOCA')):
                    # desenfilera vaso da fila limpeza acabamento boca
                    ################### v = self.vasos.remove_vaso('LIMPEZA_ACABAMENTO_BOCA')
                    ################### aloca o artesao para limpeza
                    # limpeza acabamento boca - limpeza_acabamento_boca()
                    self.DCA_limpeza_acabamento_boca()
                # SE vaso na fila de preparacao boca
                elif (self.vasos.search_vaso('PREPARACAO_BOCA')):
                    # desenfilera vaso da fila preparacao boca
                    ################### v = self.vasos.remove_vaso('PREPARACAO_BOCA')
                    ################### aloca o artesao para preparacao
                    # preparacao boca - preparacao_boca()
                    self.DCA_preparacao_boca()
                # SE vaso na fila de limpeza acabamento base
                elif (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BASE')):
                    # desenfilera vaso da fila limpeza acabamento base
                    ################### v = self.vasos.remove_vaso('LIMPEZA_ACABAMENTO_BASE')
                    ################### aloca o artesao para limpeza
                    # limpeza acabamento base - limpeza_acabamento_base()
                    self.DCA_limpeza_acabamento_base()
                # SE vaso na fila inicial
                elif (self.vasos.search_vaso('PREPARACAO_FORMA')):
                    # desenfilera vaso da fila inicial
                    ################### v = self.vasos.remove_vaso('PREPARACAO_FORMA')
                    ################### aloca o artesao para fila inicial
                    # fila inicial - preparacao_forma()
                    self.DCA_preparacao_forma()
                else:
                    ################### libera artesao
                    pass
            else:
                # SE vaso na fila de limpeza acabamento boca
                if (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BOCA')):
                    # desenfilera vaso da fila limpeza acabamento boca
                    ################### v = self.vasos.remove_vaso('LIMPEZA_ACABAMENTO_BOCA')
                    ################### aloca o artesao para limpeza
                    # limpeza acabamento boca - limpeza_acabamento_boca()
                    self.DCA_limpeza_acabamento_boca()
                # SE vaso na fila de preparacao boca
                elif (self.vasos.search_vaso('PREPARACAO_BOCA')):
                    # desenfilera vaso da fila preparacao boca
                    ################### v = self.vasos.remove_vaso('PREPARACAO_BOCA')
                    ################### aloca o artesao para preparacao
                    # preparacao boca - preparacao_boca()
                    self.DCA_preparacao_boca()
                # SE vaso na fila de limpeza acabamento base
                elif (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BASE')):
                    # desenfilera vaso da fila limpeza acabamento base
                    ################### v = self.vasos.remove_vaso('LIMPEZA_ACABAMENTO_BASE')
                    ################### aloca o artesao para limpeza
                    # limpeza acabamento base - limpeza_acabamento_base()
                    self.DCA_limpeza_acabamento_base()
                # SE vaso na fila inicial
                elif (self.vasos.search_vaso('PREPARACAO_FORMA')):
                    # desenfilera vaso da fila inicial
                    ################### v = self.vasos.remove_vaso('PREPARACAO_FORMA')
                    ################### aloca o artesao para fila inicial
                    # fila inicial - preparacao_forma()
                    self.DCA_preparacao_forma()

            x = self.CONST.get_SEC_BASE(vaso.get_size())
            rand = np.random.triangular(x[0], x[1], x[2])
            # rand = np.random.triangular(4, 12, 24)
            # Evento: atualiza tempos do sistema
            self.vasos.insert_vaso('PREPARACAO_BOCA', vaso)
            self.fel.insert_fel('PREPARACAO_BOCA', self.time_system + int(rand))
        print('fim - SECAGEM_BASE')
        self.DCA_preparacao_boca()


    ################### Existe uma fila entre essas 2 atividades

    def DCA_preparacao_boca(self):
        print('inicio - PREPARACAO_BOCA')
        if self.vasos.search_vaso('PREPARACAO_BOCA'):
            vaso = self.vasos.remove_vaso('PREPARACAO_BOCA')
            if self.haveSpecialist():
                spec = self.getSpecialist()
                # sorteia tempo de preparacao da boca
                x = self.CONST.get_PREP_BOCA(vaso.get_size())
                rand = np.random.triangular(x[0], x[1], x[2])
                # rand = np.random.triangular(7, 10, 14)
                # Evento: atualiza tempos do sistema
                self.vasos.insert_vaso('ACABAMENTO_INICIAL_BOCA', vaso)
                self.fel.insert_fel('ACABAMENTO_INICIAL_BOCA', self.time_system + int(rand))
            elif self.haveArtisan():
                spec = self.getArtisan()
                x = self.CONST.get_PREP_BOCA(vaso.get_size())
                rand = np.random.triangular(x[0], x[1], x[2])
                # rand = np.random.triangular(7, 10, 14)
                # Evento: atualiza tempos do sistema
                self.vasos.insert_vaso('ACABAMENTO_INICIAL_BOCA', vaso)
                self.fel.insert_fel('ACABAMENTO_INICIAL_BOCA', self.time_system + int(rand))
            else:
                self.vasos.insert_vaso('PREPARACAO_BOCA', vaso)
        print('fim - PREPARACAO_BOCA')
        self.DCA_acabamento_inicial_boca()


    def DCA_acabamento_inicial_boca(self):
        print('inicio - ACABAMENTO_INICIAL_BOCA')
        if self.vasos.search_vaso('ACABAMENTO_INICIAL_BOCA'):
            vaso = self.vasos.remove_vaso('ACABAMENTO_INICIAL_BOCA')
            x = self.CONST.get_ACAB_INI_BOCA(vaso.get_size())
            rand = np.random.triangular(x[0], x[1], x[2])
            # rand = np.random.triangular(3, 5, 8)
            # Evento: atualiza tempos do sistema
            self.vasos.insert_vaso('SECAGEM_ACABAMENTO_BOCA', vaso)
            self.fel.insert_fel('SECAGEM_ACABAMENTO_BOCA', self.time_system + int(rand))
        print('fim - ACABAMENTO_INICIAL_BOCA')
        self.DCA_secagem_acabamento_boca()


    def DCA_secagem_acabamento_boca(self):
        print('inicio - SECAGEM_ACABAMENTO_BOCA')
        if self.vasos.search_vaso('SECAGEM_ACABAMENTO_BOCA'):
            vaso = self.vasos.remove_vaso('SECAGEM_ACABAMENTO_BOCA')
            #################### SE recurso alocado atual == artesao
            if (1):
                # SE pouca massa (-25%)
                if (self.massa < self.pouca_massa):
                    ################### aloca o artesao para preparacao da massa
                    # Fazer massa - fazer_massa
                    self.DCA_fazer_massa()
                # SE pouca pedra (-25%)
                elif (self.pedra < self.pouca_pedra):
                    ################### aloca o artesao para coleta de pedra
                    # Coletar pedra - coleta_pedra
                    self.DCA_coleta_pedra()
                # SE vaso na fila de envernizacao geral
                elif (self.vasos.search_vaso('ENVERNIZACAO_GERAL')):
                    # desenfilera vaso da fila envernizacao geral
                    ################### v = self.vasos.remove_vaso('ENVERNIZACAO_GERAL')
                    ################### aloca o artesao para envernizacao
                    # Envernizacao Geral - envernizacao_geral()
                    self.DCA_envernizacao_geral()
                # SE vaso na fila de impermeabilizacao interna
                elif (self.vasos.search_vaso('IMPERMEABILIZACAO_INTERNA')):
                    # desenfilera vaso da fila impermeabilizacao interna
                    ################### v = self.vasos.remove_vaso('IMPERMEABILIZACAO_INTERNA')
                    ################### aloca o artesao para impermeabilizacao
                    # Impermeabilizacao Interna - impermeabilizacao_interna()
                    self.DCA_impermeabilizacao_interna()
                # SE vaso na fila de limpeza acabamento boca
                elif (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BOCA')):
                    # desenfilera vaso da fila limpeza acabamento boca
                    ################### v = self.vasos.remove_vaso('LIMPEZA_ACABAMENTO_BOCA')
                    ################### aloca o artesao para limpeza
                    # limpeza acabamento boca - limpeza_acabamento_boca()
                    self.DCA_limpeza_acabamento_boca()
                # SE vaso na fila de preparacao boca
                elif (self.vasos.search_vaso('PREPARACAO_BOCA')):
                    # desenfilera vaso da fila preparacao boca
                    ################### v = self.vasos.remove_vaso('PREPARACAO_BOCA')
                    ################### aloca o artesao para preparacao
                    # preparacao boca - preparacao_boca()
                    self.DCA_preparacao_boca()
                # SE vaso na fila de limpeza acabamento base
                elif (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BASE')):
                    # desenfilera vaso da fila limpeza acabamento base
                    v = self.vasos.remove_vaso('LIMPEZA_ACABAMENTO_BASE')
                    ################### aloca o artesao para limpeza
                    # limpeza acabamento base - limpeza_acabamento_base()
                    self.DCA_limpeza_acabamento_base()
                # SE vaso na fila inicial
                elif (self.vasos.search_vaso('PREPARACAO_FORMA')):
                    # desenfilera vaso da fila inicial
                    ################### v = self.vasos.remove_vaso('PREPARACAO_FORMA')
                    ################### aloca o artesao para fila inicial
                    # fila inicial - preparacao_forma()
                    self.DCA_preparacao_forma()
                else:
                    ################### libera artesao
                    pass
            else:
                # SE vaso na fila de limpeza acabamento boca
                if (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BOCA')):
                    # desenfilera vaso da fila limpeza acabamento boca
                    ################### v = self.vasos.remove_vaso('LIMPEZA_ACABAMENTO_BOCA')
                    ################### aloca o artesao para limpeza
                    # limpeza acabamento boca - limpeza_acabamento_boca()
                    self.DCA_limpeza_acabamento_boca()
                # SE vaso na fila de preparacao boca
                elif (self.vasos.search_vaso('PREPARACAO_BOCA')):
                    # desenfilera vaso da fila preparacao boca
                    ################### v = self.vasos.remove_vaso('PREPARACAO_BOCA')
                    ################### aloca o artesao para preparacao
                    # preparacao boca - preparacao_boca()
                    self.DCA_preparacao_boca()
                # SE vaso na fila de limpeza acabamento base
                elif (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BASE')):
                    # desenfilera vaso da fila limpeza acabamento base
                    ################### v = self.vasos.remove_vaso('LIMPEZA_ACABAMENTO_BASE')
                    ################### aloca o artesao para limpeza
                    # limpeza acabamento base - limpeza_acabamento_base()
                    self.DCA_limpeza_acabamento_base()
                # SE vaso na fila inicial
                elif (self.vasos.search_vaso('PREPARACAO_FORMA')):
                    # desenfilera vaso da fila inicial
                    ################### v = self.vasos.remove_vaso('PREPARACAO_FORMA')
                    ################### aloca o artesao para fila inicial
                    # fila inicial - preparacao_forma()
                    self.DCA_preparacao_forma()

            x = self.CONST.get_SEC_ACAB_BOCA(vaso.get_size())
            rand = np.random.triangular(x[0], x[1], x[2])
            # rand = np.random.triangular(8, 10, 13)
            # Evento: atualiza tempos do sistema
            self.vasos.insert_vaso('LIMPEZA_ACABAMENTO_BOCA', vaso)
            self.fel.insert_fel('LIMPEZA_ACABAMENTO_BOCA', self.time_system + int(rand))
        print('fim - SECAGEM_ACABAMENTO_BOCA')
        self.DCA_limpeza_acabamento_boca()


    def DCA_limpeza_acabamento_boca(self):
        print('inicio - LIMPEZA_ACABAMENTO_BOCA')
        if self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BOCA'):
            vaso = self.vasos.remove_vaso('LIMPEZA_ACABAMENTO_BOCA')
            if self.haveSpecialist():
                spec = self.getSpecialist()
                # sorteia tempo de preparacao da boca
                x = self.CONST.get_LIMP_ACAB_BOCA(vaso.get_size())
                rand = np.random.triangular(x[0], x[1], x[2])
                # rand = np.random.triangular(6, 7, 10)
                # Evento: atualiza tempos do sistema
                self.vasos.insert_vaso('SECAGEM_BOCA', vaso)
                self.fel.insert_fel('SECAGEM_BOCA', self.time_system + int(rand))
            elif self.haveArtisan():
                spec = self.getArtisan()
                x = self.CONST.get_LIMP_ACAB_BOCA(vaso.get_size())
                rand = np.random.triangular(x[0], x[1], x[2])
                # rand = np.random.triangular(6, 7, 10)
                # Evento: atualiza tempos do sistema
                self.vasos.insert_vaso('SECAGEM_BOCA', vaso)
                self.fel.insert_fel('SECAGEM_BOCA', self.time_system + int(rand))
            else:
                self.vasos.insert_vaso('LIMPEZA_ACABAMENTO_BOCA', vaso)
        print('fim - LIMPEZA_ACABAMENTO_BOCA')
        self.DCA_secagem_boca()


    def DCA_secagem_boca(self):
        print('inicio - SECAGEM_BOCA')
        if self.vasos.search_vaso('SECAGEM_BOCA'):
            vaso = self.vasos.remove_vaso('SECAGEM_BOCA')
            #################### SE recurso alocado atual == artesao
            if (1):
                # SE pouca massa (-25%)
                if (self.massa < self.pouca_massa):
                    ################### aloca o artesao para preparacao da massa
                    # Fazer massa - fazer_massa
                    self.DCA_fazer_massa()
                # SE pouca pedra (-25%)
                elif (self.pedra < self.pouca_pedra):
                    ################### aloca o artesao para coleta de pedra
                    # Coletar pedra - coleta_pedra
                    self.DCA_coleta_pedra()
                # SE vaso na fila de envernizacao geral
                elif (self.vasos.search_vaso('ENVERNIZACAO_GERAL')):
                    # desenfilera vaso da fila envernizacao geral
                    ################### v = self.vasos.remove_vaso('ENVERNIZACAO_GERAL')
                    ################### aloca o artesao para envernizacao
                    # Envernizacao Geral - envernizacao_geral()
                    self.DCA_envernizacao_geral()
                # SE vaso na fila de impermeabilizacao interna
                elif (self.vasos.search_vaso('IMPERMEABILIZACAO_INTERNA')):
                    # desenfilera vaso da fila impermeabilizacao interna
                    ################### v = self.vasos.remove_vaso('IMPERMEABILIZACAO_INTERNA')
                    ################### aloca o artesao para impermeabilizacao
                    # Impermeabilizacao Interna - impermeabilizacao_interna()
                    self.DCA_impermeabilizacao_interna()
                # SE vaso na fila de limpeza acabamento boca
                elif (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BOCA')):
                    # desenfilera vaso da fila limpeza acabamento boca
                    ################### v = self.vasos.remove_vaso('LIMPEZA_ACABAMENTO_BOCA')
                    ################### aloca o artesao para limpeza
                    # limpeza acabamento boca - limpeza_acabamento_boca()
                    self.DCA_limpeza_acabamento_boca()
                # SE vaso na fila de preparacao boca
                elif (self.vasos.search_vaso('PREPARACAO_BOCA')):
                    # desenfilera vaso da fila preparacao boca
                    ################### v = self.vasos.remove_vaso('PREPARACAO_BOCA')
                    ################### aloca o artesao para preparacao
                    # preparacao boca - preparacao_boca()
                    self.DCA_preparacao_boca()
                # SE vaso na fila de limpeza acabamento base
                elif (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BASE')):
                    # desenfilera vaso da fila limpeza acabamento base
                    ################### v = self.vasos.remove_vaso('LIMPEZA_ACABAMENTO_BASE')
                    ################### aloca o artesao para limpeza
                    # limpeza acabamento base - limpeza_acabamento_base()
                    self.DCA_limpeza_acabamento_base()
                # SE vaso na fila inicial
                elif (self.vasos.search_vaso('PREPARACAO_FORMA')):
                    # desenfilera vaso da fila inicial
                    ################### v = self.vasos.remove_vaso('PREPARACAO_FORMA')
                    ################### aloca o artesao para fila inicial
                    # fila inicial - preparacao_forma()
                    self.DCA_preparacao_forma()
                else:
                    ################### libera artesao
                    pass
            else:
                # SE vaso na fila de limpeza acabamento boca
                if (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BOCA')):
                    # desenfilera vaso da fila limpeza acabamento boca
                    ################### v = self.vasos.remove_vaso('LIMPEZA_ACABAMENTO_BOCA')
                    ################### aloca o artesao para limpeza
                    # limpeza acabamento boca - limpeza_acabamento_boca()
                    self.DCA_limpeza_acabamento_boca()
                # SE vaso na fila de preparacao boca
                elif (self.vasos.search_vaso('PREPARACAO_BOCA')):
                    # desenfilera vaso da fila preparacao boca
                    ################### v = self.vasos.remove_vaso('PREPARACAO_BOCA')
                    ################### aloca o artesao para preparacao
                    # preparacao boca - preparacao_boca()
                    self.DCA_preparacao_boca()
                # SE vaso na fila de limpeza acabamento base
                elif (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BASE')):
                    # desenfilera vaso da fila limpeza acabamento base
                    ################### v = self.vasos.remove_vaso('LIMPEZA_ACABAMENTO_BASE')
                    ################### aloca o artesao para limpeza
                    # limpeza acabamento base - limpeza_acabamento_base()
                    self.DCA_limpeza_acabamento_base()
                # SE vaso na fila inicial
                elif (self.vasos.search_vaso('PREPARACAO_FORMA')):
                    # desenfilera vaso da fila inicial
                    ################### v = self.vasos.remove_vaso('PREPARACAO_FORMA')
                    ################### aloca o artesao para fila inicial
                    # fila inicial - preparacao_forma()
                    self.DCA_preparacao_forma()

            x = self.CONST.get_SEC_BOCA(vaso.get_size())
            rand = np.random.triangular(x[0], x[1], x[2])
            # rand = np.random.triangular(3, 8, 12)
            # Evento: atualiza tempos do sistema
            self.vasos.insert_vaso('IMPERMEABILIZACAO_INTERNA', vaso)
            self.fel.insert_fel('IMPERMEABILIZACAO_INTERNA', self.time_system + int(rand))
        print('fim - SECAGEM_BOCA')
        self.DCA_impermeabilizacao_interna()


    ################### Existe uma fila entre essas 2 atividades

    def DCA_impermeabilizacao_interna(self):
        print('inicio - IMPERMEABILIZACAO_INTERNA')
        if self.vasos.search_vaso('IMPERMEABILIZACAO_INTERNA'):
            vaso = self.vasos.remove_vaso('IMPERMEABILIZACAO_INTERNA')
            if self.haveArtisan():
                spec = self.getArtisan()
                # sorteia tempo de preparacao da boca
                x = self.CONST.get_IMP_INTERNA(vaso.get_size())
                rand = np.random.triangular(x[0], x[1], x[2])
                # rand = np.random.triangular(3, 5, 8)
                # Evento: atualiza tempos do sistema
                self.vasos.insert_vaso('SECAGEM_INTERNA', vaso)
                self.fel.insert_fel('SECAGEM_INTERNA', self.time_system + int(rand))
            else:
                self.vasos.insert_vaso('IMPERMEABILIZACAO_INTERNA', vaso)
        print('fim - IMPERMEABILIZACAO_INTERNA')
        self.DCA_secagem_interna()


    def DCA_secagem_interna(self):
        print('inicio - SECAGEM_INTERNA')
        if self.vasos.search_vaso('SECAGEM_INTERNA'):
            vaso = self.vasos.remove_vaso('SECAGEM_INTERNA')
            # SE pouca massa (-25%)
            if (self.massa < self.pouca_massa):
                ################### aloca o artesao para preparacao da massa
                # Fazer massa - fazer_massa
                self.DCA_fazer_massa()
            # SE pouca pedra (-25%)
            elif (self.pedra < self.pouca_pedra):
                ################### aloca o artesao para coleta de pedra
                # Coletar pedra - coleta_pedra
                self.DCA_coleta_pedra()
            # SE vaso na fila de envernizacao geral
            elif (self.vasos.search_vaso('ENVERNIZACAO_GERAL')):
                # desenfilera vaso da fila envernizacao geral
                ################### v = self.vasos.remove_vaso('ENVERNIZACAO_GERAL')
                ################### aloca o artesao para envernizacao
                # Envernizacao Geral - envernizacao_geral()
                self.DCA_envernizacao_geral()
            # SE vaso na fila de impermeabilizacao interna
            elif (self.vasos.search_vaso('IMPERMEABILIZACAO_INTERNA')):
                # desenfilera vaso da fila impermeabilizacao interna
                ################### v = self.vasos.remove_vaso('IMPERMEABILIZACAO_INTERNA')
                ################### aloca o artesao para impermeabilizacao
                # Impermeabilizacao Interna - impermeabilizacao_interna()
                self.DCA_impermeabilizacao_interna()
            # SE vaso na fila de limpeza acabamento boca
            elif (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BOCA')):
                # desenfilera vaso da fila limpeza acabamento boca
                ################### v = self.vasos.remove_vaso('LIMPEZA_ACABAMENTO_BOCA')
                ################### aloca o artesao para limpeza
                # limpeza acabamento boca - limpeza_acabamento_boca()
                self.DCA_limpeza_acabamento_boca()
            # SE vaso na fila de preparacao boca
            elif (self.vasos.search_vaso('PREPARACAO_BOCA')):
                # desenfilera vaso da fila preparacao boca
                ################### v = self.vasos.remove_vaso('PREPARACAO_BOCA')
                ################### aloca o artesao para preparacao
                # preparacao boca - preparacao_boca()
                self.DCA_preparacao_boca()
            # SE vaso na fila de limpeza acabamento base
            elif (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BASE')):
                # desenfilera vaso da fila limpeza acabamento base
                ################### v = self.vasos.remove_vaso('LIMPEZA_ACABAMENTO_BASE')
                ################### aloca o artesao para limpeza
                # limpeza acabamento base - limpeza_acabamento_base()
                self.DCA_limpeza_acabamento_base()
            # SE vaso na fila inicial
            elif (self.vasos.search_vaso('PREPARACAO_FORMA')):
                # desenfilera vaso da fila inicial
                ################### v = self.vasos.remove_vaso('PREPARACAO_FORMA')
                ################### aloca o artesao para fila inicial
                # fila inicial - preparacao_forma()
                self.DCA_preparacao_forma()
            else:
                ################### libera artesao
                pass

            x = self.CONST.get_SEC_INTERNA(vaso.get_size())
            rand = np.random.triangular(x[0], x[1], x[2])
            # rand = np.random.triangular(6, 8, 10)
            # Evento: atualiza tempos do sistema
            self.vasos.insert_vaso('ENVERNIZACAO_GERAL', vaso)
            self.fel.insert_fel('ENVERNIZACAO_GERAL', self.time_system + int(rand))
        print('fim - SECAGEM_INTERNA')
        self.DCA_envernizacao_geral()


    ################### Existe uma fila entre essas 2 atividades

    def DCA_envernizacao_geral(self):
        print('inicio - ENVERNIZACAO_GERAL')
        if self.vasos.search_vaso('ENVERNIZACAO_GERAL'):
            vaso = self.vasos.remove_vaso('ENVERNIZACAO_GERAL')
            if self.haveArtisan():
                spec = self.getArtisan()
                # sorteia tempo de preparacao da boca
                x = self.CONST.get_ENV_GERAL(vaso.get_size())
                rand = np.random.triangular(x[0], x[1], x[2])
                # rand = np.random.triangular(10, 18, 25)
                # Evento: atualiza tempos do sistema
                self.vasos.insert_vaso('SECAGEM_ENVERNIZACAO', vaso)
                self.fel.insert_fel('SECAGEM_ENVERNIZACAO', self.time_system + int(rand))
            else:
                self.vasos.insert_vaso('ENVERNIZACAO_GERAL', vaso)
        print('fim - ENVERNIZACAO_GERAL')
        self.DCA_secagem_envernizacao()


    def DCA_secagem_envernizacao(self):
        print('inicio - SECAGEM_ENVERNIZACAO')
        if self.vasos.search_vaso('SECAGEM_ENVERNIZACAO'):
            vaso = self.vasos.remove_vaso('SECAGEM_ENVERNIZACAO')
            # SE pouca massa (-25%)
            if (self.massa < self.pouca_massa):
                ################### aloca o artesao para preparacao da massa
                # Fazer massa - fazer_massa
                self.DCA_fazer_massa()
            # SE pouca pedra (-25%)
            elif (self.pedra < self.pouca_pedra):
                ################### aloca o artesao para coleta de pedra
                # Coletar pedra - coleta_pedra
                self.DCA_coleta_pedra()
            # SE vaso na fila de envernizacao geral
            elif (self.vasos.search_vaso('ENVERNIZACAO_GERAL')):
                # desenfilera vaso da fila envernizacao geral
                ################### v = self.vasos.remove_vaso('ENVERNIZACAO_GERAL')
                ################### aloca o artesao para envernizacao
                # Envernizacao Geral - envernizacao_geral()
                self.DCA_envernizacao_geral()
            # SE vaso na fila de impermeabilizacao interna
            elif (self.vasos.search_vaso('IMPERMEABILIZACAO_INTERNA')):
                # desenfilera vaso da fila impermeabilizacao interna
                ################### v = self.vasos.remove_vaso('IMPERMEABILIZACAO_INTERNA')
                ################### aloca o artesao para impermeabilizacao
                # Impermeabilizacao Interna - impermeabilizacao_interna()
                self.DCA_impermeabilizacao_interna()
            # SE vaso na fila de limpeza acabamento boca
            elif (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BOCA')):
                # desenfilera vaso da fila limpeza acabamento boca
                ################### v = self.vasos.remove_vaso('LIMPEZA_ACABAMENTO_BOCA')
                ################### aloca o artesao para limpeza
                # limpeza acabamento boca - limpeza_acabamento_boca()
                self.DCA_limpeza_acabamento_boca()
            # SE vaso na fila de preparacao boca
            elif (self.vasos.search_vaso('PREPARACAO_BOCA')):
                # desenfilera vaso da fila preparacao boca
                ################### v = self.vasos.remove_vaso('PREPARACAO_BOCA')
                ################### aloca o artesao para preparacao
                # preparacao boca - preparacao_boca()
                self.DCA_preparacao_boca()
            # SE vaso na fila de limpeza acabamento base
            elif (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BASE')):
                # desenfilera vaso da fila limpeza acabamento base
                ################### v = self.vasos.remove_vaso('LIMPEZA_ACABAMENTO_BASE')
                ################### aloca o artesao para limpeza
                # limpeza acabamento base - limpeza_acabamento_base()
                self.DCA_limpeza_acabamento_base()
            # SE vaso na fila inicial
            elif (self.vasos.search_vaso('PREPARACAO_FORMA')):
                # desenfilera vaso da fila inicial
                ################### v = self.vasos.remove_vaso('PREPARACAO_FORMA')
                ################### aloca o artesao para fila inicial
                # fila inicial - preparacao_forma()
                self.DCA_preparacao_forma()
            else:
                ################### libera artesao
                pass

            x = self.CONST.get_SEC_FINAL(vaso.get_size())
            rand = np.random.triangular(x[0], x[1], x[2])
            # rand = np.random.triangular(18, 20, 22)
            # Evento: atualiza tempos do sistema
            vaso.setEndTime(self.time_system)
            self.vasos.insert_vaso('CHEGADA_PEDIDO', vaso)
            self.fel.insert_fel('CHEGADA_PEDIDO', self.time_system + int(rand))
        print('FINAL')
        print('fim - SECAGEM_ENVERNIZACAO')
        self.vasos.show()
        self.fel.show()
        self.time_system += 1
        #DCA_chegada_pedido()	

simulator = simulator2()
for i in range(simulator.CONST.get_NUM_ART()):
    simulator.artesoes.append(Artesao.Artesao())
for i in range(simulator.CONST.get_NUM_ESP()):
    simulator.artesoes.append(Artesao.Artesao(True))

simulator.DCA_chegada_pedido()