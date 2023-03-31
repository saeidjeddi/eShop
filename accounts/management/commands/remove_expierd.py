from django.core.management.base import BaseCommand
from accounts.models import OtpCod
from datetime import datetime, timedelta
import pytz


class Command(BaseCommand):
    help = 'remove all otp code expired'

    def handle(self, *args, **options):
        expired_tome = datetime.now(tz=pytz.timezone('Asia/Tehran')) - timedelta(minutes=1)
        OtpCod.objects.filter(created__lt=expired_tome).delete()
        self.stdout.write('کد منقضی حذف شد ')
