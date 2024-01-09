import schedule
import time
from job.job_autorun import job_autorun
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError


# 使用APSceduler
class RecurringService:
    def __init__(self, stocktype="HK", stockNum="09866"):
        """
        Initializes an instance of the RecurringService class.

        Args:
            stocktype (str, optional): The type of stock. Defaults to "HK". Accepted args include: "HK", "US", "CN".
            stockNum (str, optional): The stock number. Defaults to "09866".
        """

        self.scheduler = BackgroundScheduler()
        self.stocktype = stocktype
        self.stockNum = stockNum

    def add_task_interval(self, seconds=None, minutes=None, func=None):
        """
        Adds a new task to the scheduler.
        execute after interval minutes.seconds

        Args:
            interval (int): The interval in seconds between task executions.
            func (callable): The function to be executed as the task.
        """

        self.scheduler.add_job(func, "interval", seconds=seconds)

    def add_task_cron(
        self, day_of_week=None, hour=None, minute=None, second=None, func=None
    ):
        """
        Adds a new task to the scheduler.
        execute after interval minutes.seconds

        Args:
            interval (int): The interval in seconds between task executions.
            func (callable): The function to be executed as the task.
        """

        self.scheduler.add_job(
            func,
            "cron",
            day_of_week=day_of_week,
            hour=hour,
            minute=minute,
            second=second,
        )

    def remove_task(self, func):
        """
        Removes a task from the scheduler.

        Args:
            func (callable): The function associated with the task to be removed.
        """

        try:
            self.scheduler.remove_job(func.__name__)
        except JobLookupError:
            pass

    def run(self):
        """
        Runs the recurring tasks.

        Starts the scheduler and keeps it running until interrupted.
        """

        self.scheduler.start()
        try:
            while True:
                time.sleep(1)
                print("running jobs")
        except KeyboardInterrupt:
            self.scheduler.shutdown()


# Usage
if __name__ == "__main__":
    service = RecurringService()
    a = job_autorun("09866")
    service.add_task_interval(2, 0, a.test_run)
    service.run()


# class RecurringService:
#     def __init__(self, stocktype="HK", stockNum="09866"):
#         """
#         Initializes an instance of the Autorun class.

#         Args:
#             type (str, optional): The type of stock. Defaults to "HK". accpt args include: "HK", "US", "CN".
#             stockNum (str, optional): The stock number. Defaults to "09866".
#         """

#         self.schedule = schedule
#         if stocktype == "HK":
#             self.module = job_autorun()
#         self.job = self.module.run

#     def run(self):
#         """
#         运行自动执行任务。

#         每隔1分钟执行一次self.job方法，并持续运行。
#         """
#         # self.schedule.every(15).minutes.do(self.job)
#         self.schedule.every(15).seconds.do(self.job)
#         while True:
#             self.schedule.run_pending()
#             time.sleep(15)


# # Usage
# if __name__ == "__main__":
#     service = RecurringService()
#     service.run()
