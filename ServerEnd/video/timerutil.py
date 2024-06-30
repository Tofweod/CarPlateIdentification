import multiprocessing
import time


class Timer:
    def __init__(self, timeout, callback, *args, **kwargs):
        self.timeout = timeout
        self.callback = callback
        self.args = args
        self.kwargs = kwargs
        self.timer_progress = None
        self.lock = multiprocessing.Lock()
        self.__start_timer()

    def __timer_target(self):
        time.sleep(self.timeout)
        with self.lock:
            self.callback(*self.args, **self.kwargs)

    def __start_timer(self):
        self.timer_progress = multiprocessing.Process(target=self.__timer_target)

    def reset(self):
        with self.lock:
            if self.timer_progress is not None and self.timer_progress.is_alive():
                self.timer_progress.terminate()
            self.__start_timer()

    def cancel(self):
        with self.lock:
            if self.timer_progress is not None and self.timer_progress.is_alive():
                self.timer_progress.terminate()
                self.timer_progress = None

