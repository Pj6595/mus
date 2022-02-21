# reproductor simple 
import numpy as np         # arrays    
import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf     # para lectura/escritura de wavs


# leemos wav en array numpy (data)
# por defecto lee en formato dtype="float64". No hay problema para reproducción simple (hace conversiones internas)
data, SRATE = sf.read('ex1.wav')


# informacion de wav
print("\n\nInfo del wav ",SRATE)
print("  Sample rate ",SRATE)
print("  Sample format: ",data.dtype)
print("  Num channels: ",len(data.shape))
print("  Len: ",data.shape[0])


# bajamos volumen
data = data * 0.5

# a reproducir!
sd.play(data, SRATE)

# bloqueamos la ejecución hasta que acabe
sd.wait()