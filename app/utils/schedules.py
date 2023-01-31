from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.start(paused = True)
# scheduler.add_job(tryme,'interval',args=['BTCUSDT'],seconds = 10, id = 'interval')
# scheduler.add_job(tryme, 'cron',args=['BTCUSDT'], day='*',hour='00',minute='0', id='noche')