from InquirerPy import inquirer
from pathlib import Path
from src.config import config
from src.utils.constants import MAIN_MENU_CHOICES, CONFIG_MENU_CHOICES, MENU_MESSAGE, CONFIG_MESSAGE, END_MESSAGE
from src.core.game import Game
from src.utils.helper import clear_screen
from nicegui import app, ui

BASE_DIR = Path(__file__).resolve().parents[2]
ASSETS_DIR = BASE_DIR / 'assets'
MENU_BACKGROUND_IMAGE = '/assets/menu-background.png'
MENU_CARD_STYLE = 'background: rgba(0, 0, 0, 0.58); border-radius: 10px; color: #ffffff;'
MENU_BUTTON_PROPS = 'color=green-10 text-color=white'

# Keep shared state
#_stats = Stats()
#_main_container = None


def _clear_container():
    global _main_container
    if _main_container is not None:
        _main_container.clear()


def _show_header(title: str, subtitle: str | None = None) -> None:
    ui.label(title).classes('text-5xl font-bold text-gray-200 mb-2')
    if subtitle:
        ui.label(subtitle).classes('text-base text-gray-300 mb-4')


def _stats_text() -> str:
    return (
        f"Name: {_stats.name}\n"
        f"Wins: {_stats.winNumber}\n"
        f"Losses: {_stats.loseNumber}\n"
        f"ELO Score: {_stats.eloScore}"
    )


def _menu_button(label: str, on_click, extra_classes: str = '') -> None:
    classes = f'w-full {extra_classes}'.strip()
    ui.button(label, on_click=on_click).classes(classes).props(MENU_BUTTON_PROPS)


def _render_main_menu() -> None:
    _clear_container()

    with _main_container:
        with ui.column().classes('w-full min-h-screen items-center justify-center px-4').style(
            f'background-image: linear-gradient(rgba(10, 25, 10, 0.35), rgba(10, 25, 10, 0.35)), url("{MENU_BACKGROUND_IMAGE}"); '
            'background-size: cover; background-position: center; background-repeat: no-repeat;'
        ):
            _show_header('Battleship', 'Welcome to the Battleship game against AI!')

            with ui.card().classes('w-full max-w-md p-12').style(MENU_CARD_STYLE):
                ui.label('CHOOSE AN OPTION').classes('text-lg text-green-800 mb-2 font-bold')
                _menu_button('Start Game', game_menu, 'mb-2')
                _menu_button('Stats', stats_menu, 'mb-2')
   #            _menu_button('Config', config_menu, 'mb-2')
                _menu_button('Exit', exit_menu)


def main_menu():
    if ASSETS_DIR.exists():
        app.add_static_files('/assets', str(ASSETS_DIR))

    @ui.page('/')
    def index_page():
        global _main_container
        with ui.column().classes('w-full') as container:
            _main_container = container
            _render_main_menu()

    ui.run(title='Battleship NiceGUI')


def exit_menu():
    _clear_container()

    with _main_container:
        with ui.column().classes('w-full items-center mt-10'):
            _show_header('Goodbye')
            with ui.card().classes('w-full max-w-md p-6'):
                ui.markdown(f'```text\n{END_MESSAGE}\n```')
                ui.label('Close the browser tab to exit the app.').classes('mt-2')
                ui.button('Back to Main Menu', on_click=_render_main_menu).classes('w-full mt-4').props(MENU_BUTTON_PROPS)


def game_menu():
    _clear_container()

    with _main_container:
        with ui.column().classes('w-full items-center mt-10'):
            _show_header('Game')

            with ui.card().classes('w-full max-w-xl p-12'):
                ui.label('Start Your Game now').classes('text-lg mb-2')

                def start_cli_game():
                    try:
                        Game().start()
                    except Exception as e:
                        ui.notify(f'Error while starting the game: {e}', type='negative')

                ui.button('Start your Game', on_click=start_cli_game).classes('w-full mb-2').props(MENU_BUTTON_PROPS)
                ui.button('Back to Main Menu', on_click=_render_main_menu).classes('w-full').props(MENU_BUTTON_PROPS)


def stats_menu():
    _clear_container()

    with _main_container:
        with ui.column().classes('w-full items-center mt-10'):
            _show_header('Stats')

            with ui.card().classes('w-full max-w-xl p-12'):
                if _stats.name is None:
                    ui.label('No stats profile loaded').classes('text-lg mb-4')

                    username_input = ui.input('Username').classes('w-full mb-2')
                    filename_input = ui.input('Filename to load').classes('w-full mb-2')

                    def create_profile():
                        try:
                            if not username_input.value:
                                ui.notify('Please enter a username.', type='warning')
                                return
                            _stats.create_new(username_input.value)
                            _stats.save_to_file()
                            ui.notify('Profile created and saved.')
                            stats_menu()
                        except Exception as e:
                            ui.notify(f'Error: {e}', type='negative')

                    def load_profile():
                        try:
                            if not filename_input.value:
                                ui.notify('Please enter a filename.', type='warning')
                                return
                            _stats.load_from_file(filename_input.value)
                            ui.notify('Profile loaded.')
                            stats_menu()
                        except Exception as e:
                            ui.notify(f'Error: {e}', type='negative')

                    ui.button('Create New Profile', on_click=create_profile).classes('w-full mb-2').props(MENU_BUTTON_PROPS)
                    ui.button('Load Profile', on_click=load_profile).classes('w-full mb-2').props(MENU_BUTTON_PROPS)
                    ui.button('Back to Main Menu', on_click=_render_main_menu).classes('w-full').props(MENU_BUTTON_PROPS)
                    return

                ui.markdown(f'```text\n{_stats_text()}\n```').classes('w-full mb-4')

                filename_input = ui.input('Filename to load').classes('w-full mb-2')

                def view_stats():
                    stats_menu()

                def save_stats():
                    try:
                        _stats.save_to_file()
                        ui.notify('Stats saved successfully.')
                    except Exception as e:
                        ui.notify(f'Error: {e}', type='negative')

                def load_stats():
                    try:
                        if not filename_input.value:
                            ui.notify('Please enter a filename.', type='warning')
                            return
                        _stats.load_from_file(filename_input.value)
                        ui.notify('Stats loaded successfully.')
                        stats_menu()
                    except Exception as e:
                        ui.notify(f'Error: {e}', type='negative')

                ui.button('View Stats', on_click=view_stats).classes('w-full mb-2').props(MENU_BUTTON_PROPS)
                ui.button('Save Stats', on_click=save_stats).classes('w-full mb-2').props(MENU_BUTTON_PROPS)
                ui.button('Load Stats from File', on_click=load_stats).classes('w-full mb-2').props(MENU_BUTTON_PROPS)
                ui.button('Back to Main Menu', on_click=_render_main_menu).classes('w-full').props(MENU_BUTTON_PROPS)


def config_menu():
    _clear_container()

    with _main_container:
        with ui.column().classes('w-full items-center mt-10'):
            _show_header('Configuration')

            with ui.card().classes('w-full max-w-2xl p-12'):
                ui.markdown(f'```text\n{create_config()}\n```')
                ui.button('Back to Main Menu', on_click=_render_main_menu).classes('w-full mt-4').props(MENU_BUTTON_PROPS)


def create_config():
    config_lines = [
        "Welcome to Battleship against AI!",
        f"Board: {len(config.get_rows())}x{len(config.get_columns())}",
        f"Rows: {', '.join(config.get_rows())}",
        f"Columns: {', '.join(config.get_columns())}",
        "Ships:"
    ]

    for ship, info in config.get_ships().items():
        config_lines.append(f"- {ship}: {info['length']} cells")

    content_width = max(len(line) for line in config_lines)
    box_width = content_width + 2

    config_message = "       /\\_/\\\\  \n      ( o.o ) \n       > ^ <  \n"
    config_message += "  +" + "-" * box_width + "+\n"
    config_message += "  |" + "CONFIG".center(box_width) + "|\n"
    config_message += "  +" + "-" * box_width + "+\n"

    for line in config_lines:
        config_message += "  |" + line.ljust(box_width) + "|\n"

    config_message += "  +" + "-" * box_width + "+"
    return config_message