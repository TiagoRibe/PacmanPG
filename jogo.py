import pygame
pygame.init()
import sys
from tabuleiro import tabuleiros
from funcoes import *
from config import *

rodando = True
while rodando:
    temporizador.tick(fps)
    if cont < 19:
        cont += 1 
        if cont > 3:
            pisca= False
    else:
        cont = 0

    tela.fill('black')
    desenha_jogador ()
    desenha_tabuleiro ()


    # Verifica eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando= False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RIGHT:
                direcao = 0
            if evento.key == pygame.K_LEFT:
                direcao = 1
            if evento.key == pygame.K_UP:
                direcao = 2
            if evento.key == pygame.K_DOWN:
                direcao = 3

    pygame.display.flip()

pygame.quit()
