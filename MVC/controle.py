from modelo import Modelo
from visao import Visao
import traceback
import os
from datetime import datetime
class Controle():
    def __init__(self, visao=Visao, modelo=Modelo):
        self.janela = visao
        self.model = modelo
        
        # Definindo binding para o botao de buscar dados
        # Ao clicar no botao ele vai acionar a funcao principal
        btnBuscarDados = self.janela.get_Btn_Buscar_Dados()
        btnBuscarDados.bind("<Button-1>", self.buscar_Dados)

        # Campo de local do arquivo
        self.btnLocalSalve = self.janela.get_Input_Local_Arq()
        self.inputDe = self.janela.get_Input_Data_De()
        self.inputAte = self.janela.get_Input_Data_Ate()

    # Funcao que define local de salvamento
    def pegar_Campos(self) -> bool: 
        """
            Funcao que pega as entradas de data de inicio, fim e local de salvamento.

            Retorna:
            ------
                'True' caso tenha pego corretamente os dados;\n
                'Falso' caso não tenha pego corretamente os dados;
        """
        try:
            # Pegar dados do local de salvamento
            pasta = str(self.btnLocalSalve.get())
            
            # Pegando datas
            dataInicio = self.inputDe.get_date()
            dataFim = self.inputAte.get_date()

            # Coloca no objeto modelo
            self.model.localSave = pasta
            self.model.dataDe = dataInicio
            self.model.dataAte = dataFim
            
            return True
        except Exception as e:
            erro = "Erro: {0}",format(traceback.format_exc())
            self.janela.message_Box('Erro', erro, 'error')
            return False
 
    # Funcao que gera o relatorio
    def buscar_Dados(self, event):
        try:
            # Pegando campos
            if self.pegar_Campos():
                pastaSalvar = self.model.localSave
                # Verificar se o caminho eh valido
                if self.local_Existe(pastaSalvar):
                    # Verifica as datas
                    if self.verifica_Datas():
                        # Busca relatorio
                        if self.model.buscar_Relatorio():
                            # Relatorio gerado e nao esta vazio
                            # Salva relatorio
                            if self.model.salvar_Relatorio():
                                if str(self.janela.message_Box('Relatorio salvo', 'Gostaria de abrir a pasta do local do arquivo?', 'askquestion')) == 'yes':
                                    os.startfile(self.model.localSave)
                            else:
                                # relatorio nao salvo
                                self.janela.message_Box('Relatorio nao salvo', 'Nao foi possivel salvar o relatorio!', 'warning')
                        else:
                            # dados vazios para o relatorio
                            self.janela.message_Box('Relatorio nao gerado', 'Dados nao encontrados!\nVerifique o periodo e tente novamente.', 'warning')
                else:
                    # pasta nao localizada
                    self.janela.message_Box('Pasta nao encontrada', 'Pasta não localizada!\nVerifique o caminho e tente novamente.', 'warning')
            else:
                self.janela.message_Box('Dados nao encontrados', 'Ocorreu um erro ao pegar os dados e não foi possível gerar o arquivo.\nEntre em contato com o desenvolvedor.', 'warning')
        except Exception as e:
            error = "Erro: {0}\nNao foi possivel gerar o arquivo. Entre em contato com o desenvolvedor.".format(traceback.format_exc())
            self.janela.message_Box('Erro', error, 'error')
            

    # Verifica as datas
    # * Se a data de inicio eh maior nova que a data de fim; (OK!)
    # * Se a data eh maior do que o dia atual; (OK!)
    def verifica_Datas(self) -> bool:
        try:
            dataInicio = self.model.dataDe
            dataFim = self.model.dataAte
            
            todayString = datetime.today().strftime("%Y-%m-%d") # pega data e converte para o formato desejado
            todayTime = datetime.date(datetime.strptime(todayString,"%Y-%m-%d")) # depois converte para o tipo 'date' para ser usado nas verificacoes

            # Verifica se a data de inicio eh mais nova que a data de fim
            if dataInicio > dataFim: # consequentemente ja verifica se a data de fim eh mais antiga que a data de inicio
                self.janela.message_Box("Datas incorretas", "A data de inicio nao pode ser maior que a data final.\nVerifique as datas e tente novamente.",'warning')
                return False
            else: 
                # Verifica se a data de inicio OU data de fim eh maior que o dia atual
                if dataInicio > todayTime or dataFim > todayTime:
                    self.janela.message_Box("Datas incorretas", "A data de inicio ou data de fim nao pode ser maior que o dia atual!\nVerifique as datas e tente novamente.",'warning')
                    return False
                else:
                    # tudo certo
                    return True
        except Exception as e:
            error = "Erro: {0}\nNao foi possivel verificar as datas. Entre em contato com o desenvolvedor".format(traceback.format_exc())
            self.janela.message_Box("Erro nas verificacao das datas", error, 'error')
            return False

    # Verifica se local existe
    def local_Existe(self, caminho:str) -> bool:
        try:
            if caminho == '':
                return False
            else:
                return os.path.exists(caminho)
        except Exception as e:
            error = "Erro: {0}\nNão foi possível encontrar a pasta. Entre em contato com o desenvolvedor.".format(traceback.format_exc())
            self.janela.message_Box('Erro', error, 'error')