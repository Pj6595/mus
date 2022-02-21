'''
Librería de utilidades con
- toFloat32(sig): convierte el audio sig dad en cualquier formato (int o float, 16/32/64 bits) a float32
- getWithData(data): Obtiene el número de bytes de la muestra para pasarselo después a pyAudio


La conversión a float32 es un modificación de:
https://gist.github.com/HudsonHuang/fbdf8e9af7993fe2a91620d3fb86a182

'''


import numpy as np

def toFloat32(sig):
    if sig.dtype.kind in 'iu':
        return pcm2float(sig)
    elif sig.dtype.kind=='f':
        return np.float32(sig)


def getWidthData(data):
    # miramos tipo de datos
    if data.dtype.name == 'uint8': return 1
    elif data.dtype.name == 'int16': return 2
    elif data.dtype.name in ['int32','float32']: return 4
    else: raise Exception('Not supported')


def pcm2float(sig, dtype='float32'):
    """Convert PCM signal to floating point with a range from -1 to 1.
    Use dtype='float32' for single precision.
    Parameters
    ----------
    sig : array_like
        Input array, must have integral type.
    dtype : data type, optional
        Desired (floating point) data type.
    Returns
    -------
    numpy.ndarray
        Normalized floating point data.
    See Also
    --------
    float2pcm, dtype
    """
    sig = np.asarray(sig)
    if sig.dtype.kind not in 'iu':
        raise TypeError("'sig' must be an array of integers")
    dtype = np.dtype(dtype)
    if dtype.kind != 'f':
        raise TypeError("'dtype' must be a floating point type")

    i = np.iinfo(sig.dtype)
    abs_max = 2 ** (i.bits - 1)
    offset = i.min + abs_max
    return np.float32((sig.astype(dtype) - offset) / abs_max)




