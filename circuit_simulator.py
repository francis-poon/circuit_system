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


circuit_system = CircuitSystem(board_width, board_height)

pg.init()
fps = 30
CLOCK = pg.time.Clock()
screen = pg.display.set_mode((window_width, window_height), 0, 32)
pg.display.set_caption("Circuit Simulator")

screen.fill(bg_color)
draw_board()
pg.display.update()

# Main gameplay update loop
while(True):
  for event in pg.event.get():
    if event.type == QUIT:
      pg.quit()
      sys.exit()
  pg.display.update()
  CLOCK.tick(fps)
