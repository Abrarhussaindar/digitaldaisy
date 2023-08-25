from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.http import JsonResponse
from datetime import datetime, timedelta
import pytz
from dateutil import parser
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
import time
from .models import Employee
from datetime import time
from django.contrib.admin.views.decorators import staff_member_required
from .admin import download_employee_details,download_daily_employee_details
from django.http import HttpResponse
import openpyxl
from django.utils import timezone



from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

@login_required
@user_passes_test(lambda user: user.is_superuser)  # Only superusers can access this view
def force_logout_other_users(request):
    # Get the current superuser's session key
    superuser_session_key = request.session.session_key

    # Get sessions for all users except the current superuser
    other_sessions = Session.objects.filter(
        expire_date__gte=timezone.now(),
        session_key__not_exact=superuser_session_key
    )

    # Expire the sessions for other users
    for session in other_sessions:
        session.expire_date = timezone.now() - timedelta(seconds=1)
        session.save()

    return JsonResponse({"message": "All other users have been logged out."})


# Define constants for work time and remaining time limits
MAX_WORK_TIME = timedelta(hours=8)
MIN_REMAINING_TIME = timedelta(hours=0)

# your_app/views.py

from django.http import JsonResponse
from django.core.management import call_command

def automate_attendance_view(request):
    call_command('automate_attendance')
    return JsonResponse({"message": "Attendance automation initiated"})



@login_required(login_url='login')
def get_remaining_time(request):
    emp = request.user
    remaining_time = emp.remaining_time
    formatted_remaining_time = str(remaining_time)
    return JsonResponse({'remaining_time': formatted_remaining_time})

@require_GET
def update_work_time(request):
    emp = request.user

    while True:
        # Calculate the updated work time
        total_time = timedelta()
        for duration_str in emp.daily_duration_list:
            total_time += parse_duration_time(duration_str)

        print("total_time: ",total_time)
        # Format the work time in h:m:s format
        work_time_str = str(total_time)
        print("wts",work_time_str)
        # Save the work time to the employee instance
        emp.work_time = total_time
        print("emp.work_time: ",emp.work_time)
        emp.save()

        # Wait for 10 seconds before calculating again
        time.sleep(300)



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
    
    return JsonResponse({'work_time': formatted_work_time, 'remaining_time': formatted_remaining_time})


def download_daily_attendance(request):
    all_employees = Employee.objects.all()
    if request.method == 'POST':
        form = IndividualEmpAttendance(request.POST)
        if form.is_valid():
            employee = form.cleaned_data['employee']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            start_date = timezone.make_aware(datetime.combine(start_date, time.min), pytz.timezone('Asia/Kolkata'))
            end_date = timezone.make_aware(datetime.combine(end_date, time.max), pytz.timezone('Asia/Kolkata'))

            # Filter employees based on the provided date range
            employees_attendance = Employee.objects.filter(
                id=employee.id,
                yearly_login_dates__contains= start_date
            )
            # Create an Excel workbook and add a worksheet
            workbook = openpyxl.Workbook()
            worksheet = workbook.active
            worksheet.title = "Attendance"

            # Write headers
            worksheet.append(['Employee Name', 'Designation', 'Department', 'Login Time', 'Logout Time'])

            # Write attendance data
            for employee in employees_attendance:
                worksheet.append([employee.name, employee.designation, employee.department, employee.login_time, employee.logout_time])

            # Create a response with Excel content type
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename="attendance_{employee.name}.xlsx"'

            # Save the workbook to the response
            workbook.save(response)

            return response
            
    else:
        form = IndividualEmpAttendance()

    return render(request, 'download_attendance.html', {'form': form, 'all_employees': all_employees})

def download_attendance(request):
    all_employees = Employee.objects.all()
    if request.method == 'POST':
        form = IndividualEmpAttendance(request.POST)
        if form.is_valid():
            employee = form.cleaned_data['employee']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            # print("start date: ", start_date)
            # # Filter employees based on the provided date range
            # employees_attendance = Employee.objects.filter(
            #     id=employee.id,
            #     yearly_login_dates__contains= start_date
            # )
            # print("emp_y_l_d: ",Employee.objects.filter(yearly_login_dates__contains= start_date ))

            # print("employees_attendance: ", employees_attendance)
            start_date = timezone.make_aware(datetime.combine(start_date, time.min), pytz.timezone('Asia/Kolkata'))
            end_date = timezone.make_aware(datetime.combine(end_date, time.max), pytz.timezone('Asia/Kolkata'))

            # Filter employees based on the provided date range
            employees_attendance = Employee.objects.filter(
                id=employee.id,
                yearly_login_dates__contains= start_date
            )
            # Create an Excel workbook and add a worksheet
            workbook = openpyxl.Workbook()
            worksheet = workbook.active
            worksheet.title = "Attendance"

            # Write headers
            worksheet.append(['Employee Name', 'Designation', 'Department', 'Login Time', 'Logout Time'])

            # Write attendance data
            for employee in employees_attendance:
                worksheet.append([employee.name, employee.designation, employee.department, employee.login_time, employee.logout_time])

            # Create a response with Excel content type
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename="attendance_{employee.name}.xlsx"'

            # Save the workbook to the response
            workbook.save(response)

            return response
            
    else:
        form = IndividualEmpAttendance()

    return render(request, 'download_attendance.html', {'form': form, 'all_employees': all_employees})

def daterange(start_date, end_date):
    # A helper function to generate a list of dates between start_date and end_date (inclusive).
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timezone.timedelta(n)




def format_timedelta(td):
    seconds = int(td.total_seconds())
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def user_login(request):
    department_categories = ["Design & Development", "Process Co-Ordinator","Content Writer",  "SEO", "HR", "Sales Digital Daisy", "Sales Daisy TecMart", "Sales Daisy Fashion", "Management/Admin" ]
    permission = ""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('Password')
        department = request.POST.get('department')
        print(username, password, department)
        employee = authenticate(request, department=department, username=username, password=password)
        print(employee)
        if employee is not None and employee.permission == "given":  # Check permission
            
            login(request, employee)
            employee.login_counter += 1
            # Reset the counter to 0 on login
            request.session['counter_time'] = 0
            current_time = datetime.now(pytz.timezone('Asia/Kolkata'))
            current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
            employee.login_list.append(current_time_str)
            employee.intime = current_time_str
            employee.login_time = current_time
            previous_login_time_str = request.session.get('login_time')
            employee.daily_login_list.append(current_time_str)
            login_time = parser.isoparse(previous_login_time_str).astimezone(pytz.timezone('Asia/Kolkata')) if previous_login_time_str else current_time
            request.session['login_time'] = current_time.isoformat()
            if previous_login_time_str:
                previous_duration = current_time - login_time
                counter_time = request.session.get('counter_time', 0) + previous_duration.total_seconds()
                request.session['counter_time'] = counter_time

            employee.login_time = current_time
            employee.save()

            return redirect('home')
        # else:
        #     permission = "not given"

    context = {
        "department_categories": department_categories,
        "permission": permission
    }
    return render(request, "login.html", context)


@login_required
def user_logout(request):
    emp = request.user

    current_time = datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")
    emp.logout_list.append(current_time)
    emp.daily_logout_list.append(current_time)
    print("emp_intime: ", emp.intime)
    t1 = datetime.strptime(emp.intime, "%Y-%m-%d %H:%M:%S")
    t2 = datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S")
    duration_time = t2 - t1

    emp.duration_list.append(str(duration_time))
    emp.daily_duration_list.append(str(duration_time))
    emp.logout_counter += 1
    emp.logout_time = datetime.now()
    emp.out_time = current_time
    emp.duration = duration_time
    emp.duration_time = str(t2 - t1) # Update the duration_time calculation
    if request.user.is_superuser:
        emp.permission = "given"
    else:
        emp.permission = "given"
    total_time = timedelta()
    emp.save()

    for duration_str in emp.daily_duration_list:

        total_time += parse_duration_time(duration_str)
        print("total_time: ", total_time)

    print("outside for loop total_time: ", total_time)
    # Format the work time in h:m:s format
    work_time_str = str(total_time)

    # Save the work time to the employee instance
    emp.work_time = total_time

    total_work_time = timedelta(hours=8)
    remaining_time = total_work_time - emp.work_time
    # Update emp.remaining_time
    emp.remaining_time = remaining_time
        # emp.save()

    # Save the changes to the employee
    emp.save()

    


    logout(request)
    return redirect('login')

from django.contrib.auth import logout
from django.http import JsonResponse

# def logout_view(request):
#     logout(request)
#     return JsonResponse({"message": "Logged out successfully"})


def create_new_user(request):
    form = CreateEmployee()
    if request.method == 'POST':
        form = CreateEmployee(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'form': form}
    return render(request, "register.html", context)

@login_required(login_url='login')  
def change_permission(request):
    emp = request.user
    if request.method == 'POST':
        employee_id = request.POST.get('employee')
        permission = request.POST.get('permission')
        try:
            employee = Employee.objects.get(pk=employee_id)
            employee.permission = permission
            employee.save()
            return redirect('home') 
        except Employee.DoesNotExist:
            pass
    employees_by_dep = Employee.objects.filter(department=emp.department)
    all_employees = Employee.objects.all()
    context = {
        'employees': employees_by_dep,
        'all_employees': all_employees,
    }
    return render(request, "change_permission.html", context)


@login_required(login_url='login')
def home(request):
    emp = request.user
   # if emp.permission == "not given":
       # logout(request)
        #return redirect('login')

    date = datetime.now(pytz.timezone('Asia/Kolkata')).date()
    duration = None
    login_time_str = request.session.get('login_time')
    current_time = datetime.now(pytz.timezone('Asia/Kolkata'))
    employees_by_dep = Employee.objects.filter(department=emp.department)
    all_employees = Employee.objects.all()

    
    design_development = Employee.objects.filter(department="Design & Development")
    salestm = Employee.objects.filter(department="Sales Daisy TecMart")
    salesfs = Employee.objects.filter(department="Sales Daisy Fashion")
    salesdd = Employee.objects.filter(department="Sales Digital Daisy")
    seo = Employee.objects.filter(department="SEO")
    hr = Employee.objects.filter(department="HR")
    content_writer = Employee.objects.filter(department="Content Writer")
    admin = Employee.objects.filter(department="Management/Admin")
    process_co_ordinator = Employee.objects.filter(department="Process Co-ordinator")
    dep_list = ["Design & Development","SEO", "HR", "Content Writer", "Management/Admin", "Process Co-ordinator", "Sales Daisy TecMart", "Sales Daisy Fashion", "Sales Digital Daisy"]
    tb_list = [design_development, seo, hr, content_writer, admin, process_co_ordinator, salestm, salesfs, salesdd]
    if login_time_str:
        
        login_time = parser.isoparse(login_time_str).astimezone(pytz.timezone('Asia/Kolkata'))
        duration = current_time - login_time

        today = current_time.date()

        total_work = emp.work_time + duration
        total_work_seconds = total_work.total_seconds()
        total_work_time = timedelta(hours=8)
        remaining_time = total_work_time - total_work
        total_work_str = str(total_work)
        total_work_formatted = total_work_str.rjust(8, '0')
        print("total_work_formatted: ", total_work_formatted)
    else:

        total_work_formatted = "00:00:00"
        total_work_seconds = 0

    for em in design_development:
        if login_time_str:
            login_time = parser.isoparse(login_time_str).astimezone(pytz.timezone('Asia/Kolkata'))
            duration = current_time - login_time
            # print("duration: ", duration)
            today = current_time.date()
            total_work = em.work_time + duration
            total_work_seconds = total_work.total_seconds()
            total_work_time = timedelta(hours=8)
            remaining_time = total_work_time - total_work
            total_work_str = str(total_work)
            total_work_formatted = total_work_str.rjust(8, '0')
            # print("total_work_formatted: ", total_work_formatted)
        else:
            total_work_formatted = "00:00:00"
            total_work_seconds = 0
        # print("em: ", em)

    employees = Employee.objects.all()
        # Get the current date and time
    current_datetime = datetime.now(pytz.timezone('Asia/Kolkata'))
    # Check if it's 18:30
    dt_string = current_datetime.time().strftime("%H:%M:%S")

    context = {
        'emp': emp,

        'employees': employees_by_dep,
        'all_employees': all_employees,
        'dep_list': dep_list,
        'tb_list': tb_list,
        'design_development': design_development,
        'salesdd': salesdd,
        'salestm': salestm,
        'salesfs': salesfs,
        'seo': seo,
        'hr': hr,
        'content_writer': content_writer,
        'admin': admin,
        'process_co_ordinator': process_co_ordinator,
        'total_work_seconds': total_work_seconds,
        'total_work': total_work_formatted,
        'duration': duration.total_seconds() if duration else 0,
    }
    return render(request, "home.html", context)



def check_authentication(request):
    if request.user.is_authenticated:
        return JsonResponse({"authenticated": True})
    else:
        return JsonResponse({"authenticated": False}, status=401)
    


@staff_member_required
def download_employee_details_view(request):
    queryset = Employee.objects.all()  # You can modify this queryset to select specific employees if needed
    response = download_employee_details(None, request, queryset)
    return response

@staff_member_required
def download_daily_employee_details_view(request):
    queryset = Employee.objects.all()  # You can modify this queryset to select specific employees if needed
    response = download_daily_employee_details(None, request, queryset)
    return response


# @login_required
# def take_attendence():
#     # Perform the tasks using the existing transfer_daily_to_weekly_lists() and transfer_weekly_to_monthly_lists() functions
#     transfer_daily_to_weekly_lists()
#     transfer_weekly_to_monthly_lists()
#     transfer_monthly_to_yearly_lists()
#     return JsonResponse({"message": "Attendence taken successfully."})



def transfer_daily_to_weekly_lists():
    # Get all employees
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
    # Get all employees
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
    # Get all employees
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
def admin(request):
    return render(request)


def parse_duration_time(duration_time_str):
    if duration_time_str:
        duration_parts = duration_time_str.split(':')

        if len(duration_parts) == 3:  # Check if duration_parts has exactly 3 elements
            hours = int(duration_parts[0])
            minutes = int(duration_parts[1])
            seconds = int(duration_parts[2])

            return timedelta(hours=hours, minutes=minutes, seconds=seconds)
    return timedelta(seconds=0)



