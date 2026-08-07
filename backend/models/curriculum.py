from typing import List
from pydantic import BaseModel

class Day(BaseModel):
    day: int
    title: str
    type: str
    tools: List[str]
    objectives: List[str]

class Module(BaseModel):
    n: int
    title: str
    days: List[int]

class Curriculum(BaseModel):
    cohort: str
    modules: List[Module]
    days: List[Day]
