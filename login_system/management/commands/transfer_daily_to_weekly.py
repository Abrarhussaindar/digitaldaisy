# your_app/management/commands/transfer_daily_to_weekly.py

from django.core.management.base import BaseCommand
from login_system.views import transfer_daily_to_weekly_lists

class Command(BaseCommand):
    help = 'Transfers daily data to weekly lists'

    def handle(self, *args, **options):
        transfer_daily_to_weekly_lists()
        self.stdout.write(self.style.SUCCESS('Daily to weekly transfer complete'))
