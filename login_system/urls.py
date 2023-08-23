from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name="home"),
    path('', views.user_login, name="login"),
    path('logout/', views.user_logout, name="user_logout"),
    path('register/', views.create_new_user, name="register"),
    path('get_work_time/', views.get_work_time, name='get_work_time'),
    path('download-employee-details/', views.download_employee_details_view, name='download_employee_details'),
    path('download-daily-employee-details/', views.download_daily_employee_details_view, name='download_daily_employee_details'),
    path('permissions/', views.change_permission, name="permissions"),
    path('automate_attendance/', views.automate_attendance_view, name='automate_attendance'),
]