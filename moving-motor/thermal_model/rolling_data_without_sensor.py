import sys
sys.path.append('../')  # Adiciona o diretório pai (pasta_principal) ao PATH
from odri_spi_ftdi import SPIuDriver
from MAX31855 import SPIuDriver_Temp
import matplotlib.pyplot as plt
import numpy as np
import time
import pygame


### Dados do motor ### 
dt = 0.001
ud = SPIuDriver(absolutePositionMode=False, waitForInit=True)
ud.transfer()
t = time.perf_counter()
i=0


ids, iqs = [],[]
vds, vqs = [], []
times = []
temps_measured = []
velocitys = []
positions = []

init_time = 0

I=0

now = 0
iq = 0
vq = 0
init_time = time.time()
count = 0



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
            elif event.key == pygame.K_e:  # Pressionar a tecla "s" para finalizar
                count += 1
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Botão esquerdo do mouse
                temperature += 0.1
            elif event.button == 3:  # Botão direito do mouse
                temperature -= 0.1
        elif event.type == pygame.TEXTINPUT:
            if temperature is None:
                input_text += event.text



    ### Motor ###
    now = time.time()
    # print(now - init_time, 'James',loop_run )
    if now - init_time > 1:

        time_measured = now - init_time
        capture_velocity    = ud.velocity1
        capture_position    = ud.position1

        if count == 0:
            I = 2
        else:
            I = 0

        # set current format 
        ud.refCurrent1 = I # Iq
        # print("Temperature:",round(temperature, 1), "Time: ", round(now - init_time), "temp_5s: ", temp_5s )
        ud.transfer() # transfer
        # get data
        iq = ud.current1
        id = ud.current0
        vd = ud.adcSamples1
        vq = ud.resistance1

        if(temperature != None):
            # store data on the lists
            times.append(round(time_measured, 4))
            temps_measured.append(round(temperature, 1))
            ids.append(round(id, 3))
            iqs.append(round(iq, 3))
            vds.append(round(vd, 4))
            vqs.append(round(vq, 4))
            velocitys.append(round(capture_velocity, 3))
            positions.append(round(capture_position, 2))

    else:
        ud.transfer() # transfer
        
    if temperature is None:
        render_text("Insira a temperatura ambiente e pressione Enter:", WIDTH // 2, HEIGHT // 2 - 50)
        render_text(input_text, WIDTH // 2, HEIGHT // 2)
    else:
        render_text(f"Temperatura Motor: {temperature:.1f} °C", WIDTH // 2, HEIGHT // 2)
        render_text(f"Time: {(now - init_time):.1f} s", WIDTH // 2, (HEIGHT // 2)+30)
        render_text(f"Current: {(id):.1f} A", WIDTH // 2, (HEIGHT // 2)-30)
        render_text(f"Current: {(iq):.1f} A", WIDTH // 2, (HEIGHT // 2)-60)

    pygame.display.flip()
    #wait for next control cycle
    t +=dt
    while(time.perf_counter()-t<dt):
        pass

ud.stop() # Terminate

# Save data in file
f = open("rolling_data_2A.txt", "w")
f.write("Time, Id, Iq, Ud, Uq, Velocity, Temperature, Position\n")

for i in range(len(times)):
    f.write(str(times[i]) + ", " 
            + str(ids[i]) + ", " 
            + str(iqs[i]) + ", "
            + str(vds[i]) + ", " 
            + str(vqs[i]) + ", " 
            + str(velocitys[i]) + ", " 
            + str(temps_measured[i]) + ", " 
            + str(positions[i])
            + "\n")
f.close()

# gravar
# tempo, id, ud, temperatura medida
    
# Encerramento
pygame.quit()
sys.exit()