
# TODO: Refactor this function to improve performance
# ! This is a critical section of the code
# ? Does this logic make sense here?
# * Deprecated: No longer using this function
# This is a standard comment

#TODO: Compare the main loop to evolution.py main loop to find the differences(especially the restart condition)
#TODO: check the new_generation variable and the reproduce function, it seems like they are not being used in the loop rn

# General libraries
import pygame

# Imported files
from config import Config
from cell import Cell
from simulation import Simulation
from visualization import Visualization

# Main function
def main():

    # Initialize pygame
    pygame.init()

    # Create instances
    config = Config()
    simulation = Simulation(config)
    visualization = Visualization(config)

    # running boolean to stop the loop, when ESC or QUIT pressed
    running: bool = True

    # clock for the delay
    clock = pygame.time.Clock()

    # counter to count each round
    counter: int = 0

    # Create the food
    simulation.create_food()

    # Main loop
    while running:

        # If ESC or QUIT is pressed, the simulation ends
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                running = False

        # Update simulation
        simulation.update()

        # Draw everything
        visualization.draw(simulation)

        # Update display
        pygame.display.update()

        # Control frame rate
        clock.tick(config.delay_amount)

        # Increment counter and check for round limit
        counter += 1
        if counter > config.round_limit:
            running = False

    # Game over logic
    survivors = simulation.survive_cells()
    new_generation = simulation.reproduce_cells(survivors)

    # Ask for restart or quit
    waiting_for_restart = True
    while waiting_for_restart:
        for event in pygame.event.get():
            # If SPACE is pressed, the simulation goes onto the next generation
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main()  # Restart the simulation

            # If ESC ord QUIT is pressed, it should end the simulation
                elif event.key == pygame.K_ESCAPE:
                    waiting_for_restart = False
            elif event.type == pygame.QUIT:
                waiting_for_restart = False

    # End the pygame display
    pygame.quit()

# Extra precaution to check, whether this file is the main file to run the simulation
if __name__ == "__main__":
    # Show time baby
    main()