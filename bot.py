"""
Main entry point for OrgChar Discord bot.
"""

import sys
import os
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from orgchar.discord_bot import run_discord_bot
from orgchar.config import Config

if __name__ == "__main__":
    config = Config()
    config.ensure_directories()
    run_discord_bot(config)