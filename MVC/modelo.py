import pandas as pd
from datetime import datetime
import time
import requests
import os
class Modelo:
    def __init__(self, dataDe, dataAte, localSalvar):
        self.dataDe = dataDe
        self.dataAte = dataAte
        self.localSave = localSalvar
        self.dataFrameRelatorio = pd.DataFrame()

        # Dados api zeev
        self.tokenApi = ['enb4iHROSDegvkiZv17FxzISZ%2BZB%2FQxkSGweAsL8sB0%3D']
        self.urlApi = "https://elysia.zeev.it"
        self.tipoUrlApi = "/api/2/assignments"
    
    @property
    def localSave(self):
        return self.__localSave

    @property
    def dataDe(self):
        return self.__dataDe
    
    @property
    def dataAte(self):
        return self.__dataAte

    @localSave.setter
    def localSave(self, value):
        self.__localSave = value

    @dataAte.setter
    def dataAte(self, value):
        self.__dataAte = value    

    @dataDe.setter
    def dataDe(self, value):
        self.__dataDe = value

    def buscar_Relatorio(self) -> bool:
        '''
            Funcao que busca na zeev os dados do fluxo de Agenda Comercial Microsoft pelo periodo especificado

            Parametros
            ----------
                progressBar : Barra de progresso para manipular o progresso.
            Retorno : bool
            -------
                Retorna ´True´ caso tenha gerado com sucesso e ´False´ caso nao tenha dados.
        '''
        # ---- Inicio do codigo ----
        # Buscar o dados do fluxo 
        # Numero do fluxo: 368
        instanciasInativas = self.instances_Report_Orquestra(self.tokenApi, True, True, False, flowId=368, periodo=True) # Inativas
        instanciasAtivas = self.instances_Report_Orquestra(self.tokenApi, True, True, True, flowId=368, periodo=True) # Ativas

        # Unindo os dois conjuntos de dados
        frames = [instanciasAtivas, instanciasInativas]
        instancias = pd.concat(frames)
        instancias

        # Ajustando o dataframe 
        if instancias.empty:
            # Data frame vazio, entao retorna que nao tem nada
            return False
        else:
            arr = instancias['formFields'].array
            listDict = [dic for dic in arr]
            df = pd.DataFrame(columns=['Cliente','Projeto', 'Origem', 'Cidade', 'Executivo','Pré-Venda','Formato','Data da Visita', 'Observações'])
            valores = []
            index = 0
            for i in listDict:
                for dicio in i:
                    valores.append(dicio['value'])
                df.loc[index] = valores
                index += 1
                valores = []
            df = df[['Projeto', 'Cidade', 'Origem', 'Formato', 'Executivo','Pré-Venda','Cliente','Data da Visita', 'Observações']]
            self.dataFrameRelatorio = df
            return True

    def salvar_Relatorio(self) -> bool:
        # Definir nome de arquivo
        nomeArquivo = "{0}/relatorio_visitas__{1}_{2}.xlsx".format(self.localSave, str(self.dataDe), str(self.dataAte))
        self.dataFrameRelatorio.to_excel(nomeArquivo)
        
        # Verifica se arquivo foi salvo
        if os.path.exists(nomeArquivo):
            return True
        else:
            return False

    def requests_API_Orquestra(self, metodo='GET',urlAcesso="https://elysia.zeev.it",tipoAcesso="/api/2/assignments",head={},payload={}):
        '''
            Funcao
            ------
                Funcao que retorna a requisicao desejada a partir do url de acesso e link de tipo de acesso.
                !Sendo permitido apenas metodos POST e GET!

            Parameters
            ----------

                metodo: str (OPCIONAL)
                    Metodo a ser utilizado na requisicao, POST ou GET.
                    Se nao for especificado nenhum ele ira utilizar o metodo 'GET'.
                
                urlAcesso: str (OPCIONAL)
                    Url usada na requisicao.
                    Se nao for especificado nenhum ele ira utilizar o URL que ja esta no funcao.
                
                tipoAcesso: str (OPCIONAL)
                    Url de acesso para o tipo de funcao na API, POST ou GET.
                    Se nao for especificado nenhum ele ira utilizar o URL que ja esta no funcao.
                    Ex.: **/api/2/assignments**
                
                head: str (OBRIGATORIO)
                    Autorizacao para acesso da API.
                    Ex.: **{'Authorization': 'token_acesso'}**
                
                payload: str (OPCIONAL)
                    Parametros para acesso atraves de filtros na requisicao.
            
            Retorno
            -------
                Retorna o objeto response ou resposta de erro caso ocorra.
                Ex.: <Response [200]> 
        '''
        # verifica qual tipo de requisicao foi pedida
        if metodo == 'GET':
            req = requests.get(url=urlAcesso+tipoAcesso,headers=head,params=payload)
            return req
        elif metodo == 'POST':
            req = requests.post(url=urlAcesso+tipoAcesso,headers=head,params=payload)
            return req
        else: 
            raise NameError('Nenhum metodo valido foi passado. Passe os metodos POST ou GET.')
        
    # Se a API alterar seu campos novamente, sera necessario alterar apenas alguns filtros desta funcao
    def request_Orquestra(self, method='GET',urlReq="https://elysia.zeev.it",typeReq="/api/2/assignments",tokens=[],filters={}, forceRequisition:bool=False) -> list:
        # Variaveis de controle
        row = 1
        i = 1
        retorno = []
        # filtros base para o payload
        print("Requisicao para {} <<".format(urlReq+typeReq))
        if not typeReq.lower().__contains__('report'):
            filters['recordsPerPage'] = 100
            seconds = 1
        else:
            if not forceRequisition: 
                print("---- >> Requisicao lenta... << ---- ")
                filters['recordsPerPage'] = 30
                seconds = 3
            else:
                print("---- >> Requisicao forçada... << ---- ")
                filters['recordsPerPage'] = 100
                seconds = 1    
        
        filters['mobileEnabledOnly'] = False
        # Faz a busca para cada token
        for tk in tokens:
            # Reseta variaveis de controle
            row = 1
            i = 1
            # Iteracao com token
            authorization= {'Authorization': "Bearer " + tk[0]}
            while row != 0:
                # Aguardo x segundos devido ao limite de requisicoes - lembrando que a limite de requisicoes por segundos, minutos, horas, dias e meses
                time.sleep(seconds) 
                
                # Incremento de pagina
                filters['pageNumber'] = i
                
                # Requisicao
                print(filters)
                getReq = self.requests_API_Orquestra(metodo=method, 
                                                urlAcesso=urlReq, 
                                                tipoAcesso=typeReq, 
                                                head=authorization, 
                                                payload=filters)
            
                # Resultado JSON da requisicao
                result = getReq.json()

                # Checa se esta vazio o resultado, o que significa que nao tem mais paginas
                if (len(result) == 0) or (getReq.status_code != 200):
                        print(">> " + str(getReq.status_code))
                        break
                else:
                        # coloca cada retorno na lista
                        retorno.append(result)
                        i+=1
        # Cada usuario do token fica em uma sublista da lista de retorno, por isto a necessidade de 'explodir' ela dentro de outra lista.
        retornoLista = [item for sublista in retorno for item in sublista]
        return retornoLista 

    
    def instances_Report_Orquestra(self, userToken:str, showFinishedInstanceTasks:bool=True, showPendingInstanceTasks:bool=False, activeInstances:bool=True, forceReq:bool=False, flowId:int=0, periodo:bool=False):
        '''
            Funcao
            ------
                Lista todas instâncias de solicitações que a pessoa relacionada ao token possui permissão de consultar de acordo com filtros.
            
            Parametros
            ----------
                userToken : str, (obrigatorio)
                    Token do usuario orquestra para solicitar a requisicao.
                
                Parametros de especial atencao:
                -------------------------------

                `showFinishedTasks` : boolean, (opcional)
                    Define se vai requisitar instancias fechadas das solicitacoes.
                
                `showPendingInstanceTasks` : boolean, (opcional)
                    Define se vai requisitar instancias abertas das solicitacoes.

                * Se nao optar por `showPendingInstanceTasks` ou `showFinishedTasks`, sera necessario colocar o parametro `forceReq` como `True`.\n
                * Se `showPendingInstanceTasks` ou `showFinishedTasks` estiverem `True` o parametro `forceReq` eh alterado para `False`, mesmo se ele for passado pela funcao.
                
                forceReq : boolean, (opcional)
                    Este parametro limita a quantidade de solicitacoes por segundo.

                activeInstances : boolean, (opcional)
                    Definir se a solicitacao esta `Finalizada` ou `Em andamento`.

                flowId : str, (opcional)
                    Filtrar pelo id de instancia.
                
                periodo : boolean, (opcional)
                    Define se o periodo vai ser utilizado
            Retorno 
            -------
                Retorna um DataFrame(Pandas).
                * Se erro, retorna -1.
        '''
        # Filtro padrao - Solicitacoes Em andamento e com instancias Finalizadas
        f = {"startDateIntervalBegin": "2000-01-01T00:00:00", # < ----------
                "startDateIntervalEnd": "2030-12-31T23:59:59",# < ----------
                "showFinishedInstanceTasks": showFinishedInstanceTasks, 
                "showPendingInstanceTasks": showPendingInstanceTasks,
                "formFieldNames":["numeroDoProjeto",
                                "cidade",
                                "origemDoCliente",
                                "formatoEvento",
                                "executivoDeVendas",
                                "preVendedor",
                                "nomeDoCliente",
                                "dataDoAgendamento",
                                "observacoes"
                                ],
                "active": activeInstances}

        # Filtro de ID para solicitacoes especificas
        if flowId != 0: 
            f['flowId'] = flowId
        
        # Usar periodo de pesquisa
        if periodo:
            f['startDateIntervalBegin'] = self.dataDe.strftime("%Y-%m-%d") + "T00:00:00"
            f['startDateIntervalEnd'] = self.dataAte.strftime("%Y-%m-%d") + "T23:59:59"
        
        if showFinishedInstanceTasks == True | showPendingInstanceTasks == True:
            forceReq = False
            
        lista = self.request_Orquestra(method='GET',
                                    urlReq=self.urlApi,
                                    typeReq='/api/2/instances/report',
                                    tokens=[userToken],
                                    filters=f,
                                    forceRequisition=forceReq)
        df = pd.DataFrame(lista)
        return df
