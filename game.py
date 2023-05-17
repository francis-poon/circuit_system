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
  def update_power(self):
    
  def rotate_clockwise(self):

# Power Block with powered outputs in its triggered off state
# triggered state turns on when at least one input is powered
# and its outputs are depowered one frame later
class PowerBlockNot(Component):
  def __init__(self):
    # List of which sides of the component is an input of output
    self.inputs = []
    self.outputs = []
    
    self.neighbors = {
      Direction.UP: null,
      Direction.RIGHT: null,
      Direction.DOWN: null,
      Direction.LEFT: null
    }
    
    self.triggered = False
    
  def update_power(self):
    for input_direction in inputs:
      neighbor_component = self.neighbors[input_direction]
      if neighbor_component != null and neighbor_component.is_direction_powered(input_direction.flip()):
        self.triggered = True
        break
      self.triggered = False
    
  def rotate_clockwise(self):
    for x in range(len(self.inputs)):
      self.inputs[x] = self.inputs[x].right()
    for x in range(len(self.outputs)):
      self.outputs[x] = self.outputs[x].right()
    
  def is_direction_powered(self, direction):
    return direction in self.outputs and not self.triggered
    
  def set_direction_input(self, direction):
    if direction not in self.inputs:
      self.inputs.append(direction)
    if direction in self.outputs:
      self.outputs.remote(direction)
  
  def set_direction_output(self, direction):
    if direction not in self.outputs:
      self.outputs.append(direction)
    if direction in self.inputs:
      self.inputs.remove(direction)
      
  def clear_direction_gate(self, direction):
    if direction in self.inputs:
      self.inputs.remove(direction)
    elif direction in self.outputs:
      self.outputs.remove(direction)
  
class Wire(Component):
  
class CrossedWire:
  def __init__(self, top_wire, bottom_wire):
    self.top_wire = top_wire
    self.bottom_wire = bottom_wire
    

class WireNetwork:
  def __init__(self):
    self.wire_list = [[],[],[],[],[]]
    self.wire_ids = set()

  def generate_network(self, wire):
    if wire.id not in self.wire_ids:
      self.wire_ids.add(wire.id)
      self.wire_list[wire.power_input_count] = wire
      
    for neighbor_component in wire.neighbors.values:
      if neighbor_component != null:
        if neighbor_component.isinstance(Wire):
          
        elif neighbor_component.isinstance(CrossedWire):
          
  
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