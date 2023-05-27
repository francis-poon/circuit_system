import pygame as pg
import sys
from pygame.locals import *
from game_logic import Wire, CircuitSystem

board_width, board_height = 3, 3
component_width, component_height = 64, 64
window_width, window_height = board_width*component_width, board_height*component_height

bg_color = (255, 255, 255)

wire_assets = {
  Wire.Configuration.STRAIGHT: {
    False: pg.transform.scale(pg.image.load("assets/depowered_straight.png"), (component_width, component_height)),
    True: pg.transform.scale(pg.image.load("assets/powered_straight.png"), (component_width, component_height))
  },
  Wire.Configuration.BEND: {
    False: pg.transform.scale(pg.image.load("assets/depowered_bend.png"), (component_width, component_height)),
    True: pg.transform.scale(pg.image.load("assets/powered_bend.png"), (component_width, component_height))
  },
  Wire.Configuration.T_INTERSECT: {
    False: pg.transform.scale(pg.image.load("assets/depowered_t_intersect.png"), (component_width, component_height)),
    True: pg.transform.scale(pg.image.load("assets/powered_t_intersect.png"), (component_width, component_height))
  },
  Wire.Configuration.CROSS: {
    False: pg.transform.scale(pg.image.load("assets/depowered_cross.png"), (component_width, component_height)),
    True: pg.transform.scale(pg.image.load("assets/powered_cross.png"), (component_width, component_height))
  },
  Wire.Configuration.NUB: {
    False: pg.transform.scale(pg.image.load("assets/depowered_nub.png"), (component_width, component_height)),
    True: pg.transform.scale(pg.image.load("assets/powered_nub.png"), (component_width, component_height))
  }
}

def draw_wire(wire):
  image = wire_assets[wire.configuration][True]
  image = pg.transform.rotate(image, (wire.rotation*90)%360*-1)
  return image

def draw_component(board_width, board_height, component):
  switch = {
    Wire: draw_wire
  }
  
  image = switch[type(component)](component)
  position = board_width*component_width, board_height*component_height
  screen.blit(image, position)
  
def draw_board(circuit_board):
  for height in range(len(circuit_board)):
    for width in range(len(circuit_board[height])):
      if circuit_board[height][width] != None:
        draw_component(width, height, circuit_board[height][width])

# Setting up a test circuit board
circuit_system = CircuitSystem(board_width, board_height)
wire_a = Wire()
wire_b = Wire()
wire_c = Wire()
wire_c.rotate_clockwise()
circuit_system.add_component(wire_a, 0, 0)
circuit_system.add_component(wire_b, 1, 0)
circuit_system.add_component(wire_c, 2, 0)

pg.init()
fps = 30
CLOCK = pg.time.Clock()
screen = pg.display.set_mode((window_width, window_height), 0, 32)
pg.display.set_caption("Circuit Simulator")

screen.fill(bg_color)
draw_board(circuit_system.circuit_board)
pg.display.update()

# Main gameplay update loop
while(True):
  for event in pg.event.get():
    if event.type == QUIT:
      pg.quit()
      sys.exit()
  pg.display.update()
  CLOCK.tick(fps)
