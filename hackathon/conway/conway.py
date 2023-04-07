version = 0.1 # df april 2023

import sys
import signal
import argparse
from time import sleep
from random import getrandbits
from shutil import get_terminal_size

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

def display(buffer, rows, cols, on='*', off=' '):
  output = []
  j = 0
  for i in range(rows):
    k = j + cols
    output.append(' '.join( tuple( (off, on)[buffer[x]] for x in range(j, k) ) ) )
    j = k
  print('\033[1;1f', end='') # move cursor to top left  
  print('\n'.join(output), end='')

def evolve(rows, cols, buffers, blocks, on='*', off=' ', delay=0.333):
  toggle = 0
  while True:
    src = buffers[toggle]
    display(src, rows, cols, on, off)
    toggle = 1 - toggle
    dst = buffers[toggle]
    convolve(src, dst, blocks)
    sleep(delay)

def randomize(buffer):
  n = len(buffer)
  r = getrandbits(n)
  for i in range(n):
    buffer[i] = r & 1
    r >>= 1

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
  delay = args.delay

  num_cells = rows * cols 
  buffers = ([0] * num_cells, [0] * num_cells)
  blocks = tuple( block(i, rows, cols) for i in range(num_cells) )

  signal.signal(signal.SIGINT, cleanup)
  print('\033[2J', end='') # clear screen
  print('\033[?25l', end='') # hide cursor

  randomize(buffers[0])
  evolve(rows, cols, buffers, blocks, on, off, delay)

if __name__ == '__main__':
  main(sys.argv, len(sys.argv))
