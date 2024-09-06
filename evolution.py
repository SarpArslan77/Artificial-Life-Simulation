# ERRORS:
# 4) CELLS GOES THROUGH EACH OTHER, THEY CAN NOT BE ON THE SAME PIXEL
# 7) WHEN THE NEW GENERATION IS BEING BORN, THEY TEND TO BE IN THE MIDDLE, THEY SHOULD BE EQUALLY DISTRIBUTED ACROSS THE DISPLAY
# 8) SOMETHING CAUSES TOO MUCH LOOP AND IT DELAYS THE BORN OF THE NEW GENERATION
# 9) WORK ON RANDOMIZE_POSITION FUNCTION, RANDOMIZATION IS NOW BEING MADE IN THE CREATE_SCALED_CELLS BUT IT SHOULD HAVE A SEPERATE FUNCTION


import pygame
import random
import copy
import numpy as np

# Initialize the pygame library
pygame.init()

# Background size
screen = pygame.display.set_mode((500, 500))

# Display title
pygame.display.set_caption("Evolution Simulation")

# Clock for the delay
clock = pygame.time.Clock()

grid_size: int = 50 # Change the create_generation loop time, regarding how many cells should be created
running: bool = True
matrix: list[list[int]] = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
speed: int = 98

# Dictionary of all possible colors, which effects the movement attributes
color_mapping: dict = {
    (0, 0, 0): 1,      # BLACK, stays still
    (245, 180, 70): 2, # ORANGE, moves in every direction
    (255, 0, 0): 3,     # RED, moves only upwards
    (0, 255, 0): 4,     # GREEN, moves only downwards
    (0, 0, 255): 5,     # BLUE, moves only to right
    (255, 192, 203): 6,  # PINK, moves only to left
    (255, 255, 255): 0, # WHITE, dead cell
}
colors: list[int] = list(color_mapping.keys())

# Cell class with its attributes
class Cell_Class:

    movement: dict = {
        2: "ALL",
        3: "UP",
        4: "DOWN",
        5: "RIGHT",
        6: "LEFT"
    }

    def __init__(self, color, position_x, position_y, move=None):
        self.color = color
        self.move = move
        self.position_x = position_x
        self.position_y = position_y

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
        if direction == "UP" and self.position_y > 0 and not(check_occupancy(origin_cells, self.position_x, self.position_y-1)):
            self.position_y -= 1
        elif direction == "DOWN" and self.position_y < 49 and not(check_occupancy(origin_cells, self.position_x, self.position_y+1)):
            self.position_y += 1
        elif direction == "RIGHT" and self.position_x < 49 and not(check_occupancy(origin_cells, self.position_x+1, self.position_y)):
            self.position_x += 1
        elif direction == "LEFT" and self.position_x > 0 and not(check_occupancy(origin_cells, self.position_x-1, self.position_y-1)):
            self.position_x -= 1
        start_generation[self.position_x][self.position_y] = self.color

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
    # White cells doesn't exist
    def_color.remove((255, 255, 255))
    for i in range(grid_size*10):
        color = random.choice(def_color)

        # As long as the position is not occupied, a random colored cell will be created
        while True:
            x_pos = random.randint(0, grid_size-1)
            y_pos = random.randint(0, grid_size-1)

            if def_matrix[x_pos][y_pos] == 0:
                def_matrix[x_pos][y_pos] = color_mapping[color]
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
def move_cells(cells: list[Cell_Class]) -> list[Cell_Class]:
    if cells is not None:
        for cell in cells:
            new_cells = cell.move_cell()
        return new_cells

# Draw the cells on the grid
def draw(cells: list[Cell_Class]):
    #print("In draw there are cells amount of" + str(len(cells)))
    for cell in cells:
        value_to_find = cell.color
        # Finding the key from the value in a dictionary
        color = [key for key, value in color_mapping.items() if value == value_to_find][0]
        #print(cell.position_x, cell.position_y)
        if cell.position_x >= 50:
            cell.position_x //= 10
            cell.position_x -= random.randint(1, 5)
        if cell.position_y >= 50:
            cell.position_y //= 10
            cell.position_y -= random.randint(1, 5)
        pygame.draw.rect(screen, color, (cell.position_x*10+1, cell.position_y*10+1, 9, 9))

# Cells that are in the yellow zone, can move on to next generation
def survive(cells: list[Cell_Class]) -> list[Cell_Class]:
    survivors: list[Cell_Class] = []
    for cell in cells:
        if cell.position_x >= grid_size*4/5:
            survivors.append(cell)

    return survivors

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


#TO BE WORK ON
#def randomize_position(cells: list[Cell_Class]) -> list[Cell_Class]:


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
                x_pos = random.randint(0, grid_size * 10 - 1)
                y_pos = random.randint(0, grid_size * 10 - 1)
                position = (x_pos, y_pos)
                
                if position not in used_positions:
                    cell = Cell_Class(color, x_pos, y_pos)
                    used_positions.add(position)  # Mark this position as used
                    cell.set_movement()
                    created_scaled_cells.append(cell)
                    break  # Exit the loop and create the next cell

    return created_scaled_cells
       
counter: int = 0
print(start_generation)
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
        pygame.draw.rect(screen, (255, 255, 0), (grid_size*8, 0, 420, grid_size*10))
        # Grid of the display
        [pygame.draw.line(screen, (0, 0, 0), (x, 0), (x, 500)) for x in range(10, 500, 10)]
        [pygame.draw.line(screen, (0, 0, 0), (0, y), (500, y)) for y in range(10, 500, 10)]

        # Display the start generation at the beginning
        draw(origin_cells)

        new_cells = move_cells(origin_cells)

        # Delay the display
        clock.tick(10)

        # Update the display
        pygame.display.update()

        # Stops the generation after 10 rounds
        counter += 1
        if counter > 10:
            running = False

    # Find the survivors
    survivors: list[Cell_Class] = survive(origin_cells)

    # Scale the survivors to 500
    survivors = scale(survivors)

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



