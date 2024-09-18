
from config import Config
from cell import Cell

# A class "Stats" for the track of the attrbiutes accross generations
class Stats:
    def __init__(self, config: Config):

        # Parameter for the Class "Config"
        self.config = config

        # Consts to be changed after the update function
        self.population_count = 0
        self.average_food_sense = 0
        self.total_food_sense = 0

    # Update the stats after each generation
    def update(self, cells: list[Cell]):
        """
        Updates the statistics of the current generation based on the list of cells.

        Args:
            cells (list[Cell]): List of cell objects in the current generation.
        """
        # Count the cell count
        self.population_count = len(cells)
        
        # Calculate the average_food_sense
        if self.population_count > 0:
            self.total_food_sense = sum(cell.food_sense for cell in cells)
            self.average_food_sense = self.total_food_sense / self.population_count
        else:
            self.total_food_sense = 0
            self.average_food_sense = 0

    # Display the stats
    def display_average_food_sense(self):
        """
        Displays the statistics for the current generation, including the population count and
        the average food sense of the cells.
        """
        print(f"Generation: {self.config.generation_count}")
        print(f"Population: {self.population_count}")
        print(f"Avg Food Sense: {self.average_food_sense:.2f}")
        print("------------------------")
