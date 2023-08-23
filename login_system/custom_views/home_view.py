from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
import pytz
from dateutil import parser
from login_system.models import Employee



@login_required(login_url='login')
def home(request):
    emp = request.user
    if emp.permission == "not given":
        logout(request)
        return redirect('login')

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
        # emp.psudo_work_time = total_work_formatted
        # print("pwt: ", emp.psudo_work_time)
        emp.psudo_work_time = total_work
        emp.save()
        print("total_work_formatted: ", total_work_formatted)
        print("emp pwt", emp.psudo_work_time)
    else:
        total_work_formatted = "00:00:00"
        total_work_seconds = 0

    # for em in design_development:
    #     if login_time_str:
    #         login_time = parser.isoparse(login_time_str).astimezone(pytz.timezone('Asia/Kolkata'))
    #         duration = current_time - login_time
    #         # print("duration: ", duration)
    #         today = current_time.date()
    #         total_work = em.work_time + duration
    #         total_work_seconds = total_work.total_seconds()
    #         total_work_time = timedelta(hours=8)
    #         remaining_time = total_work_time - total_work
    #         total_work_str = str(total_work)
    #         total_work_formatted = total_work_str.rjust(8, '0')
    #         # print("total_work_formatted: ", total_work_formatted)
    #     else:
    #         total_work_formatted = "00:00:00"
    #         total_work_seconds = 0
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