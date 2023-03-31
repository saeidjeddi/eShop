from datetime import datetime, timedelta
from celery import shared_task
from accounts.models import OtpCod
import pytz


@shared_task
def remove_expierd():
    expired_tome = datetime.now(tz=pytz.timezone('Asia/Tehran')) - timedelta(minutes=1)
    OtpCod.objects.filter(created__lt=expired_tome).delete()
