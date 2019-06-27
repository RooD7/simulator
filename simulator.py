import vaso as Vaso
import inputFile as InputFile
import const as Const
import fel as Fel
import filaVaso as FilaVaso
import artesao as Artesao
import listaArtesao as ListaArtesao
import numpy as np

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

massaUtilizada = 0
pedraUtilizada = 0
prodArtesao = 0
prodEspecialista = 0
completionTimeVasoPeq = 0
completionTimeVasoMed = 0
completionTimeVasoGran = 0
seedUtilised = 0
simulationTime = 1

arquivoLog = "simulacao2.tsv"

class simulator(object):

    def __init__(self):
        self.fel = Fel.Fel()
        self.vasos = FilaVaso.FilaVaso()

        inpFile = InputFile.InputFile()

        self.CONST = Const.Const()
        self.CONST = inpFile.inputs('entrada.txt')

        self.time_system = 0
        # np.random.seed(self.CONST.get_G_TSM())
        np.random.seed(7316)
        self.massa = self.CONST.get_QTD_MASSA()
        self.pedra = self.CONST.get_QTD_PEDRA()
        self.pouca_massa = 250
        self.pouca_pedra = 250
        self.artesoes = ListaArtesao.ListaArtesao()
        self.uso_esp_sec = 0
        self.vaso = None
        print("TEMPO e " + str(self.time_system))
        self.artesao = None
        self.novoLote = True
        self.tempoNovoLote = 0
        self.simuTime = simulationTime
        # for i in range(self.CONST.get_NUM_ART()):
        for i in range(0, 1):
            self.artesoes.insert_new_artesao(specialist=False)
            self.artesao = self.artesoes.aloca_artisan('PREPARACAO_FORMA')
        # for i in range(self.CONST.get_NUM_ESP()):
        # for i in range(0, 1):
        #     self.artesoes.insert_new_artesao(specialist=True)
        #     self.artesao = self.artesoes.aloca_specialist('PREPARACAO_FORMA')


    def felControl(self):
        # ordena a fel

        while self.fel.get_fel_size() != 0:
            print('TAM FEL: '+str(self.fel.get_fel_size()))
            self.fel.sorted_fel()
            atividade = self.fel.remove_fel()
            self.time_system = atividade.get_time_event()
            self.artesoes.alocados(self.time_system)
            #print('ATIVIDADE: '+ str(atividade.get_time_event()))
            #print('TIME: '+ str(self.time_system))
            # print('##### '+atividade.get_ativ_event().name+' - Time_System: '+str(self.time_system))

            # if self.time_system > self.simuTime:
            #     pass
            if atividade.get_ativ_event().name == 'CHEGADA_PEDIDO':
                pass
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
            elif atividade.get_ativ_event().name == 'FIM':
                break
        print('TIME SYSTEM: ', str(self.time_system))
        self.fel.show()
        x = self.CONST.get_FREQ_PED()
        freq = np.random.triangular(x[0], x[1], x[2])
        self.tempoNovoLote = self.time_system + freq
        if self.tempoNovoLote < simulationTime:
            print('ENTROU: ', str(self.time_system))
            self.time_system = self.tempoNovoLote
            self.novoLote = True
            self.DCA_chegada_pedido()
        # self.simuTime -= self.time_system
            # if self.fel.get_fel_size() == 1:
            #     self.fel.show()
            #     self.vasos.show()
        self.artesoes.show()
        self.vasos.show()

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
        x = self.CONST.get_PREP_MASSA()
        # rand = np.random.triangular(x[0], x[1], x[2])
        rand = 10
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
        x = self.CONST.get_PREP_PEDRA()
        # rand = np.random.triangular(x[0], x[1], x[2])
        rand = 90
        pedraUtilizada += rand
        self.fel.insert_fel('PREPARACAO_PEDRA', self.time_system + rand)
        if self.artesao.isSpecialist():
            self.artesoes.time_specialist('PREPARACAO_PEDRA', self.artesao.get_id, 
                self.time_system + rand)
        else:
            self.artesoes.time_artisan('PREPARACAO_PEDRA', self.artesao.get_id, 
                self.time_system + rand)

    def DCA_chegada_pedido(self):
        # frequencia de chegada de pedidos
        #if self.novoLote:
        #    x = self.CONST.get_FREQ_PED()
        #    freq = np.random.triangular(x[0], x[1], x[2])
        #    self.tempoNovoLote = self.time_system + freq
        #    self.novoLote = False
        
        # tamanho do pedido (seguindo a probabilidade do CONST)
        x = self.CONST.get_TAM_PED()
        # num_pedidos = np.random.triangular(x[0], x[1], x[2])
        num_pedidos = 1
        # lista de tamanho dos vasos
        sizes = self.probSizeVaso(num_pedidos)
        # serao feitos 'num_pedidos' pedidos
        print('!!! NOVO LOTE de '+str(int(num_pedidos))+' vasos.')
        self.fel = Fel.Fel()
        # for r in range(0, int(num_pedidos)):
        for r in range(0, 1):
            self.vasos.insert_new_vaso('PREPARACAO_FORMA', 'S', self.time_system)
            # self.vasos.insert_new_vaso('PREPARACAO_FORMA', sizes[r], self.time_system)
            self.fel.insert_fel('PREPARACAO_FORMA', self.time_system)
        # for r in range(0, len(self.artesoes.get_lista())):
        #     self.artesao = self.artesoes.aloca_artisan('PREPARACAO_FORMA')
        # self.DCA_preparacao_forma()
        # self.fel.insert_fel('PREPARACAO_FORMA', self.time_system)
        self.felControl()

    ################### Existe uma fila entre essas 2 atividades

    def DCA_preparacao_forma(self):
        if self.vasos.search_vaso('PREPARACAO_FORMA'):
            vaso = self.vasos.remove_vaso('PREPARACAO_FORMA')
            # espaco de secagem
            if (self.uso_esp_sec < self.CONST.get_ESP_SEC()):
                # massa suficiente
                if (self.massa > self.pouca_massa):
                    if self.artesoes.have_specialist('PREPARACAO_FORMA'):
                        # sorteia tempo de preparacao da forma
                        x = self.CONST.get_PREP_FORM(vaso.get_size())
                        # rand = np.random.triangular(x[0], x[1], x[2])
                        rand = 1
                        self.artesao = self.artesoes.time_specialist('PREPARACAO_FORMA', self.time_system + int(rand))
                        self.fel.insert_fel('PREPARACAO_BASE', self.time_system + int(rand))
                        self.vasos.insert_vaso('PREPARACAO_BASE', vaso)
                    elif self.artesoes.have_artisan('PREPARACAO_FORMA'):
                        x = self.CONST.get_PREP_FORM(vaso.get_size())
                        # rand = np.random.triangular(x[0], x[1], x[2])
                        rand = 1
                        self.artesao = self.artesoes.time_artisan('PREPARACAO_FORMA', self.time_system + int(rand))
                        self.fel.insert_fel('PREPARACAO_BASE', self.time_system + int(rand))
                        self.vasos.insert_vaso('PREPARACAO_BASE', vaso)
                else:
                    # coloca vaso na fila de preparacao da forma
                    self.vasos.insert_vaso('PREPARACAO_FORMA', vaso)
                    self.fel.insert_fel('PREPARACAO_MASSA', self.time_system)
            else:
                # coloca vaso na fila de preparacao da forma
                self.vasos.insert_vaso('PREPARACAO_FORMA', vaso)
                self.fel.insert_fel('PREPARACAO_FORMA', self.time_system)

    def DCA_preparacao_base(self):
        if self.vasos.search_vaso('PREPARACAO_BASE'):
            vaso = self.vasos.remove_vaso('PREPARACAO_BASE')
            x = self.CONST.get_PREP_BASE(vaso.get_size())
            # rand = np.random.triangular(x[0], x[1], x[2])
            rand = 10
            self.artesao = self.artesoes.get_artisan('PREPARACAO_BASE')
            self.artesao = self.artesoes.time_artisan('PREPARACAO_BASE', self.time_system + int(rand))
            print('A')
            if self.artesao == None:
                print('AA')
                self.artesao = self.artesoes.time_specialist('PREPARACAO_BASE', self.time_system + int(rand))
                if self.artesao == None:
                    print('AAA')
                    self.artesao = self.artesoes.aloca_artisan('PREPARACAO_BASE', self.time_system + int(rand))
                if self.artesao == None:
                    print('AAAA')
                    self.artesao = self.artesoes.aloca_specialist('PREPARACAO_BASE', self.time_system + int(rand))
            if self.artesao != None:
                print('AAAAA')
                self.vasos.insert_vaso('ACABAMENTO_INICIAL_BASE', vaso)
                self.fel.insert_fel('ACABAMENTO_INICIAL_BASE', self.time_system + int(rand))
        # else:
        #     self.fel.insert_fel('PREPARACAO_BASE', self.time_system)

    def DCA_acabamento_inicial_base(self):
        # self.vasos.show()
        print('B')
        if self.vasos.search_vaso('ACABAMENTO_INICIAL_BASE'):
            print('BB')
            vaso = self.vasos.remove_vaso('ACABAMENTO_INICIAL_BASE')
            x = self.CONST.get_ACAB_INI_BOCA(vaso.get_size())
            # rand = np.random.triangular(x[0], x[1], x[2])
            rand = 2
            self.artesao = self.artesoes.get_artisan('ACABAMENTO_INICIAL_BASE')
            self.artesao = self.artesoes.time_artisan('ACABAMENTO_INICIAL_BASE', self.time_system + int(rand))
            if self.artesao == None:
                self.artesao = self.artesoes.time_specialist('ACABAMENTO_INICIAL_BASE', self.time_system + int(rand))
                if self.artesao == None:
                    self.artesao = self.artesoes.aloca_artisan('ACABAMENTO_INICIAL_BASE', self.time_system + int(rand))
                if self.artesao == None:
                    self.artesao = self.artesoes.aloca_specialist('ACABAMENTO_INICIAL_BASE', self.time_system + int(rand))
            if self.artesao != None:
                self.vasos.insert_vaso('SECAGEM_ACABAMENTO_BASE', vaso)
                self.fel.insert_fel('SECAGEM_ACABAMENTO_BASE', self.time_system + int(rand))
        # else:
        #     self.fel.insert_fel('ACABAMENTO_INICIAL_BASE', self.time_system)
        # self.artesoes.show()
        # self.DCA_secagem_acabamento_base()

    def DCA_secagem_acabamento_base(self):
        if self.vasos.search_vaso('SECAGEM_ACABAMENTO_BASE'):
            vaso = self.vasos.remove_vaso('SECAGEM_ACABAMENTO_BASE')
            # SE recurso alocado atual == artesao
            self.artesao = self.artesoes.get_artisan('SECAGEM_ACABAMENTO_BASE')
            if (self.artesao != None) and (not self.artesao.isSpecialist()):
                # SE pouca massa (-25%)
                if (self.massa < self.pouca_massa):
                    # aloca o artesao para preparacao da massa
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('PREPARACAO_MASSA')
                    self.fel.insert_fel('PREPARACAO_MASSA', self.time_system)
                # SE pouca pedra (-25%)
                elif (self.pedra < self.pouca_pedra):
                    # aloca o artesao para coleta de pedra
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('PREPARACAO_PEDRA')
                    self.fel.insert_fel('PREPARACAO_PEDRA', self.time_system)
                # SE vaso na fila de envernizacao geral
                elif (self.vasos.search_vaso('ENVERNIZACAO_GERAL')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('ENVERNIZACAO_GERAL')
                    self.fel.insert_fel('ENVERNIZACAO_GERAL', self.time_system)
                # SE vaso na fila de impermeabilizacao interna
                elif (self.vasos.search_vaso('IMPERMEABILIZACAO_INTERNA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('IMPERMEABILIZACAO_INTERNA')
                    self.fel.insert_fel('IMPERMEABILIZACAO_INTERNA', self.time_system)
                # SE vaso na fila de limpeza acabamento boca
                elif (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BOCA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('LIMPEZA_ACABAMENTO_BOCA')
                    self.fel.insert_fel('LIMPEZA_ACABAMENTO_BOCA', self.time_system)
                # SE vaso na fila de preparacao boca
                elif (self.vasos.search_vaso('PREPARACAO_BOCA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('PREPARACAO_BOCA')
                    self.fel.insert_fel('PREPARACAO_BOCA', self.time_system)
                # SE vaso na fila de preparacao boca
                elif (self.vasos.search_vaso('ACABAMENTO_INICIAL_BASE')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('ACABAMENTO_INICIAL_BASE')
                    self.fel.insert_fel('ACABAMENTO_INICIAL_BASE', self.time_system)
                # SE vaso na fila inicial
                elif (self.vasos.search_vaso('PREPARACAO_FORMA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('PREPARACAO_FORMA')
                    self.fel.insert_fel('PREPARACAO_FORMA', self.time_system)
                else:
                    #libera artesao
                    self.artesoes.libera_artisan(self.artesao.get_id())
            elif (self.artesao != None):
                # SE vaso na fila de limpeza acabamento boca
                if (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BOCA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_specialist('LIMPEZA_ACABAMENTO_BOCA')
                    self.fel.insert_fel('LIMPEZA_ACABAMENTO_BOCA', self.time_system)
                # SE vaso na fila de preparacao boca
                elif (self.vasos.search_vaso('PREPARACAO_BOCA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_specialist('PREPARACAO_BOCA')
                    self.fel.insert_fel('PREPARACAO_BOCA', self.time_system)
                # SE vaso na fila de preparacao boca
                elif (self.vasos.search_vaso('ACABAMENTO_INICIAL_BASE')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_specialist('ACABAMENTO_INICIAL_BASE')
                    self.fel.insert_fel('ACABAMENTO_INICIAL_BASE', self.time_system)
                # SE vaso na fila inicial
                elif (self.vasos.search_vaso('PREPARACAO_FORMA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_specialist('PREPARACAO_FORMA')
                    self.fel.insert_fel('PREPARACAO_FORMA', self.time_system)

            x = self.CONST.get_SEC_ACAB(vaso.get_size())
            # rand = np.random.triangular(x[0], x[1], x[2])
            rand = 6
            self.artesao = self.artesoes.time_artisan('SECAGEM_ACABAMENTO_BASE', self.time_system + int(rand))
            if self.artesao == None:
                self.artesao = self.artesoes.time_specialist('SECAGEM_ACABAMENTO_BASE', self.time_system + int(rand))
                if self.artesao == None:
                    self.artesao = self.artesoes.aloca_artisan('SECAGEM_ACABAMENTO_BASE', self.time_system + int(rand))
                if self.artesao == None:
                    self.artesao = self.artesoes.aloca_specialist('SECAGEM_ACABAMENTO_BASE', self.time_system + int(rand))
            if self.artesao != None:
                self.vasos.insert_vaso('LIMPEZA_ACABAMENTO_BASE', vaso)
                self.fel.insert_fel('LIMPEZA_ACABAMENTO_BASE', self.time_system + int(rand))
            else:
                self.fel.insert_fel('SECAGEM_ACABAMENTO_BASE', self.time_system + int(rand))
        # else:
        #     self.fel.insert_fel('SECAGEM_ACABAMENTO_BASE', self.time_system)
    
    ################### Existe uma fila entre essas 2 atividades

    def DCA_limpeza_acabamento_base(self):
        if self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BASE'):
            vaso = self.vasos.remove_vaso('LIMPEZA_ACABAMENTO_BASE')
            self.artesao = self.artesoes.get_artisan('LIMPEZA_ACABAMENTO_BASE')
            if self.artesoes.have_specialist('LIMPEZA_ACABAMENTO_BASE'):
                # sorteia tempo de limpeza acabamento base
                x = self.CONST.get_LIMP_ACAB_BASE(vaso.get_size())
                # rand = np.random.triangular(x[0], x[1], x[2])
                rand = 4
                self.artesao = self.artesoes.aloca_specialist('LIMPEZA_ACABAMENTO_BASE', self.time_system + int(rand))
                self.vasos.insert_vaso('SECAGEM_BASE', vaso)
                self.fel.insert_fel('SECAGEM_BASE', self.time_system + int(rand))
            elif self.artesoes.have_artisan('LIMPEZA_ACABAMENTO_BASE'):
                x = self.CONST.get_LIMP_ACAB_BASE(vaso.get_size())
                # rand = np.random.triangular(x[0], x[1], x[2])
                rand = 4
                self.artesao = self.artesoes.aloca_artisan('LIMPEZA_ACABAMENTO_BASE', self.time_system + int(rand))
                self.vasos.insert_vaso('SECAGEM_BASE', vaso)
                self.fel.insert_fel('SECAGEM_BASE', self.time_system + int(rand))
            else:
                self.vasos.insert_vaso('LIMPEZA_ACABAMENTO_BASE', vaso)
                self.fel.insert_fel('LIMPEZA_ACABAMENTO_BASE', self.time_system)
        # else:
        #     self.fel.insert_fel('LIMPEZA_ACABAMENTO_BASE', self.time_system)

    def DCA_secagem_base(self):
        if self.vasos.search_vaso('SECAGEM_BASE'):
            vaso = self.vasos.remove_vaso('SECAGEM_BASE')
            self.artesao = self.artesoes.get_artisan('SECAGEM_BASE')
            if (self.artesao != None) and (not self.artesao.isSpecialist()):
                # SE pouca massa (-25%)
                if (self.massa < self.pouca_massa):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('SECAGEM_BASE')
                    self.fel.insert_fel('PREPARACAO_MASSA', self.time_system)
                # SE pouca pedra (-25%)
                elif (self.pedra < self.pouca_pedra):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('SECAGEM_BASE')
                    self.fel.insert_fel('PREPARACAO_PEDRA', self.time_system)
                # SE vaso na fila de envernizacao geral
                elif (self.vasos.search_vaso('ENVERNIZACAO_GERAL')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('ENVERNIZACAO_GERAL')
                    self.fel.insert_fel('ENVERNIZACAO_GERAL', self.time_system)
                # SE vaso na fila de impermeabilizacao interna
                elif (self.vasos.search_vaso('IMPERMEABILIZACAO_INTERNA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('IMPERMEABILIZACAO_INTERNA')
                    self.fel.insert_fel('IMPERMEABILIZACAO_INTERNA', self.time_system)
                # SE vaso na fila de limpeza acabamento boca
                elif (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BOCA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('LIMPEZA_ACABAMENTO_BOCA')
                    self.fel.insert_fel('LIMPEZA_ACABAMENTO_BOCA', self.time_system)
                # SE vaso na fila de preparacao boca
                elif (self.vasos.search_vaso('PREPARACAO_BOCA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('PREPARACAO_BOCA')
                    self.fel.insert_fel('PREPARACAO_BOCA', self.time_system)
                # SE vaso na fila de limpeza acabamento base
                elif (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BASE')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('LIMPEZA_ACABAMENTO_BASE')
                    self.fel.insert_fel('LIMPEZA_ACABAMENTO_BASE', self.time_system)
                # SE vaso na fila inicial
                elif (self.vasos.search_vaso('PREPARACAO_FORMA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('PREPARACAO_FORMA')
                    self.fel.insert_fel('PREPARACAO_FORMA', self.time_system)
                else:
                    #libera artesao
                    self.libera_artisan(self.artesao.get_id())
            elif (self.artesao != None):
                # SE vaso na fila de limpeza acabamento boca
                if (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BOCA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_specialist('LIMPEZA_ACABAMENTO_BOCA')
                    self.fel.insert_fel('LIMPEZA_ACABAMENTO_BOCA', self.time_system)
                # SE vaso na fila de preparacao boca
                elif (self.vasos.search_vaso('PREPARACAO_BOCA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_specialist('PREPARACAO_BOCA')
                    self.fel.insert_fel('PREPARACAO_BOCA', self.time_system)
                # SE vaso na fila de limpeza acabamento base
                elif (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BASE')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_specialist('LIMPEZA_ACABAMENTO_BASE')
                    self.fel.insert_fel('LIMPEZA_ACABAMENTO_BASE', self.time_system)
                # SE vaso na fila inicial
                elif (self.vasos.search_vaso('PREPARACAO_FORMA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_specialist('PREPARACAO_FORMA')
                    self.fel.insert_fel('PREPARACAO_FORMA', self.time_system)

            x = self.CONST.get_SEC_BASE(vaso.get_size())
            # rand = np.random.triangular(x[0], x[1], x[2])
            rand = 180
            self.artesao = self.artesoes.time_artisan('SECAGEM_BASE', self.time_system + int(rand))
            if self.artesao == None:
                self.artesao = self.artesoes.time_specialist('SECAGEM_BASE', self.time_system + int(rand))
                if self.artesao == None:
                    self.artesao = self.artesoes.aloca_artisan('SECAGEM_BASE', self.time_system + int(rand))
                if self.artesao == None:
                    self.artesao = self.artesoes.aloca_specialist('SECAGEM_BASE', self.time_system + int(rand))
                if self.artesao != None:
                    self.vasos.insert_vaso('PREPARACAO_BOCA', vaso)
                    self.fel.insert_fel('PREPARACAO_BOCA', self.time_system + int(rand))
            else:
                self.fel.insert_fel('SECAGEM_BASE', self.time_system + int(rand))
        # else:
        #     self.fel.insert_fel('SECAGEM_BASE', self.time_system)

    ################### Existe uma fila entre essas 2 atividades

    def DCA_preparacao_boca(self):
        if self.vasos.search_vaso('PREPARACAO_BOCA'):
            vaso = self.vasos.remove_vaso('PREPARACAO_BOCA')
            self.artesao = self.artesoes.get_artisan('PREPARACAO_BOCA')
            if self.artesoes.have_specialist('PREPARACAO_BOCA'):
                # sorteia tempo de preparacao da boca
                x = self.CONST.get_PREP_BOCA(vaso.get_size())
                # rand = np.random.triangular(x[0], x[1], x[2])
                rand = 6
                self.artesao = self.artesoes.time_specialist('PREPARACAO_BOCA', self.time_system + int(rand))
                self.vasos.insert_vaso('ACABAMENTO_INICIAL_BOCA', vaso)
                self.fel.insert_fel('ACABAMENTO_INICIAL_BOCA', self.time_system + int(rand))
            elif self.artesoes.have_artisan('PREPARACAO_BOCA'):
                x = self.CONST.get_PREP_BOCA(vaso.get_size())
                # rand = np.random.triangular(x[0], x[1], x[2])
                rand = 6
                self.artesao = self.artesoes.time_artisan('PREPARACAO_BOCA', self.time_system + int(rand))
                self.vasos.insert_vaso('ACABAMENTO_INICIAL_BOCA', vaso)
                self.fel.insert_fel('ACABAMENTO_INICIAL_BOCA', self.time_system + int(rand))
            else:
                self.vasos.insert_vaso('PREPARACAO_BOCA', vaso)
                self.fel.insert_fel('PREPARACAO_BOCA', self.time_system)
        # else:
        #     self.fel.insert_fel('PREPARACAO_BOCA', self.time_system)

    def DCA_acabamento_inicial_boca(self):
        if self.vasos.search_vaso('ACABAMENTO_INICIAL_BOCA'):
            vaso = self.vasos.remove_vaso('ACABAMENTO_INICIAL_BOCA')
            x = self.CONST.get_ACAB_INI_BOCA(vaso.get_size())
            # rand = np.random.triangular(x[0], x[1], x[2])
            rand = 2
            self.artesao = self.artesoes.get_artisan('ACABAMENTO_INICIAL_BOCA')
            self.artesao = self.artesoes.time_artisan('ACABAMENTO_INICIAL_BOCA', self.time_system + int(rand))
            if self.artesao == None:
                self.artesao = self.artesoes.time_specialist('ACABAMENTO_INICIAL_BOCA', self.time_system + int(rand))
                if self.artesao == None:
                    self.artesao = self.artesoes.aloca_artisan('ACABAMENTO_INICIAL_BOCA', self.time_system + int(rand))
                if self.artesao == None:
                    self.artesao = self.artesoes.aloca_specialist('ACABAMENTO_INICIAL_BOCA', self.time_system + int(rand))
                if self.artesao != None:
                    self.vasos.insert_vaso('SECAGEM_ACABAMENTO_BOCA', vaso)
                    self.fel.insert_fel('SECAGEM_ACABAMENTO_BOCA', self.time_system + int(rand))
            else:
                self.vasos.insert_vaso('ACABAMENTO_INICIAL_BOCA', vaso)
                self.fel.insert_fel('SECAGEM_ACABAMENTO_BOCA', self.time_system + int(rand))
        # else:
        #     self.fel.insert_fel('ACABAMENTO_INICIAL_BOCA', self.time_system)

    def DCA_secagem_acabamento_boca(self):
        if self.vasos.search_vaso('SECAGEM_ACABAMENTO_BOCA'):
            vaso = self.vasos.remove_vaso('SECAGEM_ACABAMENTO_BOCA')
            self.artesao = self.artesoes.get_artisan('SECAGEM_ACABAMENTO_BOCA')
            if (self.artesao != None) and (not self.artesao.isSpecialist()):
                # SE pouca massa (-25%)
                if (self.massa < self.pouca_massa):
                    # aloca o artesao para preparacao da massa
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('PREPARACAO_MASSA')
                    self.fel.insert_fel('PREPARACAO_MASSA', self.time_system)
                # SE pouca pedra (-25%)
                elif (self.pedra < self.pouca_pedra):
                    # aloca o artesao para preparacao da massa
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('PREPARACAO_PEDRA')
                    self.fel.insert_fel('PREPARACAO_PEDRA', self.time_system)
                # SE vaso na fila de envernizacao geral
                elif (self.vasos.search_vaso('ENVERNIZACAO_GERAL')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('ENVERNIZACAO_GERAL')
                    self.fel.insert_fel('ENVERNIZACAO_GERAL', self.time_system)
                # SE vaso na fila de impermeabilizacao interna
                elif (self.vasos.search_vaso('IMPERMEABILIZACAO_INTERNA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('IMPERMEABILIZACAO_INTERNA')
                    self.fel.insert_fel('IMPERMEABILIZACAO_INTERNA', self.time_system)
                # SE vaso na fila de limpeza acabamento boca
                elif (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BOCA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('LIMPEZA_ACABAMENTO_BOCA')
                    self.fel.insert_fel('LIMPEZA_ACABAMENTO_BOCA', self.time_system)
                # SE vaso na fila de preparacao boca
                elif (self.vasos.search_vaso('PREPARACAO_BOCA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('PREPARACAO_BOCA')
                    self.fel.insert_fel('PREPARACAO_BOCA', self.time_system)
                # SE vaso na fila de limpeza acabamento base
                elif (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BASE')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('LIMPEZA_ACABAMENTO_BASE')
                    self.fel.insert_fel('LIMPEZA_ACABAMENTO_BASE', self.time_system)
                # SE vaso na fila inicial
                elif (self.vasos.search_vaso('PREPARACAO_FORMA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('PREPARACAO_FORMA')
                    self.fel.insert_fel('PREPARACAO_FORMA', self.time_system)
                else:
                    #libera artesao
                    self.libera_artisan(self.artesao.get_id())
            elif (self.artesao != None):
                # SE vaso na fila de limpeza acabamento boca
                if (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BOCA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_specialist('LIMPEZA_ACABAMENTO_BOCA')
                    self.fel.insert_fel('LIMPEZA_ACABAMENTO_BOCA', self.time_system)
                # SE vaso na fila de preparacao boca
                elif (self.vasos.search_vaso('PREPARACAO_BOCA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_specialist('PREPARACAO_BOCA')
                    self.fel.insert_fel('PREPARACAO_BOCA', self.time_system)
                # SE vaso na fila de limpeza acabamento base
                elif (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BASE')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_specialist('LIMPEZA_ACABAMENTO_BASE')
                    self.fel.insert_fel('LIMPEZA_ACABAMENTO_BASE', self.time_system)
                # SE vaso na fila inicial
                elif (self.vasos.search_vaso('PREPARACAO_FORMA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_specialist('PREPARACAO_FORMA')
                    self.fel.insert_fel('PREPARACAO_FORMA', self.time_system)

            x = self.CONST.get_SEC_ACAB_BOCA(vaso.get_size())
            # rand = np.random.triangular(x[0], x[1], x[2])
            rand = 14
            self.artesao = self.artesoes.time_artisan('SECAGEM_ACABAMENTO_BOCA', self.time_system + int(rand))
            if self.artesao == None:
                self.artesao = self.artesoes.time_specialist('SECAGEM_ACABAMENTO_BOCA', self.time_system + int(rand))
                if self.artesao == None:
                    self.artesao = self.artesoes.aloca_artisan('SECAGEM_ACABAMENTO_BOCA', self.time_system + int(rand))
                if self.artesao == None:
                    self.artesao = self.artesoes.aloca_specialist('SECAGEM_ACABAMENTO_BOCA', self.time_system + int(rand))
                if self.artesao != None:
                    self.vasos.insert_vaso('LIMPEZA_ACABAMENTO_BOCA', vaso)
                    self.fel.insert_fel('LIMPEZA_ACABAMENTO_BOCA', self.time_system + int(rand))
            else:
                self.vasos.insert_vaso('LIMPEZA_ACABAMENTO_BOCA', vaso)
                self.fel.insert_fel('LIMPEZA_ACABAMENTO_BOCA', self.time_system + int(rand))
        # else:
        #     self.fel.insert_fel('SECAGEM_ACABAMENTO_BOCA', self.time_system)    

    def DCA_limpeza_acabamento_boca(self):
        if self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BOCA'):
            vaso = self.vasos.remove_vaso('LIMPEZA_ACABAMENTO_BOCA')
            self.artesao = self.artesoes.get_artisan('LIMPEZA_ACABAMENTO_BOCA')
            if self.artesoes.have_specialist('LIMPEZA_ACABAMENTO_BOCA'):
                # sorteia tempo de preparacao da boca
                x = self.CONST.get_LIMP_ACAB_BOCA(vaso.get_size())
                # rand = np.random.triangular(x[0], x[1], x[2])
                rand = 5
                self.artesao = self.artesoes.time_specialist('LIMPEZA_ACABAMENTO_BOCA', self.time_system + int(rand))
                self.vasos.insert_vaso('SECAGEM_BOCA', vaso)
                self.fel.insert_fel('SECAGEM_BOCA', self.time_system + int(rand))
            elif self.artesoes.have_artisan('LIMPEZA_ACABAMENTO_BOCA'):
                x = self.CONST.get_LIMP_ACAB_BOCA(vaso.get_size())
                # rand = np.random.triangular(x[0], x[1], x[2])
                rand = 5
                self.artesao = self.artesoes.time_artisan('LIMPEZA_ACABAMENTO_BOCA', self.time_system + int(rand))
                self.vasos.insert_vaso('SECAGEM_BOCA', vaso)
                self.fel.insert_fel('SECAGEM_BOCA', self.time_system + int(rand))
            else:
                self.vasos.insert_vaso('LIMPEZA_ACABAMENTO_BOCA', vaso)
                self.fel.insert_fel('LIMPEZA_ACABAMENTO_BOCA', self.time_system)
        # else:
        #     self.fel.insert_fel('LIMPEZA_ACABAMENTO_BOCA', self.time_system)

    def DCA_secagem_boca(self):
        if self.vasos.search_vaso('SECAGEM_BOCA'):
            vaso = self.vasos.remove_vaso('SECAGEM_BOCA')
            # SE recurso alocado atual == artesao
            if (self.artesao != None) and (not self.artesao.isSpecialist()):
                # SE pouca massa (-25%)
                if (self.massa < self.pouca_massa):
                    #aloca o artesao para preparacao da massa
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('PREPARACAO_MASSA')
                    self.fel.insert_fel('PREPARACAO_MASSA', self.time_system)
                # SE pouca pedra (-25%)
                elif (self.pedra < self.pouca_pedra):
                    # aloca o artesao para coleta de pedra
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('PREPARACAO_PEDRA')
                    self.fel.insert_fel('PREPARACAO_PEDRA', self.time_system)
                # SE vaso na fila de envernizacao geral
                elif (self.vasos.search_vaso('ENVERNIZACAO_GERAL')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('ENVERNIZACAO_GERAL')
                    self.fel.insert_fel('ENVERNIZACAO_GERAL', self.time_system)
                # SE vaso na fila de impermeabilizacao interna
                elif (self.vasos.search_vaso('IMPERMEABILIZACAO_INTERNA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('IMPERMEABILIZACAO_INTERNA')
                    self.fel.insert_fel('IMPERMEABILIZACAO_INTERNA', self.time_system)
                # SE vaso na fila de limpeza acabamento boca
                elif (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BOCA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('LIMPEZA_ACABAMENTO_BOCA')
                    self.fel.insert_fel('LIMPEZA_ACABAMENTO_BOCA', self.time_system)
                # SE vaso na fila de preparacao boca
                elif (self.vasos.search_vaso('PREPARACAO_BOCA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('PREPARACAO_BOCA')
                    self.fel.insert_fel('PREPARACAO_BOCA', self.time_system)
                # SE vaso na fila de limpeza acabamento base
                elif (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BASE')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_artisan('LIMPEZA_ACABAMENTO_BASE')
                    self.fel.insert_fel('LIMPEZA_ACABAMENTO_BASE', self.time_system)
                # SE vaso na fila inicial
                elif (self.vasos.search_vaso('PREPARACAO_FORMA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_specialist('PREPARACAO_FORMA')
                    self.fel.insert_fel('PREPARACAO_FORMA', self.time_system)
                else:
                    # libera artesao
                    self.artesoes.libera_artisan(self.artesao.get_id())
            elif (self.artesao != None):
                # SE vaso na fila de limpeza acabamento boca
                if (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BOCA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_specialist('LIMPEZA_ACABAMENTO_BOCA')
                    self.fel.insert_fel('LIMPEZA_ACABAMENTO_BOCA', self.time_system)
                # SE vaso na fila de preparacao boca
                elif (self.vasos.search_vaso('PREPARACAO_BOCA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_specialist('PREPARACAO_BOCA')
                    self.fel.insert_fel('PREPARACAO_BOCA', self.time_system)
                # SE vaso na fila de limpeza acabamento base
                elif (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BASE')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_specialist('LIMPEZA_ACABAMENTO_BASE')
                    self.fel.insert_fel('LIMPEZA_ACABAMENTO_BASE', self.time_system)
                # SE vaso na fila inicial
                elif (self.vasos.search_vaso('PREPARACAO_FORMA')):
                    self.artesoes.libera_artisan(self.artesao.get_id())
                    self.artesao = self.artesoes.aloca_specialist('PREPARACAO_FORMA')
                    self.fel.insert_fel('PREPARACAO_FORMA', self.time_system)

            x = self.CONST.get_SEC_BOCA(vaso.get_size())
            # rand = np.random.triangular(x[0], x[1], x[2])
            rand = 120
            self.artesao = self.artesoes.time_artisan('SECAGEM_BOCA', self.time_system + int(rand))
            if self.artesao == None:
                self.artesao = self.artesoes.time_specialist('SECAGEM_BOCA', self.time_system + int(rand))
                if self.artesao == None:
                    self.artesao = self.artesoes.aloca_artisan('SECAGEM_BOCA', self.time_system + int(rand))
                if self.artesao == None:
                    self.artesao = self.artesoes.aloca_specialist('SECAGEM_BOCA', self.time_system + int(rand))
                if self.artesao != None:
                    self.vasos.insert_vaso('IMPERMEABILIZACAO_INTERNA', vaso)
                    self.fel.insert_fel('IMPERMEABILIZACAO_INTERNA', self.time_system + int(rand))
            else:
                self.vasos.insert_vaso('IMPERMEABILIZACAO_INTERNA', vaso)
                self.fel.insert_fel('IMPERMEABILIZACAO_INTERNA', self.time_system + int(rand))
        # else:
        #     self.fel.insert_fel('SECAGEM_BOCA', self.time_system)

    ################### Existe uma fila entre essas 2 atividades

    def DCA_impermeabilizacao_interna(self):
        if self.vasos.search_vaso('IMPERMEABILIZACAO_INTERNA'):
            vaso = self.vasos.remove_vaso('IMPERMEABILIZACAO_INTERNA')
            self.artesao = self.artesoes.get_artisan('IMPERMEABILIZACAO_INTERNA')
            if self.artesoes.have_artisan('IMPERMEABILIZACAO_INTERNA'):
                # sorteia tempo de preparacao da boca
                x = self.CONST.get_IMP_INTERNA(vaso.get_size())
                # rand = np.random.triangular(x[0], x[1], x[2])
                rand = 2
                self.artesao = self.artesoes.aloca_artisan('IMPERMEABILIZACAO_INTERNA', self.time_system + int(rand))
                self.vasos.insert_vaso('SECAGEM_INTERNA', vaso)
                self.fel.insert_fel('SECAGEM_INTERNA', self.time_system + int(rand))
            else:
                self.vasos.insert_vaso('IMPERMEABILIZACAO_INTERNA', vaso)
                self.fel.insert_fel('IMPERMEABILIZACAO_INTERNA', self.time_system)
        # else:
        #     self.fel.insert_fel('IMPERMEABILIZACAO_INTERNA', self.time_system)

    def DCA_secagem_interna(self):
        if self.vasos.search_vaso('SECAGEM_INTERNA'):
            vaso = self.vasos.remove_vaso('SECAGEM_INTERNA')
            self.artesao = self.artesoes.get_artisan('SECAGEM_INTERNA')
            # SE pouca massa (-25%)
            if (self.massa < self.pouca_massa):
                # aloca o artesao para preparacao da massa
                self.artesoes.libera_artisan(self.artesao.get_id())
                self.artesao = self.artesoes.aloca_artisan('PREPARACAO_MASSA')
                self.fel.insert_fel('PREPARACAO_MASSA', self.time_system)
            # SE pouca pedra (-25%)
            elif (self.pedra < self.pouca_pedra):
                # aloca o artesao para coleta de pedra
                self.artesoes.libera_artisan(self.artesao.get_id())
                self.artesao = self.artesoes.aloca_artisan('PREPARACAO_PEDRA')
                self.fel.insert_fel('PREPARACAO_PEDRA', self.time_system)
            # SE vaso na fila de envernizacao geral
            elif (self.vasos.search_vaso('ENVERNIZACAO_GERAL')):
                # self.artesoes.libera_artisan(self.artesao.get_id())
                self.artesao = self.artesoes.aloca_artisan('ENVERNIZACAO_GERAL')
                self.fel.insert_fel('ENVERNIZACAO_GERAL', self.time_system)
            # SE vaso na fila de impermeabilizacao interna
            elif (self.vasos.search_vaso('IMPERMEABILIZACAO_INTERNA')):
                # self.artesoes.libera_artisan(self.artesao.get_id())
                self.artesao = self.artesoes.aloca_artisan('IMPERMEABILIZACAO_INTERNA')
                self.fel.insert_fel('IMPERMEABILIZACAO_INTERNA', self.time_system)
            # SE vaso na fila de limpeza acabamento boca
            elif (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BOCA')):
                # self.artesoes.libera_artisan(self.artesao.get_id())
                self.artesao = self.artesoes.aloca_artisan('LIMPEZA_ACABAMENTO_BOCA')
                self.fel.insert_fel('LIMPEZA_ACABAMENTO_BOCA', self.time_system)
            # SE vaso na fila de preparacao boca
            elif (self.vasos.search_vaso('PREPARACAO_BOCA')):
                # self.artesoes.libera_artisan(self.artesao.get_id())
                self.artesao = self.artesoes.aloca_artisan('PREPARACAO_BOCA')
                self.fel.insert_fel('PREPARACAO_BOCA', self.time_system)
            # SE vaso na fila de limpeza acabamento base
            elif (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BASE')):
                # self.artesoes.libera_artisan(self.artesao.get_id())
                self.artesao = self.artesoes.aloca_artisan('LIMPEZA_ACABAMENTO_BASE')
                self.fel.insert_fel('LIMPEZA_ACABAMENTO_BASE', self.time_system)
            # SE vaso na fila inicial
            elif (self.vasos.search_vaso('PREPARACAO_FORMA')):
                # self.artesoes.libera_artisan(self.artesao.get_id())
                self.artesao = self.artesoes.aloca_specialist('PREPARACAO_FORMA')
                self.fel.insert_fel('PREPARACAO_FORMA', self.time_system)
            else:
                #libera artesao
                if self.artesao != None:
                    self.artesoes.libera_artisan(self.artesao.get_id())

            x = self.CONST.get_SEC_INTERNA(vaso.get_size())
            # rand = np.random.triangular(x[0], x[1], x[2])
            rand = 300
            self.artesao = self.artesoes.time_artisan('SECAGEM_INTERNA', self.time_system + int(rand))
            if self.artesao == None:
                self.artesao = self.artesoes.time_specialist('SECAGEM_INTERNA', self.time_system + int(rand))
                if self.artesao == None:
                    self.artesao = self.artesoes.aloca_artisan('SECAGEM_INTERNA', self.time_system + int(rand))
                if self.artesao == None:
                    self.artesao = self.artesoes.aloca_specialist('SECAGEM_INTERNA', self.time_system + int(rand))
                if self.artesao != None:
                    self.vasos.insert_vaso('ENVERNIZACAO_GERAL', vaso)
                    self.fel.insert_fel('ENVERNIZACAO_GERAL', self.time_system + int(rand))
            else:
                self.vasos.insert_vaso('ENVERNIZACAO_GERAL', vaso)
                self.fel.insert_fel('ENVERNIZACAO_GERAL', self.time_system + int(rand))
        # else:
        #     self.fel.insert_fel('SECAGEM_INTERNA', self.time_system)

    ################### Existe uma fila entre essas 2 atividades

    def DCA_envernizacao_geral(self):
        if self.vasos.search_vaso('ENVERNIZACAO_GERAL'):
            vaso = self.vasos.remove_vaso('ENVERNIZACAO_GERAL')
            if self.artesoes.have_artisan('ENVERNIZACAO_GERAL'):
                # sorteia tempo de preparacao da boca
                x = self.CONST.get_ENV_GERAL(vaso.get_size())
                # rand = np.random.triangular(x[0], x[1], x[2])
                rand = 7
                self.artesao = self.artesoes.aloca_artisan('ENVERNIZACAO_GERAL', self.time_system + int(rand))
                self.vasos.insert_vaso('SECAGEM_ENVERNIZACAO', vaso)
                self.fel.insert_fel('SECAGEM_ENVERNIZACAO', self.time_system + int(rand))
            else:
                self.vasos.insert_vaso('ENVERNIZACAO_GERAL', vaso)
                self.fel.insert_fel('ENVERNIZACAO_GERAL', self.time_system + int(rand))
        # else:
        #     self.fel.insert_fel('ENVERNIZACAO_GERAL', self.time_system)

    def DCA_secagem_envernizacao(self):
        if self.vasos.search_vaso('SECAGEM_ENVERNIZACAO'):
            vaso = self.vasos.remove_vaso('SECAGEM_ENVERNIZACAO')
            # SE pouca massa (-25%)
            if (self.massa < self.pouca_massa):
                # aloca o artesao para preparacao da massa
                self.artesoes.libera_artisan(self.artesao.get_id())
                self.artesao = self.artesoes.aloca_artisan('PREPARACAO_MASSA')
                self.fel.insert_fel('PREPARACAO_MASSA', self.time_system)
            # SE pouca pedra (-25%)
            elif (self.pedra < self.pouca_pedra):
                # aloca o artesao para coleta de pedra
                self.artesoes.libera_artisan(self.artesao.get_id())
                self.artesao = self.artesoes.aloca_artisan('PREPARACAO_PEDRA')
                self.fel.insert_fel('PREPARACAO_PEDRA', self.time_system)
            # SE vaso na fila de envernizacao geral
            elif (self.vasos.search_vaso('ENVERNIZACAO_GERAL')):
                # self.artesoes.libera_artisan(self.artesao.get_id())
                self.artesao = self.artesoes.aloca_artisan('ENVERNIZACAO_GERAL')
                self.fel.insert_fel('ENVERNIZACAO_GERAL', self.time_system)
            # SE vaso na fila de impermeabilizacao interna
            elif (self.vasos.search_vaso('IMPERMEABILIZACAO_INTERNA')):
                # self.artesoes.libera_artisan(self.artesao.get_id())
                self.artesao = self.artesoes.aloca_artisan('IMPERMEABILIZACAO_INTERNA')
                self.fel.insert_fel('ENVERNIZACAO_GERAL', self.time_system)
            # SE vaso na fila de limpeza acabamento boca
            elif (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BOCA')):
                # self.artesoes.libera_artisan(self.artesao.get_id())
                self.artesao = self.artesoes.aloca_artisan('LIMPEZA_ACABAMENTO_BOCA')
                self.fel.insert_fel('ENVERNIZACAO_GERAL', self.time_system)
            # SE vaso na fila de preparacao boca
            elif (self.vasos.search_vaso('PREPARACAO_BOCA')):
                # self.artesoes.libera_artisan(self.artesao.get_id())
                self.artesao = self.artesoes.aloca_artisan('PREPARACAO_BOCA')
                self.fel.insert_fel('ENVERNIZACAO_GERAL', self.time_system)
            # SE vaso na fila de limpeza acabamento base
            elif (self.vasos.search_vaso('LIMPEZA_ACABAMENTO_BASE')):
                # self.artesoes.libera_artisan(self.artesao.get_id())
                self.artesao = self.artesoes.aloca_artisan('LIMPEZA_ACABAMENTO_BASE')
                self.fel.insert_fel('ENVERNIZACAO_GERAL', self.time_system)
            # SE vaso na fila inicial
            elif (self.vasos.search_vaso('PREPARACAO_FORMA')):
                # self.artesoes.libera_artisan(self.artesao.get_id())
                self.artesao = self.artesoes.aloca_specialist('PREPARACAO_FORMA')
                self.fel.insert_fel('ENVERNIZACAO_GERAL', self.time_system)
            else:
                #libera artesao
                if self.artesao != None:
                    self.artesoes.libera_artisan(self.artesao.get_id())

            x = self.CONST.get_SEC_FINAL(vaso.get_size())
            # rand = np.random.triangular(x[0], x[1], x[2])
            rand = 1020
            self.artesao = self.artesoes.time_artisan('SECAGEM_ENVERNIZACAO', self.time_system + int(rand))
            if self.artesao == None:
                self.artesao = self.artesoes.time_specialist('SECAGEM_ENVERNIZACAO', self.time_system + int(rand))
                if self.artesao == None:
                    self.artesao = self.artesoes.aloca_artisan('SECAGEM_ENVERNIZACAO', self.time_system + int(rand))
                if self.artesao == None:
                    self.artesao = self.artesoes.aloca_specialist('SECAGEM_ENVERNIZACAO', self.time_system + int(rand))
                if self.artesao != None:
                    self.vasos.insert_vaso('FIM', vaso)
                    self.vasos.set_end_time(vaso, self.time_system)
                    self.fel.insert_fel('FIM', self.time_system + int(rand))
            else:
                self.vasos.insert_vaso('FIM', vaso)
                self.vasos.set_end_time(vaso, self.time_system)
                self.fel.insert_fel('FIM', self.time_system + int(rand))
        # else:
        #     self.fel.insert_fel('FIM', self.time_system)
        # self.vasos.show()
        # self.fel.show()
        #DCA_chegada_pedido()	

file = open(arquivoLog, "a")
file.write("TEMP_SIMULACAO\tUSO_MASSA\tUSO_PEDRA\tPRODUTIVIDADE\tCOMP_TIME_PEQ\tCOMP_TIME_MED\tCOMP_TIME_GRAN\tNUM_VASOS\tSEED" + "\n")

simulator = simulator()
simulator.DCA_chegada_pedido()

simulator.fel.show()
# simulator.artesoes.show()
# simulator.vasos.show()

timeSystemAux = 0
iteracao = 0
totalVasos = 0
completionTimeIter = 0


#while timeSystemAux < simulationTime:
#simulator = simulator()
#simulator.DCA_chegada_pedido()
# timeSystemAux += simulator.time_system
iteracao += 1
totalVasos += len(simulator.vasos.get_fila())
qtdPeq = 0
qtdMed = 0
qtdGran = 0
completionPeq = 0
completionMed = 0
completionGran = 0

for x in simulator.vasos.get_fila():
    if x[1].get_size() == 'S':
        completionPeq += x[1].getCompletionTime()
        qtdPeq += 1
    if x[1].get_size() == 'M':
        completionMed += x[1].getCompletionTime()
        qtdMed += 1
    if x[1].get_size() == 'B':
        completionGran += x[1].getCompletionTime()
        qtdGran += 1
        
completionTimePeq = 0
completionTimeMed = 0
completionTimeGran = 0
# completionTimePeq = completionPeq/qtdPeq
# completionTimeMed = completionMed/qtdMed
# completionTimeGran = completionGran/qtdGran

massaUtilizadaPeq = qtdPeq*simulator.CONST.get_USO_MASSA('S')
massaUtilizadaMed = qtdMed*simulator.CONST.get_USO_MASSA('M')
massaUtilizadaGran = qtdGran*simulator.CONST.get_USO_MASSA('B')
massaUtilizada = massaUtilizadaPeq + massaUtilizadaMed + massaUtilizadaGran

pedraUtilizadaPeq = qtdPeq*simulator.CONST.get_USO_PEDRA('S')
pedraUtilizadaMed = qtdMed*simulator.CONST.get_USO_PEDRA('M')
pedraUtilizadaGran = qtdGran*simulator.CONST.get_USO_PEDRA('B')
pedraUtilizada = pedraUtilizadaPeq + pedraUtilizadaMed + pedraUtilizadaGran

file.write(str(simulationTime) + '\t' + str(massaUtilizada) + '\t' + str(pedraUtilizada) + '\t' + 'TEMP' + '\t' + str(completionTimePeq) + '\t' + str(completionTimeMed) + '\t' + str(completionTimeGran) + '\t' + str(totalVasos) + '\t' + str(simulator.CONST.get_G_TSM()) + "\n")
file.close()
