# user_views.py
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from datetime import datetime, timedelta
import pytz
from dateutil import parser
from .work_time import parse_duration_time
from login_system.models import Employee
from login_system.forms import CreateEmployee

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
        emp.permission = "not given"
    total_time = timedelta()
    emp.save()


    for duration_str in emp.daily_duration_list:
        total_time += parse_duration_time(duration_str)
        # print("total_time: ", total_time)
    # print("outside for loop total_time: ", total_time)
    # Format the work time in h:m:s format
    work_time_str = str(total_time)
    # Save the work time to the employee instance
    emp.work_time = total_time
    total_work_time = timedelta(hours=8)
    remaining_time = total_work_time - emp.work_time
    # Update emp.remaining_time
    emp.remaining_time = remaining_time
    emp.save()

    logout(request)
    return redirect('login')

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


def check_authentication(request):
    if request.user.is_authenticated:
        return JsonResponse({"authenticated": True})
    else:
        return JsonResponse({"authenticated": False}, status=401)


