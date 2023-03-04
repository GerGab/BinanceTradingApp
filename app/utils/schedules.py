from apscheduler.schedulers.background import BackgroundScheduler
from ..controllers.PortfolioController import checkMarket,myBalance

scheduler = BackgroundScheduler()
scheduler.start(paused = False)# paused = True
#scheduler.add_job(myBalance,'interval',seconds = 30, id = 'interval')
scheduler.add_job(checkMarket, 'cron', day='*',hour='00',minute='0', id='noche')