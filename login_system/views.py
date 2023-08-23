# views.py
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

from .custom_views.remaning_work_time import get_remaining_time
from .custom_views.work_time import get_work_time
from .custom_views.attendance import automate_attendance_view
from .custom_views.user_views import user_login, user_logout, create_new_user, change_permission, check_authentication
from .custom_views.admin_views import download_employee_details_v, download_daily_employee_details_v
from .custom_views.home_view import home


@login_required(login_url='login')
def remaining_time(request):
    return get_remaining_time(request)

# Attendance Management
@login_required(login_url='login')
def attendance_automation(request):
    return automate_attendance_view(request)

@login_required(login_url='login')
def work_time(request):
    return get_work_time(request)

# User Views
def user_login_view(request):
    return user_login(request)

@login_required
def user_logout_view(request):
    return user_logout(request)

def create_user_view(request):
    return create_new_user(request)

@login_required(login_url='login')
def change_permission_view(request):
    return change_permission(request)

@login_required(login_url='login')
def home_view(request):
    return home(request)

def check_authentication_view(request):
    return check_authentication(request)

# Report Download
# def download_daily_attendance_view(request):
#     return download_daily_attendance(request)

# def download_attendance_view(request):
#     return download_attendance(request)

# Admin Views
@staff_member_required
def download_employee_details_view(request):
    return download_employee_details_v(request)

@staff_member_required
def download_daily_employee_details_view(request):
    return download_daily_employee_details_v(request)

# ... define other views ...

