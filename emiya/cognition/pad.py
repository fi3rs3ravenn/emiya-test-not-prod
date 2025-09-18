from __future__ import annotations
from pydantic import BaseModel
from dataclasses import dataclass, field

class Mood(BaseModel):
    pleasure: float
    arousal: float
    dominance: float

    def clamp(self):
        for f in ("pleasure","arousal","dominance"):
            v = getattr(self, f)
            setattr(self, f, max(0.0, min(1.0, v)))
        return self

@dataclass
class _State:
    mood: Mood = field(default_factory=lambda: Mood(pleasure=0.6, arousal=0.5, dominance=0.6))

_ST = _State()

class MoodState:
    @staticmethod
    def current() -> Mood:
        return _ST.mood

    @staticmethod
    def nudge(dp=0.0, da=0.0, dd=0.0):
        m = _ST.mood
        _ST.mood = Mood(
            pleasure=m.pleasure*0.9 + dp*0.1,
            arousal=m.arousal*0.9 + da*0.1,
            dominance=m.dominance*0.9 + dd*0.1,
        ).clamp()