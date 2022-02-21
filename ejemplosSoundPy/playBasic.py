# reproductor simple 
import pyaudio
from scipy.io import wavfile # para manejo de wavs
import numpy as np  # arrays    
from format_tools import *

# abrimos wav y recogemos frecMuestreo (SRATE) y el array de muestras
SRATE, data = wavfile.read('ex1.wav')

# info del wav
print("SRATE: {}   Format: {}   Channels: {}    Len: {}".
  format(SRATE,data.dtype,len(data.shape), data.shape[0]))

# normalización del audio: conversión a float32 para facilitar operaciones posteriores
data = toFloat32(data)


# arrancamos pyAudio
p = pyaudio.PyAudio()

# Abrimos un stream de PyAudio para enviar ahí los datos
stream = p.open(format=p.get_format_from_width(getWidthData(data)),
                channels=len(data.shape),            # num canales (shape de data)
                rate=SRATE,                          # frecuencia de muestreo
                frames_per_buffer=1024,              # num frames por buffer
                output=True)                         # es stream de salida ()


# escribimos en el stream -> suena!
stream.write(data.astype(data.dtype).tobytes())

# liberamos recursos
stream.stop_stream()
stream.close()
p.terminate()
