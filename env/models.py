from pydantic import BaseModel
from typing import Optional, List

class CodeDoctorObservation(BaseModel):
    task_id: str
    code: str
    description: str
    difficulty: str

class CodeDoctorAction(BaseModel):
    code_fix: str
    explanation: str

class CodeDoctorReward(BaseModel):
    score: float
    is_correct: bool
    explanation_quality: float

class CodeDoctorState(BaseModel):
    current_task_idx: int
    total_tasks: int
    done: bool
    current_observation: Optional[CodeDoctorObservation] = None
