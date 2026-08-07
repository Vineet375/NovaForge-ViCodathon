import json
from pathlib import Path
from typing import Any, Dict

from backend.utils.logger import logger

def load_json_file(file_path: Path) -> Dict[str, Any]:
    """Load and parse a JSON file securely."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            logger.info(f"Successfully loaded JSON from {file_path.name}")
            return data
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in file {file_path}: {e}")
        raise
