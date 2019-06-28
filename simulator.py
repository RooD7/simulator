import vaso as Vaso
import inputFile as InputFile
import const as Const
import fel as Fel
import filaVaso as FilaVaso
import artesao as Artesao
import listaArtesao as ListaArtesao
import numpy as np

timeSystemAux = 0
iteracao = 0
totalVasos = 0
completionTimeIter = 0

massaUtilizada = 0
pedraUtilizada = 0
prodArtesao = 0
prodEspecialista = 0
completionTimeVasoPeq = 0
completionTimeVasoMed = 0
completionTimeVasoGran = 0
seedUtilised = 0
simulationTime = 170000
iteracao += 1
qtdPeq = 0
qtdMed = 0
qtdGran = 0
completionPeq = 0
completionMed = 0
completionGran = 0
        
completionTimePeq = 0
completionTimeMed = 0
completionTimeGran = 0

arquivoLog = "simulacao2.tsv"

class simulator(object):

    def __init__(self, semente):
        global totalVasos
        global completionPeq
        global completionMed
        global completionGran
        tempoAuxInit = 0
        while tempoAuxInit < simulationTime:
            self.fel = Fel.Fel()
            self.vasos = FilaVaso.FilaVaso()

            inpFile = InputFile.InputFile()

            self.CONST = Const.Const()
            self.CONST = inpFile.inputs('entrada.txt')

            self.time_system = tempoAuxInit
            # np.random.seed(self.CONST.get_G_TSM())
            np.random.seed(semente)
            self.massa = self.CONST.get_QTD_MASSA()
            self.pedra = self.CONST.get_QTD_PEDRA()
            self.pouca_massa = 250
            self.pouca_pedra = 250
            self.artesoes = ListaArtesao.ListaArtesao()
            self.uso_esp_sec = 0
            self.vaso = None
            self.artesao = None
            self.novoLote = True
            self.tempoNovoLote = 0
            self.simuTime = tempoAuxInit
            self.semente = semente
            
            for i in range(0, 1):
                self.artesoes.insert_new_artesao(specialist=False)
                self.artesao = self.artesoes.aloca_artisan('PREPARACAO_FORMA')

            self.fel.insert_fel('CHEGADA_PEDIDO', tempoAuxInit)
            tempoAuxInit = self.felControl()

            for k in self.vasos.get_fila():
                if k[1].get_size() == 'S':
                    completionPeq += k[1].getCompletionTime()
                if k[1].get_size() == 'M':
                    completionMed += k[1].getCompletionTime()
                if k[1].get_size() == 'B':
                    completionGran += k[1].getCompletionTime()

            if tempoAuxInit < simulationTime:
                totalVasos += len(self.vasos.get_fila())


    def felControl(self):
        while self.fel.get_fel_size() != 0:
            self.fel.sorted_fel()
            atividade = self.fel.remove_fel()
            self.time_system = atividade.get_time_event()
            if self.time_system > simulationTime:
                return self.time_system
            self.artesoes.alocados(self.time_system)

            if atividade.get_ativ_event().name == 'CHEGADA_PEDIDO':
                self.DCA_chegada_pedido()
            elif atividade.get_ativ_event().name == 'PREPARACAO_FORMA':
                self.DCA_preparacao_forma()
            elif atividade.get_ativ_event().name == 'PREPARACAO_BASE':
                self.DCA_preparacao_base()
            elif atividade.get_ativ_event().name == 'ACABAMENTO_INICIAL_BASE':
                self.DCA_acabamento_inicial_base()
            elif atividade.get_ativ_event().name == 'SECAGEM_ACABAMENTO_BASE':
                self.DCA_secagem_acabamento_base()
            elif atividade.get_ativ_event().name == 'LIMPEZA_ACABAMENTO_BASE':
                self.DCA_limpeza_acabamento_base()
            elif atividade.get_ativ_event().name == 'SECAGEM_BASE':
                self.DCA_secagem_base()
            elif atividade.get_ativ_event().name == 'PREPARACAO_BOCA':
                self.DCA_preparacao_boca()
            elif atividade.get_ativ_event().name == 'ACABAMENTO_INICIAL_BOCA':
                self.DCA_acabamento_inicial_boca()
            elif atividade.get_ativ_event().name == 'SECAGEM_ACABAMENTO_BOCA':
                self.DCA_secagem_acabamento_boca()
            elif atividade.get_ativ_event().name == 'LIMPEZA_ACABAMENTO_BOCA':
                self.DCA_limpeza_acabamento_boca()
            elif atividade.get_ativ_event().name == 'SECAGEM_BOCA':
                self.DCA_secagem_boca()
            elif atividade.get_ativ_event().name == 'IMPERMEABILIZACAO_INTERNA':
                self.DCA_impermeabilizacao_interna()
            elif atividade.get_ativ_event().name == 'SECAGEM_INTERNA':
                self.DCA_secagem_interna()
            elif atividade.get_ativ_event().name == 'ENVERNIZACAO_GERAL':
                self.DCA_envernizacao_geral()
            elif atividade.get_ativ_event().name == 'SECAGEM_ENVERNIZACAO':
                self.DCA_secagem_envernizacao()
            elif atividade.get_ativ_event().name == 'PREPARACAO_MASSA':
                self.DCA_fazer_massa()
            elif atividade.get_ativ_event().name == 'PREPARACAO_PEDRA':
                self.DCA_coleta_pedra()
        
        vasoAux = self.vasos.get_fila()
        
        x = self.CONST.get_FREQ_PED()
        freq = np.random.triangular(x[0], x[1], x[2])
        self.tempoNovoLote = self.time_system + freq
        
        return self.tempoNovoLote
        
    def probSizeVaso(self, numPedidos):
        x = self.CONST.get_PROBS()
        small   = int(x[0] * numPedidos)
        medium  = int(x[1] * numPedidos)
        big     = int(x[2] * numPedidos)
        if (small + medium + big) != numPedidos:
            small += int(numPedidos - (small + medium + big))
        return (['S']*small)+(['M']*medium)+(['B']*big)

    def DCA_fazer_massa(self):
        self.massa = self.CONST.get_QTD_MASSA_MAX()
        self.massa =  self.CONST.get_QTD_MASSA_MAX()
        x = self.CONST.get_PREP_MASSA()
        rand = np.random.triangular(x[0], x[1], x[2])
        # rand = 10
        massaUtilizada += rand
        self.fel.insert_fel('PREPARACAO_MASSA', self.time_system + rand)
        if self.artesao.isSpecialist():
            self.artesoes.time_specialist('PREPARACAO_MASSA', self.artesao.get_id, 
                self.time_system + rand)
        else:
            self.artesoes.time_artisan('PREPARACAO_MASSA', self.artesao.get_id, 
                self.time_system + rand)
        
    def DCA_coleta_pedra(self):
        self.pedra = self.CONST.get_QTD_PEDRA_MAX()
        pedraUtilizada += self.CONST.get_QTD_PEDRA_MAX()
        x = self.CONST.get_PREP_PEDRA()
        rand = np.random.triangular(x[0], x[1], x[2])
        # rand = 90
        pedraUtilizada += rand
        self.fel.insert_fel('PREPARACAO_PEDRA', self.time_system + rand)
        if self.artesao.isSpecialist():
            self.artesoes.time_specialist('PREPARACAO_PEDRA', self.artesao.get_id, 
                self.time_system + rand)
        else:
            self.artesoes.time_artisan('PREPARACAO_PEDRA', self.artesao.get_id, 
                self.time_system + rand)

    def DCA_chegada_pedido(self):
        global qtdPeq
        global qtdMed
        global qtdGran

        # frequencia de chegada de pedidos
        #if self.novoLote:
        #    x = self.CONST.get_FREQ_PED()
        #    freq = np.random.triangular(x[0], x[1], x[2])
        #    self.tempoNovoLote = self.time_system + freq
        #    self.novoLote = False
        
        # tamanho do pedido (seguindo a probabilidade do CONST)
        x = self.CONST.get_TAM_PED()
        # num_pedidos = np.random.triangular(x[0], x[1], x[2])
        num_pedidos = 30
        # lista de tamanho dos vasos
        sizes = self.probSizeVaso(num_pedidos)
        # serao feitos 'num_pedidos' pedidos
        #print('!!! NOVO LOTE de '+str(int(num_pedidos))+' vasos.')
        #self.fel = Fel.Fel()
        for r in range(0, int(num_pedidos)):
            self.vasos.insert_new_vaso('PREPARACAO_FORMA', sizes[r], self.time_system)
            self.fel.insert_fel('PREPARACAO_FORMA', self.time_system)
        # for r in range(0, len(self.artesoes.get_lista())):
        for r in range(0, 1):
            self.artesao = self.artesoes.aloca_artisan('PREPARACAO_FORMA')
            self.artesao = self.artesoes.aloca_specialist('PREPARACAO_FORMA')
        
        for x in self.vasos.get_fila():
            if x[1].get_size() == 'S':
                qtdPeq += 1
            if x[1].get_size() == 'M':
                qtdMed += 1
            if x[1].get_size() == 'B':
                qtdGran += 1

    ################### Existe uma fila entre essas 2 atividades

    def DCA_preparacao_forma(self):
        if self.vasos.search_vaso('PREPARACAO_FORMA'):
            vaso = self.vasos.remove_vaso('PREPARACAO_FORMA')
            # sorteia tempo de preparacao da forma
            x = self.CONST.get_PREP_FORM(vaso.get_size())
            rand = np.random.triangular(x[0], x[1], x[2])
            # rand = 1
            vaso.set_time_atual(int(rand))
            self.time_system = vaso.getTimeAtual()
            # espaco de secagem
            if (self.uso_esp_sec < self.CONST.get_ESP_SEC()):
                # massa suficiente
                if (self.massa > self.pouca_massa):
                    if self.artesoes.have_specialist('PREPARACAO_FORMA'):
                        self.artesao = self.artesoes.time_specialist('PREPARACAO_FORMA', vaso.getTimeAtual())
                        self.fel.insert_fel('PREPARACAO_BASE', vaso.getTimeAtual())
                        self.vasos.insert_vaso('PREPARACAO_BASE', vaso)
                        # Quero deixar um comentario como conribuiçao <3 BRIGADO AMIGO REZE POR NÓS E PELA NOSSAS ALMAS rezarei pode deixar kkk
                    elif self.artesoes.have_artisan('PREPARACAO_FORMA'):
                        self.artesao = self.artesoes.time_artisan('PREPARACAO_FORMA', vaso.getTimeAtual())
                        self.fel.insert_fel('PREPARACAO_BASE', vaso.getTimeAtual())
                        self.vasos.insert_vaso('PREPARACAO_BASE', vaso)
                else:
                    # coloca vaso na fila de preparacao da forma
                    self.vasos.insert_vaso('PREPARACAO_FORMA', vaso)
                    self.fel.insert_fel('PREPARACAO_MASSA', vaso.getTimeAtual())
            else:
                # coloca vaso na fila de preparacao da forma
                self.vasos.insert_vaso('PREPARACAO_FORMA', vaso)
                self.fel.insert_fel('PREPARACAO_FORMA', vaso.getTimeAtual())

    def DCA_preparacao_base(self):
        if self.vasos.search_vaso('PREPARACAO_BASE'):
            vaso = self.vasos.remove_vaso('PREPARACAO_BASE')
            x = self.CONST.get_PREP_BASE(vaso.get_size())
            rand = np.random.triangular(x[0], x[1], x[2])
            # rand = 10
            vaso.set_time_atual(int(rand))
            self.artesao = self.artesoes.get_artisan('PREPARACAO_BASE')
            self.artesao = self.artesoes.time_artisan('PREPARACAO_BASE', vaso.getTimeAtual())
            if self.artesao == None:
                self.artesao = self.artesoes.time_specialist('PREPARACAO_BASE', vaso.getTimeAtual())
                if self.artesao == None:
                    self.artesao = self.artesoes.aloca_artisan('PREPARACAO_BASE', vaso.getTimeAtual())
                if self.artesao == None:
                    self.artesao = self.artesoes.aloca_specialist('PREPARACAO_BASE', vaso.getTimeAtual())
            if self.artesao != None:
                self.vasos.insert_vaso('ACABAMENTO_INICIAL_BASE', vaso)
                self.fel.insert_fel('ACABAMENTO_INICIAL_BASE', vaso.getTimeAtual())

    def DCA_acabamento_inicial_base(self):
        # self.vasos.show()
        if self.vasos.search_vaso('ACABAMENTO_INICIAL_BASE'):
            vaso = self.vasos.remove_vaso('ACABAMENTO_INICIAL_BASE')
            x = self.CONST.get_ACAB_INI_BOCA(vaso.get_size())
            rand = np.random.triangular(x[0], x[1], x[2])
            # rand = 2
            vaso.set_time_atual(int(rand))
            self.artesao = self.artesoes.get_artisan('ACABAMENTO_INICIAL_BASE')
            self.artesao = self.artesoes.time_artisan('ACABAMENTO_INICIAL_BASE', vaso.getTimeAtual())
            if self.artesao == None:
                self.artesao = self.artesoes.time_specialist('ACABAMENTO_INICIAL_BASE', vaso.getTimeAtual())
                if self.artesao == None:
                    self.artesao = self.artesoes.aloca_artisan('ACABAMENTO_INICIAL_BASE', vaso.getTimeAtual())
                if self.artesao == None:
                    self.artesao = self.artesoes.aloca_specialist('ACABAMENTO_INICIAL_BASE', vaso.getTimeAtual())
            if self.artesao != None:
                self.vasos.insert_vaso('SECAGEM_ACABAMENTO_BASE', vaso)
                self.fel.insert_fel('SECAGEM_ACABAMENTO_BASE', vaso.getTimeAtual())

    def DCA_secagem_acabamento_base(self):
        if self.vasos.search_vaso('SECAGEM_ACABAMENTO_BASE'):
            vaso = self.vasos.remove_vaso('SECAGEM_ACABAMENTO_BASE')
            x = self.CONST.get_SEC_ACAB(vaso.get_size())
            rand = np.random.triangular(x[0], x[1], x[2])
            # rand = 6
            vaso.set_time_atual(int(rand))
            # SE recurso alocado atual == artesao
            self.artesao = self.artesoes.get_artisan('SECAGEM_ACABAMENTO_BASE')
            if (self.artesao != None) and (not self.artesao.isSpecialist()):
                # SE pouca massa (-25%)
                if (self.massa < self.pouca_massa):
                    # aloca o artesao para preparacao da massa
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('PREPARACAO_MASSA')
                    self.fel.insert_fel('PREPARACAO_MASSA', vaso.getTimeAtual())
                # SE pouca pedra (-25%)
                elif (self.pedra < self.pouca_pedra):
                    # aloca o artesao para coleta de pedra
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('PREPARACAO_PEDRA')
                    self.fel.insert_fel('PREPARACAO_PEDRA', vaso.getTimeAtual())
                # SE vaso na fila de envernizacao geral
                elif (self.vasos.search_vaso('ENVERNIZACAO_GERAL')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('ENVERNIZACAO_GERAL')
                    self.fel.insert_fel('ENVERNIZACAO_GERAL', vaso.getTimeAtual())
                # SE vaso na fila de impermeabilizacao interna
                elif (self.vasos.search_vaso('IMPERMEABILIZACAO_INTERNA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('IMPERMEABILIZACAO_INTERNA')
                    self.fel.insert_fel('IMPERMEABILIZACAO_INTERNA', vaso.getTimeAtual())
                # SE vaso na fila de limpeza acabamento boca
                elif (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BOCA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('LIMPEZA_ACABAMENTO_BOCA')
                    self.fel.insert_fel('LIMPEZA_ACABAMENTO_BOCA', vaso.getTimeAtual())
                # SE vaso na fila de preparacao boca
                elif (self.vasos.search_vaso('PREPARACAO_BOCA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('PREPARACAO_BOCA')
                    self.fel.insert_fel('PREPARACAO_BOCA', vaso.getTimeAtual())
                # SE vaso na fila de preparacao boca
                elif (self.vasos.search_vaso('ACABAMENTO_INICIAL_BASE')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('ACABAMENTO_INICIAL_BASE')
                    self.fel.insert_fel('ACABAMENTO_INICIAL_BASE', vaso.getTimeAtual())
                # SE vaso na fila inicial
                elif (self.vasos.search_vaso('PREPARACAO_FORMA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('PREPARACAO_FORMA')
                    self.fel.insert_fel('PREPARACAO_FORMA', vaso.getTimeAtual())
                else:
                    #libera artesao
                    self.artesoes.libera_artisan(self.artesao.get_id())
            elif (self.artesao != None):
                # SE vaso na fila de limpeza acabamento boca
                if (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BOCA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_specialist('LIMPEZA_ACABAMENTO_BOCA')
                    self.fel.insert_fel('LIMPEZA_ACABAMENTO_BOCA', vaso.getTimeAtual())
                # SE vaso na fila de preparacao boca
                elif (self.vasos.search_vaso('PREPARACAO_BOCA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_specialist('PREPARACAO_BOCA')
                    self.fel.insert_fel('PREPARACAO_BOCA', vaso.getTimeAtual())
                # SE vaso na fila de preparacao boca
                elif (self.vasos.search_vaso('ACABAMENTO_INICIAL_BASE')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_specialist('ACABAMENTO_INICIAL_BASE')
                    self.fel.insert_fel('ACABAMENTO_INICIAL_BASE', vaso.getTimeAtual())
                # SE vaso na fila inicial
                elif (self.vasos.search_vaso('PREPARACAO_FORMA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_specialist('PREPARACAO_FORMA')
                    self.fel.insert_fel('PREPARACAO_FORMA', vaso.getTimeAtual())

            self.artesao = self.artesoes.time_artisan('SECAGEM_ACABAMENTO_BASE', vaso.getTimeAtual())
            if self.artesao == None:
                self.artesao = self.artesoes.time_specialist('SECAGEM_ACABAMENTO_BASE', vaso.getTimeAtual())
                if self.artesao == None:
                    self.artesao = self.artesoes.aloca_artisan('SECAGEM_ACABAMENTO_BASE', vaso.getTimeAtual())
                if self.artesao == None:
                    self.artesao = self.artesoes.aloca_specialist('SECAGEM_ACABAMENTO_BASE', vaso.getTimeAtual())
            if self.artesao != None:
                self.vasos.insert_vaso('LIMPEZA_ACABAMENTO_BASE', vaso)
                self.fel.insert_fel('LIMPEZA_ACABAMENTO_BASE', vaso.getTimeAtual())
            else:
                self.fel.insert_fel('SECAGEM_ACABAMENTO_BASE', vaso.getTimeAtual())
    
    ################### Existe uma fila entre essas 2 atividades

    def DCA_limpeza_acabamento_base(self):
        if self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BASE'):
            vaso = self.vasos.remove_vaso('LIMPEZA_ACABAMENTO_BASE')
            # sorteia tempo de limpeza acabamento base
            x = self.CONST.get_LIMP_ACAB_BASE(vaso.get_size())
            rand = np.random.triangular(x[0], x[1], x[2])
            # rand = 4
            vaso.set_time_atual(int(rand))
            self.artesao = self.artesoes.get_artisan('LIMPEZA_ACABAMENTO_BASE')
            if self.artesoes.have_specialist('LIMPEZA_ACABAMENTO_BASE'):
                self.artesao = self.artesoes.aloca_specialist('LIMPEZA_ACABAMENTO_BASE', vaso.getTimeAtual())
                self.vasos.insert_vaso('SECAGEM_BASE', vaso)
                self.fel.insert_fel('SECAGEM_BASE', vaso.getTimeAtual())
            elif self.artesoes.have_artisan('LIMPEZA_ACABAMENTO_BASE'):
                self.artesao = self.artesoes.aloca_artisan('LIMPEZA_ACABAMENTO_BASE', vaso.getTimeAtual())
                self.vasos.insert_vaso('SECAGEM_BASE', vaso)
                self.fel.insert_fel('SECAGEM_BASE', vaso.getTimeAtual())
            else:
                self.vasos.insert_vaso('LIMPEZA_ACABAMENTO_BASE', vaso)
                self.fel.insert_fel('LIMPEZA_ACABAMENTO_BASE', vaso.getTimeAtual())

    def DCA_secagem_base(self):
        if self.vasos.search_vaso('SECAGEM_BASE'):
            vaso = self.vasos.remove_vaso('SECAGEM_BASE')
            x = self.CONST.get_SEC_BASE(vaso.get_size())
            rand = np.random.triangular(x[0], x[1], x[2])
            # rand = 180
            vaso.set_time_atual(int(rand))
            self.artesao = self.artesoes.get_artisan('SECAGEM_BASE')
            if (self.artesao != None) and (not self.artesao.isSpecialist()):
                # SE pouca massa (-25%)
                if (self.massa < self.pouca_massa):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('SECAGEM_BASE')
                    self.fel.insert_fel('PREPARACAO_MASSA', vaso.getTimeAtual())
                # SE pouca pedra (-25%)
                elif (self.pedra < self.pouca_pedra):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('SECAGEM_BASE')
                    self.fel.insert_fel('PREPARACAO_PEDRA', vaso.getTimeAtual())
                # SE vaso na fila de envernizacao geral
                elif (self.vasos.search_vaso('ENVERNIZACAO_GERAL')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('ENVERNIZACAO_GERAL')
                    self.fel.insert_fel('ENVERNIZACAO_GERAL', vaso.getTimeAtual())
                # SE vaso na fila de impermeabilizacao interna
                elif (self.vasos.search_vaso('IMPERMEABILIZACAO_INTERNA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('IMPERMEABILIZACAO_INTERNA')
                    self.fel.insert_fel('IMPERMEABILIZACAO_INTERNA', vaso.getTimeAtual())
                # SE vaso na fila de limpeza acabamento boca
                elif (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BOCA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('LIMPEZA_ACABAMENTO_BOCA')
                    self.fel.insert_fel('LIMPEZA_ACABAMENTO_BOCA', vaso.getTimeAtual())
                # SE vaso na fila de preparacao boca
                elif (self.vasos.search_vaso('PREPARACAO_BOCA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('PREPARACAO_BOCA')
                    self.fel.insert_fel('PREPARACAO_BOCA', vaso.getTimeAtual())
                # SE vaso na fila de limpeza acabamento base
                elif (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BASE')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('LIMPEZA_ACABAMENTO_BASE')
                    self.fel.insert_fel('LIMPEZA_ACABAMENTO_BASE', vaso.getTimeAtual())
                # SE vaso na fila inicial
                elif (self.vasos.search_vaso('PREPARACAO_FORMA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('PREPARACAO_FORMA')
                    self.fel.insert_fel('PREPARACAO_FORMA', vaso.getTimeAtual())
                else:
                    #libera artesao
                    self.libera_artisan(self.artesao.get_id())
            elif (self.artesao != None):
                # SE vaso na fila de limpeza acabamento boca
                if (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BOCA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_specialist('LIMPEZA_ACABAMENTO_BOCA')
                    self.fel.insert_fel('LIMPEZA_ACABAMENTO_BOCA', vaso.getTimeAtual())
                # SE vaso na fila de preparacao boca
                elif (self.vasos.search_vaso('PREPARACAO_BOCA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_specialist('PREPARACAO_BOCA')
                    self.fel.insert_fel('PREPARACAO_BOCA', vaso.getTimeAtual())
                # SE vaso na fila de limpeza acabamento base
                elif (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BASE')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_specialist('LIMPEZA_ACABAMENTO_BASE')
                    self.fel.insert_fel('LIMPEZA_ACABAMENTO_BASE', vaso.getTimeAtual())
                # SE vaso na fila inicial
                elif (self.vasos.search_vaso('PREPARACAO_FORMA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_specialist('PREPARACAO_FORMA')
                    self.fel.insert_fel('PREPARACAO_FORMA', vaso.getTimeAtual())

            self.artesao = self.artesoes.time_artisan('SECAGEM_BASE', vaso.getTimeAtual())
            if self.artesao == None:
                self.artesao = self.artesoes.time_specialist('SECAGEM_BASE', vaso.getTimeAtual())
                if self.artesao == None:
                    self.artesao = self.artesoes.aloca_artisan('SECAGEM_BASE', vaso.getTimeAtual())
                if self.artesao == None:
                    self.artesao = self.artesoes.aloca_specialist('SECAGEM_BASE', vaso.getTimeAtual())
                if self.artesao != None:
                    self.vasos.insert_vaso('PREPARACAO_BOCA', vaso)
                    self.fel.insert_fel('PREPARACAO_BOCA', vaso.getTimeAtual())
            else:
                self.fel.insert_fel('SECAGEM_BASE', vaso.getTimeAtual())

    ################### Existe uma fila entre essas 2 atividades

    def DCA_preparacao_boca(self):
        if self.vasos.search_vaso('PREPARACAO_BOCA'):
            vaso = self.vasos.remove_vaso('PREPARACAO_BOCA')
            # sorteia tempo de preparacao da boca
            x = self.CONST.get_PREP_BOCA(vaso.get_size())
            rand = np.random.triangular(x[0], x[1], x[2])
            # rand = 6
            vaso.set_time_atual(int(rand))
            self.artesao = self.artesoes.get_artisan('PREPARACAO_BOCA')
            if self.artesoes.have_specialist('PREPARACAO_BOCA'):
                self.artesao = self.artesoes.time_specialist('PREPARACAO_BOCA', vaso.getTimeAtual())
                self.vasos.insert_vaso('ACABAMENTO_INICIAL_BOCA', vaso)
                self.fel.insert_fel('ACABAMENTO_INICIAL_BOCA', vaso.getTimeAtual())
            elif self.artesoes.have_artisan('PREPARACAO_BOCA'):
                self.artesao = self.artesoes.time_artisan('PREPARACAO_BOCA', vaso.getTimeAtual())
                self.vasos.insert_vaso('ACABAMENTO_INICIAL_BOCA', vaso)
                self.fel.insert_fel('ACABAMENTO_INICIAL_BOCA', vaso.getTimeAtual())
            else:
                self.vasos.insert_vaso('PREPARACAO_BOCA', vaso)
                self.fel.insert_fel('PREPARACAO_BOCA', vaso.getTimeAtual())

    def DCA_acabamento_inicial_boca(self):
        if self.vasos.search_vaso('ACABAMENTO_INICIAL_BOCA'):
            vaso = self.vasos.remove_vaso('ACABAMENTO_INICIAL_BOCA')
            x = self.CONST.get_ACAB_INI_BOCA(vaso.get_size())
            rand = np.random.triangular(x[0], x[1], x[2])
            # rand = 2
            vaso.set_time_atual(int(rand))
            self.artesao = self.artesoes.get_artisan('ACABAMENTO_INICIAL_BOCA')
            self.artesao = self.artesoes.time_artisan('ACABAMENTO_INICIAL_BOCA', vaso.getTimeAtual())
            if self.artesao == None:
                self.artesao = self.artesoes.time_specialist('ACABAMENTO_INICIAL_BOCA', vaso.getTimeAtual())
                if self.artesao == None:
                    self.artesao = self.artesoes.aloca_artisan('ACABAMENTO_INICIAL_BOCA', vaso.getTimeAtual())
                if self.artesao == None:
                    self.artesao = self.artesoes.aloca_specialist('ACABAMENTO_INICIAL_BOCA', vaso.getTimeAtual())
                if self.artesao != None:
                    self.vasos.insert_vaso('SECAGEM_ACABAMENTO_BOCA', vaso)
                    self.fel.insert_fel('SECAGEM_ACABAMENTO_BOCA', vaso.getTimeAtual())
            else:
                self.vasos.insert_vaso('ACABAMENTO_INICIAL_BOCA', vaso)
                self.fel.insert_fel('SECAGEM_ACABAMENTO_BOCA', vaso.getTimeAtual())

    def DCA_secagem_acabamento_boca(self):
        if self.vasos.search_vaso('SECAGEM_ACABAMENTO_BOCA'):
            vaso = self.vasos.remove_vaso('SECAGEM_ACABAMENTO_BOCA')
            x = self.CONST.get_SEC_ACAB_BOCA(vaso.get_size())
            rand = np.random.triangular(x[0], x[1], x[2])
            # rand = 14
            vaso.set_time_atual(int(rand))
            self.artesao = self.artesoes.get_artisan('SECAGEM_ACABAMENTO_BOCA')
            if (self.artesao != None) and (not self.artesao.isSpecialist()):
                # SE pouca massa (-25%)
                if (self.massa < self.pouca_massa):
                    # aloca o artesao para preparacao da massa
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('PREPARACAO_MASSA')
                    self.fel.insert_fel('PREPARACAO_MASSA', vaso.getTimeAtual())
                # SE pouca pedra (-25%)
                elif (self.pedra < self.pouca_pedra):
                    # aloca o artesao para preparacao da massa
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('PREPARACAO_PEDRA')
                    self.fel.insert_fel('PREPARACAO_PEDRA', vaso.getTimeAtual())
                # SE vaso na fila de envernizacao geral
                elif (self.vasos.search_vaso('ENVERNIZACAO_GERAL')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('ENVERNIZACAO_GERAL')
                    self.fel.insert_fel('ENVERNIZACAO_GERAL', vaso.getTimeAtual())
                # SE vaso na fila de impermeabilizacao interna
                elif (self.vasos.search_vaso('IMPERMEABILIZACAO_INTERNA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('IMPERMEABILIZACAO_INTERNA')
                    self.fel.insert_fel('IMPERMEABILIZACAO_INTERNA', vaso.getTimeAtual())
                # SE vaso na fila de limpeza acabamento boca
                elif (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BOCA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('LIMPEZA_ACABAMENTO_BOCA')
                    self.fel.insert_fel('LIMPEZA_ACABAMENTO_BOCA', vaso.getTimeAtual())
                # SE vaso na fila de preparacao boca
                elif (self.vasos.search_vaso('PREPARACAO_BOCA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('PREPARACAO_BOCA')
                    self.fel.insert_fel('PREPARACAO_BOCA', vaso.getTimeAtual())
                # SE vaso na fila de limpeza acabamento base
                elif (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BASE')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('LIMPEZA_ACABAMENTO_BASE')
                    self.fel.insert_fel('LIMPEZA_ACABAMENTO_BASE', vaso.getTimeAtual())
                # SE vaso na fila inicial
                elif (self.vasos.search_vaso('PREPARACAO_FORMA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('PREPARACAO_FORMA')
                    self.fel.insert_fel('PREPARACAO_FORMA', vaso.getTimeAtual())
                else:
                    #libera artesao
                    self.libera_artisan(self.artesao.get_id())
            elif (self.artesao != None):
                # SE vaso na fila de limpeza acabamento boca
                if (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BOCA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_specialist('LIMPEZA_ACABAMENTO_BOCA')
                    self.fel.insert_fel('LIMPEZA_ACABAMENTO_BOCA', vaso.getTimeAtual())
                # SE vaso na fila de preparacao boca
                elif (self.vasos.search_vaso('PREPARACAO_BOCA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_specialist('PREPARACAO_BOCA')
                    self.fel.insert_fel('PREPARACAO_BOCA', vaso.getTimeAtual())
                # SE vaso na fila de limpeza acabamento base
                elif (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BASE')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_specialist('LIMPEZA_ACABAMENTO_BASE')
                    self.fel.insert_fel('LIMPEZA_ACABAMENTO_BASE', vaso.getTimeAtual())
                # SE vaso na fila inicial
                elif (self.vasos.search_vaso('PREPARACAO_FORMA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_specialist('PREPARACAO_FORMA')
                    self.fel.insert_fel('PREPARACAO_FORMA', vaso.getTimeAtual())

            self.artesao = self.artesoes.time_artisan('SECAGEM_ACABAMENTO_BOCA', vaso.getTimeAtual())
            if self.artesao == None:
                self.artesao = self.artesoes.time_specialist('SECAGEM_ACABAMENTO_BOCA', vaso.getTimeAtual())
                if self.artesao == None:
                    self.artesao = self.artesoes.aloca_artisan('SECAGEM_ACABAMENTO_BOCA', vaso.getTimeAtual())
                if self.artesao == None:
                    self.artesao = self.artesoes.aloca_specialist('SECAGEM_ACABAMENTO_BOCA', vaso.getTimeAtual())
                if self.artesao != None:
                    self.vasos.insert_vaso('LIMPEZA_ACABAMENTO_BOCA', vaso)
                    self.fel.insert_fel('LIMPEZA_ACABAMENTO_BOCA', vaso.getTimeAtual())
            else:
                self.vasos.insert_vaso('LIMPEZA_ACABAMENTO_BOCA', vaso)
                self.fel.insert_fel('LIMPEZA_ACABAMENTO_BOCA', vaso.getTimeAtual())

    def DCA_limpeza_acabamento_boca(self):
        if self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BOCA'):
            vaso = self.vasos.remove_vaso('LIMPEZA_ACABAMENTO_BOCA')
            # sorteia tempo de preparacao da boca
            x = self.CONST.get_LIMP_ACAB_BOCA(vaso.get_size())
            rand = np.random.triangular(x[0], x[1], x[2])
            # rand = 5
            vaso.set_time_atual(int(rand))
            self.artesao = self.artesoes.get_artisan('LIMPEZA_ACABAMENTO_BOCA')
            if self.artesoes.have_specialist('LIMPEZA_ACABAMENTO_BOCA'):
                self.artesao = self.artesoes.time_specialist('LIMPEZA_ACABAMENTO_BOCA', vaso.getTimeAtual())
                self.vasos.insert_vaso('SECAGEM_BOCA', vaso)
                self.fel.insert_fel('SECAGEM_BOCA', vaso.getTimeAtual())
            elif self.artesoes.have_artisan('LIMPEZA_ACABAMENTO_BOCA'):
                self.artesao = self.artesoes.time_artisan('LIMPEZA_ACABAMENTO_BOCA', vaso.getTimeAtual())
                self.vasos.insert_vaso('SECAGEM_BOCA', vaso)
                self.fel.insert_fel('SECAGEM_BOCA', vaso.getTimeAtual())
            else:
                self.vasos.insert_vaso('LIMPEZA_ACABAMENTO_BOCA', vaso)
                self.fel.insert_fel('LIMPEZA_ACABAMENTO_BOCA', vaso.getTimeAtual())

    def DCA_secagem_boca(self):
        if self.vasos.search_vaso('SECAGEM_BOCA'):
            vaso = self.vasos.remove_vaso('SECAGEM_BOCA')
            x = self.CONST.get_SEC_BOCA(vaso.get_size())
            rand = np.random.triangular(x[0], x[1], x[2])
            # rand = 120
            vaso.set_time_atual(int(rand))
            self.artesao = self.artesoes.get_artisan('SECAGEM_BOCA')
            # SE recurso alocado atual == artesao
            if (self.artesao != None) and (not self.artesao.isSpecialist()):
                # SE pouca massa (-25%)
                if (self.massa < self.pouca_massa):
                    #aloca o artesao para preparacao da massa
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('PREPARACAO_MASSA')
                    self.fel.insert_fel('PREPARACAO_MASSA', vaso.getTimeAtual())
                # SE pouca pedra (-25%)
                elif (self.pedra < self.pouca_pedra):
                    # aloca o artesao para coleta de pedra
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('PREPARACAO_PEDRA')
                    self.fel.insert_fel('PREPARACAO_PEDRA', vaso.getTimeAtual())
                # SE vaso na fila de envernizacao geral
                elif (self.vasos.search_vaso('ENVERNIZACAO_GERAL')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('ENVERNIZACAO_GERAL')
                    self.fel.insert_fel('ENVERNIZACAO_GERAL', vaso.getTimeAtual())
                # SE vaso na fila de impermeabilizacao interna
                elif (self.vasos.search_vaso('IMPERMEABILIZACAO_INTERNA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('IMPERMEABILIZACAO_INTERNA')
                    self.fel.insert_fel('IMPERMEABILIZACAO_INTERNA', vaso.getTimeAtual())
                # SE vaso na fila de limpeza acabamento boca
                elif (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BOCA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('LIMPEZA_ACABAMENTO_BOCA')
                    self.fel.insert_fel('LIMPEZA_ACABAMENTO_BOCA', vaso.getTimeAtual())
                # SE vaso na fila de preparacao boca
                elif (self.vasos.search_vaso('PREPARACAO_BOCA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('PREPARACAO_BOCA')
                    self.fel.insert_fel('PREPARACAO_BOCA', vaso.getTimeAtual())
                # SE vaso na fila de limpeza acabamento base
                elif (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BASE')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('LIMPEZA_ACABAMENTO_BASE')
                    self.fel.insert_fel('LIMPEZA_ACABAMENTO_BASE', vaso.getTimeAtual())
                # SE vaso na fila inicial
                elif (self.vasos.search_vaso('PREPARACAO_FORMA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_specialist('PREPARACAO_FORMA')
                    self.fel.insert_fel('PREPARACAO_FORMA', vaso.getTimeAtual())
                else:
                    # libera artesao
                    self.artesoes.libera_artisan(self.artesao.get_id())
            elif (self.artesao != None):
                # SE vaso na fila de limpeza acabamento boca
                if (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BOCA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_specialist('LIMPEZA_ACABAMENTO_BOCA')
                    self.fel.insert_fel('LIMPEZA_ACABAMENTO_BOCA', vaso.getTimeAtual())
                # SE vaso na fila de preparacao boca
                elif (self.vasos.search_vaso('PREPARACAO_BOCA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_specialist('PREPARACAO_BOCA')
                    self.fel.insert_fel('PREPARACAO_BOCA', vaso.getTimeAtual())
                # SE vaso na fila de limpeza acabamento base
                elif (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BASE')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_specialist('LIMPEZA_ACABAMENTO_BASE')
                    self.fel.insert_fel('LIMPEZA_ACABAMENTO_BASE', vaso.getTimeAtual())
                # SE vaso na fila inicial
                elif (self.vasos.search_vaso('PREPARACAO_FORMA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_specialist('PREPARACAO_FORMA')
                    self.fel.insert_fel('PREPARACAO_FORMA', vaso.getTimeAtual())

            self.artesao = self.artesoes.time_artisan('SECAGEM_BOCA', vaso.getTimeAtual())
            if self.artesao == None:
                self.artesao = self.artesoes.time_specialist('SECAGEM_BOCA', vaso.getTimeAtual())
                if self.artesao == None:
                    self.artesao = self.artesoes.aloca_artisan('SECAGEM_BOCA', vaso.getTimeAtual())
                if self.artesao == None:
                    self.artesao = self.artesoes.aloca_specialist('SECAGEM_BOCA', vaso.getTimeAtual())
                if self.artesao != None:
                    self.vasos.insert_vaso('IMPERMEABILIZACAO_INTERNA', vaso)
                    self.fel.insert_fel('IMPERMEABILIZACAO_INTERNA', vaso.getTimeAtual())
            else:
                self.vasos.insert_vaso('IMPERMEABILIZACAO_INTERNA', vaso)
                self.fel.insert_fel('IMPERMEABILIZACAO_INTERNA', vaso.getTimeAtual())

    ################### Existe uma fila entre essas 2 atividades

    def DCA_impermeabilizacao_interna(self):
        if self.vasos.search_vaso('IMPERMEABILIZACAO_INTERNA'):
            vaso = self.vasos.remove_vaso('IMPERMEABILIZACAO_INTERNA')
            # sorteia tempo de preparacao da boca
            x = self.CONST.get_IMP_INTERNA(vaso.get_size())
            rand = np.random.triangular(x[0], x[1], x[2])
            # rand = 2
            vaso.set_time_atual(int(rand))
            self.artesao = self.artesoes.get_artisan('IMPERMEABILIZACAO_INTERNA')
            if self.artesoes.have_artisan('IMPERMEABILIZACAO_INTERNA'):
                self.artesao = self.artesoes.aloca_artisan('SECAGEM_INTERNA', vaso.getTimeAtual())
                self.vasos.insert_vaso('SECAGEM_INTERNA', vaso)
                self.fel.insert_fel('SECAGEM_INTERNA', vaso.getTimeAtual())
            else:
                #self.artesoes.show()
                self.vasos.insert_vaso('IMPERMEABILIZACAO_INTERNA', vaso)
                self.fel.insert_fel('IMPERMEABILIZACAO_INTERNA', vaso.getTimeAtual())

    def DCA_secagem_interna(self):
        if self.vasos.search_vaso('SECAGEM_INTERNA'):
            vaso = self.vasos.remove_vaso('SECAGEM_INTERNA')
            x = self.CONST.get_SEC_INTERNA(vaso.get_size())
            rand = np.random.triangular(x[0], x[1], x[2])
            # rand = 300
            vaso.set_time_atual(int(rand))
            self.artesao = self.artesoes.get_artisan('SECAGEM_INTERNA')
            if (self.artesao != None) and (not self.artesao.isSpecialist()):
                # SE pouca massa (-25%)
                if (self.massa < self.pouca_massa):
                    # aloca o artesao para preparacao da massa
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('PREPARACAO_MASSA')
                    self.fel.insert_fel('PREPARACAO_MASSA', vaso.getTimeAtual())
                # SE pouca pedra (-25%)
                elif (self.pedra < self.pouca_pedra):
                    # aloca o artesao para coleta de pedra
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('PREPARACAO_PEDRA')
                    self.fel.insert_fel('PREPARACAO_PEDRA', vaso.getTimeAtual())
                # SE vaso na fila de envernizacao geral
                elif (self.vasos.search_vaso('ENVERNIZACAO_GERAL')):
                    # self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('ENVERNIZACAO_GERAL')
                    self.fel.insert_fel('ENVERNIZACAO_GERAL', vaso.getTimeAtual())
                # SE vaso na fila de impermeabilizacao interna
                elif (self.vasos.search_vaso('IMPERMEABILIZACAO_INTERNA')):
                    # self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('IMPERMEABILIZACAO_INTERNA')
                    self.fel.insert_fel('IMPERMEABILIZACAO_INTERNA', vaso.getTimeAtual())
                # SE vaso na fila de limpeza acabamento boca
                elif (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BOCA')):
                    # self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('LIMPEZA_ACABAMENTO_BOCA')
                    self.fel.insert_fel('LIMPEZA_ACABAMENTO_BOCA', vaso.getTimeAtual())
                # SE vaso na fila de preparacao boca
                elif (self.vasos.search_vaso('PREPARACAO_BOCA')):
                    # self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('PREPARACAO_BOCA')
                    self.fel.insert_fel('PREPARACAO_BOCA', vaso.getTimeAtual())
                # SE vaso na fila de limpeza acabamento base
                elif (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BASE')):
                    # self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('LIMPEZA_ACABAMENTO_BASE')
                    self.fel.insert_fel('LIMPEZA_ACABAMENTO_BASE', vaso.getTimeAtual())
                # SE vaso na fila inicial
                elif (self.vasos.search_vaso('PREPARACAO_FORMA')):
                    # self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_specialist('PREPARACAO_FORMA')
                    self.fel.insert_fel('PREPARACAO_FORMA', vaso.getTimeAtual())
                else:
                    #libera artesao
                    if self.artesao != None:
                        self.artesoes.libera_artisan(self.artesao.get_id())
            
            elif (self.artesao != None):
                # SE vaso na fila de limpeza acabamento boca
                if (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BOCA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_specialist('LIMPEZA_ACABAMENTO_BOCA')
                    self.fel.insert_fel('LIMPEZA_ACABAMENTO_BOCA', vaso.getTimeAtual())
                # SE vaso na fila de preparacao boca
                elif (self.vasos.search_vaso('PREPARACAO_BOCA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_specialist('PREPARACAO_BOCA')
                    self.fel.insert_fel('PREPARACAO_BOCA', vaso.getTimeAtual())
                # SE vaso na fila de limpeza acabamento base
                elif (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BASE')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_specialist('LIMPEZA_ACABAMENTO_BASE')
                    self.fel.insert_fel('LIMPEZA_ACABAMENTO_BASE', vaso.getTimeAtual())
                # SE vaso na fila inicial
                elif (self.vasos.search_vaso('PREPARACAO_FORMA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_specialist('PREPARACAO_FORMA')
                    self.fel.insert_fel('PREPARACAO_FORMA', vaso.getTimeAtual())

            if self.artesao == None:
                self.artesao = self.artesoes.time_specialist('SECAGEM_INTERNA', vaso.getTimeAtual())
                if self.artesao == None:
                    self.artesao = self.artesoes.aloca_artisan('SECAGEM_INTERNA', vaso.getTimeAtual())
                if self.artesao == None:
                    self.artesao = self.artesoes.aloca_specialist('SECAGEM_INTERNA', vaso.getTimeAtual())
                if self.artesao != None:
                    self.vasos.insert_vaso('ENVERNIZACAO_GERAL', vaso)
                    self.fel.insert_fel('ENVERNIZACAO_GERAL', vaso.getTimeAtual())
            else:
                self.vasos.insert_vaso('ENVERNIZACAO_GERAL', vaso)
                self.fel.insert_fel('ENVERNIZACAO_GERAL', vaso.getTimeAtual())

    ################### Existe uma fila entre essas 2 atividades

    def DCA_envernizacao_geral(self):
        if self.vasos.search_vaso('ENVERNIZACAO_GERAL'):
            vaso = self.vasos.remove_vaso('ENVERNIZACAO_GERAL')
            # sorteia tempo de preparacao da boca
            x = self.CONST.get_ENV_GERAL(vaso.get_size())
            rand = np.random.triangular(x[0], x[1], x[2])
            # rand = 7
            vaso.set_time_atual(int(rand))
            if self.artesoes.have_artisan('ENVERNIZACAO_GERAL'):
                self.vasos.insert_vaso('SECAGEM_ENVERNIZACAO', vaso)
                self.fel.insert_fel('SECAGEM_ENVERNIZACAO', vaso.getTimeAtual())
            else:
                self.vasos.insert_vaso('ENVERNIZACAO_GERAL', vaso)
                self.fel.insert_fel('ENVERNIZACAO_GERAL', vaso.getTimeAtual())

    def DCA_secagem_envernizacao(self):
        if self.vasos.search_vaso('SECAGEM_ENVERNIZACAO'):
            vaso = self.vasos.remove_vaso('SECAGEM_ENVERNIZACAO')
            x = self.CONST.get_SEC_FINAL(vaso.get_size())
            rand = np.random.triangular(x[0], x[1], x[2])
            # rand = 1020
            vaso.set_time_atual(int(rand))
            self.vasos.insert_vaso('FIM', vaso)
            self.fel.insert_fel('FIM', vaso.getTimeAtual())
            self.vasos.set_end_time(vaso, vaso.getTimeAtual())	

file = open(arquivoLog, "a")
file.write("TEMP_SIMULACAO\tUSO_MASSA\tUSO_PEDRA\tCOMP_TIME_PEQ\tCOMP_TIME_MED\tCOMP_TIME_GRAN\tNUM_VASOS\tSEED" + "\n")

sementes = [24681,18459,31106,18127,19936,16876,1968,19800,28415,14632,4081,20839,19877,9786,18827,19546,20748,27947,17061,27946,28648,28962,30130,1709,19917,25396,3240,32123,21303,27023,14632,6149,11687,26474,27961,26527,9286,311,7142,12022,7089,14254,14990,27002,27579,23673,9089,8110,1917,16840,27541,1751,10578,28322,27781,11243,31562,29106,6667,27419,25160,1426,26214,28784,18936,19856,19767,28665,30856,25689,19824,31524,11106,28059,30336,22728,15797,15256,5457,11031,1912,25615,15482,6981,23828,22632,10487,28817,18845,26077,5725,23839,14243,23506,17627,6808,3984,22000,4445,30718,1611,24915,16515,28184,7762,19993,32172,12530,24794,13962,23765,22722,22082,12839,13792,2713,27718,1182,12902,25034,12576,17455,30789,2980,29467,32008,19839,371,10622,17404,5514,17843,32083,24722,13973,6151,29727,14604,19056,6464,16635,13532,25055,3400,32703,22411,6038,31809,20623,24424,9718,29962,26979,5501,20163,5139,1301,3638,2831,10687,27397,6565,20126,2180,15716,6808,9865,3144,22180,23012,15318,30553,10851,19196,28248,32363,14793,20926,14876,7659,23183,25502,15452,30363,29773,29786,20783,3536,26415,17487,22378,2078,28786,24923,19546,22267,2711,23809,29367,32354,32704,20047,21192,24895,29352,31627,961,9464,20639,5022,4313,8049,13499,6803,25656,15411,14500,10341,8935,29786,31493,8437,20971,7269,18859,5891,16669,27199,22731,12765,16810,2415,27526,24683,19969,13814,16913,7985,23486,11923,20798,19794,28948,3661,29725,10430,31384,16954,10882,29187,11492,15333,18748,2443,15620,21201,8494,22287,9430,30350,3263,3688,23419,9260,19012,16674,17613,2511,8203,13051,3427,26212,13594,24524,29475,3646,11006,4453,11359,17865,5753,29426,6580,8311,16775,14033,1078,5603,1950,15798,9443,27538,16411,28063,28852,27349,32065,27519,5810,6861,5171,12816,29537,32116,31885,5328,29059,22246,8519,25411,25794,14480,3094,12067,21951,30604,3469,11507,15419,23685,12590,28450,10989,20492,25826,23492,25114,7020,1321,28275,26190,9477,5026,3568,11372,26456,31225,22811,31982,30654,24060,24724,17246,2505,5504,7140,20433,9286,2095,23021,23688,31915,20086,13829,12847,21824,6761,24613,9461,26282,9570,1384,8494,26879,19773,26054,22572,27613,13038,21741,10873,32450,4866,32633,30143,21750,5006,2751,7423,11445,24354,18085,6979,20964,22900,24935,18725,11874,12697,24533,19165,10248,18078,12314,32034,31635,6153,4017,28275,28921,5461,11471,24012,10424,23682,32049,19836,15818,13593,1028,17658,10068,8829,17510,17202,11944,8817,14438,18755,31081,3386,7019,18701,2276,14991,14638,32377,22344,15790,6846,14790,12570,10399,28688,16044,9490,20132,31000,17050,9697,4943,15786,7717,19422,25180,2049,7041,19257,4285,29904,12950,16734,13029,28537,2052,32164,13166,14869,24864,4598,15780,2002,2510,23465,26775,20538,14023,18093,10166,22847,15202,21429,15528,17448,10686,1372,28743,17751,23259,25989,14697,8534,19115,11696,621,1971,2569,26174,7950,20605,17751,28937,14234,26776,4926,21243,25237,23292,5294,24206,23055,4230,2147,19902,13544,7712,31737,13472,3579,24345,26165,18137,31027,13545,25703,24215,12822,25949,31554,14493,28654,11251,3084,9671,18358,2641,16510,9837,30683,30544,15929,4751,1746,24370,29544,21952,25514,27780,2556,3953,24837,14098,11357,17216,13342,8445,23352,28050,15502,12243,30268,26589,25267,3581,25450,18445,21336,21135,11672,1850,28895,20653,14196,11338,15435,31707,7695,29353,18761,28227,9314,23419,7191,7874,3146,9651,10679,22625,25084,7557,18032,6774,24436,26702,4400,1639,26542,26231,19646,26813,25344,9419,10647,9629,30051,18586,31699,26355,31434,4352,21161,5009,8599,30264,29081,11888,18907,21277,17170,25893,28022,24849,11082,2161,27806,12587,15035,24491,23191,5082,30385,5184,10671,23736,26461,14194,15339,20128,6797,17440,10788,15817,25321,21995,22225,21313,1483,4022,32265,9933,25950,7714,2029,9621,23146,30090,18945,15256,11863,29082,18615,30956,30557,12307,26463,12241,25744,20925,22609,25491,8891,8837,26194,18637,16621,16157,2546,8414,3287,4793,16638,6656,1985,15962,11008,6488,26665,23627,24588,19947,9048,8587,17276,8621,15304,23066,32037,15250,30508,29656,32613,28008,18696,20937,28549,6274,11633,22453,27221,10327,9768,5491,22929,25274,21549,22201,3511,7256,2121,5574,14691,7135,3647,21410,24756,3341,14408,2462,9541,27785,8054,8075,27975,3135,13521,5065,3513,9181,10057,23020,5882,14315,22644,26281,29345,17979,24902,27941,13715,2941,4140,15825,5446,16817,26724,7877,15017,11971,7624,28632,22875,1561,2922,23609,13069,17225,4010,4729,26449,12698,2565,29629,11930,7407,8837,25784,3549,17653,21392,21303,30215,27162,31546,20759,22757,14983,13793,25932,28921,9015,6577,29863,9556,26578,10305,18011,6225,3421,1811,3627,12430,25795,20797,12986,31122,1875,4000,31013,8135,20447,16727,19956,1913,20915,20503,14337,22638,13139,10098,22198,30279,12810,20929,3682,31441,23581,9259,10368,5218,20176,21746,28290,19591,16804,11256,13395,28149,11321,22999,15723,30064,15588,17363,24796,14364,18340,5721,18503,14443,5378,24228,27874,28659,23053,5101,21578,30429,13999,23328,8613,3141,8961,7031,18530,10882,32026,19843,25377,9429,11162,18803,15661,31801,5592,8940,22207,18293,23917,15156,5123,29197,26335,25039,26291,8544,12632,11969,11807,9086,21694,17301,8342,28597,21784,7462,23170,15403,16879,22296,6157,12880,12119,8303,30995,23722,14733,3356,13555,29599,26822,19199,21712,18716,3891,22543,28987,32248,25948,12944,13196,12264,12994,27510,17098,25154,6222,11801,10165,3543,15830,15917,13756,19980,1612,31017,1673,7273,14445,6824,15033,21885,10027,8067,30757,31944,20585,23571,31475,1377,15495,7281,17989,32412,22751,11763,20840,7621,27667,32095,9664,9771,11931,32370,29324,29416,6385,1182,23007,28802,8385,5979,3271,31416,21145,31527,19694,20972,27526,20115,17261,27000,19050,1995,13001,11735,5731,9738,6517,25861,17803,10898,4088,6727,25643,23158,7304,22444,29863,13006,32583,6752,12908,29796,3456,24760,27562,30015,13325,24171,17908,14211]
simulator = simulator(sementes[0])

for k in range(0, 10):
    simulator.__init__(sementes[k]) 
    completionTimePeq = completionPeq/qtdPeq
    completionTimeMed = completionMed/qtdMed
    completionTimeGran = completionGran/qtdGran

    massaUtilizadaPeq = qtdPeq*simulator.CONST.get_USO_MASSA('S')
    massaUtilizadaMed = qtdMed*simulator.CONST.get_USO_MASSA('M')
    massaUtilizadaGran = qtdGran*simulator.CONST.get_USO_MASSA('B')
    massaUtilizada = massaUtilizadaPeq + massaUtilizadaMed + massaUtilizadaGran

    pedraUtilizadaPeq = qtdPeq*simulator.CONST.get_USO_PEDRA('S')
    pedraUtilizadaMed = qtdMed*simulator.CONST.get_USO_PEDRA('M')
    pedraUtilizadaGran = qtdGran*simulator.CONST.get_USO_PEDRA('B')
    pedraUtilizada = pedraUtilizadaPeq + pedraUtilizadaMed + pedraUtilizadaGran

    file.write(str(simulationTime) + '\t' + str(massaUtilizada) + '\t' + str(pedraUtilizada) + '\t' + '\t' + str(completionTimePeq) + '\t' + str(completionTimeMed) + '\t' + str(completionTimeGran) + '\t' + str(totalVasos) + '\t' + str(sementes[k]) + "\n")
file.close()
