from agent.memory import DB

db = DB()

def take(text: str):
    db.log_event("note", text)