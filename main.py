from customtkinter import *
from PIL import Image

# Variaveis
letras = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

# Imagens
PEAO_BRANCO = CTkImage(light_image=Image.open('peão_branco.png'),
                       dark_image=Image.open('peão_branco.png'),
                       size=(50, 62))
PEAO_PRETO = CTkImage(light_image=Image.open('peão_preto.png'),
                       dark_image=Image.open('peão_preto.png'),
                       size=(50, 62))

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

class Casa(CTkFrame):
    def __init__(self, master, pos, tem_peca, **kwargs):
        super().__init__(master, **kwargs, width=80, height=80, corner_radius=0)
        self.grid_propagate(False)

        self.bind('<Button-1>', lambda e: func_casa(self))

        self.pos = pos
        self.tem_peca = tem_peca

# Peças
# Base
def criar_circulos(*casas, peca):
    pass

class Peca(CTkButton):
    def __init__(self, master, color, value, pos, **kwargs):
        super().__init__(master,
                         **kwargs,
                         fg_color='transparent',
                         bg_color='transparent',
                         hover=False,
                         text='aaaaaa')
        self.color = color
        self.value = value
        self.pos = pos

# Peão
def peao(peca):
    pass

class Peao(Peca):
    def __init__(self, master, color, pos, **kwargs):
        super().__init__(master, color=color, value=1, pos=pos, **kwargs, width=50, height=62, command=lambda: peao(self))

        self.jogou = False
        self.color = color
        self.pos = pos

        if self.color == 'branco':
            self.configure(image=PEAO_BRANCO, text_color=pos.cget('fg_color'))
        elif self.color == 'preto':
            self.configure(image=PEAO_PRETO, text_color=pos.cget('fg_color'))

def criar_casas(master):
    casas = []
    color_um = ['#000000', 'preto']
    color_dois = ['#FFFFFF', 'branco']
    cont = 9

    for x in range(8):
        color_um, color_dois = color_dois, color_um
        cont -= 1
        for y in range(8):
            if (y + 1) % 2 == 0:
                casa = Casa(master, fg_color=color_um[0], pos=[letras[y], cont], tem_peca=[False, None])
            else:
                casa = Casa(master, fg_color=color_dois[0], pos=[letras[y], cont], tem_peca=[False, None])

            # Criando as peças
            # Peão
            if x == 1 or x == 6:
                if x == 1:
                    peao = Peao(casa, color='preto', pos=casa)
                else:
                    peao = Peao(casa, color='branco', pos=casa)

                casa.tem_peca = [True, 'peao']
                peao.grid(row=0, column=0, padx=7, pady=5)

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
