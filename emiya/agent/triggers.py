from __future__ import annotations
import psutil
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from emiya.agent.memory import DB
from emiya.cognition.pad import MoodState

class PauseState:
    paused: bool = False

class Triggers:
    def __init__(self, db: DB, vscode_minutes=15, idle_minutes=30):
        self.db = db
        self.vscode_minutes = vscode_minutes
        self.idle_minutes = idle_minutes
        self.last_activity = datetime.utcnow() 
        self.sched = BackgroundScheduler()

    def start(self):
        self.sched.add_job(self.check_vscode, "interval", minutes=5, id="vscode")
        self.sched.add_job(self.check_idle, "interval", minutes=5, id="idle")
        self.sched.start()

    def touch_activity(self):
        self.last_activity = datetime.utcnow()

    def check_vscode(self):
        if PauseState.paused:
            return
        procs = [p.info for p in psutil.process_iter(["name", "create_time"]) if p.info["name"] and "code" in p.info["name"].lower()]
        if not procs:
            return
        oldest = min(p["create_time"] for p in procs)
        alive_min = (datetime.utcnow() - datetime.utcfromtimestamp(oldest)).total_seconds() / 60
        if alive_min >= self.vscode_minutes:
            self.db.log_event("trigger.vscode_long", f"{alive_min:.1f} min")
            MoodState.nudge(dp=0.05, da=-0.05, dd=0.05)

    def check_idle(self):
        if PauseState.paused:
            return
        idle_min = (datetime.utcnow() - self.last_activity).total_seconds() / 60
        if idle_min >= self.idle_minutes:
            self.db.log_event("trigger.idle", f"{idle_min:.1f} min")
            MoodState.nudge(dp=-0.1, da=-0.05, dd=0.05)