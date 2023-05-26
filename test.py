import pygame as pg
import sys
import numpy as np
from pygame.locals import *

board_width, board_height = 3, 4
board = [[None] * board_width for x in range(board_height)]

component_width, component_height = 64, 64
window_width, window_height = board_width*component_width, board_height*component_height

bg_color = (255,255,255)
line_color = (0,0,0)

pg.init()

fps = 30
CLOCK = pg.time.Clock()
screen = pg.display.set_mode((window_width, window_height), 0, 32)
pg.display.set_caption("Circuit Test")

board_assets = {
  'straight': {
    False: pg.transform.scale(pg.image.load("assets/depowered_straight.png"), (component_width, component_height)),
    True: pg.transform.scale(pg.image.load("assets/powered_straight.png"), (component_width, component_height))
  },
  'bend': {
    False: pg.transform.scale(pg.image.load("assets/depowered_bend.png"), (component_width, component_height)),
    True: pg.transform.scale(pg.image.load("assets/powered_bend.png"), (component_width, component_height))
  },
  't_intersect': {
    False: pg.transform.scale(pg.image.load("assets/depowered_t_intersect.png"), (component_width, component_height)),
    True: pg.transform.scale(pg.image.load("assets/powered_t_intersect.png"), (component_width, component_height))
  },
  'cross': {
    False: pg.transform.scale(pg.image.load("assets/depowered_cross.png"), (component_width, component_height)),
    True: pg.transform.scale(pg.image.load("assets/powered_cross.png"), (component_width, component_height))
  },
  'nub': {
    False: pg.transform.scale(pg.image.load("assets/depowered_nub.png"), (component_width, component_height)),
    True: pg.transform.scale(pg.image.load("assets/powered_nub.png"), (component_width, component_height))
  }
}

asset_names = list(board_assets.keys())
asset_index = 0
power = False
move = False
position = (window_width/2-component_width/2, window_height/2-component_height/2)
rotate = 0

component = {
  'asset_name': 'straight',
  'power': False,
  'rotation': 0
}


board[0] = [component]*board_width
board = [[{'asset_name': 'bend', 'power': False, 'rotation': 2}, {'asset_name': 't_intersect', 'power': False, 'rotation': 0}, {'asset_name': 'straight', 'power': False, 'rotation': 0}],
         [{'asset_name': 'straight', 'power': False, 'rotation': 0}, {'asset_name': 't_intersect', 'power': False, 'rotation': 2}, {'asset_name': 'straight', 'power': False, 'rotation': 0}],
         [None, None, None]]
  
def user_click(button):
  if event.button == 1:
    global move, position
    move = True
    position = tuple(np.subtract(pg.mouse.get_pos(), component_width/2))
    
  #elif event.button == 3:
    
  elif event.button == 4 or event.button == 5:
    global asset_index
    index_mod = (event.button - 4) * 2 - 1
    asset_index = (asset_index + index_mod) % len(asset_names)
  
  draw_component()

def user_unclick(button):
  if event.button == 1:
    global move, position
    move = False
    position = snap_position()
    draw_component()
    
def snap_position():
  pos = pg.mouse.get_pos()
  return (int(pos[0]/component_width)*component_width, int(pos[1]/component_height)*component_height)
    
def user_move():
  if move:
    global position
    position = tuple(np.subtract(pg.mouse.get_pos(), component_width/2))
    draw_component()
    
def user_key_press(key):
  if key == 114:
    global rotate
    rotate = (rotate + 1) % 4
  elif key == 13:
    global board
    for row in board:
      for component in row:
        if component != None:
          component['power'] = not component['power']
    
  draw_board()
    
def draw_component():
  screen.fill(bg_color)
  image = board_assets[asset_names[asset_index]][power]
  image = pg.transform.rotate(image, rotate*90*-1)
  screen.blit(image, position)
  
def draw_grid_section(board_width, board_height, component):
  position = board_width*component_width, board_height*component_height
  image = board_assets[component['asset_name']][component['power']]
  image = pg.transform.rotate(image, (component['rotation']*90)%360*-1)
  screen.blit(image, position)
  
def draw_board():
  for height in range(len(board)):
    for width in range(len(board[height])):
      if board[height][width] != None:
        draw_grid_section(width, height, board[height][width])
  
  
screen.fill(bg_color)
draw_board()
#screen.blit(board_assets[asset_names[asset_index]][power], position)
pg.display.update()

while(True):
  for event in pg.event.get():
    #print("Processing Event {}".format(event.type))
    if event.type == QUIT:
      pg.quit()
      sys.exit()
#    elif event.type == MOUSEBUTTONDOWN:
#      user_click(event.button)
#    elif event.type == MOUSEBUTTONUP:
#      user_unclick(event.button)
#    elif event.type == MOUSEMOTION:
#      user_move()
    elif event.type == KEYDOWN:
      user_key_press(event.key)
  pg.display.update()
  CLOCK.tick(fps)