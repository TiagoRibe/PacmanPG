import pygame
import math
from tabuleiro import tabuleiros
from config import *

COR = 'blue'
PI = math.pi

fotos_rato= []
for i in range(1, 5):
    fotos_rato.append(pygame.transform.scale(pygame.image.load(f'Imagens/Fotos_rato/{i}.png'),(45,45)))
direcao= 0
jogador_x = 430
jogador_y = 540
cont= 0 #contador
pisca= False

def desenha_jogador():
    if direcao == 0:
        tela.blit(fotos_rato[cont // 5], (jogador_x, jogador_y))
    elif direcao == 1:
        tela.blit(pygame.transform.flip(fotos_rato[cont // 5], True, False), (jogador_x, jogador_y))
    elif direcao == 2:
        tela.blit(pygame.transform.rotate(fotos_rato[cont // 5], 90), (jogador_x, jogador_y))
    elif direcao == 3:
        tela.blit(pygame.transform.rotate(fotos_rato[cont // 5], 270), (jogador_x, jogador_y))

def exibir_texto(texto, fonte, cor, posicao):
    texto_superficie = fonte.render(texto, True, cor)
    texto_retangulo = texto_superficie.get_rect(center=posicao)
    tela.blit(texto_superficie, texto_retangulo)
    return texto_retangulo  # Retorna o retângulo para detecção de clique

def desenha_tabuleiro():
    num1 = ((ALTURA - 50) // 32)
    num2 = (LARGURA // 30)
    for i in range(len(level)):
        for j in range(len(level[i])):
            pos_x = j * num2 + (0.5 * num2)
            pos_y = i * num1 + (0.5 * num1)
            if level[i][j] == 1:
                pygame.draw.circle(tela, 'white', (pos_x, pos_y), 4)
            elif level[i][j] == 2 and not pisca:
                pygame.draw.circle(tela, 'white', (pos_x, pos_y), 10)
            elif level[i][j] == 3:
                pygame.draw.line(tela, COR, (pos_x, i * num1), (pos_x, i * num1 + num1), 3)
            elif level[i][j] == 4:
                pygame.draw.line(tela, COR, (j * num2, pos_y), (j * num2 + num2, pos_y), 3)
            elif level[i][j] == 5:
                pygame.draw.arc(tela, COR, [(j * num2 - (num2 * 0.4)) - 2, pos_y, num2, num1], 0, PI / 2, 3)
            elif level[i][j] == 6:
                pygame.draw.arc(tela, COR, [(j * num2 + (num2 * 0.5)), pos_y, num2, num1], PI / 2, PI, 3)
            elif level[i][j] == 7:
                pygame.draw.arc(tela, COR, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], PI, 3 * PI / 2, 3)
            elif level[i][j] == 8:
                pygame.draw.arc(tela, COR, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * PI / 2, 2 * PI, 3)
            elif level[i][j] == 9:
                pygame.draw.line(tela, 'white', (j * num2, pos_y), (j * num2 + num2, pos_y), 3)


#funcao que checa a posição
def posicao(centerx, centery):
    virar = [False, False, False, False]
    num1 = (ALTURA - 50) // 32
    num2 = (LARGURA // 30)
    num3 = 15

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
    if direcao == 0 and pode_virar[0]:
        eixo_x += velocidade_jogador
    elif direcao == 1 and pode_virar[1]:
        eixo_x -= velocidade_jogador
    if direcao == 2 and pode_virar[2]:
        eixo_y -= velocidade_jogador
    elif direcao == 3 and pode_virar[3]:
        eixo_y += velocidade_jogador
    return eixo_x, eixo_y
