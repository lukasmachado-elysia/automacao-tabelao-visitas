
from controle import Controle
from modelo import Modelo
from visao import Visao
import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Propriedades iniciais da  janela
        self.title('Gerador de Relatório de Visitas')
        self_width = 320
        self_height = 560    
         
        # Pegando o tamanho da tela
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # posicionando a janela no centro
        x = (screen_width /2) - (self_width /2) # largura 
        y = (screen_height /2) - (self_height /2) # altura
        self.geometry(f"{self_height}x{self_width}+{int(x)}+{int(y)}") # (X)+(Y) coordenates
        
        # Definindo grid da janela 
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=0) 

        self.resizable(0, 0)
        # -----
    
        # Inicializando MVC
        vis = Visao(self) 
        model = Modelo('datade', 'dataate', 'C:\\')
        control = Controle(vis, model)

if __name__ == '__main__':
    app = App()
    app.mainloop()

