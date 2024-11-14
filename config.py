import pygame
import math

# Inicialização do Pygame
pygame.init()

# Configurações globais do jogo
LARGURA = 900
ALTURA = 800
tela = pygame.display.set_mode((LARGURA, ALTURA))
temporizador = pygame.time.Clock()
fps = 60
fonte = pygame.font.Font('freesansbold.ttf', 40)
COR_TEXTO = (255, 255, 0)
COR_DESTAQUE = (100, 100, 255)
COR = 'blue'
PI = math.pi
