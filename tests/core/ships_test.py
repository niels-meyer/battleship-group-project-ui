from __future__ import annotations
from src.core.ships import Ships


def test_tc_016_has_ships_is_false_after_last_ship_removed() -> None:
    ships = Ships()
    ships.add_ship("Destroyer", [("a", "1"), ("a", "2")])

    ships.remove_ship("Destroyer")

    assert ships.has_ships() is False


def test_tc_017_decrease_ship_removes_ship_when_last_coord_hit() -> None:
    ships = Ships()
    ships.add_ship("Destroyer", [("a", "1"), ("a", "2")])

    ships.decrease_ship("Destroyer", ("a", "1"))
    ships.decrease_ship("Destroyer", ("a", "2"))

    assert "Destroyer" not in ships.get_ships()
    assert ships.has_ships() is False
