from django.http import JsonResponse
from django.core.management import call_command
from login_system.models import Employee
from datetime import datetime, timedelta
import pytz
import time


def automate_attendance_view(request):
    call_command('automate_attendance')
    return JsonResponse({"message": "Attendance automation initiated"})

def transfer_daily_to_weekly_lists():
    employees = Employee.objects.all()
    print("employees: ", employees)
    # current_user = request.user
    # Get the current date and time
    current_datetime = datetime.now(pytz.timezone('Asia/Kolkata'))

    # Check if it's 18:30
    dt_string = current_datetime.time().strftime("%H:%M:%S")
    hours, minutes, seconds = map(int, dt_string.split(':'))
    dt_time = time(hours, minutes, seconds)
    print("dt_time: ", dt_time)
    # Check if it's equal or greater than 11:40

    for emp in employees:
    
        # Transfer daily lists to weekly lists
        emp.weekly_login_list.append(emp.daily_login_list)
        emp.weekly_logout_list.append(emp.daily_logout_list)
        emp.weekly_duration_list.append(emp.daily_duration_list)
        emp.weekly_work_time_list.append(emp.work_time)
        emp.previous_work_time = emp.work_time
        # Clear daily lists
        emp.daily_login_list = "0"
        emp.daily_logout_list = "0"
        emp.daily_duration_list = "0"
        emp.login_list = "0"
        emp.logout_list = "0"
        emp.duration_list = "0"
        emp.work_time = timedelta(seconds=0)
        emp.remaining_time = timedelta(hours=8)
        

        emp.duration_time = "0:0:0"
        if emp.permission == "not given":
            emp.permission = "given"
        emp.save()

def transfer_weekly_to_monthly_lists():
    employees = Employee.objects.all()
    current_datetime = datetime.now(pytz.timezone('Asia/Kolkata'))

    for emp in employees:
        # Transfer weekly lists to monthly lists
        emp.monthly_login_list.append(emp.weekly_login_list)
        emp.monthly_logout_list.append(emp.weekly_logout_list)
        emp.monthly_duration_list.append(emp.weekly_duration_list)
        emp.monthly_work_time_list.append(emp.weekly_work_time_list)
        
        # Clear weekly lists
        emp.weekly_login_list = "0"
        emp.weekly_logout_list = "0"
        emp.weekly_duration_list = "0"
        emp.weekly_work_time_list = "0"

        # Save changes to the employee
        emp.save()

def transfer_monthly_to_yearly_lists():
    employees = Employee.objects.all()

    # Get the current date and time
    current_datetime = datetime.now(pytz.timezone('Asia/Kolkata'))

    # Check if it's the last day of the month and it's 19:00
    last_day_of_month = current_datetime.replace(day=1, month=current_datetime.month + 1) - timedelta(days=1)
    # if current_datetime.date() == last_day_of_month.date() and current_datetime.time() == time(18, 30):
    for emp in employees:
        # Transfer weekly lists to monthly lists
        emp.yearly_login_list.append(emp.monthly_login_list)
        emp.yearly_logout_list.append(emp.monthly_logout_list)
        emp.yearly_duration_list.append(emp.monthly_duration_list)
        emp.yearly_work_time_list.append(emp.monthly_work_time_list)
        
        # Save changes to the employee
        emp.save()
    for i in range(len(emp.yearly_login_list)):
        if emp.yearly_login_list[i] == "0":
            continue
        else:
            if emp.yearly_login_list[i].split()[0] not in emp.yearly_login_dates:
                emp.yearly_login_dates.append(emp.yearly_login_list[i].split()[0])
        emp.save()