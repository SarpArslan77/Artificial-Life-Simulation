
#TODO: save the stats to a cvc, to be able to examine them later on
#TODO: speed levels result in the cell jumping and not actually moving 2-3 blocks per round
#TODO: check the food_supply and use_food logic and add a stat for the food_supply and energy consumption
#! Energy consumption logic has unexpected results, check those mechanisms
#! High speed causes the cells to jump over occupied blocks, it should check whether the way is unoccupied first
#! Some cells stop moving when they reach the border of the suriviving zones
#! Some cells stop in the middle

# General libraries
import pygame
import sys

# Imported files
from config import Config
from simulation import Simulation
from visualization import Visualization
from stats import Stats

# Create instances
config = Config()
simulation = Simulation(config)
visualization = Visualization(config)
stats = Stats(config)

# Main loop
if __name__ == "__main__":

    # Initialize pygame
    pygame.init()
    
    # clock for the delay
    clock = pygame.time.Clock()

    while simulation.main_loop:


        # counter to count each round
        counter: int = 0

        # clear all the previous food
        simulation.clear_food()

        # create newly fresh food for each round
        simulation.create_food()

        # update the surviving_zone_update at the beginning of each generation
        simulation.matrix_surviving_zone_update()

        # Use one food from food_supply for each cell, at the beginning of the round
        #       also update the cell.can_move to True for each round
        for cell in simulation.cells:
            [cell.use_food() for _ in range(cell.energy_consumption)]
            cell.can_move = True

        # Main loop
        while simulation.running:
            
            # If ESC or QUIT is pressed, the simulation ends
            for event in pygame.event.get():
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                    simulation.running = False
                    simulation.main_loop = False

            # Update cell simulation
            simulation.cell_update()
            
            # Draw everything
            visualization.draw(simulation)
           
            # Update display
            pygame.display.update()
            
            # Control frame rate
            clock.tick(config.simulation_speed)
            
            # Increment counter and check for round limit
            counter += 1
            if counter > config.round_limit:
                config.generation_count += 1
                simulation.running = False
        
        # Update and display stats after each generation
        stats.update(simulation.cells)
        stats.display_average_stats()
        
        # Surviving cells are determined and reproduced to next generations
        simulation.survive_cells()
        simulation.reproduce_cells(simulation.cells)

        # Update the matrix according to new cells
        simulation.matrix_cells_update()
       
        # Ask for restart or quit
        waiting_for_restart = True
        while waiting_for_restart:
            for event in pygame.event.get():
                
                # If SPACE is pressed, the simulation goes onto the next generation
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting_for_restart = False  # Restart the simulation
                        simulation.running = True
                
                # If ESC or QUIT is pressed, it should end the simulation
                    elif event.key == pygame.K_ESCAPE:
                        waiting_for_restart = False
                        simulation.main_loop = False
                elif event.type == pygame.QUIT:
                    waiting_for_restart = False
                    simulation.main_loop = False
    
    # End the pygame display
    pygame.quit()
    # To be sure, end the whole programm
    sys.exit()
