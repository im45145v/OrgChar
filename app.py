"""
Main entry point for OrgChar Streamlit application.
"""

import sys
import os
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from orgchar.streamlit_app import main

if __name__ == "__main__":
    main()