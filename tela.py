import pygame
import sys
from tabuleiro import tabuleiros
from funcoes import *
import math

# Inicialização do Pygame
pygame.init()

# configurando a tela inicial e cores
LARGURA = 900
ALTURA = 800
tela = pygame.display.set_mode((LARGURA, ALTURA))
temporizador= pygame.time.Clock()
fps= 60
pygame.display.set_caption("Rato e Gatos - Menu")
fonte = pygame.font.Font('freesansbold.ttf', 40)
level= tabuleiros
COR= 'blue'
PI= math.pi
COR_TEXTO = (255, 255, 0)
COR_DESTAQUE = (100, 100, 255)

# loop principal para inicializar pygame
rodando = True
while rodando:
    temporizador.tick(fps)
    tela.fill('black')
    #desenha_tabuleiro() 

    jogar_retangulo = exibir_texto("Jogar", fonte, COR_TEXTO, (LARGURA // 2, ALTURA // 2 - 50))
    sair_retangulo = exibir_texto("Sair", fonte, COR_TEXTO, (LARGURA // 2, ALTURA // 2 + 50))
    
    #for de saída
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if jogar_retangulo.collidepoint(evento.pos):
                print("Jogo Iniciado")  # Aqui você pode chamar a função do jogo principal
                rodando = False  # Sai do loop da tela de início para iniciar o jogo
            elif sair_retangulo.collidepoint(evento.pos):
                pygame.quit()
                sys.exit()
    pygame.display.flip()

pygame.quit()
