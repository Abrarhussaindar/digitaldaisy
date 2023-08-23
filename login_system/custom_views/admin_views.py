# admin_views.py
from django.contrib.admin.views.decorators import staff_member_required
from login_system.models import Employee
from login_system.admin import download_employee_details,download_daily_employee_details


@staff_member_required
def download_employee_details_v(request):
    queryset = Employee.objects.all()  # You can modify this queryset to select specific employees if needed
    response = download_employee_details(None, request, queryset)
    return response

@staff_member_required
def download_daily_employee_details_v(request):
    queryset = Employee.objects.all()  # You can modify this queryset to select specific employees if needed
    response = download_daily_employee_details(None, request, queryset)
    return response
