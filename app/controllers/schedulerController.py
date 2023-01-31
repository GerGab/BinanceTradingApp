from ..utils.schedules import scheduler

def turnSchedulerOn():
    scheduler.resume()

def turnSchedulerOff():
    scheduler.pause()