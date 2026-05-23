import pytest
from nicegui import ui


"""
UI TEST CASE TEMPLATE

Test Case ID:
Feature:
Title:
Preconditions:
Steps:
Expected Result:
Actual Result:
Status:
Notes:
"""


def test_ui_imports():
    """
    Test Case ID: UI-001
    Feature: Application
    Title: Verify UI files import correctly
    """

    import start

    assert start is not None


def test_create_button():
    """
    Test Case ID: UI-002
    Feature: UI Components
    Title: Create NiceGUI button
    """

    button = ui.button("Continue")

    assert button is not None
    assert button.text == "Continue"


def test_create_label():
    """
    Test Case ID: UI-003
    Feature: UI Components
    Title: Create page label
    """

    label = ui.label("Battleship")

    assert label.text == "Battleship"


def test_select_component():
    """
    Test Case ID: UI-004
    Feature: Player Selector
    Title: Create select component
    """

    select = ui.select(
        options=["Alex", "John"],
        label="Player name",
    )

    assert select.label == "Player name"


def test_input_component():
    """
    Test Case ID: UI-005
    Feature: Input
    Title: Create input field
    """

    input_field = ui.input(label="Player")

    assert input_field.label == "Player"