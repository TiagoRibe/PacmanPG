import pygame
import math
import copy
from tabuleiro import *

# Inicialização do Pygame
pygame.init()

# Configurações globais do jogo
LARGURA = 900
ALTURA = 800
tela = pygame.display.set_mode((LARGURA, ALTURA))
temporizador = pygame.time.Clock()
fps = 60
nivel = copy.deepcopy(tabuleiros)
fonte = pygame.font.Font('freesansbold.ttf', 40)
level= tabuleiros
COR_TEXTO = (255, 255, 0)
COR_DESTAQUE = (100, 100, 255)
COR = 'blue'
PI = math.pi



#Configurações de teste + funcionalidades/mecânicas
score = 0
pode_virar = [False, False, False, False]
velocidade_jogador = 2