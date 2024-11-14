import pygame
import math
from tabuleiro import tabuleiros

COR = 'blue'
PI = math.pi

def desenha_jogador(tela, fotos_gato, jogador_x, jogador_y, direcao, cont):
    if direcao == 0:
        tela.blit(fotos_gato[cont // 5], (jogador_x, jogador_y))
    elif direcao == 1:
        tela.blit(pygame.transform.flip(fotos_gato[cont // 5], True, False), (jogador_x, jogador_y))
    elif direcao == 2:
        tela.blit(pygame.transform.rotate(fotos_gato[cont // 5], 90), (jogador_x, jogador_y))
    elif direcao == 3:
        tela.blit(pygame.transform.rotate(fotos_gato[cont // 5], 270), (jogador_x, jogador_y))

def exibir_texto(texto, fonte, cor, posicao, tela):
    texto_superficie = fonte.render(texto, True, cor)
    texto_retangulo = texto_superficie.get_rect(center=posicao)
    tela.blit(texto_superficie, texto_retangulo)
    return texto_retangulo  # Retorna o retângulo para detecção de clique

def desenha_tabuleiro(tela, level, largura=900, altura=800, cor=COR):
    num1 = ((altura - 50) // 32)
    num2 = (largura // 30)
    for i in range(len(level)):
        for j in range(len(level[i])):
            pos_x = j * num2 + (0.5 * num2)
            pos_y = i * num1 + (0.5 * num1)
            if level[i][j] == 1:
                pygame.draw.circle(tela, 'white', (pos_x, pos_y), 4)
            elif level[i][j] == 2:
                pygame.draw.circle(tela, 'white', (pos_x, pos_y), 10)
            elif level[i][j] == 3:
                pygame.draw.line(tela, cor, (pos_x, i * num1), (pos_x, i * num1 + num1), 3)
            elif level[i][j] == 4:
                pygame.draw.line(tela, cor, (j * num2, pos_y), (j * num2 + num2, pos_y), 3)
            elif level[i][j] == 5:
                pygame.draw.arc(tela, cor, [(j * num2 - (num2 * 0.4)) - 2, pos_y, num2, num1], 0, PI / 2, 3)
            elif level[i][j] == 6:
                pygame.draw.arc(tela, cor, [(j * num2 + (num2 * 0.5)), pos_y, num2, num1], PI / 2, PI, 3)
            elif level[i][j] == 7:
                pygame.draw.arc(tela, cor, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], PI, 3 * PI / 2, 3)
            elif level[i][j] == 8:
                pygame.draw.arc(tela, cor, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * PI / 2, 2 * PI, 3)
            elif level[i][j] == 9:
                pygame.draw.line(tela, 'white', (j * num2, pos_y), (j * num2 + num2, pos_y), 3)
