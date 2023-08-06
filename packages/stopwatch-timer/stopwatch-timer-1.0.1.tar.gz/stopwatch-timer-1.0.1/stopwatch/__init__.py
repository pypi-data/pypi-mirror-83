"Provides a stopwatch class that can be used as a timer."
import time as _time
from types import SimpleNamespace as _Namespace
class Stopwatch:
    "A stopwatch class implemented using everyone's favourite subject - math!"
    __slots__ = ("_internal",)
    def __init__(self, func=None):
        if func is None:
            func = _time.perf_counter
        self._internal = _Namespace(running=False, func=func, started=0.0,
                                    first_stopped=0.0, second_stopped=0.0,
                                    laps=[], first=True)
    def __repr__(self):
        res = "Stopwatch(time=%s, " % self.time
        for attr in ["running", "started", "first_stopped", "second_stopped",
                     "laps", "first", "func"]:
            res += "%s=%s, " % (attr, getattr(self._internal, attr))
        return res[:-2] + ")"
    def __str__(self):
        return str(self.time)
    @property
    def running(self):
        return self._internal.running
    @property
    def func(self):
        "The function called to get the time, defaults to time.perf_counter."
        return self._internal.func
    @property
    def laps(self):
        return self._internal.laps
    @property
    def time(self):
        "The time on the stopwatch."
        if self.running:
            self._internal.started = self.func()
            attr = self._internal.first_stopped
        else:
            attr = self._internal.second_stopped
        return self._internal.started - attr
    def start(self):
        "Start the stopwatch."
        if self._internal.first:
            time = self.func()
            self._internal.started = time
            self._internal.first_stopped = time
            self._internal.second_stopped = time
            self._internal.first = False
        self._internal.running = True
    def stop(self):
        "Stop the stopwatch."
        if self.running:
            time = self.func()
            self._internal.started = time
            self._internal.second_stopped = self._internal.first_stopped
            self._internal.first_stopped = time
            self._internal.running = False
    def reset(self):
        "Reset and stop the stopwatch."
        self.__init__(self.func)
    def reset_laps(self):
        "Reset the stopwatch's laps."
        self._internal.laps.clear()
    def restart(self):
        "Reset and start the stopwatch."
        self.reset()
        self.start()
    def add_lap(self):
        "Add a lap to the stopwatch."
        self._internal.laps.append(self.time)
