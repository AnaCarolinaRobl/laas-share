import pygame
import sys

# Inicialização do Pygame
pygame.init()

# Configurações da janela
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulação de Temperatura")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_COLOR = BLACK

# Fonte
font = pygame.font.Font(None, 36)

# Variáveis de temperatura
temperature = None
input_text = ""

# Função para renderizar o texto na tela
def render_text(text, x, y):
    text_surface = font.render(text, True, FONT_COLOR)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

# Estado da simulação
simulating = True

# Loop principal
while simulating:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            simulating = False
        elif event.type == pygame.KEYDOWN:
            if temperature is None:
                if event.key == pygame.K_RETURN:
                    try:
                        temperature = float(input_text)
                        input_text = ""
                    except ValueError:
                        pass
            elif event.key == pygame.K_s:  # Pressionar a tecla "s" para finalizar
                simulating = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Botão esquerdo do mouse
                temperature += 0.1
            elif event.button == 3:  # Botão direito do mouse
                temperature -= 0.1
        elif event.type == pygame.TEXTINPUT:
            if temperature is None:
                input_text += event.text

    if temperature is None:
        render_text("Insira a temperatura ambiente e pressione Enter:", WIDTH // 2, HEIGHT // 2 - 50)
        render_text(input_text, WIDTH // 2, HEIGHT // 2)
    else:
        render_text(f"Temperatura Motor: {temperature:.1f} °C", WIDTH // 2, HEIGHT // 2)

    pygame.display.flip()

# Encerramento
pygame.quit()
sys.exit()
