from PIL import Image
import random
import ast
import os
import pygame
import sys
pygame.init()
sz = 7
w = 1600
h = 1024
screen = pygame.display.set_mode([w, h])
pixels = {}

def pos_to_cell(pos):
    x = (pos[0] - w//2) // sz
    y = (pos[1] - h//2) // sz
    return (x, y)

def cell_to_pos(cx, cy):
    return cx * sz + w // 2, cy * sz + h // 2


def draw():
  global state, pics
  screen.fill(0)
  for pic in pics[::-1]:
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    for cell in pic:
      pos = cell_to_pos(*cell)
      pygame.draw.rect(screen, color, (pos[0], pos[1], sz, sz))
  pygame.display.update()

save_id = 0
while True:
  try:
    open('saves/' + str(save_id).zfill(4), 'r')
    save_id += 1
  except:
    break

try:
  save = open('current', 'r').readlines()
  state = save[0].strip()
  pics = ast.literal_eval(save[1].strip())
except:
  state = 'nil'
  pics = [[(0, 0)]]

draw()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            cell = pos_to_cell(pos)
            print("Clicked on", cell)
            (x, y) = cell
            intro = open('g.txt', 'r').read()
            intro += 'ap ap ap interact :galaxy ' + state + ' ap ap cons ' + str(x) + ' ' + str(y) + '\n'
            open('tmp/za.txt', 'w').write(intro)
            os.system('./sol <tmp/za.txt >tmp/z.hs')
            lines = open('tmp/z.hs', 'r').readlines()
            line = lines[4].strip().split()
            state = ''
            balance = 0
            ptr = 3
            while ptr < len(line):
              state += line[ptr]
              if line[ptr] == 'ap':
                balance += 1
              else:
                balance -= 1
              if balance == -1:
                break
              state += ' '
              ptr += 1
            pics = []
            pic = []
            while ptr < len(line):
              if line[ptr] == 'nil':
                if len(pic) > 0:
                  pics.append(pic)
                pic = []
                ptr += 1
                continue
              if '0' <= line[ptr][-1] <= '9':
                x = int(line[ptr])
                y = int(line[ptr + 1])
                pic.append((x, y))
                ptr += 2
                continue
              ptr += 1
            open('current', 'w').write(state + '\n' + str(pics))
            open('saves/' + str(save_id).zfill(4), 'w').write(state + '\n' + str(pics))
            save_id += 1
            draw()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                sz += 1
            if event.key == pygame.K_2 and sz > 1:
                sz -= 1
            draw()


    # res = interact(evaluated("galaxy"), res, Cons()(Number(0))(Number(0)))
    # sys.stderr.write(str(res))
    # sys.stderr.flush()
    # cnt += 1
    # res = res.val[0]
'''
while True:
  print('state =', state)
  print('pics  =', pics)
  x, y = map(int, input().split())
  print(x, y)
  intro = open('g.txt', 'r').read()
  intro += 'ap ap ap interact :galaxy ' + state + ' ap ap cons ' + str(x) + ' ' + str(y) + '\n'
  open('ga.txt', 'w').write(intro)
  os.system('sol.exe <ga.txt >souty.hs')
  lines = open('souty.hs', 'r').readlines()
  line = lines[4].strip().split()
  state = ''
  balance = 0
  ptr = 3
  while ptr < len(line):
    state += line[ptr]
    if line[ptr] == 'ap':
      balance += 1
    else:
      balance -= 1
    if balance == -1:
      break
    state += ' '
    ptr += 1
  pics = []
  pic = []
  while ptr < len(line):
    if line[ptr] == 'nil':
      if len(pic) > 0:
        pics.append(pic)
      pic = []
      ptr += 1
      continue
    if '0' <= line[ptr][-1] <= '9':
      x = int(line[ptr])
      y = int(line[ptr + 1])
      pic.append((x, y))
      ptr += 2
      continue
    ptr += 1
  open('current', 'w').write(state)
  open('ypics', 'w').write(str(pics))
  open('yzstate', 'a').write(state + '\n')
  open('yzpicss', 'a').write(str(pics) + '\n')

'''
