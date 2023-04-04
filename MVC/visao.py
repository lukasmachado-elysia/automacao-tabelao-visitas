from tkinter import ttk
import tkinter as tk
from tkcalendar import *
from tkinter import filedialog
from tkinter import messagebox

class Visao(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pasta = tk.StringVar(value="") # Utilizada para atualizar a label em tempo de execucao 

        # Fazendo a montagem dos elementos na janela -----------------------------------------------------------------------------------------
        self.labelDe = ttk.Label(parent, text="De:", font=('Helvatical',11)).grid(column=0, row=0, padx=5, pady=5)
        self.inputDe = DateEntry(parent, selectmode='day' ,date_pattern='dd/mm/yyyy', font=('Helvatical',11))
        self.inputDe.grid(column=1, row=0, padx=5, pady=5)

        self.labelAte = ttk.Label(parent, text="Até:", font=('Helvatical',11)).grid(column=0,row=1, padx=5, pady=5)
        self.inputAte = DateEntry(parent, selectmode='day' ,date_pattern='dd/mm/yyyy', font=('Helvatical',11))
        self.inputAte.grid(column=1, row=1, padx=5, pady=5)
        
        self.labelLocalArq = ttk.Label(parent, text="Pasta onde está o arquivo:", font=('Helvatical',11)).grid(row=2, column=0, padx=10, pady=10)
        self.inputLocalArq = ttk.Entry(parent, text="Pasta onde está o arquivo:", textvariable= self.pasta, width=25, font=('Helvatical',10))
        self.inputLocalArq.grid(row=2, column=1, padx=5, pady=5)
        # -----------------------------------------------------------------------------------------------------------------------------------

        # Botao para selecionar pasta onde sera salvo o arquivo
        self.btnSelecPasta = ttk.Button(parent, text='Selecionar pasta', command=self.selecionarPasta)
        self.btnSelecPasta.grid(row=2, column=2, padx=5, pady=5)

        # Botao para gerar o relatorio e realizar a busca
        self.btnBuscarDados = ttk.Button(parent, text='Buscar Dados')
        self.btnBuscarDados.grid(row=3, column=0, padx=10, pady=10)

    # Buscando pasta para onde sera salvo o arquivo
    def selecionarPasta(self):
        self.pasta.set(filedialog.askdirectory(title="Salvar em", initialdir='/'))

    # Criar getters e setters do input da pasta e das duas datas
    def get_Input_Local_Arq(self):
        return self.inputLocalArq
    
    # Getter dos botoes
    def get_Btn_Buscar_Dados(self):
        return self.btnBuscarDados
    
    def get_Btn_Local_Salvamento(self):
        return self.btnSelecPasta
    
    # Getter das datas
    def get_Input_Data_De(self):
        return self.inputDe
    
    def get_Input_Data_Ate(self):
        return self.inputAte
    
    # Messages box para comunicacao
    def message_Box(self, titulo, mensagem, tipo):
        """
            Mostra um message box na tela para o usuario.

            Parametros:
            ----
                titulo: (str)
                    O titulo da message box
                
                mensagem: (str)
                    Mensagem a ser exibida

                tipo: (str)
                    Tipo de message box.\n 
                    Dentre elas:\n
                        * info - informacao
                        * error - erro
                        * warning - aviso
        """
        # Info box
        if tipo=='info':
            messagebox.showinfo(message=mensagem, title=titulo)
        elif tipo=='error':
            messagebox.showerror(message=mensagem, title=titulo)
        elif tipo=='warning':
            messagebox.showwarning(message=mensagem, title=titulo)
        elif tipo=='askquestion':
            return messagebox.askquestion(message=mensagem, title=titulo)