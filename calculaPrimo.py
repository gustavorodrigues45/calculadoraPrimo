import pygame
import sys

# Inicializando o Pygame
pygame.init()

# Configurações da janela
largura, altura = 600, 400
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Calculadora de Número Primo")

# Cores e fontes
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
fonte = pygame.font.Font(None, 32)

# Função para verificar se um número é primo
def eh_primo(numero):
    if numero <= 1:
        return False
    for i in range(2, int(numero**0.5) + 1):
        if numero % i == 0:
            return False
    return True

# Variáveis do menu
input_box = pygame.Rect(200, 150, 140, 32)
cor_ativo = VERMELHO
cor_inativo = PRETO
cor_caixa = cor_inativo
texto_input = ''
mostrar_resultado = False
resultado = ''

# Loop principal
executando = True
while executando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            # Checa se o usuário clicou dentro da caixa de input
            if input_box.collidepoint(evento.pos):
                cor_caixa = cor_ativo
            else:
                cor_caixa = cor_inativo
        elif evento.type == pygame.KEYDOWN:
            if cor_caixa == cor_ativo:
                if evento.key == pygame.K_RETURN or evento.key == pygame.K_KP_ENTER:
                    # Verifica se o número é primo quando o usuário pressiona Enter
                    try:
                        numero = int(texto_input)
                        if eh_primo(numero):
                            resultado = f"O número {numero} é primo."
                        else:
                            resultado = f"O número {numero} não é primo."
                    except ValueError:
                        resultado = "Digite um número válido."
                    mostrar_resultado = True
                    texto_input = ''
                elif evento.key == pygame.K_BACKSPACE:
                    texto_input = texto_input[:-1]
                else:
                    texto_input += evento.unicode

    # Limpa a tela
    tela.fill(BRANCO)

    # Renderiza o texto da caixa de input
    txt_surface = fonte.render(texto_input, True, PRETO)
    largura_txt = max(200, txt_surface.get_width()+10)
    input_box.w = largura_txt
    tela.blit(txt_surface, (input_box.x+5, input_box.y+5))
    pygame.draw.rect(tela, cor_caixa, input_box, 2)

    # Renderiza o resultado, se necessário
    if mostrar_resultado:
        resultado_surface = fonte.render(resultado, True, PRETO)
        tela.blit(resultado_surface, (200, 250))

    # Atualiza a tela
    pygame.display.flip()

# Encerra o Pygame
pygame.quit()
sys.exit()
