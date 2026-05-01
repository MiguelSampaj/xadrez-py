from customtkinter import *
from PIL import Image
from rich.traceback import install

install()

# Variaveis
act_peca = None
letras = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
pecas_em_jogo = []

# Imagens
PEAO_BRANCO = CTkImage(light_image=Image.open('img/peão_branco.png'),
                       dark_image=Image.open('img/peão_branco.png'),
                       size=(50, 62))
PEAO_PRETO = CTkImage(light_image=Image.open('img/peão_preto.png'),
                      dark_image=Image.open('img/peão_preto.png'),
                      size=(50, 62))

# Configs
set_appearance_mode('dark')

# Configurando os huds
class Circle(CTkFrame):
    def __init__(self, master, diametro, origem, **kwargs):
        self.diametro = diametro
        self.raio = self.diametro / 2
        self.origem = origem

        super().__init__(master, **kwargs, width=self.diametro, height=self.diametro, corner_radius=self.diametro)

class CasasCircle(Circle):
    def __init__(self, master, origem, **kwargs):
        super().__init__(master, fg_color='#505050',
                         diametro=30,
                         border_width=3,
                         border_color='#101010',
                         origem=origem,
                         **kwargs)

class LabelHud(CTkLabel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, font=CTkFont(family='Roboto', size=20))

class FrameHud(CTkFrame):
    def __init__(self, master, cor, **kwargs):
        super().__init__(master, **kwargs, width=640, height=125, corner_radius=10, fg_color='#404040')
        self.grid_propagate(False)

        self.cor = cor

        if self.cor == 'branco':
            circulo = Circle(self, fg_color='#fafafa', diametro=40, origem=None)
            circulo.grid(column=0, row=0, padx=(20, 0), pady=125 / 2 - 20)

            lbl_name = LabelHud(self, text='Branco', text_color='#dfdfdf')
            lbl_name.grid(column=1, row=0, padx=15, pady=0)
        elif self.cor == 'preto':
            circulo = Circle(self, fg_color='#101010', diametro=40, origem=None)
            circulo.grid(column=0, row=0, padx=(20, 0), pady=125 / 2 - 20)

            lbl_name = LabelHud(self, text='Preto', text_color='#000000')
            lbl_name.grid(column=1, row=0, padx=15, pady=0)

class FrameTab(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, width=640, height=640, corner_radius=10, fg_color='#505050')
        self.grid_propagate(False)

        self.casas = criar_casas(self)

# Função que cria as casas
def atualizar_casas_livres(casas):
    casas_livres = []
    for casa in casas:
        if not casa.tem_peca[0]:
            casas_livres.append(casa)

    return casas_livres

def func_casa(obj):
    for casa in obj.master.casas:
        if casa.tem_peca[0]:
            tirar_circulos(casa.tem_peca[1])

class Casa(CTkFrame):
    def __init__(self, master, pos, tem_peca, circle, **kwargs):
        super().__init__(master, **kwargs, width=80, height=80, corner_radius=0)
        self.grid_propagate(False)

        self.bind('<Button-1>', lambda e: func_casa(self))

        self.pos = pos
        self.tem_peca = tem_peca
        self.circle = circle

# Peças
# Base
def criar_casas(master):
    casas = []
    color_um = ['#004500', 'preto']
    color_dois = ['#FAFAFA', 'branco']
    cont = 9

    for x in range(8):
        color_um, color_dois = color_dois, color_um
        cont -= 1
        for y in range(8):
            if (y + 1) % 2 == 0:
                casa = Casa(master, fg_color=color_um[0], pos=[letras[y], cont], tem_peca=[False, None], circle=None)
            else:
                casa = Casa(master, fg_color=color_dois[0], pos=[letras[y], cont], tem_peca=[False, None], circle=None)

            # Criando as peças
            # Peão
            if x == 1 or x == 6:
                if x == 1:
                    peao = Peao(casa, color='preto', pos=casa, casas=casas, tipo='peao')
                else:
                    peao = Peao(casa, color='branco', pos=casa, casas=casas, tipo='peao')

                casa.tem_peca = [True, peao]
                pecas_em_jogo.append(peao)
                peao.grid(row=0, column=0, padx=8, pady=7)

            casas.append(casa)

    return casas

# Função que cria os circulos que apontam onde se pode jogar
def criar_circulos(casas, casas_livres, peca):
    pos_peca = peca.pos.pos

    # Peão
    if peca.tipo == 'peao':
        if not peca.jogou:
            # Criando a parte gráfica de se pode jogar ou não
            casa_um_frente = None
            casa_dois_frente = None
            circulo_um = None
            circulo_dois = None

            for casa in casas:
                if peca.color == 'branco':
                    if casa.pos == [pos_peca[0], pos_peca[1] + 1] and not casa.tem_peca[0]:
                        casa_um_frente = casa
                        circulo_um = CasasCircle(casa, peca)
                        casa.circle = circulo_um

                    elif casa.pos == [pos_peca[0], pos_peca[1] + 2] and not casa.tem_peca[0]:
                        casa_dois_frente = casa
                        circulo_dois = CasasCircle(casa, peca)
                        casa.circle = circulo_dois

                elif peca.color == 'preto':
                    if casa.pos == [pos_peca[0], pos_peca[1] - 1] and not casa.tem_peca[0]:
                        casa_um_frente = casa
                        circulo_um = CasasCircle(casa, peca)
                        casa.circle = circulo_um

                    elif casa.pos == [pos_peca[0], pos_peca[1] - 2] and not casa.tem_peca[0]:
                        casa_dois_frente = casa
                        circulo_dois = CasasCircle(casa, peca)
                        casa.circle = circulo_dois

            if casa_um_frente.pos[1] > 7 or casa_dois_frente.pos[1] > 7:
                pass
            else:
                if casa_um_frente in casas_livres:
                    circulo_um.grid(padx=25, pady=25)
                    peca.casas_jogar.append(casa_um_frente)

                if casa_dois_frente in casas_livres:
                    circulo_dois.grid(padx=25, pady=25)
                    peca.casas_jogar.append(casa_dois_frente)
        else:
            # Criando a parte gráfica de se pode jogar ou não
            casa_um_frente = None
            circulo = None

            for casa in casas:
                if peca.color == 'branco':
                    if casa.pos == [pos_peca[0], pos_peca[1] + 1] and not casa.tem_peca[0]:
                        casa_um_frente = casa
                        circulo = CasasCircle(casa_um_frente, peca)
                        casa.circle = circulo
                elif peca.color == 'preto':
                    if casa.pos == [pos_peca[0], pos_peca[1] - 1] and not casa.tem_peca[0]:
                        casa_um_frente = casa
                        circulo = CasasCircle(casa_um_frente, peca)
                        casa.circle = circulo

            if casa_um_frente.pos[1] > 7:
                pass
            else:
                if casa_um_frente in casas_livres and not casa_um_frente.tem_peca[0]:
                    circulo.grid(padx=25, pady=25)
                    peca.casas_jogar.append(casa_um_frente)

def tirar_circulos(peca):
    if len(peca.casas_jogar) > 0:
        for casa in peca.casas_jogar:
            casa.circle.destroy()

        peca.casas_jogar.clear()

# Pecas
# Base
def func_peca(peca, casas, casas_livres):
    global act_peca

    if act_peca is not None:
        tirar_circulos(act_peca)

    act_peca = peca
    criar_circulos(peca=peca, casas=casas, casas_livres=casas_livres)

class Peca(CTkButton):
    def __init__(self, master, color, value, pos, tipo, casas, casas_jogar, **kwargs):
        super().__init__(master,
                         **kwargs,
                         fg_color='transparent',
                         bg_color='transparent',
                         hover=False,
                         text='aaaaaa',
                         command=lambda: func_peca(self, casas, atualizar_casas_livres(casas)))
        self.color = color
        self.value = value
        self.pos = pos
        self.tipe = tipo
        self.casas_jogar = casas_jogar

# Peão
class Peao(Peca):
    def __init__(self, master, color, pos, tipo, casas, **kwargs):
        super().__init__(master,
                         color=color,
                         value=1,
                         pos=pos,
                         tipo=tipo,
                         casas_jogar=[],
                         **kwargs,
                         width=50,
                         height=62,
                         casas=casas)

        self.jogou = False
        self.color = color
        self.pos = pos
        self.tipo = tipo

        if self.color == 'branco':
            self.configure(image=PEAO_BRANCO, text_color=pos.cget('fg_color'))
        elif self.color == 'preto':
            self.configure(image=PEAO_PRETO, text_color=pos.cget('fg_color'))

class App(CTk):
    def __init__(self):
        super().__init__()
        self.geometry('640x900')
        self.title('Xadrez')
        self.resizable(width=False, height=False)
        self.grid_propagate(False)

        # Frame de hud do preto
        self.frame_hud_preto = FrameHud(self, 'preto')
        self.frame_hud_preto.grid(row=0, column=0, pady=0)

        # Frame do tabuleiro
        self.frame_tab = FrameTab(self)
        self.frame_tab.grid(row=1, column=0, pady=5)

        self.casas_livres = atualizar_casas_livres(self.frame_tab.casas)

        cont = 0
        for x in range(8):
            for y in range(8):
                self.frame_tab.casas[cont].grid(row=x, column=y, padx=0, pady=0)
                cont += 1

        # Frame de hud do preto
        self.frame_hud_branco = FrameHud(self, 'branco')
        self.frame_hud_branco.grid(row=2, column=0, pady=0)

app = App()
app.mainloop()
