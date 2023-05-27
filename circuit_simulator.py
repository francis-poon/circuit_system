import pygame as pg
import sys
from pygame.locals import *
from game_logic import CircuitSystem, Wire, OverlappedWire, PowerBlockNot, Direction

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

power_block_assets = {
  PowerBlockNot: {
    False: pg.transform.scale(pg.image.load("assets/depowered_power_block_not.png"), (component_width, component_height)),
    True: pg.transform.scale(pg.image.load("assets/powered_power_block_not.png"), (component_width, component_height))
  },
  'INPUT': {
    False: pg.transform.scale(pg.image.load("assets/depowered_power_block_input.png"), (component_width, component_height)),
    True: pg.transform.scale(pg.image.load("assets/powered_power_block_input.png"), (component_width, component_height))
  },
  'OUTPUT': {
    False: pg.transform.scale(pg.image.load("assets/depowered_power_block_output.png"), (component_width, component_height)),
    True: pg.transform.scale(pg.image.load("assets/powered_power_block_output.png"), (component_width, component_height))
  }
}

def draw_wire(wire):
  image = wire_assets[wire.configuration][True]
  image = pg.transform.rotate(image, (wire.rotation*90)%360*-1)
  return [image]
  
def draw_overlapped_wire(overlapped_wire):
  bottom_image = draw_wire(overlapped_wire.bottom_wire)
  top_image = draw_wire(overlapped_wire.top_wire)
  return bottom_image + top_image
  
def draw_power_block(power_block):
  images = []
  images.append(power_block_assets[type(power_block)][True])
  for input in power_block.inputs:
    images.append(
      pg.transform.rotate(power_block_assets['INPUT'][True], (input.value - 1)*90 % 360 * -1)
    )
  for output in power_block.outputs:
    images.append(
      pg.transform.rotate(power_block_assets['OUTPUT'][True], (output.value - 1)*90 % 360 * -1)
    )
    
  return images

def draw_component(board_width, board_height, component):
  switch = {
    Wire: draw_wire,
    OverlappedWire: draw_overlapped_wire,
    PowerBlockNot: draw_power_block
  }
  
  images = switch[type(component)](component)
  position = board_width*component_width, board_height*component_height
  for image in images:
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
overlapped_wire = OverlappedWire(wire_a, wire_c)
power_block_not = PowerBlockNot()
power_block_not.set_direction_input(Direction.UP)
power_block_not.set_direction_output(Direction.DOWN)
power_block_not.set_direction_output(Direction.RIGHT)
power_block_not.rotate_clockwise()
power_block_not.rotate_clockwise()
power_block_not.rotate_clockwise()
circuit_system.add_component(wire_a, 0, 0)
circuit_system.add_component(wire_b, 1, 0)
circuit_system.add_component(wire_c, 2, 0)
circuit_system.add_component(overlapped_wire, 0, 1)
circuit_system.add_component(power_block_not, 1, 1)

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
