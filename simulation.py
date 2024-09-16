
# TODO: Refactor this function to improve performance
# ! This is a critical section of the code
# ? Does this logic make sense here?
# * Deprecated: No longer using this function
# This is a standard comment



# Libraries from general
import random

# Imported files
from cell import Cell
from config import Config

# A "Simulation" class for the all the functions of the simulation
class Simulation:
    def __init__(self, config:Config):

        # Parameter for the Class "Config"
        self.config = config

        # Consts for the simulation
        self.running: bool = True
        self.matrix: list[list[int]] = [[self.config.matrix_empty for _ in range(config.grid_size)] for _ in range(config.grid_size)]
        self.cells: list[Cell] = []
        self.positions_cells: list[tuple[int]] = []

        # Create the generation upon start
        self.create_generation()

    # Create the generation
    def create_generation(self) -> None:

        # Create as many cells as the cell_count determines
        for _ in range(self.config.cell_count):

            # Randomly create x and y positions until they are unoccupied
            while True:

                # Get a random position from the function get_random_position
                x, y = self.cells_random_position()

                # Check if the position is unoccupied in the matrix
                if self.matrix[x][y] == self.config.matrix_empty:

                    # Firstly mark the new position as occupied in the matrix
                    self.matrix[x][y] = self.config.matrix_cell_exist

                    # Secondly create the new_cell in the "Cell" class
                    new_cell = Cell(x, y, self.config, lambda: self.matrix)

                    # Finally add the "new_cell" to the "cells" list
                    self.cells.append(new_cell)

                    # Sidequest: Add the coordinates to a positions_cells list for check_occupancy function
                    self.positions_cells.append((x, y))

                    # End the loop
                    break

    # Create a random x , y coordinate
    def cells_random_position(self) -> tuple[int, int]:
        
        # 4 spawn locations are the west, north, east and south
        spawn_location = random.randint(1, 4)
        
        # All the x , y coordinates must be in the yellow-spawn-zone
        if spawn_location == 1:
            random_x = random.randint(self.config.grid_size // 20 * 19, self.config.grid_size - 1)
            random_y = random.randint(0, self.config.grid_size - 1)
        elif spawn_location == 2:
            random_x = random.randint(0, self.config.grid_size // 20)
            random_y = random.randint(0, self.config.grid_size - 1)
        elif spawn_location == 3:
            random_x = random.randint(0, self.config.grid_size - 1)
            random_y = random.randint(0, self.config.grid_size // 20)            
        else:
            random_x = random.randint(0, self.config.grid_size - 1)
            random_y = random.randint(self.config.grid_size // 20 * 19, self.config.grid_size - 1)
        
        # Return the random_x , random_y as a tuple
        return random_x, random_y
    
    # Run the simulation on each round
    def update(self):
        self.move_cells()

    # Move the cells in the simulation
    def move_cells(self) -> None:
        for cell in self.cells:
            cell.move_cell()

    # Create the foods at the beginning of each generation
    def create_food(self) -> None:
        
        # Creating of the food must be out of the yellow zone
        for x in range(self.config.grid_size // 20, self.config.grid_size // 20 * 19):
            for y in range(self.config.grid_size // 20, self.config.grid_size // 20 * 19):
                
                # According to food_creating chance, if the position is unoccupied(=0), create a food(=9)
                if random.randint(1, 100) < self.config.food_creation_chance and self.matrix[x][y] == self.config.matrix_empty:
                    self.matrix[x][y] = self.config.matrix_food_exist

    # Find all the surviving cells in the yellow zone
    def survive_cells(self) -> list[Cell]:
        surviving_cells: list[Cell] = []
        for cell in self.cells:
           
            # The cell must be in the surviving_zones(yellow zones) and have at least 1 food_supply
            if ((cell.position_x, cell.position_y) in self.config.surviving_zones) and cell.food_supply > 0:
                surviving_cells.append(cell)
      
        # Return the surviving_cells list
        return surviving_cells

    # Reproduce the surviving cells into the next generation
    def reproduce_cells(self, survivors: list[Cell]) -> list[Cell]:
        new_generation: list[Cell] = []
        for parent in survivors:
        
            # Randomize the position of the surviving cell(is parent to possible 2 other cells)
            parent.position_x, parent.position_y = self.cells_random_position()
            new_generation.append(parent)
          
            # According to reproduce_chance the parent can have offsprings
            #* random.random() without any parameters produce a float between 0 and 1
            if random.random() <= self.config.reproduce_chance:
              
                # Create 2 offsprings
                for _ in range(2):
                    # First create a randomly placed offspring
                 
                    #* "*"(Asterisk) unpacks the cells_random_position function to position_x , position_y
                    offspring = Cell(*self.cells_random_position(), self.config, lambda: self.matrix)
                   
                    # food_sense and zone_sense must be inherited from the parent cell
                    #   for that, they get changed after the cell is created
                    offspring.food_sense = parent.food_sense
                    offspring.zone_sense = parent.zone_sense
                    new_generation.append(offspring)
        
        # Returns new_generation for the cells in a list
        return new_generation
