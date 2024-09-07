# ERRORS:
# 7) WHEN THE NEW GENERATION IS BEING BORN, THEY TEND TO BE IN THE MIDDLE, THEY SHOULD BE EQUALLY DISTRIBUTED ACROSS THE DISPLAY
# 10) ADD MUTATION TO THE REPRODUCE FUNCTION
# 11) FOOD GENERATION STAYS SAME FOR THE GENERAIONS, EACH GENERATION SHOULD BE RANDOM
# 12) ADD SENSE ATTRIBUTE


import pygame
import random
import copy
import numpy as np

# Initialize the pygame library
pygame.init()

display_size: int = 800
# Background size
screen = pygame.display.set_mode((display_size, display_size))

# Display title
pygame.display.set_caption("Evolution Simulation")

# Clock for the delay
clock = pygame.time.Clock()

grid_size: int = 80 # Change the create_generation loop time, regarding how many cells should be created
running: bool = True
matrix: list[list[int]] = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
speed: int = 70
cell_count: int = 500
PURPLE: set = (128, 0, 128)
food_creation_chance: int = 5 # in percentages (%)
round_limit: int = 100
sense_chance: int = 20

# Dictionary of all possible colors, which effects the movement attributes
color_mapping_cells: dict = {
    (0, 0, 0): 1,      # BLACK, stays still
    (245, 180, 70): 2, # ORANGE, moves in every direction
    (255, 0, 0): 3,     # RED, moves only upwards
    (100, 255, 0): 4,     # GREEN, moves only downwards
    (0, 0, 255): 5,     # BLUE, moves only to right
    (255, 192, 203): 6,  # PINK, moves only to left
    (255, 255, 255): 0, # WHITE, dead cell
}

colors: list[int] = list(color_mapping_cells.keys())

# Cell class with its attributes
class Cell_Class:

    movement: dict = {
        2: "ALL",
        3: "UP",
        4: "DOWN",
        5: "RIGHT",
        6: "LEFT"
    }

    def __init__(self, color, position_x, position_y, sense=1, move=None, feed=False):
        self.color = color
        self.position_x = position_x
        self.position_y = position_y
        self.sense = sense
        self.move = move
        self.feed = feed

    # Sets the movement attribute of the cell
    def set_movement(self):

        self.move = Cell_Class.movement.get(self.color, None)

    # Moving action of the cell
    def move_cell(self) -> tuple[int, int]:
        # Determine if the cell should move
        if random.randint(1, 100) > (100-speed):
            if self.move == "ALL":
                self.move_randomly()
            elif self.move in {"UP", "DOWN", "RIGHT", "LEFT"}:
                self.move_direction(self.move)

        return self.position_x, self.position_y

    # Orange moves randomly in one of all directions
    def move_randomly(self):
        direction = random.choice(["UP", "RIGHT", "DOWN", "LEFT"])
        self.move_direction(direction)

    # Move in one direction
    def move_direction(self, direction: str):
        start_generation[self.position_x][self.position_y] == 0

        if (grid_size//20 < self.position_x < grid_size//20*19) and (grid_size//20 < self.position_y < grid_size//20*19) and (random.randint(1, 100) < sense_chance):

            if self.sense == 1:
                # With sense_chance, the cell moves towards the food in all 8 directions(including diagonal)
                    if self.position_x > 0:
                        if start_generation[self.position_x-1][self.position_y] == 7:
                            self.position_x -= 1
                    if self.position_x < grid_size-1:
                        if start_generation[self.position_x+1][self.position_y] == 7:
                            self.position_x += 1
                    if self.position_y > 0:
                        if start_generation[self.position_x][self.position_y-1] == 7:
                            self.position_y -= 1
                    if self.position_y < grid_size-1:
                        if start_generation[self.position_x][self.position_y+1] == 7:
                            self.position_y += 1
                    if self.position_x > 0 and self.position_y > 0:
                        if start_generation[self.position_x-1][self.position_y-1] == 7:
                            self.position_x -= 1
                            self.position_y -= 1
                    if self.position_x > 0 and self.position_y < grid_size-1:
                        if start_generation[self.position_x-1][self.position_y+1] == 7:
                            self.position_x -= 1
                            self.position_y += 1
                    if self.position_x < grid_size-1 and self.position_y > 0:
                        if start_generation[self.position_x+1][self.position_y-1] == 7:
                            self.position_x += 1
                            self.position_y -= 1
                    if self.position_x < grid_size-1 and self.position_y < grid_size-1:
                        if start_generation[self.position_x+1][self.position_y+1] == 7:
                            self.position_x += 1
                            self.position_y += 1
            
            if self.sense == 2:
                if self.position_x > 0:
                    if start_generation[self.position_x-1][self.position_y] == 7 or start_generation[self.position_x-2][self.position_y] == 7:
                        self.position_x -= 1
                if self.position_x < grid_size-1:
                    if start_generation[self.position_x+1][self.position_y] == 7:
                        self.position_x += 1
                if self.position_y > 0:
                    if start_generation[self.position_x][self.position_y-1] == 7:
                        self.position_y -= 1
                if self.position_y < grid_size-1:
                    if start_generation[self.position_x][self.position_y+1] == 7:
                        self.position_y += 1
                if self.position_x > 0 and self.position_y > 0:
                    if start_generation[self.position_x-1][self.position_y-1] == 7:
                        self.position_x -= 1
                        self.position_y -= 1
                if self.position_x > 0 and self.position_y < grid_size-1:
                    if start_generation[self.position_x-1][self.position_y+1] == 7:
                        self.position_x -= 1
                        self.position_y += 1
                if self.position_x < grid_size-1 and self.position_y > 0:
                    if start_generation[self.position_x+1][self.position_y-1] == 7:
                        self.position_x += 1
                        self.position_y -= 1
                if self.position_x < grid_size-1 and self.position_y < grid_size-1:
                    if start_generation[self.position_x+1][self.position_y+1] == 7:
                        self.position_x += 1
                        self.position_y += 1

        else:
            if direction == "UP" and self.position_y > 0 and not(check_occupancy(origin_cells, self.position_x, self.position_y-1)):
                self.position_y -= 1
            elif direction == "DOWN" and self.position_y < grid_size-1 and not(check_occupancy(origin_cells, self.position_x, self.position_y+1)):
                self.position_y += 1
            elif direction == "RIGHT" and self.position_x < grid_size-1 and not(check_occupancy(origin_cells, self.position_x+1, self.position_y)):
                self.position_x += 1
            elif direction == "LEFT" and self.position_x > 0 and not(check_occupancy(origin_cells, self.position_x-1, self.position_y-1)):
                self.position_x -= 1
            if start_generation[self.position_x][self.position_y] == 7:
                self.feed = self.eat_food()

        start_generation[self.position_x][self.position_y] = self.color

    # Eating food on the same location
    def eat_food(self):
        #print(str(self.position_x) + " " + str(self.position_y) + " has eaten food")
        return True




# Check if the movement can be done, since the pixel is unoccupied
def check_occupancy(check_occupancy_cells: list[Cell_Class], position_x: int, position_y: int) -> bool:
    occupant: bool = False
    for cell in check_occupancy_cells:
        if cell.position_x == position_x and cell.position_y == position_y:
            occupant = True
    
    return occupant

# Create a starting generation
start_generation: list[list[int]] = matrix 
def create_generation(def_matrix: list[list[int]]) -> list[list[int]]:
    def_matrix = copy.deepcopy(def_matrix)
    def_color = copy.deepcopy(colors)
    # White cells and food doesn't exist in cell generation
    def_color.remove((255, 255, 255))
    for i in range(cell_count):
        color = random.choice(def_color)

        # As long as the position is not occupied, a random colored cell will be created
        while True:
            spawn_location_chance = random.randint(0, 3)
            if spawn_location_chance == 0:
                x_pos = random.randint(grid_size//20*19, grid_size-1)
                y_pos = random.randint(0, grid_size-1)
            elif spawn_location_chance == 1:
                x_pos = random.randint(0, grid_size//20)
                y_pos = random.randint(0, grid_size-1)  
            elif spawn_location_chance == 2:
                x_pos = random.randint(0, grid_size-1)  
                y_pos = random.randint(0, grid_size//20)
            else:
                x_pos = random.randint(0, grid_size-1)
                y_pos = random.randint(grid_size//20*19, grid_size-1)

            if def_matrix[x_pos][y_pos] == 0:
                def_matrix[x_pos][y_pos] = color_mapping_cells[color]
                break

    return def_matrix
start_generation = create_generation(matrix)

# Creates cells through the "Cell Class" with attributes and saves them in a list
origin_cells = []
def create_random_cells(def_matrix: list[list[int]]) -> list[Cell_Class]:
    def_matrix = copy.deepcopy(def_matrix)
    for y in range(grid_size):
        for x in range(grid_size):
            if def_matrix[x][y] != 0:
               
               # Cell with color attribute is creted according to the value of the matrix[x][y]
               cell = Cell_Class(def_matrix[x][y], x, y)
               # Set the movement order according to color of itself
               cell.set_movement()
               # After setting all the attributes, add the cell to the "cells" list
               origin_cells.append(cell)

    return origin_cells

origin_cells = create_random_cells(start_generation)

# Cells move
def move_cells(def_move_cells: list[Cell_Class]) -> list[Cell_Class]:
    if def_move_cells:
        for cell in def_move_cells:
            new_cells = cell.move_cell()
        return new_cells
    else:
        print("The cells are gone extinct")
        exit()


# Draw the cells on the grid
def draw(cells: list[Cell_Class]):

    for cell in cells:
        value_to_find = cell.color
        # Finding the key from the value in a dictionary
        color = [key for key, value in color_mapping_cells.items() if value == value_to_find][0]
        if cell.position_x >= 80:
            cell.position_x //= 10
            cell.position_x -= random.randint(1, 8)
        if cell.position_y >= 80:
            cell.position_y //= 10
            cell.position_y -= random.randint(1, 8)
        pygame.draw.rect(screen, color, (cell.position_x*10+1, cell.position_y*10+1, 9, 9))

# Cells that are in the yellow zone, can move on to next generation
def survive(cells: list[Cell_Class]) -> list[Cell_Class]:
    survivors: list[Cell_Class] = []
    for cell in cells:
        if ((cell.position_x >= grid_size*19/20 or cell.position_x <= grid_size/20) or (cell.position_y >= grid_size*19/20 or cell.position_y <= grid_size/20)) and cell.feed == True:
            survivors.append(cell)
    print(len(survivors))
    return survivors

"""#NOT IN USE
# Scale the survivors to 500 cells
def scale(def_scaled_cells: list[Cell_Class]) -> list[Cell_Class]:

    # Color values
    color_mapping: list[int] = [1, 2, 3, 4, 5, 6]
    # Color counts in the cell
    color_counts = np.zeros(len(color_mapping), dtype=int)

    # Count the occurrences of each color in the cell
    for cell in def_scaled_cells:
        if cell.color in color_mapping:
            color_counts[color_mapping.index(cell.color)] += 1

    # Total count of cells
    total_count = np.sum(color_counts)

    # Calculate probabilities and scale to total_cells
    probabilities: float = color_counts / total_count
    scaled_counts = np.round(probabilities * 500).astype(int)

    # Adjust for rounding error
    diff: int = 500 - np.sum(scaled_counts)
    if diff != 0:
        max_index: int = np.argmax(probabilities)
        scaled_counts[max_index] += diff

    # Seperate the scaled counts from the list
    new_black_count, new_orange_count, new_red_count, new_green_count, new_blue_count, new_pink_count = scaled_counts
    def_scaled_cells = create_scaled_cells(new_blue_count, new_orange_count, new_red_count, new_green_count, new_black_count, new_pink_count)

    return def_scaled_cells
"""

# Every single survivor cell creates 3 kids
def reproduce(def_reproduced_cells: list[Cell_Class]) -> list[Cell_Class]:
    # Color values and initialization
    color_mapping: list[int] = [1, 2, 3, 4, 5, 6]
    color_counts = {color: 0 for color in color_mapping}
    
    # Count the initial occurrences of each color
    for cell in def_reproduced_cells:
        if cell.color in color_mapping:
            color_counts[cell.color] += 1
    
    # Calculate the updated color counts after reproduction
    new_color_counts = color_counts.copy()
    
    for color in color_mapping:
        initial_count = color_counts[color]
        # Cell reproduces with %80 2 new cells with the same color
        reproduced_count = sum(3 for _ in range(initial_count) if random.random() <= 0.8)
        new_color_counts[color] += reproduced_count

    new_blue_count = new_color_counts.get(5, 0)
    new_orange_count = new_color_counts.get(2, 0)
    new_red_count = new_color_counts.get(3, 0)
    new_green_count = new_color_counts.get(4, 0)
    new_black_count = new_color_counts.get(1, 0)
    new_pink_count = new_color_counts.get(6, 0)
    def_reproduced_cells = create_scaled_cells(new_blue_count, new_orange_count, new_red_count, new_green_count, new_black_count, new_pink_count)

    return def_reproduced_cells


# Creates a random x_pos and y_pos for a single cell use
def randomize_position() -> set[int]:

    spawn_location_chance = random.randint(0, 3)
    if spawn_location_chance == 0:
        x_pos = random.randint(grid_size//20*19, grid_size-1)
        y_pos = random.randint(0, grid_size-1)
    elif spawn_location_chance == 1:
        x_pos = random.randint(0, grid_size//20)
        y_pos = random.randint(0, grid_size-1)  
    elif spawn_location_chance == 2:
        x_pos = random.randint(0, grid_size-1)  
        y_pos = random.randint(0, grid_size//20)
    else:
        x_pos = random.randint(0, grid_size-1)
        y_pos = random.randint(grid_size//20*19, grid_size-1)

    return  (x_pos, y_pos)


# Create the new scaled cells according to survivors
def create_scaled_cells(new_blue_count, new_orange_count, new_red_count, new_green_count, new_black_count, new_pink_count):
    
    # Combine the color counts with their corresponding color mappings
    color_counts: dict = {
        5: new_blue_count,   # Blue
        1: new_black_count,  # Black
        2: new_orange_count, # Orange
        3: new_red_count,    # Red
        4: new_green_count,  # Green
        6: new_pink_count    # Pink
    }
    
    # Use a set to track used (x, y) positions to avoid overlap
    used_positions = set()
    created_scaled_cells: list[Cell_Class] = []
    
    # Create the cells based on the color counts
    for color, count in color_counts.items():
        for _ in range(count):
            while True:
                position = randomize_position()
                x_pos, y_pos = position
                if position not in used_positions:
                    cell = Cell_Class(color, x_pos, y_pos)
                    # Mark this position as used
                    used_positions.add(position)
                    cell.set_movement()
                    created_scaled_cells.append(cell)
                    # Exit the loop and create the next cell
                    break  

    return created_scaled_cells

# Food creation at the beginning of each generation
def create_food(def_start_generation: list[list[int]]) -> list[list[int]]:
    # They can only be created in the middle, so non-spawn zone for cells
    for x in range(grid_size//20, grid_size//20*19):
        for y in range(grid_size//20, grid_size//20*19):
            # Food creation chance
            if random.randint(1, 100) < food_creation_chance and def_start_generation[x][y] == 0:
                def_start_generation[x][y] = 7

    return def_start_generation

# Draw the created food
def draw_food(def_start_generation: list[list[int]]):

    for x in range(grid_size):
        for y in range(grid_size):
            if def_start_generation[x][y] == 7:
                pygame.draw.rect(screen, PURPLE, (x*10+1, y*10+1, 9, 9))

counter: int = 0
# Main loop
while True:
    
    while running:

        # Closing the display with ESC or Quit 
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                running = False
        
        # Background
        screen.fill((255, 255, 255))

        # Zone where the cells could live to the other generations
        pygame.draw.rect(screen, (255, 255, 0), (grid_size*19/2, 0, display_size-grid_size*9, grid_size*10))
        pygame.draw.rect(screen, (255, 255, 0), (0, 0, display_size-grid_size*19/2, grid_size*10))
        pygame.draw.rect(screen, (255, 255, 0), (0, grid_size*19/2, grid_size*10 , display_size-grid_size*19/2))
        pygame.draw.rect(screen, (255, 255, 0), (0, 0, grid_size*10, display_size-grid_size*19/2))

        # Grid of the display
        [pygame.draw.line(screen, (0, 0, 0), (x, 0), (x, 800)) for x in range(10, display_size, 10)]
        [pygame.draw.line(screen, (0, 0, 0), (0, y), (800, y)) for y in range(10, display_size, 10)]

        if counter == 1:
            start_generation = create_food(start_generation)
        draw_food(start_generation)
        
        # Display the start generation at the beginning
        draw(origin_cells)

        new_cells = move_cells(origin_cells)

        # Delay the display
        clock.tick(10)

        # Update the display
        pygame.display.update()

        # Stops the generation after 100 rounds
        counter += 1
        if counter > round_limit:
            running = False

    # Find the survivors
    survivors: list[Cell_Class] = survive(origin_cells)

    # Scale the survivors to 500
    survivors = reproduce(survivors)

    origin_cells = survivors

    # Ask if the survivors should be passed to next generation
    print("Do you want to re-run the simulation? If so, press the SPACEBAR to restart or ESC/QUIT to quit.")
    waiting_for_restart = True
    while waiting_for_restart:
        for event in pygame.event.get():
            # Restart on spacebar press
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                running = True
                counter = 0
                # Exit the waiting loop and restart the simulation
                waiting_for_restart = False  
            #Quit on ESC press
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                # Exit the waiting loop and quit
                waiting_for_restart = False  
                pygame.quit()
                exit()


