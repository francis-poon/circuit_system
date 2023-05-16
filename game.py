from enum import Enum

  
class Direction(Enum):
  UP = 0
  RIGHT = 1
  DOWN = 2
  LEFT = 3
  
  def left(self):
    return Direction((self.value-1)%4)
  
  def right(self):
    return Direction((self.value+1)%4)
  
  def opposite(self):
    return Direction((self.value+2)%4)
  
class CircuitSystem:
  
  def __init__(self):
    self.gameboard = []
    self.wire_network_list = []
    self.power_block_list = []
    self.frame_count = 0
  
  def update_frame(self):
    for power_block in power_block_list:
      power_block.update_power()
    for wire_network in wire_network_list:
      wire_network.update_power()
      
  def rotate_component(self):
  
  def add_component(self):
  
  def remove_component(self):
  
class Component:

class PowerBlock(Component):

class Wire(Component):

class WireNetwork:

  
#gameboard = []
#update_list = []
#frame_count = 0
#
#def update_frame():
#  while len(update_list > 0):
#    component = update_list[0]
#    updated_components = component.update_power(gameboard)
#    
#    for component in updated_components:
#      update_list.remove(component)
#      
#      
#def update_power(gameboard):
#  for neighbor in this.neighbors:
#    if neighbor is not null:
#      if neighbor.is_updated() and neighbor.is_powered():
#      
#      
#      
#ingest next power state for all power blocks
#for each non updated power block:
#  for each powered output direction, if there is a neighbor, power that neighbor