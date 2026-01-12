"""Main entry point for Word to PDF Converter application"""
import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from gui import main

if __name__ == "__main__":
    main()
