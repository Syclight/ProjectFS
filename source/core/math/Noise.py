import math
import random

from source.core.math.MathConst import PI

PERLIN_YWRAPB = 4
PERLIN_YWRAP = 1 << PERLIN_YWRAPB
PERLIN_ZWRAPB = 8
PERLIN_ZWRAP = 1 << PERLIN_ZWRAPB
PERLIN_SIZE = 4095

perlin_octaves = 4
perlin_amp_falloff = 0.5


def scaled_cosine(i):
    return 0.5 * (1.0 - math.cos(i * PI))


perlin = []


def noise(x, y=0, z=0):
    if len(perlin) == 0:
        for i in range(0, PERLIN_SIZE + 1):
            perlin.append(random.uniform(0, 1))
    _x = x if x > 0 else -x
    _y = y if y > 0 else -y
    _z = z if z > 0 else -z

    _xi = math.floor(_x)
    _yi = math.floor(_y)
    _zi = math.floor(_z)

    _xf = _x - _xi
    _yf = _y - _yi
    _zf = _z - _zi

    r, ampl = 0, 0.5

    for o in range(0, perlin_octaves):
        of = _xi + (_yi << PERLIN_YWRAPB) + (_zi << PERLIN_ZWRAPB)
        rxf = scaled_cosine(_xf)
        ryf = scaled_cosine(_yf)

        n1 = perlin[of & PERLIN_SIZE]
        n1 += rxf * (perlin[(of + 1) & PERLIN_SIZE] - n1)
        n2 = perlin[(of + PERLIN_YWRAP) & PERLIN_SIZE]
        n2 += rxf * (perlin[(of + PERLIN_YWRAP + 1) & PERLIN_SIZE] - n2)
        n1 += ryf * (n2 - n1)

        of += PERLIN_ZWRAP
        n2 = perlin[of & PERLIN_SIZE]
        n2 += rxf * (perlin[(of + 1) & PERLIN_SIZE] - n2)
        n3 = perlin[(of + PERLIN_YWRAP) & PERLIN_SIZE]
        n3 += rxf * (perlin[(of + PERLIN_YWRAP + 1) & PERLIN_SIZE] - n3)
        n2 += ryf * (n3 - n2)

        n1 += scaled_cosine(_zf) * (n2 - n1)

        r += n1 * ampl
        ampl *= perlin_amp_falloff
        _xi <<= 1
        _xf *= 2
        _yi <<= 1
        _yf *= 2
        _zi <<= 1
        _zf *= 2

        if _xf >= 1.0:
            _xi += 1
            _xf -= 1
        if _yf >= 1.0:
            _yi += 1
            _yf -= 1
        if _zf >= 1.0:
            _zi += 1
            _zf -= 1

    return r

# def noiseDetail(lod, falloff):
#     if lod > 0:
#         perlin_octaves = lod
#     if falloff > 0:
#         perlin_amp_falloff = falloff
