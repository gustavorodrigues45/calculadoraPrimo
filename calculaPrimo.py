import pygame
import sys
import os

# Inicializando o Pygame
pygame.init()

# Configurações da janela
largura, altura = 800, 400

# Centraliza a janela na tela
os.environ['SDL_VIDEO_CENTERED'] = '1'
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Calculadora de Número Primo")

# Cores e fontes
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
fonte = pygame.font.Font(None, 32)

# Função para verificar se um número é primo
def eh_primo(numero):
    if numero <= 1:
        return False
    for i in range(2, int(numero**0.5) + 1):
        if numero % i == 0:
            return False
    return True

# Função para desenhar botões com gradiente e bordas arredondadas
def desenhar_botao_gradiente(superficie, ret, cor1, cor2, texto, fonte, cor_texto):
    for i in range(ret.height):
        cor_intermediaria = (
            cor1[0] + (cor2[0] - cor1[0]) * i // ret.height,
            cor1[1] + (cor2[1] - cor1[1]) * i // ret.height,
            cor1[2] + (cor2[2] - cor1[2]) * i // ret.height,
        )
        pygame.draw.rect(superficie, cor_intermediaria, (ret.x, ret.y + i, ret.width, 1))
    
    pygame.draw.rect(superficie, cor1, ret, border_radius=10)
    pygame.draw.rect(superficie, cor2, ret.inflate(-6, -6), border_radius=8)
    
    texto_surface = fonte.render(texto, True, cor_texto)
    texto_rect = texto_surface.get_rect(center=ret.center)
    superficie.blit(texto_surface, texto_rect)

class TelaMenu:
    def __init__(self):
        self.iniciar_botao = pygame.Rect((largura - 150) // 2, 100, 150, 50)
        self.oque_sao_primos_botao = pygame.Rect((largura - 295) // 2, 180, 295, 50)
        self.tabela_primos_botao = pygame.Rect((largura - 295) // 2, 260, 295, 50)
    
    def desenhar(self):
        tela.fill(BRANCO)
        titulo = fonte.render("Bem-vindo à Calculadora de Números Primos", True, PRETO)
        titulo_rect = titulo.get_rect(center=(largura // 2, 50))
        tela.blit(titulo, titulo_rect)
        
        desenhar_botao_gradiente(
            tela, self.iniciar_botao, 
            (255, 100, 100), (200, 0, 0), 
            "Iniciar", fonte, BRANCO
        )
        
        desenhar_botao_gradiente(
            tela, self.oque_sao_primos_botao, 
            (100, 100, 255), (0, 0, 200), 
            "O que são números primos?", fonte, BRANCO
        )
        
        desenhar_botao_gradiente(
            tela, self.tabela_primos_botao, 
            (100, 255, 100), (0, 200, 0), 
            "Tabela de Primos", fonte, BRANCO
        )
    
    def lidar_eventos(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.iniciar_botao.collidepoint(evento.pos):
                return "calculadora"
            elif self.oque_sao_primos_botao.collidepoint(evento.pos):
                return "explicacao"
            elif self.tabela_primos_botao.collidepoint(evento.pos):
                return "tabela_primos"
        return "menu"

class TelaCalculadora:
    def __init__(self):
        self.input_box = pygame.Rect((largura - 200) // 2, 150, 140, 32)
        self.cor_ativo = VERMELHO
        self.cor_inativo = PRETO
        self.cor_caixa = self.cor_inativo
        self.texto_input = ''
        self.mostrar_resultado = False
        self.resultado = ''

    def desenhar(self):
        tela.fill(BRANCO)
        instrucao = fonte.render("Insira um número para verificar se é primo", True, PRETO)
        instrucao_rect = instrucao.get_rect(center=(largura // 2, 50))
        tela.blit(instrucao, instrucao_rect)
        
        txt_surface = fonte.render(self.texto_input, True, PRETO)
        largura_txt = max(200, txt_surface.get_width() + 10)
        self.input_box.w = largura_txt
        tela.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))
        pygame.draw.rect(tela, self.cor_caixa, self.input_box, 2)
        
        if self.mostrar_resultado:
            resultado_surface = fonte.render(self.resultado, True, PRETO)
            resultado_rect = resultado_surface.get_rect(center=(largura // 2, 250))
            tela.blit(resultado_surface, resultado_rect)

    def lidar_eventos(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.input_box.collidepoint(evento.pos):
                self.cor_caixa = self.cor_ativo
            else:
                self.cor_caixa = self.cor_inativo
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                return "menu"
            if self.cor_caixa == self.cor_ativo:
                if evento.key == pygame.K_RETURN:
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

class TelaExplicacao:
    def desenhar(self):
        tela.fill(BRANCO)
        titulo = fonte.render("O que são números primos?", True, PRETO)
        titulo_rect = titulo.get_rect(center=(largura // 2, 50))
        tela.blit(titulo, titulo_rect)
        explicacao = fonte.render(
            "São números naturais > 1 divisíveis apenas por 1 e por si mesmos.", True, PRETO
        )
        explicacao_rect = explicacao.get_rect(center=(largura // 2, 150))
        tela.blit(explicacao, explicacao_rect)
        voltar_texto = fonte.render("Pressione ESC para voltar ao menu.", True, PRETO)
        voltar_rect = voltar_texto.get_rect(center=(largura // 2, 300))
        tela.blit(voltar_texto, voltar_rect)
    
    def lidar_eventos(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                return "menu"
        return "explicacao"

class TelaTabelaPrimos:
    def __init__(self):
        self.imagem = pygame.image.load("tabela_primos.png")
        self.imagem = pygame.transform.scale(self.imagem, (600, 300))
    
    def desenhar(self):
        tela.fill(BRANCO)
        imagem_rect = self.imagem.get_rect(center=(largura // 2, altura // 2))
        tela.blit(self.imagem, imagem_rect)
        voltar_texto = fonte.render("Pressione ESC para voltar ao menu.", True, PRETO)
        voltar_rect = voltar_texto.get_rect(center=(largura // 2, altura - 30))
        tela.blit(voltar_texto, voltar_rect)
    
    def lidar_eventos(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                return "menu"
        return "tabela_primos"

class Aplicacao:
    def __init__(self):
        self.tela_atual = "menu"
        self.menu = TelaMenu()
        self.calculadora = TelaCalculadora()
        self.explicacao = TelaExplicacao()
        self.tabela_primos = TelaTabelaPrimos()
    
    def executar(self):
        executando = True
        while executando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    executando = False
                
                if self.tela_atual == "menu":
                    self.tela_atual = self.menu.lidar_eventos(evento)
                elif self.tela_atual == "calculadora":
                    self.tela_atual = self.calculadora.lidar_eventos(evento)
                elif self.tela_atual == "explicacao":
                    self.tela_atual = self.explicacao.lidar_eventos(evento)
                elif self.tela_atual == "tabela_primos":
                    self.tela_atual = self.tabela_primos.lidar_eventos(evento)

            if self.tela_atual == "menu":
                self.menu.desenhar()
            elif self.tela_atual == "calculadora":
                self.calculadora.desenhar()
            elif self.tela_atual == "explicacao":
                self.explicacao.desenhar()
            elif self.tela_atual == "tabela_primos":
                self.tabela_primos.desenhar()

            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

app = Aplicacao()
app.executar()
