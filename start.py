from src.ui.menu import main_menu
from src.utils.helper import clear_screen

def main():
    try:
        main_menu()
    except KeyboardInterrupt:
        clear_screen()
    
if __name__ == "__main__":
    main()