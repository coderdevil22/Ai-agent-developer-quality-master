from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
from environment import DevEnv

app = FastAPI()
env = DevEnv()

# Observation model
class Observation(BaseModel):
    bugs: int
    code_quality: int
    features: int
    deadline: int
    logs: list

# Action model
class Action(BaseModel):
    action: str

# Response model
class StepResponse(BaseModel):
    observation: Observation
    reward: float
    done: bool
    info: Dict = {}

@app.get("/reset", response_model=Observation)
def reset():
    return env.reset()

@app.post("/step", response_model=StepResponse)
def step(req: Action):
    state, reward, done = env.step(req.action)

    return {
        "observation": state,
        "reward": reward,
        "done": done,
        "info": {
            "message": "Step executed successfully"
        }
    }

@app.get("/state", response_model=Observation)
def state():
    return env.state()

@app.get("/")
def home():
    return {"message": "Dev Debug Environment Running"}