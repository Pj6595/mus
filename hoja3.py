import kbhit
import sounddevice as sd
import soundfile as sf
from scipy.io import wavfile
import numpy as np
import matplotlib
from format_tools import *
from basicGenerators import *

CHUNK = 1024

SRATE = 44100
SECONDS = 0.5
VOLUME = 1.0
frequency = 50

partitura = [('G', 0.5), ('G', 0.5), ('A', 1), ('G', 1),
            ('c', 1), ('B', 2),
            ('G', 0.5), ('G', 0.5), ('A', 1), ('G', 1),
            ('d', 1), ('c', 2), 
            ('G', 0.5), ('G', 0.5), ('g', 1), ('e', 1),
            ('c', 1), ('B', 1), ('A', 1),
            ('f', 0.5), ('f', 0.5), ('e', 1), ('c', 1),
            ('d', 1), ('c', 2)]

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

def generateMusicData(partitura):
    data = np.empty([1,0])
    for nota, duracion in partitura:
        data = np.append(data, osci(noteToFreq(nota), duracion, VOLUME))
    return data


def osc(f,d):
    a=np.linspace(0, (2*np.pi)*f*d, d * SRATE)
    a = np.sin(a)
    return a

def squ(f,d):
    a=np.linspace(0, (2*np.pi)*f*d, d * SRATE - 1)
    a = np.sin(a)
    seq = np.linspace(0, d * SRATE - 1, d * SRATE, dtype = int)
    for x in seq - 1:
        if a[x] >= 0:
            a[x]=1
        else:
            a[x]=-1
    return a

def tri(f,d):
    a=np.linspace(0, (2*np.pi)*f*d, d * SRATE)
    a = np.arcsin(np.sin(a)) * 2/np.pi
    return a

def saw(f,d):
    a=np.linspace(0, (np.pi)*f*d, d * SRATE)
    a = np.arctan(np.tan(a)) * 2/np.pi
    return a

# abrimos wav y recogemos frecMuestreo y array de datos
# SRATE, data = wavfile.read('piano.wav')

test = np.zeros(shape = [1, 0])
for t in range(0, 5):
    test = np.append(test, t)

#data = osci(frequency, SECONDS, VOLUME)
data = generateMusicData(partitura)
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

# En data tenemos el wav completo, ahora procesamos por bloques (chunks)
# bloque = np.arange(CHUNK,dtype=data.dtype)
# numBloque = 0
# kb = kbhit.KBHit()
# c= ' '
# while len(bloque>0) and c!= 'q': 
#     # nuevo bloque
#     bloque = data[ numBloque*CHUNK : numBloque*CHUNK+CHUNK ]    

#     # pasamos al stream  haciendo conversion de tipo 
#     stream.write(bloque.astype(data.dtype).tobytes())

#     if kb.kbhit():
#         c = kb.getch()
#         if(c == 'F'): 
#             frequency = frequency + 5
#             data = osc(frequency, SECONDS)
#         elif(c == 'f'):
#             frequency = frequency - 5
#             data = osc(frequency, SECONDS)

#     numBloque += 1
#     print('.',end='')

# kb.set_normal_term()        
# stream.stop_stream()
# stream.close()
# p.terminate()


# En data tenemos el wav completo, ahora procesamos por bloques (chunks)
# bloque = np.arange(CHUNK,dtype=data.dtype)
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
        if(c == 'F'): 
            frequency = frequency + 5
            data = osc(frequency, SECONDS)
            data = toFloat32(data)
        elif(c == 'f'):
            frequency = frequency - 5
            data = osc(frequency, SECONDS)
            data = toFloat32(data)
        if (c=='v'): VOLUME= max(0,VOLUME-0.05)
        elif (c=='V'): VOLUME= min(1,VOLUME+0.05)
        print("Vol: ",VOLUME)

    numBloque += 1
    print('.',end='')


print('end')
stream.stop()