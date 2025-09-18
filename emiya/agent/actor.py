from agent.memory import DB
from cognition.pad import MoodState
from colorama import Fore, Style

class Actor:
    def __init__(self):
        self.db = DB()

    def speak(self, text: str):
        self.db.log_event("say", text)
        return f"{Fore.MAGENTA}{text}{Style.RESET_ALL}"

    def style_for_mood(self):
        m = MoodState.current()
        speed = 10 + int(20 * m.arousal)
        return {"speed": speed}
    