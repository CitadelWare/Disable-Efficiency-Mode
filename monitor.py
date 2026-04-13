import threading
import psutil
from efficiency import disable_efficiency_mode


class Monitor:
    def __init__(self, interval: float = 5.0):
        self._interval = interval
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self.protected = 0
        self.failed = 0

    def start(self):
        self._thread.start()

    def stop(self):
        self._stop.set()

    def _loop(self):
        while not self._stop.is_set():
            ok = 0
            fail = 0
            for proc in psutil.process_iter(["pid"]):
                try:
                    if disable_efficiency_mode(proc.info["pid"]):
                        ok += 1
                    else:
                        fail += 1
                except (psutil.NoSuchProcess, psutil.AccessDenied, OSError):
                    fail += 1
            self.protected = ok
            self.failed = fail
            self._stop.wait(timeout=self._interval)
