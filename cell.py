
# Libraries from general
import random

# Imported files
from config import Config

# "Cell" class for the cells
class Cell:
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
        self.speed = random.randint(1, 3)
        self.energy_consumption = self.food_sense+self.zone_sense+self.speed


        # pre-determined-Attributes for the cell, which could *not* inherited from the parent cell
        self.food_supply: int = 6
        self.go_back: bool = False
        self.can_move: bool = True

        # They are pre-determined, but changes depending on the level of food_supply
        self.food_sense_chance: int = 90
        self.surviving_zone_sense_chance: int = 10

        # A visited blocks list to track down and go back to surviving_zones
        self.visited_positions: list[tuple[int, int]] = []

        # Consts for the cell
        self.allowed_directions: list[str] = ["UP", "DOWN", "RIGHT", "LEFT"]
        #?self.allowed_directions: list[str] = ["UP"]
        self.zone_sense_colors = {
            1: (70, 0, 0),  # Dark red
            2: (140, 0, 0),  # Medium red
            3: (210, 0, 0)   # Light red
        }

        self.food_sense_colors = {
            1: (0, 70, 0),  # Dark green
            2: (0, 140, 0),  # Medium green
            3: (0, 210, 0)   # Light green
        }

        self.speed_colors = {
            1: (0, 0, 70),  # Dark blue
            2: (0, 0, 140),  # Medium blue
            3: (0, 0, 210)   # Light blue
        }

    # Mixes the colors according to the level of cell-attributes
    def mix_colors(self, brightness_factor: float = 2.8) -> tuple[int, int, int]:
        """
        Mix the colors of the cell's attributes (zone_sense, food_sense, speed)
        by averaging their RGB values and applying a brightness factor.

        Args:
            brightness_factor (float): Factor to brighten the mixed color. Default is 1.5.

        Returns:
            tuple[int, int, int]: The brightened and mixed RGB color as a tuple of three integers.
        """
        # Get colors for each attribute level
        zone_color = self.zone_sense_colors[self.zone_sense]
        food_color = self.food_sense_colors[self.food_sense]
        speed_color = self.speed_colors[self.speed]
        
        # Calculate the average color
        mixed_color = (
            (zone_color[0] + food_color[0] + speed_color[0]) // 3,
            (zone_color[1] + food_color[1] + speed_color[1]) // 3,
            (zone_color[2] + food_color[2] + speed_color[2]) // 3
        )
        
        # Apply the brightness factor and ensure the values stay within the valid range (0-255)
        brightened_color = (
            min(int(mixed_color[0] * brightness_factor), 255),
            min(int(mixed_color[1] * brightness_factor), 255),
            min(int(mixed_color[2] * brightness_factor), 255)
        )
        
        return brightened_color


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


    def move_cell(self) -> tuple[int, int]:
        """
        Moves the cell based on its food supply, sense abilities, and random chance.

        The cell's behavior is determined by its current food supply:
        - With no food, it prioritizes finding food.
        - With full food supply, it prioritizes finding a surviving zone.
        - With intermediate food levels, it balances between finding food and surviving zones.

        The function updates the cell's position in the matrix and handles food collection
        if the cell lands on a food cell.

        Returns:
            tuple[int, int]: The new (x, y) position of the cell after moving.
        """
        matrix = self.matrix()

        # self.speed determines, how many times a cell should move per round
        for _ in range(self.speed):
            
            # Determine if the cell should move based on the move chance
            if random.randint(1, 100) <= self.config.move_chance:
                
                # Choose a random direction
                direction = random.choice(self.allowed_directions)
                
                # Clear the cell's previous position in the matrix if within bounds
                matrix[self.position_x][self.position_y] = self.config.matrix_empty

                # Update sense chances based on food supply
                self.update_sense_chances()

                # Determine movement based on food supply and sense chances
                if self.food_supply < self.energy_consumption:
                    self.seek_food_or_move_randomly(direction)
                elif (2*self.energy_consumption < self.food_supply) or (self.food_supply == 10):
                    self.go_back = True
                    self.return_starting_point()
                else:
                    self.balanced_movement(direction)

                # Collect food if the new position contains food
                if matrix[self.position_x][self.position_y] == self.config.matrix_food_exist:
                    self.add_food_supply()

                # Mark the cell's new position in the matrix if within bounds
                matrix[self.position_x][self.position_y] = self.config.matrix_cell_exist

                # Add the new position to visited_positions to, if necessary, track back down
                if not(self.go_back):
                    self.visited_positions.append((self.position_x, self.position_y)) 

        # Return the new position
        return self.position_x, self.position_y

    # Adjusts the chances of detecting food and surviving zones based on available food supply.
    def update_sense_chances(self):
        """
        Updates food sense and surviving zone sense chances based on food supply.
        """
        if self.food_supply < self.energy_consumption:
            self.food_sense_chance = 100
            self.surviving_zone_sense_chance = 0
        elif self.energy_consumption < self.food_supply < 2*self.energy_consumption:
            self.food_sense_chance = 67
            self.surviving_zone_sense_chance = 33
        elif 2*self.energy_consumption < self.food_supply < 3*self.energy_consumption:
            self.food_sense_chance = 33
            self.surviving_zone_sense_chance = 67
        elif 3*self.energy_consumption < self.food_supply:
            self.food_sense_chance = 0
            self.surviving_zone_sense_chance = 100

    # Attempts to find food first; if unavailable, moves randomly.
    def seek_food_or_move_randomly(self, direction):
        """
        Seeks food if possible, otherwise moves randomly.
        """
        food_positions = self.find_nearby_food()
        if food_positions:
            self.move_towards_food(food_positions)
        else:
            self.move_in_direction(direction)


    # Attempts to locate a surviving zone next; if not possible, moves randomly.
    def seek_surviving_zone_or_move_randomly(self, direction):
        """
        Seeks surviving zone if possible, otherwise moves randomly.
        """
        surviving_zone_positions = self.find_nearby_surviving_zone()
        if surviving_zone_positions:
            self.move_towards_surviving_zone(surviving_zone_positions)
        else:
            self.move_in_direction(direction)


    # Balances the actions of searching for food, finding a surviving zone, and random movement.
    def balanced_movement(self, direction):
        """
        Balances between seeking food, surviving zone, and random movement.
        """
        if random.randint(1, 100) < self.food_sense_chance:
            food_positions = self.find_nearby_food()
            if food_positions:
                self.move_towards_food(food_positions)
                return
        if random.randint(1, 100) < self.surviving_zone_sense_chance:
            surviving_zone_positions = self.find_nearby_surviving_zone()
            if surviving_zone_positions:
                self.move_towards_surviving_zone(surviving_zone_positions)
                return
        self.move_in_direction(direction)

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
        # Calculate the closest food in food positions according to the positions of the cell using lambda function
        #*(lambda arguments: expression) -> Format of lambda functions
        #*   1) lambda: This keyword defines the start of an anonymous function.
        #*   2) arguments: These are the inputs to the lambda function, similar to parameters in a regular function.
        #*   3) expression: This is a single expression that is evaluated and returned. The expression can use the arguments.
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

    #Find if at the zone_sense distance any surviving zone is present and track a list of them
    def find_nearby_surviving_zone(self) -> list[tuple]:
        """
        Finds surviving cells within the cell's sensing range (zone_sense).

        The function scans the area around the cell, determined by its zone_sense value,
        and identifies any positions that is a zone.

        Returns:
            list[tuple[int, int]]: A list of coordinates where surviving zones are located nearby.
        """
        surviving_zone_positions = []
        matrix = self.matrix()

        # Sense according to food_sense value, bigger value checks a bigger area
        for dx in range(-self.zone_sense, self.zone_sense + 1):
            for dy in range(-self.zone_sense, self.zone_sense + 1):

                # Don't check the position of the cell, isn't needed
                if dx == 0 and dy == 0:
                    continue

                # Check the position according to double for loops
                x, y = self.position_x + dx, self.position_y + dy

                # Within the boundaries of the grid, check if there is any food in the food_sense zone
                if 0 <= x < self.config.grid_size and 0 <= y < self.config.grid_size and matrix[x][y] == self.config.matrix_surviving_zone_exist:
                    surviving_zone_positions.append((x, y))

        # Return the found food positions in a tuple
        return surviving_zone_positions


    # Move towards the surviving zone according to survibing_zone_positions
    def move_towards_surviving_zone(self, surviving_zone_positions: list[int]) -> None:
        """
        Moves the cell towards the closest surviving_zone position.

        The function identifies the closest surviving zone in the provided surviving_zone_positions list and
        adjusts the cell's position to move toward it, either horizontally or vertically.

        Args:
            surviving_zone_positions (list[int]): A list of coordinates where the surviving zones are located.
        """
        # Calculate the closest surviving zone in surviving zone positions according to the positions of the cell
        closest_surviving_zone = min(surviving_zone_positions, key=lambda pos: ((pos[0] - self.position_x)**2 + (pos[1] - self.position_y)**2))
        
        # Unpack the closest_surviving_zone coordinates and subtract the self positions
        dx: int = closest_surviving_zone[0] - self.position_x
        dy: int = closest_surviving_zone[1] - self.position_y

        # Move in the direction of the closest surviving zone
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
        if self.food_supply != 10:
            self.food_supply += 1


    # Use a food from the cell's food_supply
    def use_food(self) -> None:
        """
        Decreases the cell's food supply by 1 and prints the remaining food supply.

        This is called when the cell consumes food to survive.
        """
        self.food_supply -= 1

    # It should return to its starting point under certain circumstances(food_supply)
    def return_starting_point(self):
        """
        Move the cell back to its starting point using the `visited_positions` list.
        """
        #print(self.visited_positions)

        # If there is only one position left(starting point) it means that, the cell has reached its starting position sucessuflly
        if len(self.visited_positions) > 1:
            # Get the last visited position
            last_position = self.visited_positions[-1]
            
            # Calculate the direction to move towards the last visited position
            dx = last_position[0] - self.position_x
            dy = last_position[1] - self.position_y
            
            # Move one step towards the last visited position
            if dx != 0:
                self.position_x += 1 if dx > 0 else -1
            elif dy != 0:
                self.position_y += 1 if dy > 0 else -1
            
            # If we've reached the last visited position, remove it from the list
            if ((self.position_x, self.position_y) == last_position):
                self.visited_positions.pop()
        
        # Once the list is empty, the cell has returned to its starting point
        else:
            self.can_move = False
            self.go_back = False





  
