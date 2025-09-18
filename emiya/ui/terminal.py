from PyQt6 import QtWidgets, QtGui, QtCore
from colorama import Fore, Style
import sys, time

class TerminalWindow(QtWidgets.QPlainTextEdit):
    typed = QtCore.pyqtSignal()

    def __init__(self, beep=False, always_on_top=True):
        super().__init__()
        self.setReadOnly(True)
        self.setStyleSheet("""
            QPlainTextEdit {background-color:#000;color:#e6e6e6;font-family:Consolas,Menlo,monospace;font-size:14px;}
        """)
        self.setWindowTitle("Emiya")
        if always_on_top:
            self.setWindowFlag(QtCore.Qt.WindowType.WindowStaysOnTopHint, True)
        self.beep = beep
        self.cursor = "_"
        self.cursor_timer = QtCore.QTimer()
        self.cursor_timer.timeout.connect(self._blink)
        self.cursor_on = True
        self.cursor_timer.start(500)

    def _blink(self):
        self.cursor_on = not self.cursor_on
        self._refresh_cursor()

    def _refresh_cursor(self):
        doc = self.document()
        cursor = self.textCursor()
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.End)
        self.setTextCursor(cursor)

    def type_line(self, text: str, cps: int = 22):
        for ch in text:
            self.insertPlainText(ch)
            if self.beep:
                sys.stdout.write('\a'); sys.stdout.flush()
            QtWidgets.QApplication.processEvents()
            time.sleep(1.0/max(1,cps))
        self.insertPlainText("\n")
        self._refresh_cursor()