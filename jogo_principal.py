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
fotos_rato = []
for i in range(1, 5):
    fotos_rato.append(pygame.transform.scale(pygame.image.load(f'Imagens/Fotos_rato/{i}.png'), (45, 45)))
fotos_gato1 = []
fotos_gato2 = []
fotos_gato3 = []
fotos_gato4 = []
for j in range(5,11):
    fotos_gato1.append(pygame.transform.scale(pygame.image.load(f'Imagens/Fotos_gatos/{j}.png'), (45, 45)))
    fotos_gato2.append(pygame.transform.scale(pygame.image.load(f'Imagens/Fotos_gatos/{j}.png'), (45, 45)))
    fotos_gato3.append(pygame.transform.scale(pygame.image.load(f'Imagens/Fotos_gatos/{j}.png'), (45, 45)))
    fotos_gato4.append(pygame.transform.scale(pygame.image.load(f'Imagens/Fotos_gatos/{j}.png'), (45, 45)))

imagem_assustado = pygame.transform.scale(pygame.image.load(f'Imagens/Fotos_gatos/Hurt.png'), (45, 45))
imagem_morto = pygame.transform.scale(pygame.image.load(f'Imagens/Fotos_gatos/Death.png'), (45, 45))
jogador_x = 450
jogador_y = 663
direcao = 0
gato2_x = 56
gato2_y = 58
direcao_gato2 = 0
gato3_x = 440
gato3_y = 388
direcao_gato3 = 2
gato4_x = 440
gato4_y = 438
direcao_gato4 = 2
gato1_x = 440
gato1_y = 438
direcao_gato1 = 2
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
gato2_morto = False
gato3_morto = False
gato1_morto = False
gato4_morto = False
gato2_na_casa = False
gato3_na_casa = False
gato1_na_casa = False
gato4_na_casa = False
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
        self.giros, self.na_casa = self.verificar_colisoes()
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
        self.giros = [False, False, False, False]
        if 0 < self.centro_x // 30 < 29:
            if nivel[(self.centro_y - num3) // num1][self.centro_x // num2] == 9:
                self.giros[2] = True
            if nivel[self.centro_y // num1][(self.centro_x - num3) // num2] < 3 \
                    or (nivel[self.centro_y // num1][(self.centro_x - num3) // num2] == 9 and (
                    self.na_casa or self.morto)):
                self.giros[1] = True
            if nivel[self.centro_y // num1][(self.centro_x + num3) // num2] < 3 \
                    or (nivel[self.centro_y // num1][(self.centro_x + num3) // num2] == 9 and (
                    self.na_casa or self.morto)):
                self.giros[0] = True
            if nivel[(self.centro_y + num3) // num1][self.centro_x // num2] < 3 \
                    or (nivel[(self.centro_y + num3) // num1][self.centro_x // num2] == 9 and (
                    self.na_casa or self.morto)):
                self.giros[3] = True
            if nivel[(self.centro_y - num3) // num1][self.centro_x // num2] < 3 \
                    or (nivel[(self.centro_y - num3) // num1][self.centro_x // num2] == 9 and (
                    self.na_casa or self.morto)):
                self.giros[2] = True

            if self.direcao == 2 or self.direcao == 3:
                if 12 <= self.centro_x % num2 <= 18:
                    if nivel[(self.centro_y + num3) // num1][self.centro_x // num2] < 3 \
                            or (nivel[(self.centro_y + num3) // num1][self.centro_x // num2] == 9 and (
                            self.na_casa or self.morto)):
                        self.giros[3] = True
                    if nivel[(self.centro_y - num3) // num1][self.centro_x // num2] < 3 \
                            or (nivel[(self.centro_y - num3) // num1][self.centro_x // num2] == 9 and (
                            self.na_casa or self.morto)):
                        self.giros[2] = True
                if 12 <= self.centro_y % num1 <= 18:
                    if nivel[self.centro_y // num1][(self.centro_x - num2) // num2] < 3 \
                            or (nivel[self.centro_y // num1][(self.centro_x - num2) // num2] == 9 and (
                            self.na_casa or self.morto)):
                        self.giros[1] = True
                    if nivel[self.centro_y // num1][(self.centro_x + num2) // num2] < 3 \
                            or (nivel[self.centro_y // num1][(self.centro_x + num2) // num2] == 9 and (
                            self.na_casa or self.morto)):
                        self.giros[0] = True

            if self.direcao == 0 or self.direcao == 1:
                if 12 <= self.centro_x % num2 <= 18:
                    if nivel[(self.centro_y + num3) // num1][self.centro_x // num2] < 3 \
                            or (nivel[(self.centro_y + num3) // num1][self.centro_x // num2] == 9 and (
                            self.na_casa or self.morto)):
                        self.giros[3] = True
                    if nivel[(self.centro_y - num3) // num1][self.centro_x // num2] < 3 \
                        or (nivel[(self.centro_y - num3) // num1][self.centro_x // num2] == 9 and (
                        self.na_casa or self.morto)):
                            self.giros[2] = True
                if 12 <= self.centro_y % num1 <= 18:
                    if nivel[self.centro_y // num1][(self.centro_x - num3) // num2] < 3 \
                            or (nivel[self.centro_y // num1][(self.centro_x - num3) // num2] == 9 and (
                            self.na_casa or self.morto)):
                        self.giros[1] = True
                    if nivel[self.centro_y // num1][(self.centro_x + num3) // num2] < 3 \
                            or (nivel[self.centro_y // num1][(self.centro_x + num3) // num2] == 9 and (
                            self.na_casa or self.morto)):
                        self.giros[0] = True
            else:
                self.giros[0] = True
                self.giros[1] = True

            if 350 < self.pos_x < 550 and 370 < self.pos_y < 480:
                    self.na_casa = True

            else:
                    self.na_casa = False

        return self.giros, self.na_casa

    def movimento_gato1(self):
        # D, E, C, B (Direita, Esquerda, Cima, Baixo)
        if self.direcao == 0:
            if self.alvo[0] > self.pos_x and self.giros[0]:
                self.pos_x += self.velocidade
            elif not self.giros[0]:
                if self.alvo[1] > self.pos_y and self.giros[3]:
                    self.direcao = 3
                    self.pos_y += self.velocidade
                elif self.alvo[1] < self.pos_y and self.giros[2]:
                    self.direcao = 2
                    self.pos_y -= self.velocidade
                elif self.alvo[0] < self.pos_x and self.giros[1]:
                    self.direcao = 1
                    self.pos_x -= self.velocidade
                elif self.giros[3]:
                    self.direcao = 3
                    self.pos_y += self.velocidade
                elif self.giros[2]:
                    self.direcao = 2
                    self.pos_y -= self.velocidade
                elif self.giros[1]:
                    self.direcao = 1
                    self.pos_x -= self.velocidade
            elif self.giros[0]:
                if self.alvo[1] > self.pos_y and self.giros[3]:
                    self.direcao = 3
                    self.pos_y += self.velocidade
                if self.alvo[1] < self.pos_y and self.giros[2]:
                    self.direcao = 2
                    self.pos_y -= self.velocidade
                else:
                    self.pos_x += self.velocidade
        elif self.direcao == 1:
            if self.alvo[1] > self.pos_y and self.giros[3]:
                self.direcao = 3
            elif self.alvo[0] < self.pos_x and self.giros[1]:
                self.pos_x -= self.velocidade
            elif not self.giros[1]:
                if self.alvo[1] > self.pos_y and self.giros[3]:
                    self.direcao = 3
                    self.pos_y += self.velocidade
                elif self.alvo[1] < self.pos_y and self.giros[2]:
                    self.direcao = 2
                    self.pos_y -= self.velocidade
                elif self.alvo[0] > self.pos_x and self.giros[0]:
                    self.direcao = 0
                    self.pos_x += self.velocidade
                elif self.giros[3]:
                    self.direcao = 3
                    self.pos_y += self.velocidade
                elif self.giros[2]:
                    self.direcao = 2
                    self.pos_y -= self.velocidade
                elif self.giros[0]:
                    self.direcao = 0
                    self.pos_x += self.velocidade
            elif self.giros[1]:
                if self.alvo[1] > self.pos_y and self.giros[3]:
                    self.direcao = 3
                    self.pos_y += self.velocidade
                if self.alvo[1] < self.pos_y and self.giros[2]:
                    self.direcao = 2
                    self.pos_y -= self.velocidade
                else:
                    self.pos_x -= self.velocidade
        elif self.direcao == 2:
            if self.alvo[0] < self.pos_x and self.giros[1]:
                self.direcao = 1
                self.pos_x -= self.velocidade
            elif self.alvo[1] < self.pos_y and self.giros[2]:
                self.direcao = 2
                self.pos_y -= self.velocidade
            elif not self.giros[2]:
                if self.alvo[0] > self.pos_x and self.giros[0]:
                    self.direcao = 0
                    self.pos_x += self.velocidade
                elif self.alvo[0] < self.pos_x and self.giros[1]:
                    self.direcao = 1
                    self.pos_x -= self.velocidade
                elif self.alvo[1] > self.pos_y and self.giros[3]:
                    self.direcao = 3
                    self.pos_y += self.velocidade
                elif self.giros[1]:
                    self.direcao = 1
                    self.pos_x -= self.velocidade
                elif self.giros[3]:
                    self.direcao = 3
                    self.pos_y += self.velocidade
                elif self.giros[0]:
                    self.direcao = 0
                    self.pos_x += self.velocidade
            elif self.giros[2]:
                if self.alvo[0] > self.pos_x and self.giros[0]:
                    self.direcao = 0
                    self.pos_x += self.velocidade
                elif self.alvo[0] < self.pos_x and self.giros[1]:
                    self.direcao = 1
                    self.pos_x -= self.velocidade
                else:
                    self.pos_y -= self.velocidade
        elif self.direcao == 3:
            if self.alvo[1] > self.pos_y and self.giros[3]:
                self.pos_y += self.velocidade
            elif not self.giros[3]:
                if self.alvo[0] > self.pos_x and self.giros[0]:
                    self.direcao = 0
                    self.pos_x += self.velocidade
                elif self.alvo[0] < self.pos_x and self.giros[1]:
                    self.direcao = 1
                    self.pos_x -= self.velocidade
                elif self.alvo[1] < self.pos_y and self.giros[2]:
                    self.direcao = 2
                    self.pos_y -= self.velocidade
                elif self.giros[2]:
                    self.direcao = 2
                    self.pos_y -= self.velocidade
                elif self.giros[1]:
                    self.direcao = 1
                    self.pos_x -= self.velocidade
                elif self.giros[0]:
                    self.direcao = 0
                    self.pos_x += self.velocidade
            elif self.giros[3]:
                if self.alvo[0] > self.pos_x and self.giros[0]:
                    self.direcao = 0
                    self.pos_x += self.velocidade
                elif self.alvo[0] < self.pos_x and self.giros[1]:
                    self.direcao = 1
                    self.pos_x -= self.velocidade
                else:
                    self.pos_y += self.velocidade
        if self.pos_x < -30:
            self.pos_x = 900
        elif self.pos_x > 900:
            self.pos_x - 30
        return self.pos_x, self.pos_y, self.direcao
    
    def movimento_gato2(self):
        if self.direcao == 0:
            if self.alvo[0] > self.pos_x and self.alvo[0]:
                self.pos_x += self.velocidade
            elif not self.alvo[0]:
                if self.alvo[1] > self.pos_y and self.alvo[3]:
                    self.direcao = 3
                    self.pos_y += self.velocidade
                elif self.alvo[1] < self.pos_y and self.alvo[2]:
                    self.direcao = 2
                    self.pos_y -= self.velocidade
                elif self.alvo[0] < self.pos_x and self.alvo[1]:
                    self.direcao = 1
                    self.pos_x -= self.velocidade
                elif self.alvo[3]:
                    self.direcao = 3
                    self.pos_y += self.velocidade
                elif self.alvo[2]:
                    self.direcao = 2
                    self.pos_y -= self.velocidade
                elif self.alvo[1]:
                    self.direcao = 1
                    self.pos_x -= self.velocidade
            elif self.alvo[0]:
                self.pos_x += self.velocidade
        elif self.direcao == 1:
            if self.alvo[0] < self.pos_x and self.alvo[1]:
                self.pos_x -= self.velocidade
            elif not self.alvo[1]:
                if self.alvo[1] > self.pos_y and self.alvo[3]:
                    self.direcao = 3
                    self.pos_y += self.velocidade
                elif self.alvo[1] < self.pos_y and self.alvo[2]:
                    self.direcao = 2
                    self.pos_y -= self.velocidade
                elif self.alvo[0] > self.pos_x and self.alvo[0]:
                    self.direcao = 0
                    self.pos_x += self.velocidade
                elif self.alvo[3]:
                    self.direcao = 3
                    self.pos_y += self.velocidade
                elif self.alvo[2]:
                    self.direcao = 2
                    self.pos_y -= self.velocidade
                elif self.alvo[0]:
                    self.direcao = 0
                    self.pos_x += self.velocidade
            elif self.alvo[1]:
                self.pos_x -= self.velocidade
        elif self.direcao == 2:
            if self.alvo[1] < self.pos_y and self.alvo[2]:
                self.direcao = 2
                self.pos_y -= self.velocidade
            elif not self.alvo[2]:
                if self.alvo[0] > self.pos_x and self.alvo[0]:
                    self.direcao = 0
                    self.pos_x += self.velocidade
                elif self.alvo[0] < self.pos_x and self.alvo[1]:
                    self.direcao = 1
                    self.pos_x -= self.velocidade
                elif self.alvo[1] > self.pos_y and self.alvo[3]:
                    self.direcao = 3
                    self.pos_y += self.velocidade
                elif self.alvo[3]:
                    self.direcao = 3
                    self.pos_y += self.velocidade
                elif self.alvo[0]:
                    self.direcao = 0
                    self.pos_x += self.velocidade
                elif self.alvo[1]:
                    self.direcao = 1
                    self.pos_x -= self.velocidade
            elif self.alvo[2]:
                self.pos_y -= self.velocidade
        elif self.direcao == 3:
            if self.alvo[1] > self.pos_y and self.alvo[3]:
                self.pos_y += self.velocidade
            elif not self.alvo[3]:
                if self.alvo[0] > self.pos_x and self.alvo[0]:
                    self.direcao = 0
                    self.pos_x += self.velocidade
                elif self.alvo[0] < self.pos_x and self.alvo[1]:
                    self.direcao = 1
                    self.pos_x -= self.velocidade
                elif self.alvo[1] < self.pos_y and self.alvo[2]:
                    self.direcao = 2
                    self.pos_y -= self.velocidade
                elif self.alvo[2]:
                    self.direcao = 2
                    self.pos_y -= self.velocidade
                elif self.alvo[0]:
                    self.direcao = 0
                    self.pos_x += self.velocidade
                elif self.alvo[1]:
                    self.direcao = 1
                    self.pos_x -= self.velocidade
            elif self.alvo[3]:
                self.pos_y += self.velocidade
        if self.pos_x < -30:
            self.pos_x = 900
        elif self.pos_x > 900:
            self.pos_x - 30
        return self.pos_x, self.pos_y, self.direcao
    
    def movimento_gato3(self):
        if self.direcao == 0:
            if self.alvo[0] > self.pos_x and self.giros[0]:
                self.pos_x += self.velocidade
            elif not self.giros[0]:
                if self.alvo[1] > self.pos_y and self.giros[3]:
                    self.direcao = 3
                    self.pos_y += self.velocidade
                elif self.alvo[1] < self.pos_y and self.giros[2]:
                    self.direcao = 2
                    self.pos_y -= self.velocidade
                elif self.alvo[0] < self.pos_x and self.giros[1]:
                    self.direcao = 1
                    self.pos_x -= self.velocidade
                elif self.giros[3]:
                    self.direcao = 3
                    self.pos_y += self.velocidade
                elif self.giros[2]:
                    self.direcao = 2
                    self.pos_y -= self.velocidade
                elif self.giros[1]:
                    self.direcao = 1
                    self.pos_x -= self.velocidade
            elif self.giros[0]:
                if self.alvo[1] > self.pos_y and self.giros[3]:
                    self.direcao = 3
                    self.pos_y += self.velocidade
                if self.alvo[1] < self.pos_y and self.giros[2]:
                    self.direcao = 2
                    self.pos_y -= self.velocidade
                else:
                    self.pos_x += self.velocidade
        elif self.direcao == 1:
            if self.alvo[1] > self.pos_y and self.giros[3]:
                self.direcao = 3
            elif self.alvo[0] < self.pos_x and self.giros[1]:
                self.pos_x -= self.velocidade
            elif not self.giros[1]:
                if self.alvo[1] > self.pos_y and self.giros[3]:
                    self.direcao = 3
                    self.pos_y += self.velocidade
                elif self.alvo[1] < self.pos_y and self.giros[2]:
                    self.direcao = 2
                    self.pos_y -= self.velocidade
                elif self.alvo[0] > self.pos_x and self.giros[0]:
                    self.direcao = 0
                    self.pos_x += self.velocidade
                elif self.giros[3]:
                    self.direcao = 3
                    self.pos_y += self.velocidade
                elif self.giros[2]:
                    self.direcao = 2
                    self.pos_y -= self.velocidade
                elif self.giros[0]:
                    self.direcao = 0
                    self.pos_x += self.velocidade
            elif self.giros[1]:
                if self.alvo[1] > self.pos_y and self.giros[3]:
                    self.direcao = 3
                    self.pos_y += self.velocidade
                if self.alvo[1] < self.pos_y and self.giros[2]:
                    self.direcao = 2
                    self.pos_y -= self.velocidade
                else:
                    self.pos_x -= self.velocidade
        elif self.direcao == 2:
            if self.alvo[1] < self.pos_y and self.giros[2]:
                self.direcao = 2
                self.pos_y -= self.velocidade
            elif not self.giros[2]:
                if self.alvo[0] > self.pos_x and self.giros[0]:
                    self.direcao = 0
                    self.pos_x += self.velocidade
                elif self.alvo[0] < self.pos_x and self.giros[1]:
                    self.direcao = 1
                    self.pos_x -= self.velocidade
                elif self.alvo[1] > self.pos_y and self.giros[3]:
                    self.direcao = 3
                    self.pos_y += self.velocidade
                elif self.giros[1]:
                    self.direcao = 1
                    self.pos_x -= self.velocidade
                elif self.giros[3]:
                    self.direcao = 3
                    self.pos_y += self.velocidade
                elif self.giros[0]:
                    self.direcao = 0
                    self.pos_x += self.velocidade
            elif self.giros[2]:
                self.pos_y -= self.velocidade
        elif self.direcao == 3:
            if self.alvo[1] > self.pos_y and self.giros[3]:
                self.pos_y += self.velocidade
            elif not self.giros[3]:
                if self.alvo[0] > self.pos_x and self.giros[0]:
                    self.direcao = 0
                    self.pos_x += self.velocidade
                elif self.alvo[0] < self.pos_x and self.giros[1]:
                    self.direcao = 1
                    self.pos_x -= self.velocidade
                elif self.alvo[1] < self.pos_y and self.giros[2]:
                    self.direcao = 2
                    self.pos_y -= self.velocidade
                elif self.giros[2]:
                    self.direcao = 2
                    self.pos_y -= self.velocidade
                elif self.giros[1]:
                    self.direcao = 1
                    self.pos_x -= self.velocidade
                elif self.giros[0]:
                    self.direcao = 0
                    self.pos_x += self.velocidade
            elif self.giros[3]:
                self.pos_y += self.velocidade
        if self.pos_x < -30:
            self.pos_x = 900
        elif self.pos_x > 900:
            self.pos_x - 30
        return self.pos_x, self.pos_y, self.direcao
    
    def movimento_gato4(self):
        if self.direcao == 0:
            if self.alvo[0] > self.pos_x and self.giros[0]:
                self.pos_x += self.velocidade
            elif not self.giros[0]:
                if self.alvo[1] > self.pos_y and self.giros[3]:
                    self.direcao = 3
                    self.pos_y += self.velocidade
                elif self.alvo[1] < self.pos_y and self.giros[2]:
                    self.direcao = 2
                    self.pos_y -= self.velocidade
                elif self.alvo[0] < self.pos_x and self.giros[1]:
                    self.direcao = 1
                    self.pos_x -= self.velocidade
                elif self.giros[3]:
                    self.direcao = 3
                    self.pos_y += self.velocidade
                elif self.giros[2]:
                    self.direcao = 2
                    self.pos_y -= self.velocidade
                elif self.giros[1]:
                    self.direcao = 1
                    self.pos_x -= self.velocidade
            elif self.giros[0]:
                self.pos_x += self.velocidade
        elif self.direcao == 1:
            if self.alvo[1] > self.pos_y and self.giros[3]:
                self.direcao = 3
            elif self.alvo[0] < self.pos_x and self.giros[1]:
                self.pos_x -= self.velocidade
            elif not self.giros[1]:
                if self.alvo[1] > self.pos_y and self.giros[3]:
                    self.direcao = 3
                    self.pos_y += self.velocidade
                elif self.alvo[1] < self.pos_y and self.giros[2]:
                    self.direcao = 2
                    self.pos_y -= self.velocidade
                elif self.alvo[0] > self.pos_x and self.giros[0]:
                    self.direcao = 0
                    self.pos_x += self.velocidade
                elif self.giros[3]:
                    self.direcao = 3
                    self.pos_y += self.velocidade
                elif self.giros[2]:
                    self.direcao = 2
                    self.pos_y -= self.velocidade
                elif self.giros[0]:
                    self.direcao = 0
                    self.pos_x += self.velocidade
            elif self.giros[1]:
                self.pos_x -= self.velocidade
        elif self.direcao == 2:
            if self.alvo[0] < self.pos_x and self.giros[1]:
                self.direcao = 1
                self.pos_x -= self.velocidade
            elif self.alvo[1] < self.pos_y and self.giros[2]:
                self.direcao = 2
                self.pos_y -= self.velocidade
            elif not self.giros[2]:
                if self.alvo[0] > self.pos_x and self.giros[0]:
                    self.direcao = 0
                    self.pos_x += self.velocidade
                elif self.alvo[0] < self.pos_x and self.giros[1]:
                    self.direcao = 1
                    self.pos_x -= self.velocidade
                elif self.alvo[1] > self.pos_y and self.giros[3]:
                    self.direcao = 3
                    self.pos_y += self.velocidade
                elif self.giros[1]:
                    self.direcao = 1
                    self.pos_x -= self.velocidade
                elif self.giros[3]:
                    self.direcao = 3
                    self.pos_y += self.velocidade
                elif self.giros[0]:
                    self.direcao = 0
                    self.pos_x += self.velocidade
            elif self.giros[2]:
                if self.alvo[0] > self.pos_x and self.giros[0]:
                    self.direcao = 0
                    self.pos_x += self.velocidade
                elif self.alvo[0] < self.pos_x and self.giros[1]:
                    self.direcao = 1
                    self.pos_x -= self.velocidade
                else:
                    self.pos_y -= self.velocidade
        elif self.direcao == 3:
            if self.alvo[1] > self.pos_y and self.giros[3]:
                self.pos_y += self.velocidade
            elif not self.giros[3]:
                if self.alvo[0] > self.pos_x and self.giros[0]:
                    self.direcao = 0
                    self.pos_x += self.velocidade
                elif self.alvo[0] < self.pos_x and self.giros[1]:
                    self.direcao = 1
                    self.pos_x -= self.velocidade
                elif self.alvo[1] < self.pos_y and self.giros[2]:
                    self.direcao = 2
                    self.pos_y -= self.velocidade
                elif self.giros[2]:
                    self.direcao = 2
                    self.pos_y -= self.velocidade
                elif self.giros[1]:
                    self.direcao = 1
                    self.pos_x -= self.velocidade
                elif self.giros[0]:
                    self.direcao = 0
                    self.pos_x += self.velocidade
            elif self.giros[3]:
                if self.alvo[0] > self.pos_x and self.giros[0]:
                    self.direcao = 0
                    self.pos_x += self.velocidade
                elif self.alvo[0] < self.pos_x and self.giros[1]:
                    self.direcao = 1
                    self.pos_x -= self.velocidade
                else:
                    self.pos_y += self.velocidade
        if self.pos_x < -30:
            self.pos_x = 900
        elif self.pos_x > 900:
            self.pos_x - 30
        return self.pos_x, self.pos_y, self.direcao
    
def desenha_variavel():
    texto_pontuacao = fonte.render(f'Pontos: {pontuacao}', True, 'white')
    tela.blit(texto_pontuacao, (10, 920))
    if powerup_ativo:
        pygame.draw.circle(tela, 'blue', (140, 930), 15)
    for i in range(vidas):
        tela.blit(pygame.transform.scale(fotos_rato[0], (30, 30)), (650 + i * 40, 915))
    if jogo_encerrado:
        pygame.draw.rect(tela, 'white', [50, 200, 800, 300],0, 10)
        pygame.draw.rect(tela, 'dark gray', [70, 220, 760, 260], 0, 10)
        gameover_text = fonte.render('Você perdeu! Aperte espaço para recomeçar!', True, 'red')
        tela.blit(gameover_text, (100, 300))
    if jogo_vencido:
        pygame.draw.rect(tela, 'white', [50, 200, 800, 300],0, 10)
        pygame.draw.rect(tela, 'dark gray', [70, 220, 760, 260], 0, 10)
        gameover_text = fonte.render('Parabens, você venceu! Aperte espaço para recomeçar!', True, 'green')
        tela.blit(gameover_text, (100, 300))

def checa_colisao(pont, poder, conta_poder, gatos_comidos):
    num1 = (ALTURA - 50) // 32
    num2 = LARGURA // 30
    if 0 < jogador_x < 870:
        if nivel[centro_y // num1][centro_x // num2] == 1:
            nivel[centro_y // num1][centro_x // num2] = 0
            pont += 10
        if nivel[centro_y // num1][centro_x // num2] == 2:
            nivel[centro_y // num1][centro_x // num2] = 0
            pont += 50
            poder = True
            conta_poder = 0
            gatos_comidos = [False, False, False, False]
    return pont, poder, conta_poder, gatos_comidos

def desenha_tabuleiro():
    num1 = ((ALTURA - 50) // 32)
    num2 = (LARGURA // 30)
    for i in range(len(nivel)):
        for j in range(len(nivel[i])):
            if nivel[i][j] == 1:
                pygame.draw.circle(tela, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
            if nivel[i][j] == 2 and not piscar:
                pygame.draw.circle(tela, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
            if nivel[i][j] == 3:
                pygame.draw.line(tela, cor, (j * num2 + (0.5 * num2), i * num1),
                                 (j * num2 + (0.5 * num2), i * num1 + num1), 3)
            if nivel[i][j] == 4:
                pygame.draw.line(tela, cor, (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
            if nivel[i][j] == 5:
                pygame.draw.arc(tela, cor, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1],
                                0, PI / 2, 3)
            if nivel[i][j] == 6:
                pygame.draw.arc(tela, cor,
                                [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], PI / 2, PI, 3)
            if nivel[i][j] == 7:
                pygame.draw.arc(tela, cor, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], PI,
                                3 * PI / 2, 3)
            if nivel[i][j] == 8:
                pygame.draw.arc(tela, cor,
                                [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * PI / 2,
                                2 * PI, 3)
            if nivel[i][j] == 9:
                pygame.draw.line(tela, 'white', (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)


def desenha_jogador():
    if direcao == 0:
        tela.blit(fotos_rato[contador // 5], (jogador_x, jogador_y))
    elif direcao == 1:
        tela.blit(pygame.transform.flip(fotos_rato[contador // 5], True, False), (jogador_x, jogador_y))
    elif direcao == 2:
        tela.blit(pygame.transform.rotate(fotos_rato[contador // 5], 90), (jogador_x, jogador_y))
    elif direcao == 3:
        tela.blit(pygame.transform.rotate(fotos_rato[contador // 5], 270), (jogador_x, jogador_y))

def checa_posicao(centerx, centery):
    virar = [False, False, False, False]
    num1 = (ALTURA - 50) // 32
    num2 = (LARGURA // 30)
    num3 = 15

    #checa colisao baseado no centro x e centro y
    if centerx // 30 < 29:
        if direcao == 0:
            if nivel[centery // num1][(centerx - num3) // num2] < 3:
                virar[1] = True
        if direcao == 1:
            if nivel[centery // num1][(centerx + num3) // num2] < 3:
                virar[0] = True
        if direcao == 2:
            if nivel[(centery + num3) // num1][centerx // num2] < 3:
                virar[3] = True
        if direcao == 3:
            if nivel[(centery - num3) // num1][centerx // num2] < 3:
                virar[2] = True

        if direcao == 2 or direcao == 3:
            if 12 <= centerx % num2 <= 18:
                if nivel[(centery + num3) // num1][centerx // num2] < 3:
                    virar[3] = True
                if nivel[(centery - num3) // num1][centerx // num2] < 3:
                    virar[2] = True
            if 12 <= centery % num1 <= 18:
                if nivel[centery // num1][(centerx - num2) // num2] < 3:
                    virar[1] = True
                if nivel[centery // num1][(centerx + num2) // num2] < 3:
                    virar[0] = True
        if direcao == 0 or direcao == 1:
            if 12 <= centerx % num2 <= 18:
                if nivel[(centery + num1) // num1][centerx // num2] < 3:
                    virar[3] = True
                if nivel[(centery - num1) // num1][centerx // num2] < 3:
                    virar[2] = True
            if 12 <= centery % num1 <= 18:
                if nivel[centery // num1][(centerx - num3) // num2] < 3:
                    virar[1] = True
                if nivel[centery // num1][(centerx + num3) // num2] < 3:
                    virar[0] = True
    else:
        virar[0] = True
        virar[1] = True

    return virar

def movimentacao(eixo_x, eixo_y):
    if direcao == 0 and giros_permitidos[0]:
        eixo_x += velocidade_jogador
    elif direcao == 1 and giros_permitidos[1]:
        eixo_x -= velocidade_jogador
    if direcao == 2 and giros_permitidos[2]:
        eixo_y -= velocidade_jogador
    elif direcao == 3 and giros_permitidos[3]:
        eixo_y += velocidade_jogador
    return eixo_x, eixo_y

def obter_alvos(gato2_x, gato2_y, gato3_x, gato3_y, gato4_x, gato4_y, gato1_x, gato1_y):
    if jogador_x < 450:
        fugir_x = 900
    else:
        fugir_x = 0
    if jogador_y < 450:
        fugir_y = 900
    else:
        fugir_y = 0
    alvo_retorno = (380, 400)
    if powerup_ativo:
        if not gato2_morto and not fantasmas_comidos[0]:
            alvo_gato2 = (fugir_x, fugir_y)
        elif not gato2_morto and fantasmas_comidos[0]:
            if 340 < gato2_x < 560 and 340 < gato2_y < 500:
                alvo_gato2 = (400, 100)
            else:
                alvo_gato2 = (jogador_x, jogador_y)
        else:
            alvo_gato2 = alvo_retorno
        if not gato3_morto and not fantasmas_comidos[1]:
            alvo_gato3 = (fugir_x, jogador_y)
        elif not gato3_morto and fantasmas_comidos[1]:
            if 340 < gato3_x < 560 and 340 < gato3_y < 500:
                alvo_gato3 = (400, 100)
            else:
                alvo_gato3 = (jogador_x, jogador_y)
        else:
            alvo_gato3 = alvo_retorno
        if not gato4_morto:
            alvo_gato4 = (jogador_x, fugir_y)
        elif not gato4_morto and fantasmas_comidos[2]:
            if 340 < gato4_x < 560 and 340 < gato4_y < 500:
                alvo_gato4 = (400, 100)
            else:
                alvo_gato4 = (jogador_x, jogador_y)
        else:
            alvo_gato4 = alvo_retorno
        if not gato1_morto and not fantasmas_comidos[3]:
            alvo_gato1 = (450, 450)
        elif not gato1_morto and fantasmas_comidos[3]:
            if 340 < gato1_x < 560 and 340 < gato1_y < 500:
                alvo_gato1 = (400, 100)
            else:
                alvo_gato1 = (jogador_x, jogador_y)
        else:
            alvo_gato1 = alvo_retorno
    else:
        if not gato2_morto:
            if 340 < gato2_x < 560 and 340 < gato2_y < 500:
                alvo_gato2 = (400, 100)
            else:
                alvo_gato2 = (jogador_x, jogador_y)
        else:
            alvo_gato2 = alvo_retorno
        if not gato3_morto:
            if 340 < gato3_x < 560 and 340 < gato3_y < 500:
                alvo_gato3 = (400, 100)
            else:
                alvo_gato3 = (jogador_x, jogador_y)
        else:
            alvo_gato3 = alvo_retorno
        if not gato4_morto:
            if 340 < gato4_x < 560 and 340 < gato4_y < 500:
                alvo_gato4 = (400, 100)
            else:
                alvo_gato4 = (jogador_x, jogador_y)
        else:
            alvo_gato4 = alvo_retorno
        if not gato1_morto:
            if 340 < gato1_x < 560 and 340 < gato1_y < 500:
                alvo_gato1 = (400, 100)
            else:
                alvo_gato1 = (jogador_x, jogador_y)
        else:
            alvo_gato1 = alvo_retorno
    return [alvo_gato2, alvo_gato3, alvo_gato4, alvo_gato1]

rodando = True

def menu_inicio():
    while True:
        tela.fill('black')
        fonte_menu = pygame.font.Font('freesansbold.ttf', 40)
        texto_jogar = fonte_menu.render("Jogar", True, 'white')
        texto_instrucoes = fonte_menu.render("Instruções", True, 'white')
        texto_sair = fonte_menu.render("Sair", True, 'white')

        pos_jogar = texto_jogar.get_rect(center=(LARGURA // 2, ALTURA // 3))
        pos_instrucoes = texto_instrucoes.get_rect(center=(LARGURA // 2, ALTURA // 2))
        pos_sair = texto_sair.get_rect(center=(LARGURA // 2, ALTURA * 2 // 3))

        tela.blit(texto_jogar, pos_jogar)
        tela.blit(texto_instrucoes, pos_instrucoes)
        tela.blit(texto_sair, pos_sair)

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if pos_jogar.collidepoint(evento.pos):
                    return  # Sai do menu e inicia o jogo
                elif pos_instrucoes.collidepoint(evento.pos):
                    menu_instrucoes()
                elif pos_sair.collidepoint(evento.pos):
                    pygame.quit()
                    exit()

def menu_instrucoes():
    while True:
        tela.fill('black')
        fonte_instrucoes = pygame.font.Font('freesansbold.ttf', 30)
        texto_instrucoes = fonte_instrucoes.render(
            "Objetivo: Comer todos os pontos sem ser pego pelos gatos!", True, 'white')
        texto_movimento = fonte_instrucoes.render(
            "Movimento: Use as setas para se mover.", True, 'white')
        texto_voltar = fonte_instrucoes.render("Voltar", True, 'white')

        pos_instrucoes = texto_instrucoes.get_rect(center=(LARGURA // 2, ALTURA // 3))
        pos_movimento = texto_movimento.get_rect(center=(LARGURA // 2, ALTURA // 2))
        pos_voltar = texto_voltar.get_rect(center=(LARGURA // 2, ALTURA * 2 // 3))

        tela.blit(texto_instrucoes, pos_instrucoes)
        tela.blit(texto_movimento, pos_movimento)
        tela.blit(texto_voltar, pos_voltar)

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if pos_voltar.collidepoint(evento.pos):
                    return  # Volta para o menu principal

# Início do programa
menu_inicio()

# Loop principal do jogo
while rodando:
    relogio.tick(fps)

    if contador < 19:
        contador += 1
        if contador > 3:
            piscar = False
    else:
        contador = 0
        piscar = True

    if powerup_ativo and contador_powerup < 600:
        contador_powerup += 1
    elif powerup_ativo and contador_powerup >= 600:
        contador_powerup = 0
        powerup_ativo = False
        fantasmas_comidos = [False, False, False, False]

    if contador_inicio < 180 and not jogo_encerrado and not jogo_vencido:
        em_movimento = False
        contador_inicio += 1
    else:
        em_movimento = True

    tela.fill('black')
    desenha_tabuleiro()
    centro_x = jogador_x + 23
    centro_y = jogador_y + 24

    if powerup_ativo:
        velocidades_gatos = [1, 1, 1, 1]
    else:
        velocidades_gatos = [2, 2, 2, 2]
    if fantasmas_comidos[0]:
        velocidades_gatos[0] = 2
    if fantasmas_comidos[1]:
        velocidades_gatos[1] = 2
    if fantasmas_comidos[2]:
        velocidades_gatos[2] = 2
    if fantasmas_comidos[3]:
        velocidades_gatos[3] = 2
    if gato2_morto:
        velocidades_gatos[0] = 4
    if gato3_morto:
        velocidades_gatos[1] = 4
    if gato4_morto:
        velocidades_gatos[2] = 4
    if gato1_morto:
        velocidades_gatos[3] = 4

    jogo_vencido = True
    for i in range(len(nivel)):
        if 1 in nivel[i] or 2 in nivel[i]:
            jogo_vencido = False

    circulo_jogador = pygame.draw.circle(tela, 'black', (centro_x, centro_y), 20, 2)
    desenha_jogador()

    gato2 = Fantasma(gato2_x, gato2_y, alvos[0], velocidades_gatos[0], fotos_gato2, direcao_gato2, gato2_morto, 
                 gato2_na_casa, 0)
    gato3 = Fantasma(gato3_x, gato3_y, alvos[1], velocidades_gatos[1], fotos_gato3, direcao_gato3, gato3_morto, 
                 gato3_na_casa, 1)
    gato4 = Fantasma(gato4_x, gato4_y, alvos[2], velocidades_gatos[2], fotos_gato4, direcao_gato4, gato4_morto, 
                 gato4_na_casa, 2)
    gato1 = Fantasma(gato1_x, gato1_y, alvos[3], velocidades_gatos[3], fotos_gato1, direcao_gato1, gato1_morto, 
                 gato1_na_casa, 3)

    desenha_variavel()
    alvos = obter_alvos(gato2_x, gato2_y, gato3_x, gato3_y, gato4_x, gato4_y, gato1_x, gato1_y)

    giros_permitidos = checa_posicao(centro_x, centro_y)
    if em_movimento:
        jogador_x, jogador_y = movimentacao(jogador_x, jogador_y)
        if not gato2_morto and not gato2.na_casa:
            gato2_x, gato2_y, direcao_gato2 = gato2.mover_gato2()
        else:
            gato2_x, gato2_y, direcao_gato2 = gato2.mover_gato1()
        if not gato4_morto and not gato4.na_casa:
            gato4_x, gato4_y, direcao_gato4 = gato4.mover_gato4()
        else:
            gato4_x, gato4_y, direcao_gato4 = gato4.mover_gato1()
        if not gato3_morto and not gato3.na_casa:
            gato3_x, gato3_y, direcao_gato3 = gato3.mover_gato3()
        else:
            gato3_x, gato3_y, direcao_gato3 = gato3.mover_gato1()
        gato1_x, gato1_y, direcao_gato1 = gato1.mover_gato1()

    pontuacao, powerup_ativo, contador_powerup, fantasmas_comidos = checa_colisao(pontuacao, powerup_ativo, contador_powerup, fantasmas_comidos)

    if not powerup_ativo:
        if (circulo_jogador.colliderect(gato2.retangulo) and not gato2.morto) or \
                (circulo_jogador.colliderect(gato3.retangulo) and not gato3.morto) or \
                (circulo_jogador.colliderect(gato4.retangulo) and not gato4.morto) or \
                (circulo_jogador.colliderect(gato1.retangulo) and not gato1.morto):
            if vidas > 0:
                vidas -= 1
                contador_inicio = 0
                powerup_ativo = False
                contador_powerup = 0
                jogador_x = 450
                jogador_y = 663
                direcao = 0
                comando_direcao = 0
                gato2_x = 56
                gato2_y = 58
                direcao_gato2 = 0
                gato3_x = 440
                gato3_y = 388
                direcao_gato3 = 2
                gato4_x = 440
                gato4_y = 438
                direcao_gato4 = 2
                gato1_x = 440
                gato1_y = 438
                direcao_gato1 = 2
                fantasmas_comidos = [False, False, False, False]
                gato2_morto = False
                gato3_morto = False
                gato1_morto = False
                gato4_morto = False
            else:
                jogo_encerrado = True
                em_movimento = False
                contador_inicio = 0
    if powerup_ativo and circulo_jogador.colliderect(gato2.retangulo) and fantasmas_comidos[0] and not gato2.morto:
        if vidas > 0:
            powerup_ativo = False
            contador_powerup = 0
            vidas -= 1
            contador_inicio = 0
            jogador_x = 450
            jogador_y = 663
            direcao = 0
            comando_direcao = 0
            gato2_x = 56
            gato2_y = 58
            direcao_gato2 = 0
            gato3_x = 440
            gato3_y = 388
            direcao_gato3 = 2
            gato4_x = 440
            gato4_y = 438
            direcao_gato4 = 2
            gato1_x = 440
            gato1_y = 438
            direcao_gato1 = 2
            fantasmas_comidos = [False, False, False, False]
            gato2_morto = False
            gato3_morto = False
            gato1_morto = False
            gato4_morto = False
        else:
            jogo_encerrado = True
            em_movimento = False
            contador_inicio = 0
    if powerup_ativo and circulo_jogador.colliderect(gato3.retangulo) and fantasmas_comidos[1] and not gato3.morto:
        if vidas > 0:
            powerup_ativo = False
            contador_powerup = 0
            vidas -= 1
            contador_inicio = 0
            jogador_x = 450
            jogador_y = 663
            direcao = 0
            comando_direcao = 0
            gato2_x = 56
            gato2_y = 58
            direcao_gato2 = 0
            gato3_x = 440
            gato3_y = 388
            direcao_gato3 = 2
            gato4_x = 440
            gato4_y = 438
            direcao_gato4 = 2
            gato1_x = 440
            gato1_y = 438
            direcao_gato1 = 2
            fantasmas_comidos = [False, False, False, False]
            gato2_morto = False
            gato3_morto = False
            gato1_morto = False
            gato4_morto = False
        else:
            jogo_encerrado = True
            em_movimento = False
            contador_inicio = 0
    if powerup_ativo and circulo_jogador.colliderect(gato4.retangulo) and fantasmas_comidos[2] and not gato4.morto:
        if vidas > 0:
            powerup_ativo = False
            contador_powerup = 0
            vidas -= 1
            contador_inicio = 0
            jogador_x = 450
            jogador_y = 663
            direcao = 0
            comando_direcao = 0
            gato2_x = 56
            gato2_y = 58
            direcao_gato2 = 0
            gato3_x = 440
            gato3_y = 388
            direcao_gato3 = 2
            gato4_x = 440
            gato4_y = 438
            direcao_gato4 = 2
            gato1_x = 440
            gato1_y = 438
            direcao_gato1 = 2
            fantasmas_comidos = [False, False, False, False]
            gato2_morto = False
            gato3_morto = False
            gato1_morto = False
            gato4_morto = False
        else:
            jogo_encerrado = True
            em_movimento = False
            contador_inicio = 0
    if powerup_ativo and circulo_jogador.colliderect(gato1.retangulo) and fantasmas_comidos[3] and not gato1.morto:
        if vidas > 0:
            powerup_ativo = False
            contador_powerup = 0
            vidas -= 1
            contador_inicio = 0
            jogador_x = 450
            jogador_y = 663
            direcao = 0
            comando_direcao = 0
            gato2_x = 56
            gato2_y = 58
            direcao_gato2 = 0
            gato3_x = 440
            gato3_y = 388
            direcao_gato3 = 2
            gato4_x = 440
            gato4_y = 438
            direcao_gato4 = 2
            gato1_x = 440
            gato1_y = 438
            direcao_gato1 = 2
            fantasmas_comidos = [False, False, False, False]
            gato2_morto = False
            gato3_morto = False
            gato1_morto = False
            gato4_morto = False
        else:
            jogo_encerrado = True
            em_movimento = False
            contador_inicio = 0
    if powerup_ativo and circulo_jogador.colliderect(gato2.retangulo) and not gato2.morto and not fantasmas_comidos[0]:
        gato2_morto = True
        fantasmas_comidos[0] = True
        pontuacao += (2 ** fantasmas_comidos.count(True)) * 100
    if powerup_ativo and circulo_jogador.colliderect(gato3.retangulo) and not gato3.morto and not fantasmas_comidos[1]:
        gato3_morto = True
        fantasmas_comidos[1] = True
        pontuacao += (2 ** fantasmas_comidos.count(True)) * 100
    if powerup_ativo and circulo_jogador.colliderect(gato4.retangulo) and not gato4.morto and not fantasmas_comidos[2]:
        gato4_morto = True
        fantasmas_comidos[2] = True
        pontuacao += (2 ** fantasmas_comidos.count(True)) * 100
    if powerup_ativo and circulo_jogador.colliderect(gato1.retangulo) and not gato1.morto and not fantasmas_comidos[3]:
        gato1_morto = True
        fantasmas_comidos[3] = True
        pontuacao += (2 ** fantasmas_comidos.count(True)) * 100

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RIGHT:
                comando_direcao = 0
            if evento.key == pygame.K_LEFT:
                comando_direcao = 1
            if evento.key == pygame.K_UP:
                comando_direcao = 2
            if evento.key == pygame.K_DOWN:
                comando_direcao = 3
            if evento.key == pygame.K_SPACE and (jogo_encerrado or jogo_vencido):
                powerup_ativo = False
                contador_powerup = 0
                vidas -= 1
                contador_inicio = 0
                jogador_x = 450
                jogador_y = 663
                direcao = 0
                comando_direcao = 0
                gato2_x = 56
                gato2_y = 58
                direcao_gato2 = 0
                gato3_x = 440
                gato3_y = 388
                direcao_gato3 = 2
                gato4_x = 440
                gato4_y = 438
                direcao_gato4 = 2
                gato1_x = 440
                gato1_y = 438
                direcao_gato1 = 2
                fantasmas_comidos = [False, False, False, False]
                gato2_morto = False
                gato3_morto = False
                gato1_morto = False
                gato4_morto = False
                pontuacao = 0
                vidas = 3
                nivel = copy.deepcopy(tabuleiros)
                jogo_encerrado = False
                jogo_vencido = False

        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_RIGHT and comando_direcao == 0:
                comando_direcao = direcao
            if evento.key == pygame.K_LEFT and comando_direcao == 1:
                comando_direcao = direcao
            if evento.key == pygame.K_UP and comando_direcao == 2:
                comando_direcao = direcao
            if evento.key == pygame.K_DOWN and comando_direcao == 3:
                comando_direcao = direcao

    if comando_direcao == 0 and giros_permitidos[0]:
        direcao = 0
    if comando_direcao == 1 and giros_permitidos[1]:
        direcao = 1
    if comando_direcao == 2 and giros_permitidos[2]:
        direcao = 2
    if comando_direcao == 3 and giros_permitidos[3]:
        direcao = 3

    if jogador_x > 900:
        jogador_x = -47
    elif jogador_x < -50:
        jogador_x = 897

    if gato2.in_box and blinky_dead:
        blinky_dead = False
    if gato3.in_box and inky_dead:
        inky_dead = False
    if gato4.in_box and pinky_dead:
        pinky_dead = False
    if gato1.in_box and clyde_dead:
        clyde_dead = False

    pygame.display.flip()
pygame.quit()
