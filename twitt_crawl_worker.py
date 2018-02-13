from celery import Celery
from datetime import timedelta, datetime
from kombu import Queue
from celery.schedules import crontab

from service.send_slack_service import SlackPushService
from service.twitt_crawl_service import TwittCrawlService

BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

app = Celery('tasks', broker=BROKER_URL, backend=CELERY_RESULT_BACKEND)

app.conf.update(
    CELERY_DEFAULT_QUEUE='twitt_push',
    CELERY_QUEUES={
        Queue('twitt_push', routing_key='task.cron_crawl_twitt'),
    },
    CELERY_ROUTES={
        'task.cron_crawl_twitt': {
            'queue': 'twitt_push',
            'routing_key': 'task.cron_crawl_twitt'
        }
    },

    CELERY_ACCEPT_CONTENT=['json', ],
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
    CELERYBEAT_SCHEDULE={
        'cron_twitt_push': {
            'task': 'task.cron_crawl_twitt',
            'schedule': timedelta(seconds=120)
        }
    }
)


@app.task(name='task.cron_crawl_twitt')
def cron_crawl_twitt():
    task_crawl_twitt()


@app.task(name='task.task_crawl_twitt')
def task_crawl_twitt():
    twitt_service = TwittCrawlService()
    twitt_service.parseTwittAll()
    push_service = SlackPushService()
    push_service.pushSlack()
