import time
import requests

# Se a API alterar seu campos novamente, sera necessario alterar apenas alguns filtros desta funcao
def request_Orquestra(method='GET',urlReq="https://elysia.zeev.it",typeReq="/api/2/assignments",tokens={},filters={}, forceRequisition:bool=False) -> list:
        try:
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
                        authorization= {'Authorization': "Bearer " + tk}
                        while row != 0:
                                # Aguardo x segundos devido ao limite de requisicoes - lembrando que a limite de requisicoes por segundos, minutos, horas, dias e meses
                                time.sleep(seconds) 
                                
                                # Incremento de pagina
                                filters['pageNumber'] = i
                                
                                # Requisicao
                                print(filters)
                                getReq = requests_API_Orquestra(metodo=method, 
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
        except Exception as e:
                print('--> Erro na funcao \'request_Orquestra\' <--')
                printError(e,"autOKRs")
                return []

def requests_API_Orquestra(metodo='GET',urlAcesso="https://elysia.zeev.it",tipoAcesso="/api/2/assignments",head={},payload={}):
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
    try:
        if metodo == 'GET':
            req = requests.get(url=urlAcesso+tipoAcesso,headers=head,params=payload)
            return req
        elif metodo == 'POST':
            req = requests.post(url=urlAcesso+tipoAcesso,headers=head,params=payload)
            return req
        else: 
            raise NameError('Nenhum metodo valido foi passado. Passe os metodos POST ou GET.')
    except Exception as e:
        print('funcoes')
        printError(e)

def printError(e):
    print('\n------------------------------------') 
    print('Nao foi possível realizar a operacao!')
    print('------------------------------------\n') 

    templateError = '!!! ---> Um erro do tipo: "{0}" ocorreu <--- !!!\nArgumentos:\n{1}'
    messageError = templateError.format(type(e).__name__,e.args)
    print(messageError)