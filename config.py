from app_types import TConfig, TConfigShips, TConfigRows, TConfigColumns
import json

with open('config.json', 'r') as file:
    _config: TConfig = json.load(file)
    _ships: TConfigShips = _config.get("ships", {})
    _rows: TConfigRows = _config.get("rows", [])
    _columns: TConfigColumns = _config.get("columns", [])

def get_ships() -> TConfigShips:
    return _ships

def get_rows() -> TConfigRows:
    return _rows

def get_columns() -> TConfigColumns:
    return _columns

