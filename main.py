import argparse;
import pygame;

from collections import deque;

from noise1d import Noise1D;

################################################################################

def PrintString(screen, font, text, pos : tuple, color : tuple):
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

  periodMarkColor = (128, 0, 0);
  ballColor       = (0, 255, 0);
  trailColor      = (0, 128, 0);
  fontColor       = (255, 255, 255);
  gridColor       = (32, 32, 32);

  ballMultY = multY;

  iters = 0;

  showPeriodMark = True;

  periodHit = 0;

  if noiseStep < 1.0:
    periodHit = int(float(pn._size) / noiseStep);
  else:
    periodHit = pn._size;

  periodCounter = 0;

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
        elif event.key == pygame.K_p:
          showPeriodMark = not showPeriodMark;

    screen.fill((0,0,0));

    pygame.draw.line(screen, gridColor, (screenSize[0] // 2, 0), (screenSize[0] // 2, screenSize[1]), 1);
    pygame.draw.line(screen, gridColor, (0, screenSize[1] // 2), (screenSize[0], screenSize[1] // 2), 1);
    pygame.draw.line(screen, fontColor, (screenSize[0] // 2 - 5, screenSize[1] // 2 - ballMultY), (screenSize[0] // 2 + 5, screenSize[1] // 2 - ballMultY), 1);

    noiseRaw = pn.Noise(noiseInd);
    noiseVal = noiseRaw * ballMultY;

    if not paused:
      if periodCounter == periodHit:
        points.append((noiseVal, periodMarkColor));
        periodCounter = 0;
      else:
        points.append((noiseVal, trailColor));

      noiseInd += noiseStep;

    if len(points) >= ballStart:
      points.popleft();

    xOff = ballStart - len(points);

    for p in points:
      if showPeriodMark and p[1] == periodMarkColor:
        pygame.draw.line(screen,
                         p[1],
                         (xOff, 0),
                         (xOff, screenSize[1]),
                         1);
      else:
        pygame.draw.circle(screen,
                           p[1],
                           (xOff, screenSize[1] // 2 - p[0]),
                           1);
      xOff += 1;

    pygame.draw.circle(screen,
                       ballColor,
                       (ballStart, screenSize[1] // 2 - noiseVal),
                       10);

    PrintString(screen,
                font,
                (
            f"Noise params: seed = { pn._seed }, "
            f"size = { pn._size }, "
            f"step = { noiseStep }, "
            f"showPeriod = { showPeriodMark }"
          ),
                (0, 0),
                fontColor);

    PrintString(screen,
                font,
          f"Iterations = { iters }",
                (0, screenSize[1] - 30),
                fontColor);

    PrintString(screen,
                font,
          f"Noise value: raw = {noiseRaw:.4f}, scaled = {noiseVal:.2f}",
                (0, screenSize[1] - 60),
                fontColor);

    PrintString(screen,
                font,
          f"{ ballMultY }",
                (screenSize[0] // 2 + 15, screenSize[1] // 2 - ballMultY - 30),
                fontColor);

    PrintString(screen,
                font,
          "Press 'Space' to toggle pause",
                (screenSize[0] - 340, screenSize[1] - 30),
                fontColor);

    PrintString(screen,
                font,
          "Press 'P' to toggle period marker",
                (screenSize[0] - 380, screenSize[1] - 60),
                fontColor);

    PrintString(screen,
                font,
          f"{ screenSize[0] }x{ screenSize[1] }",
                (screenSize[0] - 110, 0),
                fontColor);

    pygame.display.flip();

    if not paused:
      iters += 1;
      periodCounter += 1;

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

  if noiseStep <= 0.0:
    print("Noise step cannot be zero!");
    exit(1);

  pn = Noise1D(size, seed=seed);

  Draw(pn, multY, noiseStep);

################################################################################

if __name__ == "__main__":
  main();
