import argparse;
import random;
import math;
import pygame;

from enum import Enum, auto;
from collections import deque;

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

def Print(screen, font, text, pos : tuple, color : tuple):
  ts, _ = font.render(text, color);
  screen.blit(ts, pos);

################################################################################

def Draw(pn : Noise1D, multY : int, ns : float):
  screenSize = [ 1280, 720 ];

  ballStart = screenSize[0] // 2 + 1.9 * (screenSize[0] // 4);

  points = deque();

  pygame.init();

  pygame.display.set_caption("1D noise demo");

  screen = pygame.display.set_mode(screenSize);
  font   = pygame.freetype.Font(None, 24);

  running = True;

  noiseInd  = 0.0;
  noiseStep = ns;

  c = pygame.time.Clock();

  ballColor  = (0, 255, 0);
  trailColor = (0, 128, 0);
  fontColor  = (255, 255, 255);
  gridColor  = (32, 32, 32);

  ballMultY = multY;

  iters = 0;

  paused = False;

  while running:

    c.tick(60);

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False;
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          running = False;
        elif event.key == pygame.K_SPACE:
          paused = not paused;

    screen.fill((0,0,0));

    pygame.draw.line(screen, gridColor, (screenSize[0] // 2, 0), (screenSize[0] // 2, screenSize[1]), 1);
    pygame.draw.line(screen, gridColor, (0, screenSize[1] // 2), (screenSize[0], screenSize[1] // 2), 1);
    pygame.draw.line(screen, fontColor, (screenSize[0] // 2 - 5, screenSize[1] // 2 - ballMultY), (screenSize[0] // 2 + 5, screenSize[1] // 2 - ballMultY), 1);

    noiseRaw = pn.Noise(noiseInd);
    noiseVal = noiseRaw * ballMultY;

    if not paused:
      points.append(noiseVal);
      noiseInd += noiseStep;

    if len(points) >= ballStart:
      points.popleft();

    xOff = ballStart - len(points);

    for p in points:
      pygame.draw.circle(screen,
                         trailColor,
                         (xOff, screenSize[1] // 2 - p),
                         1);
      xOff += 1;

    pygame.draw.circle(screen,
                       ballColor,
                       (ballStart, screenSize[1] // 2 - noiseVal),
                       10);

    Print(screen,
          font,
          (
            f"Noise params: seed = { pn._seed }, "
            f"size = { pn._size }, "
            f"step = { noiseStep }"
          ),
          (0, 0),
          fontColor);

    Print(screen,
          font,
          f"Iterations = { iters }",
          (0, screenSize[1] - 30),
          fontColor);

    Print(screen,
          font,
          f"Noise value: raw = {noiseRaw:.4f}, scaled = {noiseVal:.2f}",
          (0, screenSize[1] - 60),
          fontColor);

    Print(screen,
          font,
          f"{ ballMultY }",
          (screenSize[0] // 2 + 15, screenSize[1] // 2 - ballMultY - 30),
          fontColor);

    Print(screen,
          font,
          "Press 'Space' to toggle pause",
          (screenSize[0] // 2 + 100, screenSize[1] - 30),
          fontColor);

    Print(screen,
          font,
          f"{ screenSize[0] }",
          (screenSize[0] - 60, 0),
          fontColor);

    Print(screen,
          font,
          f"{screenSize[1]}",
          (screenSize[0] - 60, screenSize[1] - 30),
          fontColor);

    pygame.display.flip();

    if not paused:
      iters += 1;

  pygame.quit();

################################################################################

def main():
  parser = argparse.ArgumentParser();

  parser.add_argument("SIZE",   help="Affects noise period.");
  parser.add_argument("--seed", help="E.g. 12345. Default: None.");
  parser.add_argument("--mult", help="Graph Y multiplier for drawing. Default: 100");
  parser.add_argument("--step", help="Noise step. Affects drawing smoothness. Default: 0.025");

  args = parser.parse_args();
  seed = None;
  multY = 100;
  noiseStep = 0.025;

  try:
    size = int(args.SIZE);

    if args.seed is not None:
      seed = args.seed;

    if args.mult is not None:
      multY = int(args.mult);

    if args.step is not None:
      noiseStep = float(args.step);

    if multY <= 0:
      print("Mult Y must be positive!");
      exit(1);

  except:
    print("Numbers only!");
    exit(1);

  if (size <= 0):
    print("Size must be greater than 0!");
    exit(1);

  pn = Noise1D(size, seed=seed);
  
  Draw(pn, multY, noiseStep);

################################################################################

if __name__ == "__main__":
  main();
