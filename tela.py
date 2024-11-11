import pygame
import sys
from tabuleiro import tabuleiros

# Inicialização do Pygame
pygame.init()

# configurando a tela inicial e cores
LARGURA = 900
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
temporizador= pygame.time.Clock()
fps= 60
pygame.display.set_caption("Rato e Gatos - Menu")
fonte = pygame.font.Font('freesansbold.ttf', 40)
level= tabuleiros

COR_FUNDO = (2, 13, 63)
COR_TEXTO = (255, 255, 0)
COR_DESTAQUE = (100, 100, 255)


# primeira função para exibir o texto na tela
def exibir_texto(texto, fonte, cor, posicao):
    texto_superficie = fonte.render(texto, True, cor)
    texto_retangulo = texto_superficie.get_rect(center=posicao)
    tela.blit(texto_superficie, texto_retangulo)
    return texto_retangulo  # Retorna o retângulo para detecção de clique
# loop principal para inicializar pygame
rodando = True
while rodando:
    temporizador.tick(fps)
    
    tela.fill(COR_FUNDO)
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
