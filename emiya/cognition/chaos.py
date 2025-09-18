class Logistic:
    def __init__(self, r: float = 3.9, x0: float = 0.123456):
        self.r = r
        self.x = x0

    def step(self) -> float:
        self.x = self.r * self.x * (1 - self.x)
        return self.x