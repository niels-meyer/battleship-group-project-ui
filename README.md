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

---

This project is a console-based Battleship game written in Python.

It aims to:

- provide a playable Battleship game against AI
- demonstrate clean separation between UI, game logic, and helper utilities
- support multiple AI difficulty levels
- keep the code testable and maintainable

---

## 📝 Application Requirements

### Problem

Battleship is a turn-based strategy game where players must place ships, guess enemy ship positions, and avoid repeating shots.

---

### Scenario

The application allows users to:

- place ships on a board
- shoot at enemy coordinates
- play against AI opponents with different difficulty levels
- track wins/losses via the stats system

---

## 📖 User Stories

### 1. Start a Game

**As a user, I want to start a new Battleship match from the main menu.**

- **Inputs:** menu selection
- **Outputs:** active game session

---

### 2. Place Ships

**As a user, I want to place my ships on the board.**

- **Inputs:** start coordinate, end coordinate
- **Outputs:** placed ships on the player board

---

### 3. Shoot at Enemy Board

**As a user, I want to enter a coordinate to shoot at the enemy board.**

- **Inputs:** coordinate (`row`, `column`)
- **Outputs:** hit or miss result, updated board state

---

### 4. Play Against AI

**As a user, I want to play against an AI opponent with different difficulty levels.**

- **Inputs:** selected difficulty
- **Outputs:** AI moves based on the selected strategy

---

### 5. View and Save Stats

**As a user, I want to view and save my statistics.**

- **Inputs:** username, stats menu selection
- **Outputs:** stored stats, saved/loaded profile

---

## 🧩 Use Cases

![UML Use Case Diagram](docs/architecture-diagrams/uml_use_case_diagram.png)

### Main Use Cases

- Start Game
- Place Ships
- Shoot at Enemy Board
- Use AI Opponent
- View Stats

### Actors

- Player
- AI Opponent
- Stats User

---

### Wireframes / Mockups

> 🚧 Add screenshots of the wireframes or gameplay screens you chose to implement.

![Wireframes – Home/Gameplay](docs/ui-images/wireframes.png)

---

## 🏛️ Architecture

![UML Class Diagram](docs/architecture-diagrams/uml_class_architecture.png)

### Layers

- **UI:** terminal-based menus and prompts
- **Application logic:** game loop, turn handling, stats flow
- **Domain/Core:** board, player, ships, and statistics
- **Helpers:** coordinate parsing, placement validation, display utilities

### Design Decisions

- Separate core game logic from UI prompts
- Keep AI behavior behind a dedicated AI class
- Use helper functions for coordinate and board utilities

### Patterns Used

- Game loop orchestration
- Strategy-like AI difficulty handling
- Utility/helper pattern for shared logic

---

## 🗄️ Database and ORM

![ER Diagram](docs/architecture-diagrams/er_diagram.png)

This project currently does not use a database or ORM.

### Entities

> 🚧 Not applicable in the current version.

### Relationships

> 🚧 Not applicable in the current version.

---

## ✅ Project Requirements

---

> 🚧 Requirements act as a contract: implement and demonstrate each point below.

Each app must meet the following criteria in order to be accepted (see also the official project guidelines PDF on Moodle):

1. Interactive application flow
2. Data validation in the app
3. Clear separation of game logic and state handling

---

### 1. Interactive App

The application interacts with the user via the terminal. Users can:

- navigate the main menu
- create or load stats
- place ships
- shoot at coordinates
- observe board updates after each turn

---

### 2. Data Validation

The application validates user input to ensure correct coordinates and legal ship placement.

- coordinate format is checked before use
- ship placement is checked against board boundaries and overlap
- repeated shots are prevented

---

### 3. Game State Management

Game state is managed in the core classes:

- `Board` stores ship and shot state
- `Player` combines board and ships
- `AI` controls enemy shot selection and ship placement
- `Stats` stores profile and game results

---

## ⚙️ Implementation

### Technology

- Python
- InquirerPy
- pytest
- JSON-based persistence for stats

### Libraries Used

- **InquirerPy** – menu prompts
- **pytest** – testing
- **json** – stats persistence
- **random** – AI shot selection and turn order

---

## 📂 Repository Structure

```text
start.py
test.py

src/
├── app_types.py
├── ai/
│   ├── ai.py
│   ├── algorithmic_ai.py
│   └── llm_ai.py
├── config/
│   ├── config.py
│   └── config.json
├── core/
│   ├── board.py
│   ├── game.py
│   ├── player.py
│   └── ships.py
├── ui/
│   ├── app.py
│   ├── constants.py
│   ├── styles.py
│   └── pages/
│       ├── player_selector_page.py
│       ├── main_menu_page.py
│       ├── stats_page.py
│       ├── help_page.py
│       ├── game_page.py
│       └── helpers/
│           ├── access_control.py
│           ├── navigation.py
│           ├── player_selection.py
│           └── storage_session.py
└── utils/
    └── helpers.py

tests/
└── ai/
    └── algorithmic_ai.test.py

database/
├── db.py
├── player.py
└── match.py
```

---

### How to Run

#### 1. Project Setup

- Python 3.10+ is required
- Create and activate a virtual environment:

  **Windows:**

  ```bash
  python -m venv .venv
  .venv\Scripts\Activate.ps1
  ```

- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

#### 2. Configuration

> 🚧 Add configuration details here if needed.

#### 3. Launch

From the project root:

```bash
python start.py
```

#### 4. Usage

1. Start the application from the main menu.
2. Create or load a stats profile if needed.
3. Place all ships on the board.
4. Shoot at enemy coordinates on your turn.
5. Continue until one side loses all ships.

---

## 🧪 Testing

> 🚧 Explain what you test and how to run tests.

**Test mix:**

- Unit tests for board and ship handling
- AI strategy tests for shot selection
- Integration tests for game flow

Current automated AI test cases are in [tests/ai/algorithmic_ai.test.py](tests/ai/algorithmic_ai.test.py):

| Test case ID | Title                                                         |
| ------------ | ------------------------------------------------------------- |
| TC_001       | Impossible AI selects an unshot ship cell when one exists     |
| TC_002       | Hard AI extends a horizontal hit group                        |
| TC_003       | Normal AI never returns an already-shot coordinate            |
| TC_004       | Reset clears tracked shots and strategy                       |
| TC_005       | Unsunk hit detection returns only valid shot ship coordinates |

Run tests with:

```bash
python test.py
```

### Template for writing test cases

1. Test case ID – unique identifier
2. Test case title/description – what the test covers
3. Preconditions – required setup
4. Test steps – actions performed
5. Test data/input
6. Expected result
7. Actual result
8. Status – pass or fail
9. Comments – additional notes

---

## 👥 Team & Contributions

> 🚧 Fill in the names of all team members and describe their individual contributions below.

| Name      | Contribution                       |
| --------- | ---------------------------------- |
| Student A | UI and menu flow                   |
| Student B | Core game logic and board handling |
| Student C | AI logic and stats                 |

---

## 🤝 Contributing

> 🚧 This is a template repository for student projects.  
> 🚧 Do not change this section in your final submission.

- Use this repository as a starting point by importing it into your own GitHub account
- Work only within your own copy — do not push to the original template
- Commit regularly to track your progress

---

## 📝 License

This project is provided for educational use only as part of the Advanced Programming module.

[MIT License](LICENSE)
