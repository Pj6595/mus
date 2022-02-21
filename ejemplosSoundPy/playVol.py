# 1_numPy/playNumPyVol.py reproductor con control de volumen
import pyaudio, kbhit
from scipy.io import wavfile # para manejo de wavs
import numpy as np  # arrays    
from format_tools import *


# abrimos wav y recogemos frecMuestreo y array de datos
#fs, data = wavfile.read('../0_basics/expousure.wav')
SRATE, data = wavfile.read('ex1.wav')

data = toFloat32(data)


print("Sample rate ",SRATE)
print("Sample format: ",data.dtype)
print("Num channels: ",len(data.shape))
print("Len ",data.shape[0])

# arrancamos pyAudio
p = pyaudio.PyAudio()


CHUNK = 1024
stream = p.open(format=p.get_format_from_width(getWidthData(data)),
                channels=len(data.shape),
                rate=SRATE,
                frames_per_buffer=CHUNK,
                output=True)


# En data tenemos el wav completo, ahora procesamos por bloques (chunks)
bloque = np.arange(CHUNK,dtype=data.dtype)
numBloque = 0
kb = kbhit.KBHit()
c= ' '

vol = 1.0
while c!= 'q': 
    # nuevo bloque
    bloque = data[ numBloque*CHUNK : numBloque*CHUNK+CHUNK ]    

    # modificación del volumen: multiplicacion de todas las muestras * vol
    bloque = bloque*vol

    # ojo: esta operación convierte el dtype de bloque a 'float64'      
    # esto es incorrecto: stream.write(bloque.tobytes())         
    # -> para lanzarlo al stream de salida hay que hacer conversion con "astype"

    stream.write(bloque.astype(data.dtype).tobytes())        
    

    if kb.kbhit():
        c = kb.getch()
        if (c=='v'): vol= max(0,vol-0.05)
        elif (c=='V'): vol= min(1,vol+0.05)
        print("Vol: ",vol)

    numBloque += 1

kb.set_normal_term()        
stream.stop_stream()
stream.close()
p.terminate()
