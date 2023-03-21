class Modelo:
    def __init__(self, dataDe, dataAte):
        self.dataDe = dataDe
        self.dataAte = dataAte
    @property
    def dataDe(self):
        return self.__dataDe
    
    @property
    def dataAte(self):
        return self.__dataAte

    @dataAte.setter
    def dataAte(self, value):
        self.__dataAte = value    

    @dataDe.setter
    def dataDe(self, value):
        self.__dataDe = value

    def gerar_Relatorio(self):
        print(self.dataDe)
        print(self.dataAte)

    
