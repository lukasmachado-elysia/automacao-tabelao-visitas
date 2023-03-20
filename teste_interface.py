from tkinter import *
from tkinter import filedialog

def selecionarPasta():
    pasta.set(filedialog.askdirectory(
        title="Salvar em", 
        initialdir='/'))



window = Tk()
window.title('Teste da Tela')
window_width = 320
window_height = 480

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# posicionando a janela no centro
x = (screen_width /2) - (window_width /2) # largura 
y = (screen_height /2) - (window_height /2) # altura
window.geometry(f"{window_height}x{window_width}+{int(x)}+{int(y)}") # (X)+(Y) coordenates
window.resizable(0,0)

pasta = StringVar()

window.columnconfigure(0, weight=0)
window.columnconfigure(1, weight=0)
window.columnconfigure(2, weight=0)

label1 = Label(window, text="De:").grid(column=0, row=0, padx=5, pady=5)
input1 = Entry(window).grid(column=1, row=0, padx=5, pady=5)

label2 = Label(window, text="Até:").grid(column=0,row=1, padx=5, pady=5)
input2 = Entry(window).grid(column=1, row=1, padx=5, pady=5)

label3 = Label(window, text="Pasta onde está o arquivo:").grid(row=2, column=0, padx=5, pady=5)
input3 = Entry(window, text="Pasta onde está o arquivo:", textvariable= pasta, width=25).grid(row=2, column=1, padx=5, pady=5)

btn1 = Button(
    window,
    text='Selecionar pasta',
    command=selecionarPasta).grid(
                                    row=2, 
                                    column=2, 
                                    padx=5, 
                                    pady=5)

btn2 = Button(
    window,
    text='Buscar Dados').grid(
                                row=3, 
                                column=0, 
                                padx=10, 
                                pady=10)


window.mainloop()

