import random
from typing import List, Set
from backend.models.candidate import Candidate
from backend.models.curriculum import Curriculum
from backend.models.interview import QuestionDifficulty

class DifficultyStrategy:
    """Strategy to calculate the starting interview difficulty for a candidate."""
    
    @staticmethod
    def calculate_difficulty(candidate: Candidate) -> QuestionDifficulty:
        """
        Calculate difficulty based on candidate's learning signals and experience.
        """
        signals = candidate.signals
        
        # Calculate success rate safely
        success_rate = 0.0
        if signals.missionsCompleted > 0:
            success_rate = signals.missionsFirstTry / signals.missionsCompleted
            
        score = 0
        
        # Experience component
        if candidate.member.yearsExperience > 3:
            score += 2
        elif candidate.member.yearsExperience > 1:
            score += 1
            
        # Quality component
        if success_rate >= 0.8:
            score += 2
        elif success_rate >= 0.5:
            score += 1
            
        # Consistency component
        if signals.commitDays > 30:
            score += 1
            
        if score >= 4:
            return QuestionDifficulty.HARD
        elif score >= 2:
            return QuestionDifficulty.MEDIUM
        return QuestionDifficulty.EASY


class TopicSelectionStrategy:
    """Strategy to select curriculum days/topics for an interview."""
    
    @staticmethod
    def select_topics(candidate: Candidate, curriculum: Curriculum, num_days: int = 4) -> List[int]:
        """
        Selects curriculum days to cover in the interview.
        Prioritizes completed days, avoids skipped days.
        Ensures at least `num_days` are selected and no duplicates.
        """
        completed_days: Set[int] = set()
        skipped_days: Set[int] = set()
        
        for mission in candidate.missions:
            if mission.passed:
                completed_days.add(mission.day)
            elif mission.skipped:
                skipped_days.add(mission.day)
                
        # All available days in curriculum
        all_days = [day.day for day in curriculum.days]
        
        selected: Set[int] = set()
        
        # 1. Prioritize completed days
        available_completed = list(completed_days.intersection(all_days))
        random.shuffle(available_completed)
        for day in available_completed:
            if len(selected) < num_days:
                selected.add(day)
                
        # 2. Add days that are neither completed nor skipped (unattempted)
        if len(selected) < num_days:
            unattempted = [d for d in all_days if d not in completed_days and d not in skipped_days]
            random.shuffle(unattempted)
            for day in unattempted:
                if len(selected) < num_days:
                    selected.add(day)
                    
        # 3. Finally, add skipped days (testing knowledge gaps intentionally)
        if len(selected) < num_days:
            available_skipped = list(skipped_days.intersection(all_days))
            random.shuffle(available_skipped)
            for day in available_skipped:
                if len(selected) < num_days:
                    selected.add(day)
                    
        return list(selected)
