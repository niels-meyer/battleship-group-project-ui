from src.database.db import create_db_and_tables
from src.ui.app import run_app


def main():
    try:
        create_db_and_tables()
        run_app()
    except KeyboardInterrupt:
        print("\nShutting down Battleship...")


if __name__ == "__main__":
    main()
