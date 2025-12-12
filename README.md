# Battleship Game
A console-based Battleship game written in Python.

# Battleship CLI Game

A console-based implementation of the Battleship game where you place ships on a 10×10 grid and battle against a simple AI opponent. The game also tracks basic player statistics such as wins, losses, and an ELO-like score.

## Features

- Interactive text UI using `InquirerPy` menus and prompts.
- Classic fleet contening one Carrier, a Battleship, a Cruiser, a Submarine and a Destroyer the size of the ships are defined in `config.json`.
- 10×10 configurable board with customizable row/column labels and cell symbols via `config.json`.
- Human vs AI gameplay with random AI ship placement and shooting.
- Player stats (wins, losses, score, username) saved and loaded from JSON files.

## Project structure

- `start.py` – Entry point that shows the main menu and starts the game.
- `menu.py` – Main menu and stats menu logic.
- `game.py` – Core game loop: ship placement, taking shots, turn switching, win detection.
- `board.py` – Board representation, ship placement on the grid, and handling shots.
- `player.py` – Player wrapper combining a `Board` and `Ships` collection.
- `ai.py` – AI player with random ship placement and shooting logic.
- `ships.py` – Manages ship coordinates and tracking when ships are sunk.
- `utils.py` – Coordinate parsing, validation, and helper functions for ship placement.
- `config.json` – Configuration for rows, columns, ship sizes, and display symbols.
- `stats.py` – Player statistics model with JSON-based persistence.
- `constants.py` – Text constants for menu messages and choices.
- `app_types.py` – Type aliases used across the project (not shown here but referenced).

## Requirements

- Python 3.10+ (for type hints and `match` statements).
- `InquirerPy` for interactive prompts in the terminal.

Install dependencies with pip install InquirerPy

## Configuration

Game board and symbols are controlled by `config.json`:

- `rows` and `columns` define board dimensions and labels.
- `ships` define ship names and lengths.
- `cell_symbols` define how cells are rendered (empty, ship, hit, miss).

You can tweak these to change board size, fleet composition, or symbols, as long as the code assumptions (e.g., rectangular board) are preserved.

## How to run

From the project root start.py

You will see a main menu with options:

- **Start** – Begin a new game of Battleship.
- **Stats** – View, save, or load player stats.
- **Rules** – Placeholder for rules text (to be implemented).
- **Exit** – Quit the application.

## Gameplay

1. **Ship placement**  
   - After starting a game, you place each ship manually.  
   - Enter a start coordinate like `a 1` when prompted.  
   - The game will suggest valid end coordinates based on ship length and board rules.  
   - Choose an end coordinate from the list to place the ship.  
   - The AI places the same ship type automatically on its own board.

2. **Taking turns**  
   - The first turn (player or AI) is chosen at random.  
   - On your turn, enter a coordinate (e.g. `c 5`) to shoot.  
   - The game prevents you from shooting the same cell twice.  
   - The AI takes random valid shots on your board.

3. **Winning and losing**  
   - Each ship tracks its remaining coordinates.  
   - When all coordinates of all ships for a player are hit, that player loses.  
   - The game prints a win or loss message at the end of the match.

## Stats system

The `Stats` class tracks:

- Player name.
- Unique ID (UUID).
- Number of wins and losses.
- ELO-like score (starting at 500).

From the **Stats** menu, you can:

- View current stats.
- Save stats to a JSON file under `stats/<id>.json`.
- Load stats from an existing JSON file.

The ELO-like score is updated after each game using simple increments/decrements.

## Possible improvements

- Improve AI logic for smarter ship placement and shooting.
- Slow the time between the taking turn
- Avoid the repetition of the terminal for each output.




