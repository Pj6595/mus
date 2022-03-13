import kbhit
import sounddevice as sd
import soundfile as sf
from scipy.io import wavfile
import numpy as np
import matplotlib
from format_tools import *
from basicGenerators import *

#Ejercicio 8: piano

#Velocidades de cada nota
noteSpeeds = {
    'C': 1,
    'D': 1.12,
    'E': 1.26,
    'F': 1.33,
    'G': 1.5,
    'A': 1.68,
    'B': 1.89,
}

CHUNK = 1024
VOLUME = 1.0
ORIGINALSRATE = 0
SRATE = 0

# abrimos wav y recogemos frecMuestreo y array de datos
ORIGINALSRATE, data = wavfile.read('piano.wav')

data = toFloat32(data)

# informacion de wav
print("Sample rate ",ORIGINALSRATE)
print("Sample format: ",data.dtype)
print("Num channels: ",len(data.shape))
print("Len: ",data.shape[0])

kb = kbhit.KBHit()
c= ' '

#Suena la tecla según el input dado
while c != 'a':
    c = kb.getch()
    SRATE = ORIGINALSRATE
    if c=='z':
        SRATE *= noteSpeeds['C']
    elif c == 'x':
        SRATE *= noteSpeeds['D']
        pass
    elif c== 'c':
        SRATE *= noteSpeeds['E']
        pass
    elif c== 'v':
        SRATE *= noteSpeeds['F']
        pass
    elif c== 'b':
        SRATE *= noteSpeeds['G']
        pass
    elif c== 'n':
        SRATE *= noteSpeeds['A']
        pass
    elif c== 'm':
        SRATE *= noteSpeeds['B']
        pass
    elif c== 'q':
        SRATE *= noteSpeeds['C']*2
        pass
    elif c== 'w':
        SRATE *= noteSpeeds['D']*2
        pass
    elif c== 'e':
        SRATE *= noteSpeeds['E']*2
        pass
    elif c== 'r':
        SRATE *= noteSpeeds['F']*2
        pass
    elif c== 't':
        SRATE *= noteSpeeds['G']*2
        pass
    elif c== 'y':
        SRATE *= noteSpeeds['A']*2
        pass
    elif c== 'u':
        SRATE *= noteSpeeds['B']*2
        pass
    else: continue

    # abrimos stream de salida
    stream = sd.OutputStream(
        samplerate = SRATE,            # frec muestreo 
        blocksize  = CHUNK,            # tamaño del bloque (muy recomendable unificarlo en todo el programa)
        channels   = len(data.shape))  # num de canales

    # arrancamos stream
    stream.start()

    numBloque = 0

    nSamples = CHUNK 
    print('\n\nProcessing chunks: ',end='')

    # termina con 'q' o cuando el último bloque ha quedado incompleto (menos de CHUNK samples)
    while nSamples==CHUNK: 
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