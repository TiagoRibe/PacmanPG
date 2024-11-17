# Crie Pac-Man do Zero em Python com PyGame!!
import copy
from tabuleiro import tabuleiros
import pygame
import math

pygame.init()

LARGURA = 900
ALTURA = 950
tela = pygame.display.set_mode([LARGURA, ALTURA])
relogio = pygame.time.Clock()
fps = 60
fonte = pygame.font.Font('freesansbold.ttf', 20)
nivel = copy.deepcopy(tabuleiros)
cor = 'azul'
PI = math.pi
imagens_jogador = []
for i in range(1, 5):
    imagens_jogador.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (45, 45)))
imagem_blinky = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/red.png'), (45, 45))
imagem_pinky = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/pink.png'), (45, 45))
imagem_inky = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/blue.png'), (45, 45))
imagem_clyde = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/orange.png'), (45, 45))
imagem_assustado = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/powerup.png'), (45, 45))
imagem_morto = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/dead.png'), (45, 45))
jogador_x = 450
jogador_y = 663
direcao = 0
blinky_x = 56
blinky_y = 58
direcao_blinky = 0
inky_x = 440
inky_y = 388
direcao_inky = 2
pinky_x = 440
pinky_y = 438
direcao_pinky = 2
clyde_x = 440
clyde_y = 438
direcao_clyde = 2
contador = 0
piscar = False
# D, E, C, B
giros_permitidos = [False, False, False, False]
comando_direcao = 0
velocidade_jogador = 2
pontuacao = 0
powerup_ativo = False
contador_powerup = 0
fantasmas_comidos = [False, False, False, False]
alvos = [(jogador_x, jogador_y), (jogador_x, jogador_y), (jogador_x, jogador_y), (jogador_x, jogador_y)]
blinky_morto = False
inky_morto = False
clyde_morto = False
pinky_morto = False
blinky_na_casa = False
inky_na_casa = False
clyde_na_casa = False
pinky_na_casa = False
em_movimento = False
velocidades_fantasmas = [2, 2, 2, 2]
contador_inicio = 0
vidas = 3
jogo_encerrado = False
jogo_vencido = False

class Fantasma:
    def __init__(self, coordenada_x, coordenada_y, alvo, velocidade, imagem, direcao, morto, na_casa, id):
        self.pos_x = coordenada_x
        self.pos_y = coordenada_y
        self.centro_x = self.pos_x + 22
        self.centro_y = self.pos_y + 22
        self.alvo = alvo
        self.velocidade = velocidade
        self.imagem = imagem
        self.direcao = direcao
        self.morto = morto
        self.na_casa = na_casa
        self.id = id
        self.giros_permitidos, self.na_casa = self.verificar_colisoes()
        self.retangulo = self.desenhar()

    def desenhar(self):
        if (not powerup_ativo and not self.morto) or (fantasmas_comidos[self.id] and powerup_ativo and not self.morto):
            tela.blit(self.imagem, (self.pos_x, self.pos_y))
        elif powerup_ativo and not self.morto and not fantasmas_comidos[self.id]:
            tela.blit(imagem_assustado, (self.pos_x, self.pos_y))
        else:
            tela.blit(imagem_morto, (self.pos_x, self.pos_y))
        retangulo_fantasma = pygame.rect.Rect((self.centro_x - 18, self.centro_y - 18), (36, 36))
        return retangulo_fantasma

def verificar_colisoes(self):
    # D, E, C, B (Direita, Esquerda, Cima, Baixo)
    num1 = ((ALTURA - 50) // 32)
    num2 = (LARGURA // 30)
    num3 = 15
    self.giros_permitidos = [False, False, False, False]
    if 0 < self.centro_x // 30 < 29:
        if nivel[(self.centro_y - num3) // num1][self.centro_x // num2] == 9:
            self.giros_permitidos[2] = True
        if nivel[self.centro_y // num1][(self.centro_x - num3) // num2] < 3 \
                or (nivel[self.centro_y // num1][(self.centro_x - num3) // num2] == 9 and (
                self.na_casa or self.morto)):
            self.giros_permitidos[1] = True
        if nivel[self.centro_y // num1][(self.centro_x + num3) // num2] < 3 \
                or (nivel[self.centro_y // num1][(self.centro_x + num3) // num2] == 9 and (
                self.na_casa or self.morto)):
            self.giros_permitidos[0] = True
        if nivel[(self.centro_y + num3) // num1][self.centro_x // num2] < 3 \
                or (nivel[(self.centro_y + num3) // num1][self.centro_x // num2] == 9 and (
                self.na_casa or self.morto)):
            self.giros_permitidos[3] = True
        if nivel[(self.centro_y - num3) // num1][self.centro_x // num2] < 3 \
                or (nivel[(self.centro_y - num3) // num1][self.centro_x // num2] == 9 and (
                self.na_casa or self.morto)):
            self.giros_permitidos[2] = True

        if self.direcao == 2 or self.direcao == 3:
            if 12 <= self.centro_x % num2 <= 18:
                if nivel[(self.centro_y + num3) // num1][self.centro_x // num2] < 3 \
                        or (nivel[(self.centro_y + num3) // num1][self.centro_x // num2] == 9 and (
                        self.na_casa or self.morto)):
                    self.giros_permitidos[3] = True
                if nivel[(self.centro_y - num3) // num1][self.centro_x // num2] < 3 \
                        or (nivel[(self.centro_y - num3) // num1][self.centro_x // num2] == 9 and (
                        self.na_casa or self.morto)):
                    self.giros_permitidos[2] = True
            if 12 <= self.centro_y % num1 <= 18:
                if nivel[self.centro_y // num1][(self.centro_x - num2) // num2] < 3 \
                        or (nivel[self.centro_y // num1][(self.centro_x - num2) // num2] == 9 and (
                        self.na_casa or self.morto)):
                    self.giros_permitidos[1] = True
                if nivel[self.centro_y // num1][(self.centro_x + num2) // num2] < 3 \
                        or (nivel[self.centro_y // num1][(self.centro_x + num2) // num2] == 9 and (
                        self.na_casa or self.morto)):
                    self.giros_permitidos[0] = True

        if self.direcao == 0 or self.direcao == 1:
            if 12 <= self.centro_x % num2 <= 18:
                if nivel[(self.centro_y + num3) // num1][self.centro_x // num2] < 3 \
                        or (nivel[(self.centro_y + num3) // num1][self.centro_x // num2] == 9 and (
                        self.na_casa or self.morto)):
                    self.giros_permitidos[3] = True
                if nivel[(self.centro_y - num3) // num1][self.centro_x // num2] < 3 \
                    or (nivel[(self.centro_y - num3) // num1][self.centro_x // num2] == 9 and (
                    self.na_casa or self.morto)):
                        self.giros_permitidos[2] = True
            if 12 <= self.centro_y % num1 <= 18:
                if nivel[self.centro_y // num1][(self.centro_x - num3) // num2] < 3 \
                        or (nivel[self.centro_y // num1][(self.centro_x - num3) // num2] == 9 and (
                        self.na_casa or self.morto)):
                    self.giros_permitidos[1] = True
                if nivel[self.centro_y // num1][(self.centro_x + num3) // num2] < 3 \
                        or (nivel[self.centro_y // num1][(self.centro_x + num3) // num2] == 9 and (
                        self.na_casa or self.morto)):
                    self.giros_permitidos[0] = True
        else:
            self.giros_permitidos[0] = True
            self.giros_permitidos[1] = True

        if 350 < self.pos_x < 550 and 370 < self.pos_y < 480:
                self.na_casa = True
            
        else:
                self.na_casa = False

    return self.giros_permitidos, self.na_casa

