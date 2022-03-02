# callBacks

import numpy as np         # arrays    
import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf     # para lectura/escritura de wavs
import kbhit               # para lectura de teclas no bloqueante

CHUNK = 1024


'''
if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)
'''

# leemos wav en array numpy (data)
# por defecto lee float64, pero podemos hacer directamente la conversion a float32
data, SRATE = sf.read('ex1.wav',dtype="float32")

# info del wav
print("SRATE: {}   Format: {}   Channels: {}    Len: {}".
  format(SRATE,data.dtype,len(data.shape), data.shape[0]))


# contador de frames
current_frame = 0
def callback(outdata, frames, time, status):
    global current_frame       # para actualizarlo en cada callBack
    if status: print(status)
    print("Bloque: ",current_frame//CHUNK, outdata.dtype, len(outdata))  # num bloque

    # vemos si podemos coger un CHUNK entero o lo que quede en 
    chunksize = min(len(data) - current_frame, frames)  
    
    # escribimos en outdata los samples correspondientes
    outdata[:chunksize] = data[current_frame:current_frame + chunksize]    
    # es una forma compacta de hacer:
    # for i in range(chunksize): outdata[i] = data[current_frame+i]

    # NO funcionaría hacer outdata = data[current_frame:current_frame + chunksize]
    # porque asignaría (compartiría) referencias (objetos array de numpy)
    # outdata tiene que ser un nuevo array para enviar al stream y que no se reescriba
    
    if chunksize < frames: # ha terminado?
        outdata[chunksize:] = 0
        raise sd.CallbackStop()

    # actualizamos current_frame con los frames procesados    
    current_frame += chunksize


# stream de salida con callBack
stream = sd.OutputStream(samplerate=SRATE, channels=data.shape[1], callback=callback, blocksize=CHUNK)

# arrancamos stream
stream.start()

kb = kbhit.KBHit()
c = ' ' 
while c!='q':
    if kb.kbhit():
        c = kb.getch()