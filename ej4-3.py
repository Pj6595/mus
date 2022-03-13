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
MINAMPL = 0
MAXAMPL = 1

Incr_X = (MAXFREQ - MINFREQ) / WIDTH 
Incr_Y = (MAXAMPL - MINAMPL) / HEIGHT 

stream = sd.OutputStream(samplerate=SRATE,blocksize=CHUNK,channels=1)  
stream.start()

# obtencion de la posicion del raton
playing = True
while playing:
    samples = oscFM(fc,fm,beta,vol,frame)
    stream.write(np.float32(0.5*samples)) 
    frame += CHUNK

    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            mouseX, mouseY = event.pos
            print("Mouse X: ", mouseX, " Mouse Y: ", mouseY)
            beta = mouseY * Incr_Y + MINAMPL
            fm = mouseX * Incr_X + MINFREQ
            print("Frec moduladora: ", fm)
            print("Factor (beta): ",beta)
        if event.type == pygame.QUIT:
            playing = False

pygame.quit()      
stream.stop()