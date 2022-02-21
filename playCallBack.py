# callBacks
import pyaudio, wave, kbhit
from scipy.io import wavfile
import numpy as np
from format_tools import *
import time, sys



if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)




# abrimos wav y recogemos frecMuestreo (SRATE) y el array de muestras
SRATE, data = wavfile.read('ex1.wav')
# info del wav
print("SRATE: {}   Format: {}   Channels: {}    Len: {}".
  format(SRATE,data.dtype,len(data.shape), data.shape[0]))

p = pyaudio.PyAudio()

CHUNK = 2048

numBloque = 0
def callback(in_data, frame_count, time_info, status):
    #  frame_count: numero de frames que hay que devolver
    #  frame_count = frames_per_buffer = CHUNK
    global numBloque
    print("Callback bloque ",numBloque, "fc ", frame_count)
    bloque = data[ numBloque*CHUNK : numBloque*CHUNK+CHUNK ]
    numBloque += 1
    return (bloque, pyaudio.paContinue)
    
stream = p.open(format=p.get_format_from_width(getWidthData(data)),
                channels=len(data.shape),
                rate=SRATE,
                frames_per_buffer = CHUNK,
                output=True,
                stream_callback=callback)


# start the stream (4)
stream.start_stream()

# wait for stream to finish (5)
while stream.is_active():
    time.sleep(1)

print("fin")
# stop stream (6)
stream.stop_stream()
stream.close()
#wf.close()

# close PyAudio (7)
p.terminate()
