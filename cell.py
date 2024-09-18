
# TODO: Refactor this function to improve performance
# ! This is a critical section of the code
# ? Does this logic make sense here?
# * Deprecated: No longer using this function
# This is a standard comment



# Libraries from general
import random

# Imported files
from config import Config

# "Cell" class for the cells
class Cell:
    # Simulation is the "Simulation" class
    def __init__(self, position_x:int, position_y:int, config: Config, matrix):

        # Parameter for the Class "Config"
        self.config = config

        # Use the general matrix, it should be passed as a parameter
        self.matrix = matrix

        # non-determined-Attributes for the cell
        self.position_x = position_x
        self.position_y = position_y

        # pre-determined-Attributes for the cell, which could be inherited from the parent cell
        self.food_sense = random.randint(1, 3)
        self.zone_sense = random.randint(1, 3)

        # pre-determined-Attributes for the cell, which could *not* inherited from the parent cell
        self.food_supply = 1

        # Consts for the cell
        self.sense_chance = 20
        self.PURPLE: tuple = (128, 0, 128)
        self.ORANGE: tuple = (245, 180, 70)
        self.movement: dict[int, str] = {
            3: "UP",
            4: "DOWN",
            5: "RIGHT",
            6: "LEFT"
        }
        self.allowed_directions: list[str] = ["UP", "DOWN", "RIGHT", "LEFT"]
    
    # Check the occupancy of the position_x , position_y
    def check_occupancy(self, position_x: int, position_y: int) -> bool:
        """
        Checks whether a given position (position_x, position_y) is occupied by a cell.

        Args:
            position_x (int): The x-coordinate of the position to check.
            position_y (int): The y-coordinate of the position to check.

        Returns:
            bool: True if the position is occupied, False otherwise.
        """
        matrix = self.matrix()
        return matrix[position_x][position_y] == self.config.matrix_cell_exist


    # Moving action of the cell
    def move_cell(self) -> tuple[int, int]:
        """
        Moves the cell based on its movement chance and sense abilities.

        The cell will either move towards nearby food or in a random direction.
        After moving, the cell updates its position in the grid and may collect
        food if it lands on a food cell.

        Returns:
            tuple[int, int]: The new (x, y) position of the cell after moving.
        """
        matrix = self.matrix()

        # Determine if the cell should move
        if random.randint(1, 100) > (100 - self.config.move_chance):
            direction = random.choice(self.allowed_directions)
            
            # If the position of the cell within the boundaries of the grid, the previous position should be marked as empty(=0) in the matrix
            if (self.config.grid_size // 20 < self.position_x < self.config.grid_size // 20 * 19) and (self.config.grid_size // 20 < self.position_y < self.config.grid_size // 20 * 19):
                matrix[self.position_x][self.position_y] = self.config.matrix_empty

            # With the sense_chance find the food in the near of the cell
            if (self.config.grid_size // 20 < self.position_x < self.config.grid_size // 20 * 19) and (self.config.grid_size // 20 < self.position_y < self.config.grid_size // 20 * 19) and (random.randint(1, 100) < self.sense_chance):
                food_positions = self.find_nearby_food()

                # If food found, go towards it
                if food_positions:
                    self.move_towards_food(food_positions)

            # If sense_chance doesn't work, move in any direction
            else:
                self.move_in_direction(direction)

            # If the moved direction has food in it, eat and add it to its food supply
            if matrix[self.position_x][self.position_y] == self.config.matrix_food_exist:
                self.add_food_supply()

            # If the new position is within the boundaries, mark the new position of the cell(=1) in the matrix
            if (self.config.grid_size // 20 < self.position_x < self.config.grid_size // 20 * 19) and (self.config.grid_size // 20 < self.position_y < self.config.grid_size // 20 * 19):
                matrix[self.position_x][self.position_y] = self.config.matrix_cell_exist

        # Return the new positions in a tuple
        return self.position_x, self.position_y


    # Find if at the food_sense distance any food is present and track a list of them
    def find_nearby_food(self) -> list[tuple]:
        """
        Finds food cells within the cell's sensing range (food_sense).

        The function scans the area around the cell, determined by its food_sense value,
        and identifies any positions that contain food.

        Returns:
            list[tuple[int, int]]: A list of coordinates where food is located nearby.
        """
        food_positions = []
        matrix = self.matrix()

        # Sense according to food_sense value, bigger value checks a bigger area
        for dx in range(-self.food_sense, self.food_sense + 1):
            for dy in range(-self.food_sense, self.food_sense + 1):

                # Don't check the position of the cell, isn't needed
                if dx == 0 and dy == 0:
                    continue

                # Check the position according to double for loops
                x, y = self.position_x + dx, self.position_y + dy

                # Within the boundaries of the grid, check if there is any food in the food_sense zone
                if 0 <= x < self.config.grid_size and 0 <= y < self.config.grid_size and matrix[x][y] == self.config.matrix_food_exist:
                    food_positions.append((x, y))

        # Return the found food positions in a tuple
        return food_positions


    # Move towards the food according to food_positions
    def move_towards_food(self, food_positions: list[int]) -> None:
        """
        Moves the cell towards the closest food position.

        The function identifies the closest food in the provided food_positions list and
        adjusts the cell's position to move toward it, either horizontally or vertically.

        Args:
            food_positions (list[int]): A list of coordinates where food is located.
        """
        # Calculate the closest food in food positions according to the positions of the cell
        closest_food = min(food_positions, key=lambda pos: ((pos[0] - self.position_x)**2 + (pos[1] - self.position_y)**2))
        
        # Unpack the closest_food coordinates and subtract the self positions
        dx: int = closest_food[0] - self.position_x
        dy: int = closest_food[1] - self.position_y

        # Move in the direction of the closest food
        if abs(dx) > abs(dy):
            # Move horizontally
            if dx > 0:
                self.position_x += 1
            elif dx < 0:
                self.position_x -= 1
        else:
            # Move vertically
            if dy > 0:
                self.position_y += 1
            elif dy < 0:
                self.position_y -= 1


    # Move the cell in a direction
    def move_in_direction(self, direction: str) -> None:
        """
        Moves the cell in a specified direction (UP, DOWN, RIGHT, LEFT).

        The function checks the new position to ensure it's within the grid's boundaries 
        and not already occupied before moving the cell.

        Args:
            direction (str): The direction to move the cell. Can be "UP", "DOWN", "RIGHT", or "LEFT".
        """
        # Unpack the tuple in dx and dy according to the direction, if direction is not in the dictionary
        dx, dy = {
            "UP": (0, -1),
            "DOWN": (0, 1),
            "RIGHT": (1, 0),
            "LEFT": (-1, 0)
        }.get(direction, (0, 0))

        # Add the direction to the coordinates
        new_x, new_y = self.position_x + dx, self.position_y + dy

        # Within the boundaries of the grid, if the new position is not occupied move the cell
        if 0 <= new_x < self.config.grid_size and 0 <= new_y < self.config.grid_size and not self.check_occupancy(new_x, new_y):
            self.position_x, self.position_y = new_x, new_y


    # Eating food on the same location
    def add_food_supply(self) -> None:
        """
        Increases the cell's food supply by 1, up to a maximum of 3.

        This is called when the cell lands on a food cell.
        """
        if self.food_supply != 3:
            self.food_supply += 1


    # Use a food from the cell's food_supply
    def use_food(self) -> None:
        """
        Decreases the cell's food supply by 1 and prints the remaining food supply.

        This is called when the cell consumes food to survive.
        """
        self.food_supply -= 1
        print(self.food_supply)




  
