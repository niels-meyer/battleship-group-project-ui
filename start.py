from src.ui.menu import main_menu
from database.db import create_db_and_tables
from src.utils.helper import clear_screen

def main():
    try:
        create_db_and_tables()
        main_menu()
    except KeyboardInterrupt:
        clear_screen()
    
if __name__ == "__main__":
    main()