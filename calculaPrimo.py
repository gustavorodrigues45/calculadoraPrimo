import pygame
import sys

# Inicializando o Pygame
pygame.init()

# Configurações da janela
largura, altura = 650, 400
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

class TelaMenu:
    def __init__(self):
        self.iniciar_botao = pygame.Rect(250, 200, 100, 50)
    
    def desenhar(self):
        tela.fill(BRANCO)
        titulo = fonte.render("Bem-vindo à Calculadora de Números Primos", True, PRETO)
        tela.blit(titulo, (100, 100))
        
        # Desenha o botão "Iniciar"
        pygame.draw.rect(tela, VERMELHO, self.iniciar_botao)
        iniciar_texto = fonte.render("Iniciar", True, BRANCO)
        tela.blit(iniciar_texto, (self.iniciar_botao.x + 15, self.iniciar_botao.y + 10))
    
    def lidar_eventos(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            # Verifica se o usuário clicou no botão "Iniciar"
            if self.iniciar_botao.collidepoint(evento.pos):
                return "calculadora"  # Muda para a tela da calculadora
        return "menu"

class TelaCalculadora:
    def __init__(self):
        self.input_box = pygame.Rect(200, 150, 140, 32)
        self.cor_ativo = VERMELHO
        self.cor_inativo = PRETO
        self.cor_caixa = self.cor_inativo
        self.texto_input = ''
        self.mostrar_resultado = False
        self.resultado = ''

    def desenhar(self):
        tela.fill(BRANCO)
        
        # Exibe a instrução para o usuário
        instrucao = fonte.render("Insira algum número para verificar se são primos", True, PRETO)
        tela.blit(instrucao, (100, 50))
        
        # Renderiza o texto da caixa de input
        txt_surface = fonte.render(self.texto_input, True, PRETO)
        largura_txt = max(200, txt_surface.get_width() + 10)
        self.input_box.w = largura_txt
        tela.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))
        pygame.draw.rect(tela, self.cor_caixa, self.input_box, 2)
        
        # Renderiza o resultado, se necessário
        if self.mostrar_resultado:
            resultado_surface = fonte.render(self.resultado, True, PRETO)
            tela.blit(resultado_surface, (200, 250))

    def lidar_eventos(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            # Checa se o usuário clicou dentro da caixa de input
            if self.input_box.collidepoint(evento.pos):
                self.cor_caixa = self.cor_ativo
            else:
                self.cor_caixa = self.cor_inativo
        elif evento.type == pygame.KEYDOWN:
            # Verifica se a tecla "Esc" foi pressionada para retornar ao menu
            if evento.key == pygame.K_ESCAPE:
                return "menu"
            if self.cor_caixa == self.cor_ativo:
                if evento.key == pygame.K_RETURN or evento.key == pygame.K_KP_ENTER:
                    # Verifica se o número é primo quando o usuário pressiona Enter
                    try:
                        numero = int(self.texto_input)
                        if eh_primo(numero):
                            self.resultado = f"O número {numero} é primo."
                        else:
                            self.resultado = f"O número {numero} não é primo."
                    except ValueError:
                        self.resultado = "Digite um número válido."
                    self.mostrar_resultado = True
                    self.texto_input = ''
                elif evento.key == pygame.K_BACKSPACE:
                    self.texto_input = self.texto_input[:-1]
                else:
                    self.texto_input += evento.unicode
        return "calculadora"

class Aplicacao:
    def __init__(self):
        self.tela_atual = "menu"
        self.menu = TelaMenu()
        self.calculadora = TelaCalculadora()
    
    def executar(self):
        executando = True
        while executando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    executando = False
                
                # Lidar com eventos dependendo da tela atual
                if self.tela_atual == "menu":
                    self.tela_atual = self.menu.lidar_eventos(evento)
                elif self.tela_atual == "calculadora":
                    self.tela_atual = self.calculadora.lidar_eventos(evento)

            # Desenhar a tela atual
            if self.tela_atual == "menu":
                self.menu.desenhar()
            elif self.tela_atual == "calculadora":
                self.calculadora.desenhar()

            # Atualiza a tela
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

# Inicializa e executa a aplicação
app = Aplicacao()
app.executar()
