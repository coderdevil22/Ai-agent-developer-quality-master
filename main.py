from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, List
from environment import DevEnv

app = FastAPI()
env = DevEnv()

# Observation model
class Observation(BaseModel):
    bugs: int
    code_quality: int
    features: int
    deadline: int
    logs: List[str]

# Action model
class Action(BaseModel):
    action: str

# Step response
class StepResponse(BaseModel):
    observation: Observation
    reward: float
    done: bool
    info: Dict = {}

# ✅ POST RESET (IMPORTANT FIX)
@app.post("/reset", response_model=Observation)
def reset():
    return env.reset()

# ✅ STEP
@app.post("/step", response_model=StepResponse)
def step(req: Action):
    state, reward, done = env.step(req.action)

    return {
        "observation": state,
        "reward": reward,
        "done": done,
        "info": {}
    }

# STATE (optional)
@app.get("/state", response_model=Observation)
def state():
    return env.state()

# HOME
@app.get("/")
def home():
    return {"message": "Dev Debug Environment Running"}
