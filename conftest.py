"""Root pytest configuration for battleship project."""

from pathlib import Path
import sys

# Add src directory to Python path so modules are discoverable
SRC_DIR = Path(__file__).parent / "src"
sys.path.insert(0, str(SRC_DIR))
