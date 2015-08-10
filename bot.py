import requests
import os
import cfg
from apscheduler.schedulers.background import BackgroundScheduler


class Bot():
    def __init__(self, cfg):
        self.token = cfg.TOKEN_BOT
       
        self.scheduler = BackgroundScheduler({
            'apscheduler.jobstores.default': {
                'type': 'sqlalchemy',
                'url': cfg.POSTGRESQL_DB
            },
            'apscheduler.executors.default': {
                'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
                'max_workers': '20'
            },
            'apscheduler.executors.processpool': {
                'type': 'processpool',
                'max_workers': '5'
            },
            'apscheduler.job_defaults.coalesce': 'false',
            'apscheduler.job_defaults.max_instances': '3',
            'apscheduler.timezone': 'UTC',
        })

    def post(self, text, channel):
        url = 'https://{domain}/services/hooks/slackbot?token={token}&channel=%23{channel}'
        r = requests.post(url.format(domain=cfg.TEAMDOMAIN, token=self.token, channel=channel), data=text)

    def test(self, args=None):
        print 'Scheduler test'
        if args:
            print 'job args: {0}'.format(' '.join(args))

    def add_reminder(self):
        self.scheduler.add_job(self.test, 'interval', minutes=1, id='job_id', jobstore='default')
        # return self.scheduler.get_jobs('default')

