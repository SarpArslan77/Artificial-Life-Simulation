# Artificial-Life-Simulation

This project simulates artificial life forms in a grid-based environment, exploring concepts of survival, reproduction, and adaptation.

## Key Features

- Grid-based simulation environment
- Cells with attributes like food sense and zone sense
- Food generation and consumption mechanics
- Survival zones and generational cycles
- Pygame-based visualization

## How It Works

1. **Initialization**: The simulation starts with a set number of cells randomly placed in survival zones.

2. **Cell Behavior**: 
   - Cells move randomly or towards food if sensed.
   - They consume food to increase their food supply.
   - Cells must reach survival zones with food supply to survive each generation.

3. **Environment**: 
   - Food generates randomly within the grid.
   - Survival zones are preset areas where cells must reach to survive.

4. **Generational Cycle**:
   - After a set number of rounds, surviving cells reproduce.
   - Offspring inherit sensory attributes from parents.

5. **Visualization**: 
   - Pygame renders the grid, cells, food, and survival zones.
   - Cells and food are color-coded for easy identification.

## Components

- `main.py`: Entry point, manages the simulation loop.
- `config.py`: Contains configuration settings.
- `cell.py`: Defines the Cell class with movement and sensing logic.
- `simulation.py`: Manages the overall simulation state and logic.
- `visualization.py`: Handles the Pygame-based rendering.

## Running the Simulation

Execute `main.py` to start the simulation. Press SPACE to start a new generation or ESC to quit.
