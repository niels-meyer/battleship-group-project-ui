import json
from pathlib import Path

from utils.app_types import TConfig, TConfigShips, TConfigRows, TConfigColumns, TConfigCellSymbols

_config_path = Path(__file__).with_name("config.json")

with _config_path.open("r", encoding="utf-8") as file:
    _config: TConfig = json.load(file)
    _ships: TConfigShips = _config.get("ships", {})
    _rows: TConfigRows = _config.get("rows", [])
    _columns: TConfigColumns = _config.get("columns", [])
    _cell_symbols = _config.get("cell_symbols", {})

def get_ships() -> TConfigShips:
    return _ships

def get_rows() -> TConfigRows:
    return _rows

def get_columns() -> TConfigColumns:
    return _columns

def get_cell_symbols() -> TConfigCellSymbols:
    return _cell_symbols
