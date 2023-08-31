import sys
sys.path.append('../')  # Adiciona o diretório pai (pasta_principal) ao PATH
from odri_spi_ftdi import SPIuDriver
from MAX31855 import SPIuDriver_Temp
import matplotlib.pyplot as plt
import numpy as np
import time
import pygame
import random


### Dados do motor ### 
dt = 0.001
ud = SPIuDriver(absolutePositionMode=False, waitForInit=True)
st = SPIuDriver_Temp()
ud.transfer()
N=30000 #30 seconds
t = time.perf_counter()
i=0
w = 25 # rad/s


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
kd= 0 # 10**(-4)*2
kp=2/9
ki = 0
int_error = 0
error=0
temp_measured = 0
init_time = time.time()
time_sin = time.time()
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
            if event.key == pygame.K_s:  # Pressionar a tecla "s" para finalizar
                simulating = False
            elif event.key == pygame.K_e:
                count += 1


    ### Motor ###
    now = time.time()
    # print(now - init_time, 'James',loop_run )
    if now - init_time > 1:

        ##PID
        time_measured = now - init_time
        ref = 1 # np.sin(w*time_measured)*2*np.pi #valor a enviar para a velocidade
        derivate_ref        = 0 # w*np.cos(w*time_measured)
        capture_velocity    = ud.velocity1
        capture_position    = ud.position1

        error = ref-capture_position
        int_error += error*dt
        
        ##Sinus
        if(now-time_sin>=5):
            r = random.random()
            r2=(r/2)+0.5
            time_sin = time.time()

        if(count==0):
            kp=3/28
            I = (error*kp) #+ ((derivate_ref-capture_velocity)*kd) #4+ int_error*ki
        elif(count==1):
            I = 2*r*np.sin(r2*w*time_measured)
        elif(count==2):
            kp=0.5/28
            I = (error*kp)
        else:
            I=0

        # set current format 
        ud.refCurrent1 = I # Iq
        # print("I=",round(I,2), "Iq=",round(iq,2),"Temperature:",round(temp_measured, 1), "Time: ", round(now - init_time), "Error: ", ud.error )
        ud.transfer() # transfer
        # get data
        temp_measured = st.read()
        iq = ud.current1
        id = ud.current0
        vd = ud.adcSamples1
        vq = ud.resistance1

        # store data on the lists
        times.append(round(time_measured, 4))
        temps_measured.append(round(temp_measured, 1))
        ids.append(round(id, 3))
        iqs.append(round(iq, 3))
        vds.append(round(vd, 4))
        vqs.append(round(vq, 4))
        velocitys.append(round(capture_velocity, 3))
        positions.append(round(capture_position, 2))

    else:
        ud.transfer() # transfer
        
    render_text(f"Temperatura Motor: {temp_measured:.1f} °C", WIDTH // 2, HEIGHT // 2)
    render_text(f"Time: {(now - init_time):.1f} s", WIDTH // 2, (HEIGHT // 2)+30)
    render_text(f"Iq: {(iq):.1f} A", WIDTH // 2, (HEIGHT // 2)-30)

    pygame.display.flip()
    #wait for next control cycle
    t +=dt
    while(time.perf_counter()-t<dt):
        pass

ud.stop() # Terminate

# Save data in file
f = open("rolling_data_PID_SIN.txt", "w")
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