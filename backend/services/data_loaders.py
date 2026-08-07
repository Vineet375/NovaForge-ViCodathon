from typing import Optional
from pydantic import ValidationError

from backend.utils.constants import CURRICULUM_FILE, CANDIDATES_FILE
from backend.utils.file_utils import load_json_file
from backend.models.curriculum import Curriculum
from backend.models.candidate import CandidateList
from backend.utils.logger import logger

class DataLoader:
    _curriculum_cache: Optional[Curriculum] = None
    _candidates_cache: Optional[CandidateList] = None

    @classmethod
    def load_curriculum(cls) -> Curriculum:
        if cls._curriculum_cache:
            return cls._curriculum_cache
            
        try:
            raw_data = load_json_file(CURRICULUM_FILE)
            cls._curriculum_cache = Curriculum(**raw_data)
            logger.info("Curriculum successfully loaded and validated.")
            return cls._curriculum_cache
        except ValidationError as e:
            logger.error(f"Curriculum validation failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to load curriculum: {e}")
            raise

    @classmethod
    def load_candidates(cls) -> CandidateList:
        if cls._candidates_cache:
            return cls._candidates_cache
            
        try:
            raw_data = load_json_file(CANDIDATES_FILE)
            cls._candidates_cache = CandidateList(**raw_data)
            logger.info("Candidates successfully loaded and validated.")
            return cls._candidates_cache
        except ValidationError as e:
            logger.error(f"Candidates validation failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to load candidates: {e}")
            raise
