import numpy as np         # arrays    
import sounddevice as sd   # modulo de conexión con portAudio
import kbhit
from format_tools import *
from basicGenerators import *

SRATE = 44100 
CHUNK = 1024
VOLUME = 1.0
ORIGINALSRATE = 0

class Nota:
    def __init__(self, frec, dur):
        self.bloque = 0
        self.data = KarplusStrong(frec, dur)
    def getChunk(self):
        self.bloque += 1
        return self.data[CHUNK * (self.bloque-1): min(len(self.data),CHUNK * self.bloque)]


def KarplusStrong(frec, dur):
    N = SRATE // int(frec) # la frecuencia determina el tamanio del buffer
    buf = np.random.rand(N) * 2 - 1 # buffer inicial: ruido
    nSamples = int(dur*SRATE)
    samples = np.empty(nSamples, dtype=float) # salida
    # generamos los nSamples haciendo recorrido circular por el buffer
    for i in range(nSamples):
        samples[i] = buf[i % N] # recorrido de buffer circular
        buf[i % N] = 0.5 * (buf[i % N] + buf[(1 + i) % N]) # filtrado
    return samples

#Frecuencias de cada nota
noteFrecs = {
    'C': 523.251,
    'D': 587.33,
    'E': 659.255,
    'F': 698.456,
    'G': 789.991,
    'A': 880,
    'B': 987.767,
}

#Recibe un caracter con la nota que sea y devuelve su frecuencia
def noteToFreq(note):
    if(note.isupper()): 
        return noteFrecs[note]
    else:
        return noteFrecs[note.upper()]*2

kb = kbhit.KBHit()
c= ' '

notas = []

    # abrimos stream de salida
stream = sd.OutputStream(
    samplerate = SRATE,            # frec muestreo 
    blocksize  = CHUNK,            # tamaño del bloque (muy recomendable unificarlo en todo el programa)
    channels   = 1)  # num de canales

stream.start()

#Añadimos a la lista la nota que corresponda a la tecla pulsada
while c != 'a':
    if kb.kbhit():
        c = kb.getch()
        if c=='z':
            notas.append(Nota(noteToFreq('C'), 1))
        elif c == 'x':
            notas.append(Nota(noteToFreq('D'), 1))
            pass
        elif c== 'c':
            notas.append(Nota(noteToFreq('E'), 1))
            pass
        elif c== 'v':
            notas.append(Nota(noteToFreq('F'), 1))
            pass
        elif c== 'b':
            notas.append(Nota(noteToFreq('G'), 1))
            pass
        elif c== 'n':
            notas.append(Nota(noteToFreq('A'), 1))
            pass
        elif c== 'm':
            notas.append(Nota(noteToFreq('B'), 1))
            pass
        elif c== 'q':
            notas.append(Nota(noteToFreq('C') * 2, 1))
            pass
        elif c== 'w':
            notas.append(Nota(noteToFreq('D') * 2, 1))
            pass
        elif c== 'e':
            notas.append(Nota(noteToFreq('E') * 2, 1))
            pass
        elif c== 'r':
            notas.append(Nota(noteToFreq('F') * 2, 1))
            pass
        elif c== 't':
            notas.append(Nota(noteToFreq('G') * 2, 1))
            pass
        elif c== 'y':
            notas.append(Nota(noteToFreq('A') * 2, 1))
            pass
        elif c== 'u':
            notas.append(Nota(noteToFreq('B') * 2, 1))
            pass
        else: continue

    # Por cada nota que esté en la cola cogemos el bloque que toque y lo sumamos al chunk que va a sonar en esta iteración
    data = np.zeros(CHUNK)
    for nota in notas:
        currentChunk = nota.getChunk()
        if(len(currentChunk) != CHUNK) : #Final de la nota
            notas.remove(nota)
        data += np.resize(currentChunk, CHUNK)
    
    # Mandamos al stream el chunk resultante 
    stream.write(toFloat32(data))