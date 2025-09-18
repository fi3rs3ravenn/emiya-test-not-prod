from fastapi import FastAPI
from pydantic import BaseModel
from emiya.agent.memory import DB
from emiya.agent.triggers import PauseState
from emiya.cognition.pad import MoodState

app = FastAPI(title="Emiya API")

db = DB()
pauser = PauseState()

class SayIn(BaseModel):
    text: str

@app.get("/state")
def get_state():
    return {
        "paused": pauser.paused,
        "mood": MoodState.current().model_dump(),
    }

@app.post("/say")
def say(data: SayIn):
    db.log_event("user_say", data.text)
    return {"ok": True}

@app.post("/pause")
def pause(toggle: bool):
    pauser.paused = bool(toggle)
    db.log_event("pause_toggle", str(pauser.paused))
    return {"paused": pauser.paused}

@app.get("/logs")
def logs(limit: int = 50):
    return db.recent_logs(limit)