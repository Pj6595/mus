import kbhit
import sounddevice as sd
import soundfile as sf
from scipy.io import wavfile
import numpy as np
import matplotlib
from format_tools import *
from basicGenerators import *

#Recibe un array de datos y un número con los segundos de delay
class Delay:
    def __init__(self, data, seconds):
        self.data = data
        self.seconds = seconds
    
    #Devuelve el array con seconds segundos de silencio al principio
    def applyDelay(self):
        nSamples = int(SRATE*float(self.seconds))
        delayedData = np.append(np.float32(np.zeros(nSamples)),self.data)
        return delayedData


CHUNK = 1024
SRATE = 44100
SECONDS = 3
DELAYSECONDS = 1
VOLUME = 1.0
frequency = 50

data = osci(frequency, SECONDS, VOLUME)
data = toFloat32(data)

#Aplicamos el retraso a los datos
delay = Delay(data, DELAYSECONDS)
data = delay.applyDelay()

# informacion de wav
print("Sample rate ",SRATE)
print("Sample format: ",data.dtype)
print("Num channels: ",len(data.shape))
print("Len: ",data.shape[0])

sd.play(data, SRATE)

# abrimos stream de salida
stream = sd.OutputStream(
    samplerate = SRATE,            # frec muestreo 
    blocksize  = CHUNK,            # tamaño del bloque (muy recomendable unificarlo en todo el programa)
    channels   = len(data.shape))  # num de canales

# arrancamos stream
stream.start()

numBloque = 0
kb = kbhit.KBHit()
c= ' '

nSamples = CHUNK 
print('\n\nProcessing chunks: ',end='')

# termina con 'q' o cuando el último bloque ha quedado incompleto (menos de CHUNK samples)
while c!= 'q' and nSamples==CHUNK: 
    # numero de samples a procesar: CHUNK si quedan sufucientes y si no, los que queden
    nSamples = min(CHUNK,data.shape[0] - (numBloque+1)*CHUNK)

    # nuevo bloque
    bloque = data[numBloque*CHUNK : numBloque*CHUNK+nSamples]
    bloque *= VOLUME

    # lo pasamos al stream
    stream.write(bloque) # escribimos al stream

    # modificación de volumen 
    if kb.kbhit():
        c = kb.getch()
        if (c=='v'): VOLUME= max(0,VOLUME-0.05)
        elif (c=='V'): VOLUME= min(1,VOLUME+0.05)
        print("Vol: ",VOLUME)

    numBloque += 1
    print('.',end='')

print('end')
stream.stop()