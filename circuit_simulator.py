import pygame as pg
import sys
from pygame.locals import *
from game_logic import CircuitSystem, Wire, OverlappedWire, PowerBlockNot, Direction

class CircuitSimulator:
  def __init__(self, board_width=None, board_height=None):
    self.system = CircuitSystem(cols=board_width, rows=board_height)
    self.board_width, self.board_height = board_width, board_height
    self.component_width, self.component_height = 64, 64
    self.window_width, self.window_height = self.board_width*self.component_width, self.board_height*self.component_height
    
    self.bg_color = (255, 255, 255)

    self.wire_assets = {
      Wire.Configuration.STRAIGHT: {
        False: pg.transform.scale(pg.image.load("assets/depowered_straight.png"), (self.component_width, self.component_height)),
        True: pg.transform.scale(pg.image.load("assets/powered_straight.png"), (self.component_width, self.component_height))
      },
      Wire.Configuration.BEND: {
        False: pg.transform.scale(pg.image.load("assets/depowered_bend.png"), (self.component_width, self.component_height)),
        True: pg.transform.scale(pg.image.load("assets/powered_bend.png"), (self.component_width, self.component_height))
      },
      Wire.Configuration.T_INTERSECT: {
        False: pg.transform.scale(pg.image.load("assets/depowered_t_intersect.png"), (self.component_width, self.component_height)),
        True: pg.transform.scale(pg.image.load("assets/powered_t_intersect.png"), (self.component_width, self.component_height))
      },
      Wire.Configuration.CROSS: {
        False: pg.transform.scale(pg.image.load("assets/depowered_cross.png"), (self.component_width, self.component_height)),
        True: pg.transform.scale(pg.image.load("assets/powered_cross.png"), (self.component_width, self.component_height))
      },
      Wire.Configuration.NUB: {
        False: pg.transform.scale(pg.image.load("assets/depowered_nub.png"), (self.component_width, self.component_height)),
        True: pg.transform.scale(pg.image.load("assets/powered_nub.png"), (self.component_width, self.component_height))
      }
    }
  
    self.power_block_assets = {
      PowerBlockNot: {
        False: pg.transform.scale(pg.image.load("assets/depowered_power_block_not.png"), (self.component_width, self.component_height)),
        True: pg.transform.scale(pg.image.load("assets/powered_power_block_not.png"), (self.component_width, self.component_height))
      },
      'INPUT': {
        False: pg.transform.scale(pg.image.load("assets/depowered_power_block_input.png"), (self.component_width, self.component_height)),
        True: pg.transform.scale(pg.image.load("assets/powered_power_block_input.png"), (self.component_width, self.component_height))
      },
      'OUTPUT': {
        False: pg.transform.scale(pg.image.load("assets/depowered_power_block_output.png"), (self.component_width, self.component_height)),
        True: pg.transform.scale(pg.image.load("assets/powered_power_block_output.png"), (self.component_width, self.component_height))
      }
    }
  
  def draw_wire(self, wire):
    image = self.wire_assets[wire.configuration][wire.is_powered()]
    image = pg.transform.rotate(image, (wire.rotation*90)%360*-1)
    return [image]
    
  def draw_overlapped_wire(self, overlapped_wire):
    bottom_image = self.draw_wire(overlapped_wire.bottom_wire)
    top_image = self.draw_wire(overlapped_wire.top_wire)
    return bottom_image + top_image
    
  # TODO: Rename to power_block_not
  def draw_power_block(self, power_block):
    images = []
    images.append(self.power_block_assets[type(power_block)][power_block.triggered])
    for input in power_block.inputs:
      input_power = power_block.neighbors[input] != None and power_block.neighbors[input].is_direction_powered(input.opposite())
      images.append(
        pg.transform.rotate(self.power_block_assets['INPUT'][input_power], (input.value - 1)*90 % 360 * -1)
      )
    for output in power_block.outputs:
      images.append(
        pg.transform.rotate(self.power_block_assets['OUTPUT'][not power_block.triggered], (output.value - 1)*90 % 360 * -1)
      )
      
    return images
  
  def draw_component(self, board_width, board_height, component):
    switch = {
      Wire: self.draw_wire,
      OverlappedWire: self.draw_overlapped_wire,
      PowerBlockNot: self.draw_power_block
    }
    
    images = switch[type(component)](component)
    position = board_width*self.component_width, board_height*self.component_height
    for image in images:
      screen.blit(image, position)
    
  def draw_board(self, circuit_board):
    for height in range(len(circuit_board)):
      for width in range(len(circuit_board[height])):
        if circuit_board[height][width] != None:
          self.draw_component(width, height, circuit_board[height][width])
          
  def handle_key_down(self, key):
    if key == 13:
      self.system.update_frame()
      self.draw_board(self.system.circuit_board)
      pg.display.update()
    else:
      print(key)

# Setting up a test circuit board
sim = CircuitSimulator(board_width=3, board_height=2)
wire_a = Wire(configuration=Wire.Configuration.BEND, rotation=3)
wire_b = Wire(configuration=Wire.Configuration.BEND, rotation=0)
wire_c = Wire(configuration=Wire.Configuration.BEND, rotation=2)
wire_d = Wire(configuration=Wire.Configuration.STRAIGHT, rotation=0)
wire_e = Wire(configuration=Wire.Configuration.BEND, rotation=1)
power_block_not = PowerBlockNot()
power_block_not.set_direction_input(Direction.LEFT)
power_block_not.set_direction_output(Direction.RIGHT)
sim.system.enable_edit()
sim.system.add_component(wire_a, row=0, col=0)
sim.system.add_component(power_block_not, row=0, col=1)
sim.system.add_component(wire_b, row=0, col=2)
sim.system.add_component(wire_c, row=1, col=0)
sim.system.add_component(wire_d, row=1, col=1)
sim.system.add_component(wire_e, row=1, col=2)
sim.system.save_edit()

pg.init()
fps = 30
CLOCK = pg.time.Clock()
screen = pg.display.set_mode((sim.window_width, sim.window_height), 0, 32)
pg.display.set_caption("Circuit Simulator")

screen.fill(sim.bg_color)
sim.draw_board(sim.system.circuit_board)
pg.display.update()

# Main gameplay update loop
while(True):
  for event in pg.event.get():
    if event.type == QUIT:
      pg.quit()
      sys.exit()
    elif event.type == KEYDOWN:
      sim.handle_key_down(event.key)
  pg.display.update()
  CLOCK.tick(fps)
