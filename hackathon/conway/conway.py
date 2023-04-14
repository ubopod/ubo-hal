version = 0.5 # df april 2023

import sys
import signal
import argparse
from lcd import LCD
from PIL import Image, ImageDraw
from simple_keypad import simple_KEYPAD
from time import sleep
from random import getrandbits

class grid_display(LCD):
  def __init__(self, *args, **kwargs):
    super(grid_display, self).__init__(*args, **kwargs)
    self.width = 240
    self.height = 240
    self.base = Image.new("RGBA", (self.width, self.height), (0, 0, 0))
    self.overlay = Image.new("RGBA", self.base.size, (255, 255, 255, 0))

  def draw_cell(self, diameter, color):
    c = Image.new('RGB', (diameter, diameter), (0, 0, 0, 0))
    ImageDraw.Draw(c).ellipse(
      (0, 0, diameter - 2, diameter - 2),
      fill = color,
      outline = None,
      width = 0)
    return c

  def display_cells(self, buffer, rows = 16, cols = 16,
                    on_color = 'green', off_color = 'black'):
    cell_diameter = min(self.width // cols, self.height // rows)
    x_offset = (self.width - (cell_diameter * cols)) // 2
    y_offset = (self.height - (cell_diameter * rows)) // 2
    k = 0
    x = x_offset
    for i in range(rows):
      y = y_offset
      for j in range(cols):
        color = on_color if buffer[k] else off_color
        cell = self.draw_cell(cell_diameter, color)
        self.overlay.paste(cell, (x, y))
        k += 1
        y += cell_diameter 
      x += cell_diameter
    out = Image.alpha_composite(self.base, self.overlay)
    # method 0: FLIP_LEFT_RIGHT 
    out = out.transpose(method=0).rotate(90).convert('RGB')
    lcd.show_image(out)

####

class simple_keypad(simple_KEYPAD):
  def __init__(self, *args, **kwargs):
    super(simple_keypad, self).__init__(*args, **kwargs)

  def button_event(self):
    global button_pressed
    button_pressed = True
    print('button pressed', self.buttonPressed)
    return self.buttonPressed

####

# some globals, for now
# (moving stuff around, classes in flux)

lcd = grid_display()
button_pressed = False

def block(i, rows, cols):
  row = i // cols
  col = i % cols
  up = (row - 1) % rows
  down = (row + 1) % rows
  left = (col - 1) % cols
  right = (col + 1) % cols
  return tuple( (row * cols) + col for row, col in (
    (up, left),   (up, col),   (up, right),
    (row, left),  (row, col),  (row, right),
    (down, left), (down, col), (down, right) ) )

def conway(three_by_three):
  center = three_by_three[4]
  n = sum(three_by_three) - center
  if n < 2 or n > 3:
    center = 0
  elif n == 3:
    center = 1
  return center

def highlife(three_by_three):
  #
  # the highlife ruleset is a variation on conway's game of life
  # see https://en.wikipedia.org/wiki/Life-like_cellular_automaton
  #
  center = three_by_three[4]
  n = sum(three_by_three) - center
  if n < 2 or n > 3:
    center = 0
  elif n == 3 or n == 6:
    center = 1
  return center

def convolve(src, dst, blocks, ruleset = 'conway'):
  if ruleset == 'conway':
    fn = conway
  elif ruleset == 'highlife':
    fn = highlife
  for i, block in enumerate(blocks):
    cells = tuple(src[j] for j in block)
    dst[i] = fn(cells)

def randomize(buffer):
  n = len(buffer)
  r = getrandbits(n)
  for i in range(n):
    buffer[i] = r & 1
    r >>= 1

def cycle_detection(buffers):
  unique = False
  a, b, c = buffers
  for i in range(len(a)):
    if a[i] != b[i]:
      unique = True
      break
  if unique == True:
    unique = False
    for i in range(len(a)):
      if a[i] != c[i]:
        unique = True
        break
  return False if unique else True

def evolve(rows, cols, buffers, blocks,
           on_color = 'yellow', off_color = 'purple',
           ruleset = 'conway', delay=0.2):
  troggle = 0
  global button_pressed

  while True:
    src = buffers[troggle]
    lcd.display_cells(src, rows, cols, on_color, off_color)
    troggle += 1
    if troggle > 2:
      troggle = 0
    dst = buffers[troggle]
    convolve(src, dst, blocks, ruleset)
    sleep(delay)
    if button_pressed:
      troggle = 0
      randomize(buffers[troggle])
      button_pressed = False      
    if cycle_detection(buffers):
      troggle = 0
      randomize(buffers[troggle])

def cleanup(sig, frame):
  print('\033[?25h', end='') # restore cursor
  print()
  sys.exit(0)

def main(argv, argc):
  parser = argparse.ArgumentParser(description='conway\'s game of life')
  parser.add_argument('--cols', type=int, default=20, help='cols default 20')
  parser.add_argument('--rows', type=int, default=20, help='rows default 20')
  parser.add_argument('--on_color', type=str, default='yellow', help='on default yellow')
  parser.add_argument('--off_color', type=str, default='purple', help='off default purple')
  parser.add_argument('--ruleset', type=str, default='conway', help='ruleset default conway')
  parser.add_argument('--delay', type=float, default=0.2, help='delay default 0.2')
  parser.add_argument('--version', action='store_true', help=str(version))
  args = parser.parse_args()

  if args.version:
    print(version)
    exit(0)

  rows = args.rows
  cols = args.cols
  on_color = args.on_color
  off_color = args.off_color
  ruleset = args.ruleset
  delay = args.delay

  num_cells = rows * cols 
  # pre-allocate 3 buffers
  buffers = ([0] * num_cells, [0] * num_cells, [0] * num_cells)
  blocks = tuple( block(i, rows, cols) for i in range(num_cells) )

  signal.signal(signal.SIGINT, cleanup)
  print('\033[2J', end='') # clear screen
  print('\033[?25l', end='') # hide cursor

  try:
    keypad = simple_keypad()
  except:
    # did not detect keypad on i2c bus
    print("failed to initialize keypad")
  if keypad.bus_address ==  False:
    print("keypad bus_address False")

  randomize(buffers[0])
  evolve(rows, cols, buffers, blocks, on_color, off_color, ruleset, delay)

if __name__ == '__main__':
  main(sys.argv, len(sys.argv))
