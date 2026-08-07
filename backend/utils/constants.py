from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# Data files
CURRICULUM_FILE = DATA_DIR / "curriculum.json"
CANDIDATES_FILE = DATA_DIR / "candidates.json"
