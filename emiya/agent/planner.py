from emiya.cognition.chaos import Logistic

class Planner:
    def __init__(self):
        self.chaos = Logistic()

    def next_social_move(self) -> str:
        x = self.chaos.step()
        if x < 0.33: return "TXT"
        if x < 0.66: return "TXT"
        return "TXT"