from typing import List, Optional

from backend.services.data_loaders import DataLoader
from backend.models.curriculum import Curriculum, Day, Module
from backend.models.candidate import Candidate
from backend.utils.logger import logger

class CurriculumRepository:
    def __init__(self):
        self.curriculum = DataLoader.load_curriculum()
        
    def get_curriculum(self) -> Curriculum:
        return self.curriculum
        
    def get_day(self, day_number: int) -> Optional[Day]:
        for day in self.curriculum.days:
            if day.day == day_number:
                return day
        logger.warning(f"Day {day_number} not found in curriculum.")
        return None
        
    def get_module(self, module_name: str) -> Optional[Module]:
        for module in self.curriculum.modules:
            if module.title.lower() == module_name.lower():
                return module
        logger.warning(f"Module '{module_name}' not found in curriculum.")
        return None

class CandidateRepository:
    def __init__(self):
        self.candidates_data = DataLoader.load_candidates()
        
    def get_all_candidates(self) -> List[Candidate]:
        return self.candidates_data.candidates
        
    def get_candidate_by_id(self, candidate_id: str) -> Optional[Candidate]:
        for candidate in self.candidates_data.candidates:
            if candidate.member.id == candidate_id:
                return candidate
        logger.warning(f"Candidate {candidate_id} not found.")
        return None
