from agent.memory import DB

class Critic:
    def __init__(self):
        self.db = DB()

    def log(self, reason: str):
        self.db.log_event("critic", reason)