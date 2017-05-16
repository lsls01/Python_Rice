"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_zombie_gui
import poc_queue

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        self.__init__(self.get_grid_height(), self.get_grid_width())
        # self._obstacle_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        # replace with an actual generator
        for zombie in self._zombie_list:
            yield zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        for human in self._human_list:
            yield human
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        visited = [[False for dummy_col in range(\
            self.get_grid_width())] for dummy_row in range(\
            self.get_grid_height())]
        initial_distance = self.get_grid_width() * self.get_grid_height()
        distance_field = [[initial_distance for dummy_col in range(\
            self.get_grid_width())] for dummy_row in range(\
            self.get_grid_height())]
        boundary = poc_queue.Queue()
        if entity_type == ZOMBIE:
            for zombie in self.zombies():
                boundary.enqueue(zombie)
        else:
            for human in self.humans():
                boundary.enqueue(human)
        for cell in boundary:
            visited[cell[0]][cell[1]] = True
            distance_field[cell[0]][cell[1]] = 0
        
        while len(boundary)!= 0:
            current_cell = boundary.dequeue()
            neighbours = self.four_neighbors(current_cell[0], current_cell[1])
            for one_neighbour in neighbours:
                if visited[one_neighbour[0]][one_neighbour[1]] == False and \
                        self.is_empty(one_neighbour[0], one_neighbour[1]):
                    visited[one_neighbour[0]][one_neighbour[1]] = True
                    boundary.enqueue(one_neighbour)
                    distance_field[one_neighbour[0]][one_neighbour[1]] = \
                        distance_field[current_cell[0]][current_cell[1]] + 1

        return distance_field
    
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        for index in range(len(self._human_list)):
            human = self._human_list[index]
            human_distance = zombie_distance_field[human[0]][human[1]]
            neighbours = self.eight_neighbors(human[0], human[1])
            best_position = human
            best_distance = human_distance
            for neighbour in neighbours:
                neighbour_distance = zombie_distance_field[neighbour[0]][neighbour[1]]
                if neighbour_distance > best_distance and self.is_empty(neighbour[0], neighbour[1]):
                    best_position = neighbour
                    best_distance = neighbour_distance
            self._human_list[index] = best_position
    
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        for index in range(len(self._zombie_list)):
            zombie = self._zombie_list[index]
            zombie_distance = human_distance_field[zombie[0]][zombie[1]]
            neighbours = self.four_neighbors(zombie[0], zombie[1])
            best_move = []
            best_position = zombie
            best_distance = zombie_distance
            best_move.append(best_position)
            for neighbour in neighbours:
                neighbour_distance = human_distance_field[neighbour[0]][neighbour[1]]
                if neighbour_distance < best_distance and self.is_empty(neighbour[0], neighbour[1]):
                    best_move = []
                    best_distance = neighbour_distance
                    best_position = neighbour
                    best_move.append(best_position)
                elif neighbour_distance == best_distance and self.is_empty(neighbour[0], neighbour[1]):
                    best_move.append(best_position)
            self._zombie_list[index] = random.choice(best_move)

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Apocalypse(30, 40))
