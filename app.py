"""
Main entry point for OrgChar Streamlit application.
"""

import sys
import subprocess
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def _is_running_under_streamlit() -> bool:
    """Return True when script is already running inside Streamlit runtime."""
    return any(module.startswith("streamlit.runtime") for module in sys.modules)


def _run_streamlit_app() -> None:
    """Import and execute the Streamlit app after runtime is confirmed."""
    from orgchar.streamlit_app import main

    main()


if __name__ == "__main__":
    if _is_running_under_streamlit():
        _run_streamlit_app()
    else:
        # Running via `python app.py`; re-launch under Streamlit for correct runtime context.
        app_file = Path(__file__).resolve()
        cmd = [sys.executable, "-m", "streamlit", "run", str(app_file)]
        raise SystemExit(subprocess.call(cmd))