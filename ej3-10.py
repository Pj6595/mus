import numpy as np         # arrays    
import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf     # para lectura/escritura de wavs
import kbhit               # para lectura de teclas no bloqueante

CHUNK = 1024
CHANNELS = 1
SRATE = 44100
DELAYSECONDS = 0.2
VOLUME = 1.0

class Delay:
    def __init__(self, data, seconds):
        self.data = data
        self.seconds = seconds
    
    def applyDelay(self):
        nSamples = int(SRATE*float(self.seconds))
        delayedData = np.append(np.float32(np.zeros(nSamples)),self.data)
        return delayedData

# abrimos stream de entrada (InpuStream)
inStream = sd.InputStream(samplerate=SRATE, blocksize=CHUNK, dtype="float32", channels=1)

# arrancamos stream
inStream.start()

# buffer para acumular grabación.
# (0,1): con un canal (1), vacio (de tamaño 0)
buffer = np.empty((0, 1), dtype="float32")

delay = Delay(buffer, DELAYSECONDS)
buffer = delay.applyDelay()

# abrimos stream de salida
outStream = sd.OutputStream( samplerate = SRATE, blocksize = CHUNK, channels = 1)

outStream.start()

numBloque = 0
nSamples = CHUNK 
print('\n\nProcessing chunks: ',end='')

# bucle de grabación
kb = kbhit.KBHit()
c = ' '
while c != 'q': 
    bloque = inStream.read(CHUNK)  # recogida de samples en array numpy    
    # read devuelve un par (samples,bool)
    buffer = np.append(buffer,bloque[0]) # en bloque[0] están los samples

    # nuevo bloque
    bloque = buffer[numBloque*CHUNK : numBloque*CHUNK+nSamples ]
    bloque *= VOLUME

    # lo pasamos al stream
    outStream.write(bloque) # escribimos al stream

    # modificación de volumen 
    if kb.kbhit():
        c = kb.getch()
        if (c=='v'): VOLUME= max(0,VOLUME-0.05)
        elif (c=='V'): VOLUME= min(1,VOLUME+0.05)
        print("Vol: ",VOLUME)

    numBloque += 1
    print('.',end='')

inStream.stop()
outStream.stop()

kb.set_normal_term()