import numpy as np
import matplotlib.pyplot as plt

SRATE = 44100

def ej1():
    #v = np.arange(44100)
    v = np.random.random(44100)
    v = v*2-1
    x = np.linspace(0, 44100, 44100)
    plt.plot(x, v)
    plt.savefig("ejercicio1")

def ej2():
    a=np.linspace(0, 2*np.pi, 44100)
    a = np.sin(a)
    x = np.linspace(0, 44100, 44100)
    plt.plot(x, a)
    plt.savefig("ejercicio2_1")
    
    plt.figure()
    a=np.linspace(0, 2*np.pi * 2, 44100)
    a = np.sin(a)
    x = np.linspace(0, 44100, 44100)
    plt.plot(x, a)
    plt.savefig("ejercicio2_2")

    plt.figure()
    a=np.linspace(0, 2*np.pi * 3, 44100)
    a = np.sin(a)
    x = np.linspace(0, 44100, 44100)
    plt.plot(x, a)
    plt.savefig("ejercicio2_3")

def osc(f,d):
    a=np.linspace(0, (2*np.pi)*f*d, d * SRATE)
    a = np.sin(a)
    x = np.linspace(0, d*SRATE, d* SRATE)
    return x,a

def osc0to1(f,d):
    a=np.linspace(0, (2*np.pi)*f*d, d * SRATE)
    a = np.sin(a)
    x = np.linspace(0, d*SRATE, d* SRATE)
    a = vol(a, 0.5)
    a = a+1
    return x,a

def squ(f,d):
    a=np.linspace(0, (2*np.pi)*f*d, d * SRATE - 1)
    a = np.sin(a)
    seq = np.linspace(0, d * SRATE - 1, d * SRATE, dtype = int)
    for x in seq - 1:
        if a[x] >= 0:
            a[x]=1
        else:
            a[x]=-1
    x = np.linspace(0, d*SRATE - 1, d* SRATE - 1)
    plt.plot(x, a)
    plt.show()
    plt.savefig("ejercicio3_2")

def tri(f,d):
    a=np.linspace(0, (2*np.pi)*f*d, d * SRATE)
    a = np.arcsin(np.sin(a)) * 2/np.pi
    x = np.linspace(0, d*SRATE - 1, d* SRATE)
    plt.plot(x, a)
    plt.show()
    plt.savefig("ejercicio3_3")

def saw(f,d):
    a=np.linspace(0, (np.pi)*f*d, d * SRATE)
    a = np.arctan(np.tan(a)) * 2/np.pi
    x = np.linspace(0, d*SRATE - 1, d* SRATE)
    plt.plot(x, a)
    plt.show()
    plt.savefig("ejercicio3_4")

def vol(sample, factor):
    return sample * factor 

def modulaVol(sample, frec):
    return sample * osc0to1(frec, np.shape(sample)[0] / SRATE)

def ej4():
    x, a = osc(1,1)
    a = modulaVol(a, 0.1)
    plt.plot(x, a)
    plt.show()
    
ej4()