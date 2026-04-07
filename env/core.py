from typing import Tuple, Dict, Any
from .models import CodeDoctorObservation, CodeDoctorAction, CodeDoctorState

class CodeDoctorEnv:
    def __init__(self):
        self.tasks = [
            {
                "task_id": "task_1_easy",
                "difficulty": "EASY",
                "description": "Fix the syntax error so that the function prints hello.",
                "code": "print(\"Hello\"",
                "expected_code_snippets": ["print(\"Hello\")", "print('Hello')"],
                "expected_explanation_keywords": ["syntax", "parenthesis", "missing", "close", "bracket"]
            },
            {
                "task_id": "task_2_medium",
                "difficulty": "MEDIUM",
                "description": "Fix the logic bug so that the add function correctly adds two numbers.",
                "code": "def add(a,b):\n    return a-b",
                "expected_code_snippets": ["return a+b", "return a + b", "return b+a"],
                "expected_explanation_keywords": ["minus", "subtract", "plus", "add", "instead", "logic"]
            },
            {
                "task_id": "task_3_hard",
                "difficulty": "HARD",
                "description": "Optimize the inefficient code. The loop uses index iteration but a direct element iteration is more Pythonic.",
                "code": "def print_elements(lst):\n    for i in range(len(lst)):\n        print(lst[i])",
                "expected_code_snippets": ["for element in lst:", "for item in lst:", "for x in lst:", "for i in lst:"],
                "expected_explanation_keywords": ["range", "len", "direct", "pythonic", "iterate", "elements", "index"]
            }
        ]
        self.current_idx = 0
        self.reset_count = 0
        
    def reset(self) -> CodeDoctorObservation:
        if self.reset_count > 0:
            self.current_idx += 1
        self.reset_count += 1
        return self._get_observation()
        
    def _get_observation(self) -> CodeDoctorObservation:
        if self.current_idx >= len(self.tasks):
            return CodeDoctorObservation(
                task_id="done", code="", description="All tasks complete.", difficulty="NONE"
            )
        task = self.tasks[self.current_idx]
        return CodeDoctorObservation(
            task_id=task["task_id"],
            code=task["code"],
            description=task["description"],
            difficulty=task["difficulty"]
        )

    def state(self) -> CodeDoctorState:
        return CodeDoctorState(
            current_task_idx=self.current_idx,
            total_tasks=len(self.tasks),
            done=self.current_idx >= len(self.tasks),
            current_observation=self._get_observation() if self.current_idx < len(self.tasks) else None
        )

    def step(self, action: CodeDoctorAction) -> Tuple[CodeDoctorObservation, float, bool, Dict[str, Any]]:
        if self.current_idx >= len(self.tasks):
            return self._get_observation(), 0.0, True, {"error": "Environment is already done."}
            
        task = self.tasks[self.current_idx]

        
        # Grading code fix
        code_correct = False
        action_code = action.code_fix.replace(" ", "")  # simple normalization just in case
        for snippet in task["expected_code_snippets"]:
            if snippet.replace(" ", "") in action_code:
                code_correct = True
                break
                
        # Grading explanation
        exp_score = 0.0
        explanation_lower = action.explanation.lower()
        matched_keywords = sum(1 for kw in task["expected_explanation_keywords"] if kw in explanation_lower)
        if matched_keywords > 0:
            exp_score = min(0.3, matched_keywords * 0.15) 
            
        # Overall score deterministic logic
        reward = 0.0
        if code_correct:
            reward += 0.6
        elif action.code_fix != task["code"] and action.code_fix.strip() != "":
            # Partial fix: they changed it but it's not correct
            reward += 0.2
            
        reward += exp_score
        
        # Cap reward
        reward = min(1.0, reward)
        
        # RL episodic completion logic
        done = reward >= 0.9
        
        info = {
            "task_id": task["task_id"],
            "code_correct": code_correct,
            "explanation_score": exp_score
        }
        
        return self._get_observation(), reward, done, info
