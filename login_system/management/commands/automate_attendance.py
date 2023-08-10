# your_app/management/commands/automate_attendance.py

from django.core.management.base import BaseCommand
from login_system.views import transfer_daily_to_weekly_lists, transfer_weekly_to_monthly_lists, transfer_monthly_to_yearly_lists


class Command(BaseCommand):
    help = 'Automates the attendance tasks'

    def handle(self, *args, **options):
        transfer_daily_to_weekly_lists()
        transfer_weekly_to_monthly_lists()
        transfer_monthly_to_yearly_lists()
        self.stdout.write(self.style.SUCCESS('Attendance tasks completed'))
