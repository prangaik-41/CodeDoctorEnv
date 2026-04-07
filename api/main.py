from typing import Dict, Any
from pydantic import BaseModel
from fastapi import FastAPI
from env.models import CodeDoctorAction, CodeDoctorObservation, CodeDoctorState
from env.core import CodeDoctorEnv

class StepResponse(BaseModel):
    observation: CodeDoctorObservation
    reward: float
    done: bool
    info: Dict[str, Any]

app = FastAPI(title="CodeDoctorEnv API", version="1.0.0")
env = CodeDoctorEnv()

@app.get("/reset", response_model=CodeDoctorObservation)
def reset_env():
    return env.reset()

@app.post("/step", response_model=StepResponse)
def step_env(action: CodeDoctorAction):
    obs, reward, done, info = env.step(action)
    return StepResponse(
        observation=obs,
        reward=reward,
        done=done,
        info=info
    )

@app.get("/state", response_model=CodeDoctorState)
def get_state():
    return env.state()
