
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
        self.main_loop: bool = True
        self.matrix: list[list[int]] = [[self.config.matrix_empty for _ in range(config.grid_size)] for _ in range(config.grid_size)]
        self.cells: list[Cell] = []
        self.positions_cells: list[tuple[int]] = []

        # Create the generation upon start
        self.create_generation()

    # Create the generation
    def create_generation(self) -> None:
        """
        Creates a generation of cells in the simulation by placing them at random unoccupied positions on the grid.
        Each cell's position is marked as occupied in the matrix, and the cell is added to the list of cells.
        """

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
                    print(new_cell.position_x, new_cell.position_y)

                    # Finally add the "new_cell" to the "cells" list
                    self.cells.append(new_cell)

                    # Add the starting position fo visited_positions, to be able to fully go back to its starting position
                    new_cell.visited_positions.append((new_cell.position_x, new_cell.position_y))

                    # Sidequest: Add the coordinates to a positions_cells list for check_occupancy function
                    self.positions_cells.append((x, y))

                    # End the loop
                    break

    # Create a random x , y coordinate
    def cells_random_position(self) -> tuple[int, int]:
        """
        Generates random x and y coordinates for cell placement based on spawn location.
        There are 4 spawn locations on the grid: west, north, east, and south.
        Returns:
            tuple[int, int]: Random x and y coordinates.
        """
        
        # 4 spawn locations are the west, north, east and south
        spawn_location = random.randint(1, 4)
        
        # All the x , y coordinates must be in the yellow-spawn-zone
        # EAST
        if spawn_location == 1:
            random_x = random.randint(self.config.grid_size // 20 * 19, self.config.grid_size - 1)
            random_y = random.randint(0, self.config.grid_size - 1)
        # WEST
        elif spawn_location == 2:
            random_x = random.randint(0, self.config.grid_size // 20 - 1)
            random_y = random.randint(0, self.config.grid_size - 1)
        # NORTH
        elif spawn_location == 3:
            random_x = random.randint(0, self.config.grid_size - 1)
            random_y = random.randint(0, self.config.grid_size // 20 - 1)      
        # SOUTH      
        else:
            random_x = random.randint(0, self.config.grid_size - 1)
            random_y = random.randint(self.config.grid_size // 20 * 19, self.config.grid_size - 1)
        
        # Return the random_x , random_y as a tuple
        return random_x, random_y

    # Run the simulation on each round
    def cell_update(self) -> None:
        """
        Updates the state of all cells in the simulation by calling their movement functions.
        """
        self.move_cells()

    # Move the cells in the simulation
    def move_cells(self) -> None:
        """
        Iterates through all cells in the simulation and moves them according to their movement logic.
        """
        for cell in self.cells:
            if cell.can_move:
                cell.move_cell()

    # Create the foods at the beginning of each generation
    def create_food(self) -> None:
        """
        Generates food at random positions in the grid outside the yellow-spawn-zone.
        Food is placed only in unoccupied cells based on a defined food creation chance.
        """

        # Clear all the previous food, to create a new food for the next generation
        self.clear_food()
        
        # Creating of the food must be out of the yellow zone
        for x in range(self.config.grid_size // 20+1, self.config.grid_size // 20 * 19-1):
            for y in range(self.config.grid_size // 20+1, self.config.grid_size // 20 * 19-1):
                
                # According to food_creating chance, if the position is unoccupied(=0), create a food(=9)
                if random.randint(1, 100) < self.config.food_creation_chance and self.matrix[x][y] == self.config.matrix_empty:
                    self.matrix[x][y] = self.config.matrix_food_exist

    # Find all the surviving cells in the yellow zone
    def survive_cells(self) -> None:
        """
        Identifies cells that have survived in the simulation. 
        A cell is considered to have survived if it is within the yellow-surviving-zone and has a sufficient food supply.
        Updates the list of active cells to only include the surviving cells.
        """
        surviving_cells: list[Cell] = []
        for cell in self.cells:
           
            # The cell must be in the surviving_zones(yellow zones) and have at least 1 food_supply
            if ((cell.position_x, cell.position_y) in self.config.surviving_zones) and cell.food_supply > 0:
                surviving_cells.append(cell)
      
        # Updates the self.cells to surviving_cells
        self.cells = surviving_cells

    # Reproduce the surviving cells into the next generation
    def reproduce_cells(self, survivors: list[Cell]) -> None:
        """
        Reproduces the surviving cells into the next generation. 
        Survivors may randomly produce 2 offspring. Both offspring inherit their parent's sense attributes.
        If no survivors exist, the simulation ends.
        
        Args:
            survivors (list[Cell]): List of cells that survived the current generation.
        """
        new_generation: list[Cell] = []

        # Check if there are any survivors
        if survivors:
            for parent in survivors:
            
                # Randomize the position of the surviving cell, until the newly created position is unoccupied
                #       (is parent to possible 2 other cells) and update its location to the matrix
                while True:
                    parent.position_x, parent.position_y = self.cells_random_position()
                    if self.matrix[parent.position_x][parent.position_y] == self.config.matrix_empty:
                        break

                # If it is unoccupied, use the positions
                new_generation.append(parent)
                self.matrix[parent.position_x][parent.position_y] = self.config.matrix_cell_exist
            
                # According to reproduce_chance the parent can have offsprings
                #* random.random() without any parameters produce a float between 0 and 1
                if random.random() <= self.config.reproduce_chance:
                
                    # Create 2 offsprings
                    for _ in range(2):
                        
                        # First create a randomly placed offspring and update its location to the matrix
                        #* "*"(Asterisk) unpacks the cells_random_position function to position_x , position_y
                        offspring = Cell(*self.cells_random_position(), self.config, lambda: self.matrix)
                        self.matrix[offspring.position_x][offspring.position_y] = self.config.matrix_cell_exist

                        # Add the starting position fo visited_positions, to be able to fully go back to its starting position
                        offspring.visited_positions.append((offspring.position_x, offspring.position_y))
                    
                        # food_sense, zone_sense and speed must be inherited from the parent cell
                        #   for that, they get changed after the cell is created
                        offspring.food_sense = parent.food_sense
                        offspring.zone_sense = parent.zone_sense
                        offspring.speed = parent.speed
                        new_generation.append(offspring)
            
            # Updates the self.cells to new_generation
            self.cells = new_generation

        # Else end the simulation completely
        else:
            print("All cells are gone extinct")
            exit()
    
    # Update the matrix
    def matrix_cells_update(self) -> None:
        """
        Updates the matrix to reflect the new state of the simulation.
        Resets the positions of any  cells.
        """
        for x in range(self.config.grid_size):
            for y in range(self.config.grid_size):
                if self.matrix[x][y] == self.config.matrix_cell_exist:
                    self.matrix[x][y] == self.config.matrix_empty      

    # Clears food from the matrix, when a new generation is borned
    def clear_food(self) -> None:
        """
        Clears all food from the matrix.
        """
        for x in range(self.config.grid_size):
            for y in range(self.config.grid_size):
                if self.matrix[x][y] == self.config.matrix_food_exist:
                    self.matrix[x][y] = self.config.matrix_empty 

    # update the matrix according to surviving_zones(yellow zones=5)
    def matrix_surviving_zone_update(self) -> None:
        """
        Updates the matrix cells that are part of the surviving zones.

        For each (x, y) coordinate in the grid, if the cell is in the 
        `surviving_zones`, its value is updated to `matrix_surviving_zone_exist`.
        
        Returns:
            None
        """
        for x in range(self.config.grid_size):
            for y in range(self.config.grid_size):
                if (x, y) in self.config.surviving_zones:
                    self.matrix[x][y] = self.config.matrix_surviving_zone_exist
        
