version = 0.1 # df april 2023

import sys
import signal
import argparse
from lcd import LCD as LCD
from ubo_keypad import *
from PIL import Image
from time import sleep
from random import getrandbits
from shutil import get_terminal_size

lcd = LCD()
button_pressed = False

class simple_keypad(KEYPAD):
  def __init__(self, *args, **kwargs):
    super(simple_keypad, self).__init__(*args, **kwargs)
  def button_event(self):
    global button_pressed
    button_pressed = True
    print('xxxxxx', self.buttonPressed)
    return self.buttonPressed

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

def convolve(src, dst, blocks):
  for i, block in enumerate(blocks):
    cells = tuple(src[j] for j in block)
    dst[i] = conway(cells)

def display_text(buffer, rows, cols, on='*', off=' '):
  output = []
  j = 0
  for i in range(rows):
    k = j + cols
    output.append(' '.join( tuple( (off, on)[buffer[x]] for x in range(j, k) ) ) )
    j = k
  print('\033[1;1f', end='') # move cursor to top left  
  print('\n'.join(output), end='')

def display_lcd(buffer, rows, cols, on_color='green', off_color='black'):
  width = height = 240
  base = Image.new("RGBA", (width, height), (0, 0, 0))
  overlay = Image.new("RGBA", base.size, (255, 255, 255, 0))
  txt = Image.new("RGBA", base.size, (255, 255, 255, 0))
  radius = min( width // (cols * 2), height // (rows * 2) )
  x_offset = width - (radius * 2 * cols)
  y_offset = height - (radius * 2 * cols)
  x = x_offset // 2
  k = 0
  for i in range(rows):
    y = y_offset // 2
    for j in range(cols):
      coordinates = (x, y)
      color = on_color if buffer[k] else off_color
      cell = lcd.ellipse(radius, fill=color)
      overlay.paste(cell, coordinates)
      k += 1
      y += (radius * 2)
    x += (radius * 2)
  out = Image.alpha_composite(base, txt)
  out.paste(overlay, (0, 0), overlay)
  out = out.transpose(method=0).rotate(90).convert('RGB')
  # out = out.convert('RGB')
  lcd.show_image(out)

def randomize(buffer):
  n = len(buffer)
  r = getrandbits(n)
  for i in range(n):
    buffer[i] = r & 1
    r >>= 1

def evolve(rows, cols, buffers, blocks, on='*', off=' ', on_color='green', off_color='black', delay=0.333):
  toggle = 0
  global button_pressed
  while True:
    src = buffers[toggle]
    # display_text(src, rows, cols, on, off)
    display_lcd(src, rows, cols, on_color, off_color)
    toggle = 1 - toggle
    dst = buffers[toggle]
    convolve(src, dst, blocks)
    sleep(delay)
    if button_pressed:
      randomize(dst)
      button_pressed = False      

def cleanup(sig, frame):
  print('\033[?25h', end='') # restore cursor
  print()
  sys.exit(0)

def main(argv, argc):
  parser = argparse.ArgumentParser(description='conway\'s game of life')
  parser.add_argument('--cols', type=int, default=0, help='cols default $COLUMNS / 2')
  parser.add_argument('--rows', type=int, default=0, help='rows default $LINES')
  parser.add_argument('--on', type=str, default='*', help='on default \'*\'')
  parser.add_argument('--off', type=str, default=' ', help='off default \' \'')
  parser.add_argument('--on_color', type=str, default='green', help='on default \'*\'')
  parser.add_argument('--off_color', type=str, default='black', help='off default \' \'')
  parser.add_argument('--delay', type=float, default=0.333, help='delay default 0.333')
  parser.add_argument('--version', action='store_true', help=str(version))
  args = parser.parse_args()

  if args.version:
    print(version)
    exit(0)

  rows = args.rows
  cols = args.cols
  if rows == 0 or cols == 0:
    size = get_terminal_size((80, 24))
    if rows == 0: rows = size.lines
    if cols == 0: cols = size.columns // 2
  on = args.on
  off = args.off
  on_color = args.on_color
  off_color = args.off_color
  delay = args.delay

  num_cells = rows * cols 
  buffers = ([0] * num_cells, [0] * num_cells)
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
  evolve(rows, cols, buffers, blocks, on, off, on_color, off_color, delay)

if __name__ == '__main__':
  main(sys.argv, len(sys.argv))
