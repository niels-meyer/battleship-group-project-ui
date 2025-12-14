from menu import main_menu
from utils import clear_screen

def main():
    try:
        main_menu()
    except KeyboardInterrupt:
        clear_screen()
    
if __name__ == "__main__":
    main()