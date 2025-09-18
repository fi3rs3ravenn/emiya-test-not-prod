from apscheduler.schedulers.background import BackgroundScheduler
from emiya.skills.rituals import morning_ping, evening_reflection

class RitualScheduler:
    def __init__(self):
        self.s = BackgroundScheduler()

    def start(self, morning="09:00", evening="21:30"):
        h, m = map(int, morning.split(":"))
        self.s.add_job(morning_ping, "cron", hour=h, minute=m, id="morning")
        h, m = map(int, evening.split(":"))
        self.s.add_job(evening_reflection, "cron", hour=h, minute=m, id="evening")
        self.s.start()