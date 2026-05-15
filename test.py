"""Run tests matching *.test.py pattern."""
import subprocess
import sys

if __name__ == "__main__":
    result = subprocess.run([sys.executable, "-m", "pytest"])
    sys.exit(result.returncode)
