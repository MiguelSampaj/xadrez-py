from customtkinter import *

# Variaveis
letras = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

# Configs
set_appearance_mode('dark')

# Configurando os huds
class Circle(CTkCanvas):
    def __init__(self, master, fg_color, **kwargs):
        diametro = 75
        raio = diametro / 2

        self.fg_color = fg_color

        super().__init__(master, **kwargs, width=80, height=80, background='#2B2B2B', highlightbackground='#2B2B2B')
        self.create_oval(raio, raio, diametro, diametro, fill=self.fg_color, outline='')

class LabelHud(CTkLabel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, font=CTkFont(family='Roboto', size=20))

class FrameHud(CTkFrame):
    def __init__(self, master, cor, **kwargs):
        super().__init__(master, **kwargs, width=640, height=125, corner_radius=10)
        self.grid_propagate(False)

        self.cor = cor

        if self.cor == 'branco':
            circulo = Circle(self, fg_color='#fafafa')
            circulo.grid(column=0, row=0, padx=0, pady=0)

            lbl_name = LabelHud(self, text='Branco', text_color='#dfdfdf')
            lbl_name.grid(column=1, row=0, padx=30, pady=0)
        elif self.cor == 'preto':
            circulo = Circle(self, fg_color='#101010')
            circulo.grid(column=0, row=0, padx=0, pady=0)

            lbl_name = LabelHud(self, text='Preto', text_color='#000000')
            lbl_name.grid(column=1, row=0, padx=30, pady=0)

class FrameTab(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, width=640, height=640, corner_radius=10, fg_color='#505050')
        self.grid_propagate(False)

# Função que cria as casas
def func_casa(obj):
    print(obj.pos)

class Casa(CTkButton):
    def __init__(self, master, pos, **kwargs):
        super().__init__(master, **kwargs, width=80, height=80, corner_radius=0, text='', command=lambda: func_casa(self))
        self.grid_propagate(False)

        self.pos = pos

def criar_casas(master):
    casas = []
    color_um = '#000000'
    color_dois = '#FFFFFF'
    cont = 9

    for x in range(8):
        color_um, color_dois = color_dois, color_um
        cont -= 1
        for y in range(8):
            if (y + 1) % 2 == 0:
                casa = Casa(master, fg_color=color_um, pos=[letras[y], cont])
                casa.configure(hover_color=color_um)
            else:
                casa = Casa(master, fg_color=color_dois, pos=[letras[y], cont])
                casa.configure(hover_color=color_dois)

            casas.append(casa)

    return casas

class App(CTk):
    def __init__(self):
        super().__init__()
        self.geometry('640x900')
        self.title('Xadrez')
        self.resizable(width=False, height=False)
        self.grid_propagate(False)

        # Frame de hud do preto
        frame_hud_preto = FrameHud(self, 'preto')
        frame_hud_preto.grid(row=0, column=0, pady=0)

        # Frame do tabuleiro
        frame_tab = FrameTab(self)
        frame_tab.grid(row=1, column=0, pady=5)

        casas = criar_casas(frame_tab)

        cont = 0
        for x in range(8):
            for y in range(8):
                casas[cont].grid(row=x, column=y, padx=0, pady=0)
                cont += 1

        # Frame de hud do preto
        frame_hud_branco = FrameHud(self, 'branco')
        frame_hud_branco.grid(row=2, column=0, pady=0)

app = App()
app.mainloop()
