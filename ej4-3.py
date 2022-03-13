# creacion de una ventana de pygame
import pygame
from pygame.locals import *
import numpy as np         # arrays    
import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf     # para lectura/escritura de wavs
import kbhit
import os

# fc, carrier = pitch, fm frecuencia moduladora, beta = indice de modulacion
def oscFM(fc,fm,beta,vol,frame):
    # sin(2πfc+βsin(2πfm))   http://www.mrcolson.com/2016/04/21/Simple-Python-FM-Synthesis.html
    sample = np.arange(CHUNK)+frame
    mod = beta*np.sin(2*np.pi*fm*sample/SRATE)
    res = np.sin(2*np.pi*fc*sample/SRATE + mod)
    return vol*res

WIDTH = 800
HEIGHT = 600
SRATE = 44100       # sampling rate, Hz, must be integer
CHUNK = 1024

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Theremin")

kb = kbhit.KBHit()
c = ' '

fc = 440
fm = 300
beta = 1
vol = 0.8
frame = 0

MAXFREQ = 10000
MINFREQ = 100
MINVOLUME = 0
MAXVOLUME = 1

# Cuanto cambia la frecuencia y el volumen por cada ud de distancia en el eje x/y
Incr_X = (MAXFREQ - MINFREQ) / WIDTH 
Incr_Y = (MAXVOLUME - MINVOLUME) / HEIGHT 

stream = sd.OutputStream(samplerate=SRATE,blocksize=CHUNK,channels=1)  
stream.start()

# obtencion de la posicion del raton
playing = True
while playing:
    # Obtenemos el sonido con fm, beta y fc
    samples = oscFM(fc,fm,beta,vol,frame)
    stream.write(np.float32(0.5*samples) * vol) 
    frame += CHUNK

    # Calculamos fm y el volumen con las coordenadas del mouse
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            mouseX, mouseY = event.pos
            print("Mouse X: ", mouseX, " Mouse Y: ", mouseY)
            vol = mouseY * Incr_Y + MINVOLUME
            fm = mouseX * Incr_X + MINFREQ
            print("Frec moduladora: ", fm)
            print("Volumen: ",vol)
        if event.type == pygame.QUIT:
            playing = False

# Cierre del bucle del programa
pygame.quit()      
stream.stop()