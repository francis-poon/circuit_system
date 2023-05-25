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
  
  def set_neighbor(self, direction, component):
    self.neighbors[direction] = component
    
  def remove_neighbor(self, direction):
    self.neighbors[direction] = null
  
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
  class Configuration(Enum):
    NUB = [Direction.LEFT]
    STRAIGHT = [Direction.LEFT, Direction.RIGHT]
    BEND = [Direction.LEFT, Direction.DOWN]
    T_INTERSECT = [Direction.LEFT, Direction.RIGHT, Direction.DOWN]
    CROSS = [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]
    
  def __init__(self, network=null, configuration=Configuration.STRAIGHT):
    self.network = network
    self.connections = configuration.value
    self.power_input_count
    
    self.neighbors = {
      Direction.UP: null,
      Direction.RIGHT: null,
      Direction.DOWN: null,
      Direction.LEFT: null
    }
    
  def rotate_clockwise(self):
    for x in range(len(self.connections)):
      self.connections[x] = self.connections[x].right()
  
  def set_neighbor(self, direction, component):
    self.neighbors[direction] = component
    
  def remove_neighbor(self, direction):
    self.neighbors[direction] = null
  
  def is_direction_powered(self, direction):
    return self.has_connection(direction) and self.network.is_powered
    
  def has_connection(self, direction):
    return direction in self.connections
    
  def has_network(self):
    return network == null
  
class OverlappedWire:
  def __init__(self, top_wire, bottom_wire):
    self.top_wire = top_wire
    self.bottom_wire = bottom_wire
    
  def rotate_clockwise(self):
    self.topwire.rotate_clockwise()
    self.bottom_wire.rotate_clockwise()
    
  def is_direction_powered(self, direction):
    return self.get_wire(direction).is_direction_powered(direction)
  
  def get_wire(self, direction):
    if self.top_wire.has_connection(direction):
      return self.top_wire
    else:
      return self.bottom_wire

class WireNetwork:
  def __init__(self):
    self.wire_list = [{},{},{},{},{}]
    self.wire_ids = set()
    
    self.is_powered = False

  def update_power(self):
    for power_input_count in range(len(self.wire_list), 0):
      for wire in self.wire_list[power_input_count]:
        if wire.has_powered_input:
          self.is_powered = True
          return
    self.is_powered = False

  def generate_network(self, wire):
    if wire.id not in self.wire_ids:
      self.wire_ids.add(wire.id)
      self.wire_list[wire.power_input_count].append(wire)
      
      # Recursively add neighbors to network if they are a wire and aren't part of the network yet
      for input_direction in wire.connections:
        neighbor_component = wire.neighbors[input_direction]
        neighbor_wire = null
        if neighbor_component != null:
          if neighbor_component.isinstance(Wire):
            self.generate_network(neighbor_component)
          elif neighbor_component.isinstance(OverlappedWire):
            self.generate_network(neighbor_component.get_wire(input_direction.flip()))

  def add_wire(self, wire):
    if component.isinstance(Wire) and wire.network != self:
      self.wire_list[wire.power_input_count].append(wire)
      wire.network = self
      
      
  
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