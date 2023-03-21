from tkinter import *
from tkinter import filedialog

class Visao(Tk):
    def __init__(self, controle):
        super().__init__()
        self.controle = controle
        # Propriedades iniciais da janela
        self.title('Gerador de Relatório de Visitas')
        self_width = 320
        self_height = 480    
         
        # Pegando o tamanho da tela
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # posicionando a janela no centro
        x = (screen_width /2) - (self_width /2) # largura 
        y = (screen_height /2) - (self_height /2) # altura
        self.geometry(f"{self_height}x{self_width}+{int(x)}+{int(y)}") # (X)+(Y) coordenates

        self.pasta = StringVar()

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=0)

        self.label1 = Label(self, text="De:", font=('Helvatical',11)).grid(column=0, row=0, padx=5, pady=5)
        self.input1 = Entry(self).grid(column=1, row=0, padx=5, pady=5)

        self.label2 = Label(self, text="Até:", font=('Helvatical',11)).grid(column=0,row=1, padx=5, pady=5)
        self.input2 = Entry(self)
        self.input2.grid(column=1, row=1, padx=5, pady=5)
        
        self.label3 = Label(self, text="Pasta onde está o arquivo:", font=('Helvatical',11)).grid(row=2, column=0, padx=10, pady=10)
        self.input3 = Entry(self, text="Pasta onde está o arquivo:", textvariable= self.pasta, width=25, font=('Helvatical',10))
        self.input3.grid(row=2, column=1, padx=5, pady=5)

        # Botao para selecionar pasta onde sera salvo o arquivo
        self.btn1 = Button(self, text='Selecionar pasta', command=self.selecionarPasta).grid(row=2, column=2, padx=5, pady=5)

        # Botao para gerar o relatorio e realizar a busca
        self.btn2 = Button(self, text='Buscar Dados')
        self.btn2.grid(row=3, column=0, padx=10, pady=10)
        self.btn2.bind("<Button>", controle.principal)
        
    def selecionarPasta(self):
        self.pasta.set(filedialog.askdirectory(title="Salvar em", initialdir='/'))

    # criar getters e setters do input da pasta e das duas datas