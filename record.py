# basic/record0.py Grabacion de un archivo de audio 'q' para terminar
import pyaudio, kbhit
import numpy as np
from scipy.io.wavfile import write
#from format_tools import *


CHUNK = 1024
FORMAT = pyaudio.paFloat32
CHANNELS = 1
SRATE = 44100

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, 
                channels=CHANNELS,
                rate=SRATE,                 
                frames_per_buffer=CHUNK, # tamanio buffer == CHUNK !!
                input=True)   # ahora es flujo de entrada

print("* grabando")
print("* pulsa q para termninar")

data = np.array(CHUNK,dtype=np.float32)

kb = kbhit.KBHit()
c = ' '
while c != 'q': 
    bloque = stream.read(CHUNK)  # recogida de samples (en bruto)
    bloque = np.frombuffer(bloque,dtype=np.float32) #conversión a np.array
    data = np.append(data,bloque) # acumulado
    if kb.kbhit(): c = kb.getch()

print("* grabacion terminada")
stream.stop_stream(); 
stream.close(); 

# guardamos wav

print('Quieres reproducir [S/n]? ',end='')
while not kb.kbhit(): 
    True

c = kb.getch()
if c!='n':
    stream = p.open(format=FORMAT,
                    channels=len(data.shape),
                    rate=SRATE,
                    frames_per_buffer=CHUNK,
                    output=True)

    stream.write(data.tobytes())    
    stream.stop_stream()
    stream.close()

kb.set_normal_term(); 
p.terminate()

# escritura del wav
write("rec.wav", SRATE, data.astype(np.float32))

