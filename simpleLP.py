'''
simple reproductor con filtro de agudos
'''


import pyaudio
import wave
import sys
import kbhit
from scipy.io import wavfile
import numpy as np
from format_tools import *



if len(sys.argv) < 2:
    #print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    #sys.exit(-1)
    wav = 'tormenta.wav'
else:
    wav = sys.argv[1]



fs, data = wavfile.read(wav)
data = toFloat32(data)

p = pyaudio.PyAudio()


CHUNK = 1024

stream = p.open(format=p.get_format_from_width(getWidthData(data)),
                channels=len(data.shape),
                rate=fs,
                frames_per_buffer=CHUNK,
                output=True)



kb = kbhit.KBHit()


# contador de frames
frame = 0
c= ' '

print("[A] activar filtro\n[a] desactivar")
# memoria el filtro (sample anterior)
prev = 0
act = False
while c!= 'q':
    # sacamos bloque
    bloque = data[frame*CHUNK:(frame+1)*CHUNK]

    if act:
        # procesamos
        bloqueOut = np.zeros(CHUNK,dtype=data.dtype)
        bloqueOut[0] = prev + bloque[0]
        for i in range(1,CHUNK): 
            bloqueOut[i] = 0.5*bloque[i-1] + 0.5*bloque[i]
    else: 
        bloqueOut = bloque
    # memoria para el siguiente    
    prev = bloque[CHUNK-1]

    
    # a la salida
    stream.write(bloqueOut.astype((data.dtype)).tobytes())    
    
    if kb.kbhit():
        c = kb.getch()
        print(c)
        if c =='q': break
        elif c=='a': act = False 
        elif c=='A': act = True
        print("Activo: ",act)


    frame += 1

kb.set_normal_term()

        
stream.stop_stream()
stream.close()

p.terminate()
