"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def get_target(self, row, col):
        """
        Get the target value
        """
        return row * self.get_width() + col
        
    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        # replace with your code
        if self.get_number(target_row, target_col) != 0:
            return False
        
        if target_row == self.get_height() - 1 and target_col == self.get_width() - 1:
            return True
        
        for row in range(target_row + 1, self.get_height()):
            for col in range(0, self.get_width()):
                if (self.get_number(row, col) != self.get_target(row, col)):
                    return False
        for col in range(target_col + 1, self.get_width()):
            if (self.get_number(target_row, col) != self.get_target(target_row, col)):
                return False

        return True

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        # replace with your code
        target_position = self.current_position(target_row, target_col)
        assert target_position[0] < target_row or (target_position[0] == target_row and target_position[1] < target_col)
        
        assert self.lower_row_invariant(target_row, target_col)
        
        move_str = self.position_tile(target_row, target_col, target_position)
        self.update_puzzle(move_str)
        
        # self.update_from_move_str(target_row, target_col, move_str)
        assert self.lower_row_invariant(target_row, target_col - 1);
        return move_str

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        # special case, target tile is just above zero
        if self.get_target(target_row, 0) == self.get_number(target_row - 1, 0):
            move_str = 'u' + 'r' * (self.get_width() - 1)
            self.update_puzzle(move_str)
            return move_str
        
        # Reposition the target tile to position (i−1,1)
        # and the zero tile to position (i−1,0)
        tile_row, tile_col = self.current_position(target_row, 0)
        move_str = 'u'
        # special case, target tile is just above the row where 0 is.
        if tile_row + 1 == target_row:
            if tile_col != 1:
                move_str += 'r' * tile_col
                move_str += 'ulldr' * (tile_col - 2)
                move_str += 'ulld'
        else:
            move_str += 'r' * tile_col
            move_str += 'u' * (target_row - tile_row - 1)
            if tile_col == 0:
                move_str += 'rddlu' * (target_row - tile_row - 2)
                move_str += 'rdlur'
            else:
                move_str += 'lddru' * (target_row - tile_row - 2)
                move_str += 'ldrul' * (tile_col - 1)
            move_str += 'ld'

        move_str += 'ruldrdlurdluurddlur'
        move_str += 'r' * (self.get_width() - 2)
        self.update_puzzle(move_str)
        return move_str

    def position_tile(self, target_row, target_col, target_position):
        """
        Moves a tile from start position to target position
        Updates puzzle and returns a move string
        """
        rel_row = target_row - target_position[0]
        rel_col = target_col - target_position[1]
        
        # special case for rel_row == 0
        if rel_row == 0:
            horizontal = 'l' * rel_col
            move_right = 'urrdl' * (rel_col - 1)
            move_str = horizontal + move_right
            return move_str
            
        move_up = 'u' * rel_row
        if rel_col > 0:
            horizontal = 'l' * rel_col
        else:
            horizontal = 'r' * (-rel_col)
        # move across target tile, now zero is above the target tile
        move_str = horizontal + move_up
        
        # horizontal move first
        # target_tile is to the right of the target_col
        if rel_col < 0:
            move_str += 'ldrul' * (-rel_col)
        elif rel_col > 0:
            move_str += 'rdlur' * (rel_col)
        
        # move down
        move_str += 'lddru' * (rel_row - 1)
        
        # move zero to the left of target
        move_str += 'ld'
        
        return move_str

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self.get_number(0, target_col) != 0:
            return False
        
        for row in range(2, self.get_height()):
            for col in range(0, self.get_width()):
                if (self.get_number(row, col) != self.get_target(row, col)):
                    return False
        for col in range(target_col + 1, self.get_width()):
            if (self.get_number(0, col) != self.get_target(0, col)):
                return False
            if (self.get_number(1, col) != self.get_target(1, col)):
                return False
        
        if (self.get_number(1, target_col) != self.get_target(1, target_col)):
            return False

        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self.get_number(1, target_col) != 0:
            return False
                
        for row in range(2, self.get_height()):
            for col in range(0, self.get_width()):
                if (self.get_number(row, col) != self.get_target(row, col)):
                    return False
        for col in range(target_col + 1, self.get_width()):
            if (self.get_number(0, col) != self.get_target(0, col)):
                return False
            if (self.get_number(1, col) != self.get_target(1, col)):
                return False

        return True
        
    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row0_invariant(target_col)
        if self.get_number(0, target_col - 1) == self.get_target(0, target_col):
            move_str = 'ld'
        else:
            tile_row, tile_col = self.current_position(0, target_col)
            if tile_row == 1:
                if tile_col == target_col - 1:
                    move_str = 'lld'
                else:
                    move_str = 'l' * (target_col - tile_col - 1) + 'dl'
                    move_str += 'urrdl' * (target_col - tile_col - 2)
            else:
                move_str = 'l' * (target_col - tile_col)
                move_str += 'druld'
                move_str += 'urrdl' * (target_col - tile_col - 2)
            # after reposition the target tile to position (1,j−1)
            # with tile zero in position (1,j−2)
            move_str += 'urdlurrdluldrruld'
        # after solve move zero to (1, target_col - 1)
        self.update_puzzle(move_str)
        assert self.row1_invariant(target_col - 1)
        return move_str

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row1_invariant(target_col)
        
        tile_row, tile_col = self.current_position(1, target_col)
        if tile_row == 0:
            move_str = 'u' + 'l' * (target_col - tile_col)
            move_str += 'drrul' * (target_col - tile_col - 1)
            if tile_col != target_col:
                move_str += 'dru'
        else:
            move_str = 'l' * (target_col - tile_col)
            move_str += 'urrdl' * (target_col - tile_col - 1)
            move_str += 'ur'

        self.update_puzzle(move_str)
        # after solve move zero to (0, target_col)
        assert self.row0_invariant(target_col)
        return move_str

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        # start from (1, 1)
        move_str = 'lu'
        self.update_puzzle(move_str)
        while self.get_number(0, 1) != 1:
            move_str += 'rdlu'
            self.update_puzzle('rdlu')
        return move_str

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        solution_str = ""
        zero_str = ""
        for row in range(self.get_height()):
            for col in range(self.get_width()):
                if self.get_number(row, col) == 0:
                    zero_str += 'd' * (self.get_height() - row - 1)
                    zero_str += 'r' * (self.get_width() - col - 1)
                    break
        self.update_puzzle(zero_str)
        solution_str += zero_str
        
        for row in range(self.get_height() - 1, 1, -1):
            for col in range(self.get_width() - 1, -1, -1):
                if col > 0:
                    solution_str += self.solve_interior_tile(row, col)
                else:
                    solution_str += self.solve_col0_tile(row)
        for col in range(self.get_width() - 1, 1, -1):
            solution_str += self.solve_row1_tile(col)
            solution_str += self.solve_row0_tile(col)
        twoxtwo_str = self.solve_2x2()
        solution_str += twoxtwo_str
        return solution_str

# Start interactive simulation
poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))


