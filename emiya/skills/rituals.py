from emiya.agent.memory import DB
from emiya.cognition.pad import MoodState

db = DB()

def morning_ping():
    db.log_event("ritual.morning", "ping")
    MoodState.nudge(dp=0.1, da=0.05, dd=0.05)


def evening_reflection():
    db.log_event("ritual.evening", "reflect")
    MoodState.nudge(dp=0.05, da=-0.05, dd=0.05)