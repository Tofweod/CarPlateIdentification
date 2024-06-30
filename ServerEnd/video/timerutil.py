from apscheduler.schedulers.background import BackgroundScheduler


class MultiTimer:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.jobs = {}
        self.callbacks = {}

    def timeout_task(self, timer_id):
        if timer_id in self.callbacks:
            self.callbacks[timer_id]()  # 调用回调函数

    def start_timer(self, timer_id, interval, callback):
        self.stop_timer(timer_id)  # 如果已有任务，先停止
        self.callbacks[timer_id] = callback  # 保存回调函数
        self.jobs[timer_id] = self.scheduler.add_job(self.timeout_task, 'interval', seconds=interval, args=[timer_id])

    def stop_timer(self, timer_id):
        if timer_id in self.jobs:
            self.jobs[timer_id].remove()
            del self.jobs[timer_id]

    def reset_timer(self, timer_id, interval):
        self.start_timer(timer_id, interval,self.callbacks[timer_id])