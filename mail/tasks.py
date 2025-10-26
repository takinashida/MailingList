from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore

scheduler = BackgroundScheduler(timezone="Europe/Moscow")
scheduler.add_jobstore(DjangoJobStore(), "default")
