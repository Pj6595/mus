import kbhit
import sounddevice as sd
import soundfile as sf
from scipy.io import wavfile
import numpy as np
import matplotlib
from format_tools import *
from basicGenerators import *

#Ejercicio 7: cumpleaños feliz

notes = {
    'C': 523.251,
    'D': 587.33,
    'E': 659.255,
    'F': 698.456,
    'G': 789.991,
    'A': 880,
    'B': 987.767,
}

def noteToFreq(note):
    if(note.isupper()): 
        return notes[note]
    else:
        return notes[note.upper()]*2

def generateMusicData(partitura, volume):
    data = np.empty([1,0])
    for nota, duracion in partitura:
        data = np.append(data, osci(noteToFreq(nota), duracion, volume))
    return data
    
CHUNK = 1024

SRATE = 44100
VOLUME = 1.0

partitura = [('G', 0.5), ('G', 0.5), ('A', 1), ('G', 1),
            ('c', 1), ('B', 2),
            ('G', 0.5), ('G', 0.5), ('A', 1), ('G', 1),
            ('d', 1), ('c', 2), 
            ('G', 0.5), ('G', 0.5), ('g', 1), ('e', 1),
            ('c', 1), ('B', 1), ('A', 1),
            ('f', 0.5), ('f', 0.5), ('e', 1), ('c', 1),
            ('d', 1), ('c', 2)]

# abrimos wav y recogemos frecMuestreo y array de datos
# SRATE, data = wavfile.read('piano.wav')

#data = osci(frequency, SECONDS, VOLUME)
data = generateMusicData(partitura, VOLUME)
data = toFloat32(data)

# informacion de wav
print("Sample rate ",SRATE)
print("Sample format: ",data.dtype)
print("Num channels: ",len(data.shape))
print("Len: ",data.shape[0])

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
    bloque = data[numBloque*CHUNK : numBloque*CHUNK+nSamples ]
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