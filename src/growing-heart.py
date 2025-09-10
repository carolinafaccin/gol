"""
Creates a .gif image with a 20x20 grid, 21 steps, featuring 1 growing heart.

Under traditional rules, the cells forming the heart would diminish
due to the rules of loneliness (a live cell with fewer than 2 neighbors dies)
and overpopulation (a live cell with more than 3 neighbors dies).

To make the heart "grow", the rules needed to be made more "generous",
allowing cells to survive with more neighbors and thus expand.

To change this rule, the 'update' method within the 'Game' class was adjusted.
"""

# Importing necessary libraries
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import imageio
import os

# --- Main Game of Life Class ---
# --- Main Game of Life Class ---
class Game():
    def __init__(self, linhas, colunas) -> None:
        """
        Initializes the Game of Life board with a single heart pattern in the center.
        
        Args:
            linhas (int): Number of rows on the board.
            colunas (int): Number of columns on the board.
        """
        self.linhas = linhas
        self.colunas = colunas
        
        # 1. Start with a completely empty grid (dtype=int is fine for 0s and 1s)
        self.grid = np.zeros((linhas, colunas), dtype=int)

        # 2. Define the heart pattern using 1 for "alive"
        heart_pattern = np.array([
            [0, 1, 1, 0, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 0]
        ], dtype=int)

        # Helper function to place a pattern at a given position
        def place_pattern(grid, pattern, center_row, center_col):
            pattern_height, pattern_width = pattern.shape
            start_row = center_row - pattern_height // 2
            start_col = center_col - pattern_width // 2
            
            # Ensures the pattern fits on the grid before placing it
            if start_row >= 0 and start_col >= 0 and \
               (start_row + pattern_height) <= grid.shape[0] and \
               (start_col + pattern_width) <= grid.shape[1]:
                grid[start_row : start_row + pattern_height, start_col : start_col + pattern_width] = pattern
        
        # 3. Calculate the center of the grid
        center_row = self.linhas // 2
        center_col = self.colunas // 2

        # 4. Place the heart pattern in the center of the grid
        place_pattern(self.grid, heart_pattern, center_row, center_col)

    def update(self) -> None:
        """
        Applies the Game of Life rules to advance one generation (step).
        
        Standard Rules:
            1. A live cell survives if it has 2 or 3 live neighbors.
            2. A dead cell is born if it has exactly 3 live neighbors.
        
        New "Growth" Rules:
            1. A live cell survives with a wider range of neighbors, e.g., 2 to 5.
               This combats "overpopulation" and encourages larger clusters to form.
               We defined the values 2 to 4.
            2. The birth rule is kept the same (born with 3 neighbors), as it already
               promotes expansion into empty areas.
        """

        new_grid = self.grid.copy()
        for i in range(self.linhas):
            for j in range(self.colunas):
                # The sum now correctly counts neighbors again
                total_vizinhos = int((
                    self.grid[(i-1) % self.linhas, (j-1) % self.colunas] +
                    self.grid[(i-1) % self.linhas, j % self.colunas] +
                    self.grid[(i-1) % self.linhas, (j+1) % self.colunas] +
                    self.grid[i % self.linhas, (j-1) % self.colunas] +
                    self.grid[i % self.linhas, (j+1) % self.colunas] +
                    self.grid[(i+1) % self.linhas, (j-1) % self.colunas] +
                    self.grid[(i+1) % self.linhas, j % self.colunas] +
                    self.grid[(i+1) % self.linhas, (j+1) % self.colunas]
                ))


                # Survival Rule check now uses 1 for "alive"
                if self.grid[i, j] == 1 and (total_vizinhos < 2 or total_vizinhos > 5):
                    new_grid[i, j] = 0
                # Birth Rule sets new cells to 1
                elif self.grid[i, j] == 0 and total_vizinhos == 3:
                    new_grid[i, j] = 1
                
        
        self.grid = new_grid

# --- Function to create and save the animation ---
def create_animation(matriz_size, steps, output_filename):
    """
    Runs the simulation and generates an animated GIF.
    """
    game = Game(matriz_size, matriz_size)
    frames = []

    print("Generating frames for the animation...")
    
    for step_num in range(steps):
        fig, ax = plt.subplots(figsize=(3.5, 3.5), dpi=100)

        # Define as cores: a primeira para o valor 0, a segunda para o valor 1
        colors = ["white", "#f77877"] # 0 -> white, 1 -> red
        custom_cmap = mcolors.ListedColormap(colors)
        ax.imshow(game.grid, cmap=custom_cmap) 

        ax.set_title(
            f"Step: {step_num}", 
            fontsize=14, 
            fontname='Helvetica',
            pad=10
        )
        ax.set_xticks([])
        ax.set_yticks([])

        fig.canvas.draw()

        width_float, height_float = fig.canvas.renderer.get_canvas_width_height()
        width = int(width_float)
        height = int(height_float)
        
        buffer = fig.canvas.tostring_argb()
        image_rgba = np.frombuffer(buffer, dtype='uint8').reshape(height, width, 4)
        frames.append(image_rgba[:, :, 1:].copy()) # Get the R, G, B channels, ignoring Alpha

        plt.close(fig)
        game.update()
        print(f"  - Step {step_num + 1}/{steps} completed.")

    print(f"\nSaving animation to '{output_filename}'...")
    imageio.mimsave(output_filename, frames, fps=10, loop=0)
    print("Animation saved successfully!")

# --- Main Script Execution ---
if __name__ == '__main__':
    
    # --- FIXED SIMULATION PARAMETERS ---
    matriz_size = 20
    total_steps = 26
    
    print(f"Starting simulation: {matriz_size}x{matriz_size} grid, {total_steps} steps.")

    # --- Logic to create folder and filename ---

    # Get the current script's directory
    script_dir = os.path.dirname(__file__)
    # Go up one level to the project root directory
    project_root = os.path.dirname(script_dir)
    # Create the path for the output folder
    output_dir = os.path.join(project_root, 'figures', 'gif', 'tests')

    # Create the directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Dynamically create the base filename from the script's name
    base_filename = os.path.splitext(os.path.basename(__file__))[0]

    # Find the next available version number
    version = 1
    while True:
        # Format the version number with 3 digits (e.g., 1 -> '001')
        version_str = f"v{version:03d}"
        # Assemble the filename with the version
        gif_filename = f"{base_filename}_{version_str}.gif"
        # Assemble the full path for the file
        full_path = os.path.join(output_dir, gif_filename)

        # Check if a file with this name already exists
        if not os.path.exists(full_path):
            break # If it doesn't exist, we've found the right name and exit the loop
        version += 1 # If it exists, try the next version
    
    # Call the main function with the fixed values and the versioned path
    create_animation(matriz_size, total_steps, full_path)