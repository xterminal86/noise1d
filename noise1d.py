import math;
import random;

from enum import Enum, auto;

################################################################################

class Interpolation(Enum):
  LINEAR = auto()
  COSINE = auto()

class Noise1D:
  _size  = 0;
  _noise = [];
  _amplitude = 1.0;
  _seed = None;

  # ----------------------------------------------------------------------------

  def __init__(self, size : int, amplitude : float = 1.0, seed = None):
    self._size = size;

    self.Reset(size, amplitude, seed);

  # ----------------------------------------------------------------------------

  def Reset(self, newSize : int = 0, newAmp : float = 1.0, newSeed = None):
    if (newSize > 0):
      self._size = newSize;

    self._amplitude = newAmp;
    self._noise     = [ 0 ] * newSize;
    self._seed      = newSeed;

    random.seed(self._seed);

    for i in range(self._size):
      self._noise[i] = random.random() * self._amplitude;

  # ----------------------------------------------------------------------------

  def Noise(self, x : float, interpolation=Interpolation.COSINE):
    ind = int(x);

    t = math.modf(x)[0];

    y1 = self._noise[ind       % self._size];
    y2 = self._noise[(ind + 1) % self._size];

    if interpolation is Interpolation.LINEAR:
      val = (1 - t) * y1 + t * y2;
    else:
      val = (math.cos(t * math.pi) + 1) * 0.5 * (y1 - y2) + y2;

    return val;

  # ----------------------------------------------------------------------------

  def PrintNoise(self):
    for item in self._noise:
      print(f"{item:.4f}, ", end="");

    print();

################################################################################

class PerlinNoise:
  _rnd     = [];
  _noise   = [];
  _size    = 0;
  _seed    = None;
  _octaves = 8;
  _interpolation = Interpolation.LINEAR;

  # ----------------------------------------------------------------------------

  def __init__(self, size : int, octaves=8, seed = None, interpolation=Interpolation.LINEAR):
    self._seed    = seed;
    self._size    = size;
    self._octaves = octaves;
    self._interpolation = interpolation;

    random.seed(self._seed);

    self.Reset();

  # ----------------------------------------------------------------------------

  def Reset(self):
    self._rnd   = [ 0.0 ] * self._size;
    self._noise = [ 0.0 ] * self._size;

    #
    # Generate seed array.
    #
    for i in range(self._size):
      self._rnd[i] = random.random();

    for i in range(self._size):

      noise = 0.0;
      scale = 1.0;
      normCoeff = 0;

      for o in range(1, self._octaves):
        pitch = (self._size >> o);

        if pitch == 0:
          break;

        ind1 = (i // pitch) * pitch;
        ind2 = (ind1 + pitch) % self._size;

        blend = float(i - ind1) / float(pitch);

        if self._interpolation == Interpolation.LINEAR:
          sample = (1.0 - blend) * self._rnd[ind1] + blend * self._rnd[ind2];
        else:
          sample = (math.cos(blend * math.pi) + 1) * 0.5 * (self._rnd[ind1] - self._rnd[ind2]) + self._rnd[ind2];

        noise += sample * scale;
        normCoeff += scale;
        scale /= 2.0;

      #
      # Rescale result back to [ 0.0 ; 1.0 ]
      #
      if normCoeff != 0:
        self._noise[i] = noise / normCoeff;

  # ----------------------------------------------------------------------------

  def Noise(self, x : float) -> float:
    ind = int(x) % self._size;
    return self._noise[ind];
