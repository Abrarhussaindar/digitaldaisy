# attendance.py
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
import pytz
from dateutil import parser

MAX_WORK_TIME = timedelta(hours=8)
MIN_REMAINING_TIME = timedelta(hours=0)


@login_required(login_url='login')
@require_GET
def get_work_time(request):
    emp = request.user
    work_time = emp.work_time
    login_time_str = request.session.get('login_time')
    current_time = datetime.now(pytz.timezone('Asia/Kolkata'))

    if login_time_str:
        login_time = parser.isoparse(login_time_str).astimezone(pytz.timezone('Asia/Kolkata'))
        duration = current_time - login_time
        today = current_time.date()
        total_work = work_time + duration
        total_work_time = timedelta(hours=8)  # Set the maximum total work time to 8 hours

        if total_work >= total_work_time:
            # If the total_work reaches 8 hours or exceeds it, set it to 8 hours
            total_work = total_work_time

        remaining_time = total_work_time - total_work

        if remaining_time < timedelta(seconds=0):
            # If the remaining_time is negative, set it to 0
            remaining_time = timedelta(seconds=0)
        

        formatted_work_time = format_timedelta(total_work)
        formatted_remaining_time = format_timedelta(remaining_time)
        return JsonResponse({'work_time': formatted_work_time, 'remaining_time': formatted_remaining_time})

    # If there is no login_time_str, return 0 duration
    formatted_work_time = format_timedelta(work_time)
    formatted_remaining_time = format_timedelta(emp.remaining_time)
    
    return JsonResponse({'work_time': formatted_work_time, 'remaining_time': formatted_remaining_time})# ... your implementation ...

def format_timedelta(td):
    seconds = int(td.total_seconds())
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def parse_duration_time(duration_time_str):
    if duration_time_str:
        duration_parts = duration_time_str.split(':')

        if len(duration_parts) == 3:  # Check if duration_parts has exactly 3 elements
            hours = int(duration_parts[0])
            minutes = int(duration_parts[1])
            seconds = int(duration_parts[2])

            return timedelta(hours=hours, minutes=minutes, seconds=seconds)
    return timedelta(seconds=0)

