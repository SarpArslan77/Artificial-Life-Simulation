
# TODO: Refactor this function to improve performance
# ! This is a critical section of the code
# ? Does this logic make sense here?
# * Deprecated: No longer using this function
# This is a standard comment



# "Config" class for the general constants


class Config:
    def __init__(self):
        # General constants
        self.display_size: int = 800
        self.grid_size: int = 80
        self.cell_count: int = 500
        self.round_limit: int = 100
        self.delay_amount: int = 5 
        self.move_chance: int = 90
        self.food_creation_chance: int = 3
        self.reproduce_chance: float = 0.8
        self.matrix_empty: int = 0
        self.matrix_cell_exist: int = 1
        self.matrix_food_exist: int = 9
        self.matrix_zone_exist: int = 5

        # Constants for the simulation
        self.running: bool = True
        
        # Create the surviving_zones, zones that the cells could live to next generation upon the creation of the cell "Config"
        self.surviving_zones: list[tuple[int, int]] = self.get_surviving_locations()

    # Create all the surviving locations for the cells the survive
    def get_surviving_locations(self) -> list[tuple[int, int]]:
        surviving_locations = []

        # Define the zone boundaries
        west_x_start = self.grid_size * 19 // 20
        north_y_end = self.grid_size // 20
        south_y_start = self.grid_size * 19 // 20
        east_x_end = self.grid_size // 20

        # West Zone
        surviving_locations.extend(((x, y) for x in range(west_x_start, self.grid_size) for y in range(self.grid_size)))

        # North Zone
        surviving_locations.extend(((x, y) for x in range(north_y_end) for y in range(self.grid_size)))

        # East Zone
        surviving_locations.extend(((x, y) for x in range(self.grid_size) for y in range(east_x_end)))

        # South Zone
        surviving_locations.extend(((x, y) for x in range(self.grid_size) for y in range(south_y_start, self.grid_size)))

        return surviving_locations

        