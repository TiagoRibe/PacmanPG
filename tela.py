import pygame
pygame.init()
import sys
from tabuleiro import tabuleiros
from funcoes import *
from config import *

rodando = True
while rodando:
    temporizador.tick(fps)
    tela.fill('black')

    # Exibe opções de jogo
    jogar_retangulo = exibir_texto("Jogar", fonte, COR_TEXTO, (450, 400), tela)
    sair_retangulo = exibir_texto("Sair", fonte, COR_TEXTO, (450, 500), tela)

    # Verifica eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if jogar_retangulo.collidepoint(evento.pos):
                desenha_tabuleiro(tela, tabuleiros)  # Passa a tela como parâmetro
                print("Jogo Iniciado")
                rodando = False
            elif sair_retangulo.collidepoint(evento.pos):
                pygame.quit()
                sys.exit()

    pygame.display.flip()

pygame.quit()
