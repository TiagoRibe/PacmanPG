import pygame
import math
from tabuleiro import tabuleiros


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

fotos_gato= []
for i in range(1, 5):
    fotos_gato.append(pygame.transform.scale(pygame.image.load(f'imagens/Fotos_rato/{i}.png'),(45,45)))
direcao= 0
jogador_x = 450
jogador_y = 660
cont= 0 #contador

def desenha_jogador():
    if direcao == 0:
        tela.blit(fotos_gato[cont // 5], (jogador_x, jogador_y))
    elif direcao == 1:
        tela.blit(pygame.transform.flip(fotos_gato[cont // 5], True, False), (jogador_x, jogador_y))
    elif direcao == 2:
        tela.blit(pygame.transform.rotate(fotos_gato[cont // 5], 90), (jogador_x, jogador_y))
    elif direcao == 3:
        tela.blit(pygame.transform.rotate(fotos_gato[cont // 5], 270), (jogador_x, jogador_y))

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
            if level[i][j] == 1:
                pygame.draw.circle(tela, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
            if level[i][j] == 2 and not False:
                pygame.draw.circle(tela, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
            if level[i][j] == 3:
                pygame.draw.line(tela, COR, (j * num2 + (0.5 * num2), i * num1), (j * num2 + (0.5 * num2), i * num1 + num1), 3)
            if level[i][j] == 4:
                pygame.draw.line(tela, COR, (j * num2, i * num1 + (0.5 * num1)), (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
            if level[i][j] == 5:
                pygame.draw.arc(tela, COR, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1], 0, PI / 2, 3)
            if level[i][j] == 6:
                pygame.draw.arc(tela, COR, [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], PI / 2, PI, 3)
            if level[i][j] == 7:
                pygame.draw.arc(tela, COR, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], PI, 3 * PI / 2, 3)
            if level[i][j] == 8:
                pygame.draw.arc(tela, COR, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * PI / 2, 2 * PI, 3)
            if level[i][j] == 9:
                pygame.draw.line(tela, 'white', (j * num2, i * num1 + (0.5 * num1)), (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
