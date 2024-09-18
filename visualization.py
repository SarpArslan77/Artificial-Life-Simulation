
# Libraries from general
import pygame

# Imported files
from config import Config


# A class "Visualizer" for the display, drawing and pygame 
class Visualization:
    def __init__(self, config:Config):

        # Parameter for the Class "Config"
        self.config = config

        # Settings for the pygame-display
        self.screen = pygame.display.set_mode((config.display_size, config.display_size))
        self.display_caption = pygame.display.set_caption("Evolution Simulation")

        # Set the pygame clock for delaying the display
        self.clock = pygame.time.Clock()

        # Const for the visualization
        self.YELLOW: tuple = (255, 255, 0)
        self.PURPLE: tuple = (128, 0, 128)
        self.ORANGE: tuple = (245, 180, 70)

    # Draw the display at each update
    def draw(self, simulation) -> None:
        """
        Clears the screen and redraws the simulation elements including survival zones, grid, food, and cells.
        
        Args:
            simulation: The simulation object containing matrix and cells to be drawn.
        """
        
        # Fill the screen white
        self.screen.fill((255, 255, 255))
        
        # Draw the survival zones(yellow zones)
        self.draw_survival_zones()
        
        # Draw the grid for the cells
        self.draw_grid()
        self.draw_food(simulation.matrix)
        self.draw_cells(simulation.cells)

    # Draw the survival zones(yellow_zones)
    def draw_survival_zones(self) -> None:
        """
        Draws the yellow survival zones on the screen based on the predefined zone coordinates.
        """
        pygame.draw.rect(self.screen, self.YELLOW, (self.config.grid_size*19/2, 0, self.config.display_size-self.config.grid_size*9, self.config.grid_size*10))
        pygame.draw.rect(self.screen, self.YELLOW, (0, 0, self.config.display_size-self.config.grid_size*19/2, self.config.grid_size*10))
        pygame.draw.rect(self.screen, self.YELLOW, (0, self.config.grid_size*19/2, self.config.grid_size*10, self.config.display_size-self.config.grid_size*19/2))
        pygame.draw.rect(self.screen, self.YELLOW, (0, 0, self.config.grid_size*10, self.config.display_size-self.config.grid_size*19/2))

    # Draw the grid for the cells
    def draw_grid(self) -> None:
        """
        Draws the grid lines on the screen at intervals of 10 pixels.
        """
        for x in range(10, self.config.display_size, 10):
            pygame.draw.line(self.screen, (0, 0, 0), (x, 0), (x, self.config.display_size))
        for y in range(10, self.config.display_size, 10):
            pygame.draw.line(self.screen, (0, 0, 0), (0, y), (self.config.display_size, y))

    # Draw the foods according to the simulation matrix
    def draw_food(self, matrix) -> None:
        """
        Draws food items on the screen based on the matrix values.
        
        Args:
            matrix: The matrix representing the simulation grid, where food items are marked.
        """
        for x in range(self.config.grid_size):
            for y in range(self.config.grid_size):
                if matrix[x][y] == self.config.matrix_food_exist:
                    pygame.draw.rect(self.screen, self.PURPLE, (x*10+2, y*10+2, 7, 7))

    # Draw cells according to the simulation cells
    def draw_cells(self, cells) -> None:
        """
        Draws the cells on the screen based on their positions.
        
        Args:
            cells: List of Cell objects to be drawn on the screen.
        """
        for cell in cells:
            pygame.draw.rect(self.screen, self.ORANGE, (cell.position_x*10+1, cell.position_y*10+1, 9, 9))
