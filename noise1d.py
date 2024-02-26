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
