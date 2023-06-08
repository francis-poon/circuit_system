from enum import Enum
import pickle
  
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
  
  def __init__(self, rows=0, cols=0):
    self.circuit_board = CircuitBoard(rows=rows, cols=cols)
    self.wire_network_list = []
    self.wires = [set(), set()]
    self.power_block_list = []
    self.frame_count = 0
    self.editting = False
    self.save_state = None
    
  def enable_edit(self):
    if self.editing == False:
      self.save_state = None
      self.save_state = pickle.dumps(self.__dict__)
      self.editing = True
    
  def cancel_edit(self):
    if self.editing == True:
      self.__dict__ = pickle.loads(self.save_state)
      self.save_state = None
      self.editting = False
    
  def save_edit(self):
    self.wire_network_list = []
    
    while len(self.wires[0]) > 0:
      wire = self.wires[0].pop()
      self.wires[1].add(wire)
      
      network = WireNetwork()
      WireNetwork.generate_network(wire, network)
      self.wire_network_list.append(network)
      self.wires[1] = self.wires[1] | network.get_wires()
      self.wires[0] = self.wires[0] - network.get_wires()
      
    self.wires[0] = self.wires[1]
    self.wires[1] = {}
    
    self.save_state = None
    self.editing = False
  
  def update_frame(self):
    for power_block in power_block_list:
      power_block.update_power()
    for wire_network in wire_network_list:
      wire_network.update_power()
    frame_count += 1
      
  def rotate_component(self):
    # rotate component
    # if component was a wire, add wire to "recheck network" set
    # overlapped wire will need to do this check if the overlapped wires are bends, but if they're straights, just swap their networks
    return None
  def add_component(self, component, col, row):
    self.circuit_board[row][col] = component
    for direction in Direction:
      neighbor = self.circuit_board.get_direction(row, col, direction)
      if neighbor != None:
        component.set_neighbor(direction, neighbor)
        neighbor.set_neighbor(direction.opposite(), component)
  
  def remove_component(self):
    return None
  
class CircuitBoard:
  def __init__(self, rows=0, cols=0):
    self.board = [[None] * cols for x in range(rows)]
    
  def __getitem__(self, key):
    return self.board[key]
    
  def __setitem__(self, key, val):
    self.board[key] = val
    
  def __delitem__(self, key):
    self.board[key] = None
    
  def __len__(self):
    return len(self.board)
    
  def get_direction(self, row, col, direction):
    if direction == Direction.UP and row-1 >= 0:
      return self.board[row-1][col]
    if direction == Direction.RIGHT and col+1 < len(self.board[row]):
      return self.board[row][col+1]
    if direction == Direction.DOWN and row+1 < len(self.board):
      return self.board[row+1][col]
    if direction == Direction.LEFT and col-1 >= 0:
      return self.board[row][col-1]
    return None
    
  
# TODO: consolidate actual Component parent variables and methods
# TODO: Have children use/overwrite Component variables and methods
class Component:
  def __init__(self):
    self.neighbors = {
      Direction.UP: None,
      Direction.RIGHT: None,
      Direction.DOWN: None,
      Direction.LEFT: None
    }
    
  def update_power(self):
    return None
  def rotate_clockwise(self):
    return None
    

class PowerBlock(Component):
  def __init__(self):
    # TODO: Figure out how to use parent class self.neighbors variable
    self.inputs = []
    self.outputs = []
    
    self.update_queue = []
    self.triggered = False
    
  def is_direction_output(self, direction):
    return direction in self.outputs

# Power Block with powered outputs in its triggered off state
# triggered state turns on when at least one input is powered
# and its outputs are depowered one frame later
class PowerBlockNot(PowerBlock):
  def __init__(self):
    # List of which sides of the component is an input of output
    self.inputs = []
    self.outputs = []
    
    self.neighbors = {
      Direction.UP: None,
      Direction.RIGHT: None,
      Direction.DOWN: None,
      Direction.LEFT: None
    }
    
    self.update_queue = []
    self.triggered = False
    
  def update_power(self):
    self.triggered = self.update_queue.pop(0) if len(self.update_queue) > 0 else False
    update_value = False
    for input_direction in inputs:
      neighbor_component = self.neighbors[input_direction]
      if neighbor_component != None and neighbor_component.is_direction_powered(input_direction.opposite()):
        update_value = True
        break
    self.update_queue.append(update_value)
    
  def rotate_clockwise(self):
    for x in range(len(self.inputs)):
      self.inputs[x] = self.inputs[x].right()
    for x in range(len(self.outputs)):
      self.outputs[x] = self.outputs[x].right()
  
  def set_neighbor(self, direction, component):
    self.neighbors[direction] = component
    
  def remove_neighbor(self, direction):
    self.neighbors[direction] = None
  
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
    
  def __init__(self, network=None, configuration=Configuration.STRAIGHT):
    self.id = 0 # TODO: Generate UUID
    self.network = network
    self.configuration = configuration
    self.connections = configuration.value
    self.rotation = 0
    
    self.neighbors = {
      Direction.UP: None,
      Direction.RIGHT: None,
      Direction.DOWN: None,
      Direction.LEFT: None
    }
    
  def count_power_inputs(self):
    power_input_count = 0
    for connection in self.connections:
      if self.neighbors[connection] != None and isinstance(self.neighbors[connection], PowerBlock)
      and self.neighbors[connection].is_direction_output(connection.opposite()):
        power_input_count += 1
    return power_input_count
    
  def rotate_clockwise(self):
    self.rotation = (self.rotation + 1) % 4
    for x in range(len(self.connections)):
      self.connections[x] = self.connections[x].right()
  
  def set_neighbor(self, direction, component):
    self.neighbors[direction] = component
    
  def remove_neighbor(self, direction):
    self.neighbors[direction] = None
  
  def is_powered(self):
    return self.network.is_powered()
  
  def is_direction_powered(self, direction):
    return self.has_connection(direction) and self.network.is_powered()
    
  def has_connection(self, direction):
    return direction in self.connections
    
  def has_network(self):
    return network == None
  
class OverlappedWire:
  def __init__(self, top_wire, bottom_wire):
    self.top_wire = top_wire
    self.bottom_wire = bottom_wire
    
  def rotate_clockwise(self):
    self.topwire.rotate_clockwise()
    self.bottom_wire.rotate_clockwise()
    
  def set_neighbor(self, direction, neighbor):
    self.top_wire.set_neighbor(direction, neighbor)
    self.bottom_wire.set_neighbor(direction, neighbor)
    
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

  def is_powered(self):
    return self.is_powered

  def update_power(self):
    for power_input_count in range(len(self.wire_list), 0):
      for wire in self.wire_list[power_input_count]:
        if wire.has_powered_input:
          self.is_powered = True
          return
    self.is_powered = False

  @classmethod
  def generate_network(cls, wire, network):
    if wire.id not in network.wire_ids:
      network.add_wire(wire)
      
      # Recursively add neighbors to network if they are a wire and aren't part of the network yet
      for input_direction in wire.connections:
        neighbor_component = wire.neighbors[input_direction]
        neighbor_wire = None
        if neighbor_component != None:
          if neighbor_component.isinstance(Wire) and neighbor_component.has_connection(input_direction.opposite():
            cls.generate_network(neighbor_component)
          elif neighbor_component.isinstance(OverlappedWire):
            cls.generate_network(neighbor_component.get_wire(input_direction.opposite()))

  def add_wire(self, wire):
    if component.isinstance(Wire) and wire.id not in self.wire_ids:
      self.wire_list[wire.count_power_inputs()].append(wire)
      self.wire_ids.add(wire.id)
      wire.network = self
      
  def get_wires(self):
    complete_set = set()
    for wire_set in self.wire_list:
      complete_set = complete_set | wire_set
      
    return complete_set