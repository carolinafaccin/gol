![](https://img.shields.io/badge/status-development-red.svg)
![Top Language](https://img.shields.io/github/languages/top/carolinafaccin/gol)

# GOL
**GOL** - _Game of Life_ - is a coding project for hands-on practice with programming logic, data structures, and algorithms. 

The project aims to build a functional version of John Conway's classic cellular automaton, a system that simulates the evolution of cells based on a set of simple rules.

[![Documentation](https://img.shields.io/badge/docs-read%20the%20documentation-brightgreen)](https://carolinafaccin.github.io/gol/)

## Project Goals
- Implement core logic: Develop the rules for a two-dimensional grid based on Conway's four rules.
- Visualize the simulation: Create a visual representation of the grid and its evolution over time.
- Explore different patterns: Experiment with famous initial patterns like the Glider, Lightweight Spaceship, and Gosper Glider Gun.

## Installing and running GOL on a local machine

Follow these generic steps:

1) Install `python 3`;
2) Install the following Python dependencies:
   * `numpy`;
   * `matplotlib`;
   * `imageio`.
3) Clone the [latest release of this repository](https://github.com/carolinafaccin/gol.git) (download the asset zip folder);
4) Extract the files to a folder of preference (ex: `C:\Users\Home\Documents\gol`);
> **Warning**: do not change internal folder and file names.
6) Execute the scripts in the notebook file `notebook/gol.ipynb`, choose the pattern desired and choose parameters.
7) Each script will print the status bar of the simulation in the terminal. You can choose to generate a live animation or a new versioned .gif file will be saved in the `figures/gif/tests/` directory.

## Example outputs

Example output from the pattern `growing heart`:

<img src="https://raw.githubusercontent.com/carolinafaccin/gol/main/figures/gif/growingheart_intro1.gif?raw=true" alt="Animated GIF of a growing heart pattern" width="350">


## Repository structure
```
gol/
├── src/            # Source code for the Game of Life
├── figures/        # Figures and animations generated
├── source/         # Sphinx source files for the documentation (.rst)
├── docs/           # Final HTML output for GitHub Pages
├── examples/       # Scripts for different patterns
├── notebooks/      # Notebook with different patterns to run
└── README.md       # This file
```
