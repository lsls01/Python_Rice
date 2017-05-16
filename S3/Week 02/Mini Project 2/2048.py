"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    newline = [0]*len(line)
    count_num_in_newline = 0
    tmp_store = [num for num in line if num != 0]
    for line_number in range (len(tmp_store) - 1):
        if tmp_store[line_number] == tmp_store[line_number + 1]:
            tmp_store[line_number] = 2*tmp_store[line_number]
            tmp_store[line_number + 1] = 0
    for number in tmp_store:  #move number to newline
        if number != 0:
            newline[count_num_in_newline] = number
            count_num_in_newline += 1
    return newline

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        # replace with your code
        self._height = grid_height
        self._width = grid_width
        self.reset()
        
        # initialize indiced grid
        self._direction = {}
        self._direction[UP] = []
        self._direction[DOWN] = []
        self._direction[LEFT] = []
        self._direction[RIGHT] = []
        for dummy_col in range(grid_width):
            self._direction[UP].append((0, dummy_col))
            self._direction[DOWN].append((self._height - 1, dummy_col))
        for dummy_row in range(grid_height):
            self._direction[LEFT].append((dummy_row, 0))
            self._direction[RIGHT].append((dummy_row, self._width - 1))

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        # replace with your code
        self._grid = [[0 for dummy_col in range(self._width)] for dummy_row in range(self._height)]
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        # replace with your code
        grid_str = "["
        for row in range(self._height):
            grid_str += " " + str(self._grid[row]) + "\n"
        grid_str = grid_str[0:1] + grid_str[2:]
        grid_str = grid_str[:-1]
        grid_str += "]"
        return grid_str

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        # replace with your code
        return self._height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        # replace with your code
        return self._width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        # replace with your code
        tiles_moved = False
        
        if direction == UP or direction == DOWN:
            index = self._height
        else:
            index = self._width
        for dummy_itr in self._direction[direction]:
            tmp_list = []
            tile_pos = list(dummy_itr)
            tmp_list.append(self.get_tile(tile_pos[0], tile_pos[1]))
            for dummy_index in range(index - 1):
                tile_pos[0] += OFFSETS[direction][0]
                tile_pos[1] += OFFSETS[direction][1]
                tmp_list.append(self.get_tile(tile_pos[0], tile_pos[1]))
            
            merged_list = merge(tmp_list)
            
            tile_pos = list(dummy_itr)
            for dummy_index in range(index):
                cur_value = self.get_tile(tile_pos[0], tile_pos[1])
                if cur_value != merged_list[dummy_index]:
                    tiles_moved = True
                    self.set_tile(tile_pos[0], tile_pos[1], merged_list[dummy_index])
                tile_pos[0] += OFFSETS[direction][0]
                tile_pos[1] += OFFSETS[direction][1]
        
        if tiles_moved == True:
            self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        # replace with your code
        vacant_tiles = []
        for dummy_col in range(self.get_grid_width()):
            for dummy_row in range(self.get_grid_height()):
                if self.get_tile(dummy_row, dummy_col) == 0:
                    vacant_tiles.append((dummy_row, dummy_col))
        if vacant_tiles != []:
            pos_chosen = random.choice(vacant_tiles)
            random_value = random.choice([2] * 9 + [4])
            self.set_tile(pos_chosen[0], pos_chosen[1], random_value)

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        # replace with your code
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        # replace with your code
        return self._grid[row][col]


poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
