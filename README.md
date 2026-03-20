# Battleship Game

A console-based Battleship game written in Python.

## Requirements

- Python 3.10+ (for type hints and `match` statements).
- Dependencies listed in `requirements.txt`.

## Environment setup

Prepare the project with a virtual environment and install dependencies:

1. Create the virtual environment:

   ```bash
   python3 -m venv .venv
   ```

   This creates an isolated Python environment in the `.venv` folder.

2. Activate the virtual environment:

   ```bash
   source .venv/bin/activate
   ```

   This switches your current terminal to use the `.venv` Python and pip.

3. Install packages from requirements.txt:
   ```bash
   pip install -r requirements.txt
   ```
   This installs all required dependencies into the active virtual environment.

## Updating local dependencies

If a package has been added/updated and updated `requirements.txt`, you only need to sync your local environment:

1. Activate the virtual environment:

   ```bash
   source .venv/bin/activate
   ```

2. Install/update dependencies from `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
   This installs any missing packages and updates versions to match the project file.

## Adding a new package (contributors)

Only use this when you are the one introducing a new dependency:

1. Activate the virtual environment:

   ```bash
   source .venv/bin/activate
   ```

2. Install the package:

   ```bash
   pip install <package-name>
   ```

3. Save the updated environment to `requirements.txt`:
   ```bash
   pip freeze > requirements.txt
   ```

## Deactivating the environment

When you stop working on the project, you can deactivate the environment with:

```bash
deactivate
```

This returns your terminal to the system Python environment.

(You do not have to deactivate if you are just closing that terminal window, but deactivating is recommended when you want to continue using the same terminal for other projects.)

## How to run

From the project root:

```bash
python start.py
```

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

## Features

- Classic fleet containing one Carrier, a Battleship, a Cruiser, a Submarine and a Destroyer; ship sizes are defined in `config.json`.
- 10×10 configurable board with customizable row/column labels and cell symbols via `config.json`.
- Human vs AI gameplay with random AI ship placement and shooting.
- Player stats (wins, losses, score, username) saved and loaded from JSON files.

## Configuration

Game board and symbols are controlled by `config.json`:

- `rows` and `columns` define board dimensions and labels.
- `ships` define ship names and lengths.
- `cell_symbols` define how cells are rendered (empty, ship, hit, miss).

You can tweak these to change board size, fleet composition, or symbols, as long as the code assumptions (e.g., rectangular board) are preserved.

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
