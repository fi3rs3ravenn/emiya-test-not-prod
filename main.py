import subprocess, sys, threading, time, yaml
from pathlib import Path
from emiya.ui.terminal import TerminalWindow
from PyQt6 import QtWidgets
from emiya.agent.memory import DB
from emiya.agent.triggers import Triggers, PauseState
from emiya.integrations.monitor import RitualScheduler
from emiya.agent.planner import Planner
from emiya.agent.actor import Actor

ROOT = Path(__file__).parent

with open(ROOT/"config"/"settings.yaml", "r", encoding="utf-8") as f:
    CFG = yaml.safe_load(f)


def run_api():
    return subprocess.Popen([sys.executable, "-m", "uvicorn", "api:app", "--host", "127.0.0.1", "--port", "8765"], cwd=str(ROOT))


def run_ui():
    app = QtWidgets.QApplication(sys.argv)
    win = TerminalWindow(beep=CFG["app"]["window"]["beep"], always_on_top=CFG["app"]["window"]["always_on_top"])
    win.resize(900, 400)
    win.show()

    db = DB(); db.log_event("boot", "emiya v0.1 start")

    trig = Triggers(db, CFG["triggers"]["vscode_minutes"], CFG["triggers"]["idle_minutes"])
    trig.start()

    rit = RitualScheduler(); rit.start(CFG["app"]["morning_ping"], CFG["app"]["evening_reflect"])

    planner = Planner(); actor = Actor()

    win.type_line("[Emiya]", cps=actor.style_for_mood()["speed"])  


    def loop():
        last_sent = 0
        while True:
            if PauseState.paused:
                time.sleep(1); continue
            if time.time() - last_sent > 60:
                msg = planner.next_social_move()
                win.type_line(msg, cps=actor.style_for_mood()["speed"])  
                last_sent = time.time()
            time.sleep(1)

    threading.Thread(target=loop, daemon=True).start()

    sys.exit(app.exec())

if __name__ == "__main__":
    api_proc = run_api()
    try:
        run_ui()
    finally:
        api_proc.terminate()