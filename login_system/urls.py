from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="user_logout"),
    path('register/', views.create_new_user, name="register"),
    path('get_work_time/', views.get_work_time, name='get_work_time'),
    path('admin/', views.admin, name="admin"),
    path('force-logout/', views.force_logout_other_users, name='force_logout_other_users'),
    path('download-employee-details/', views.download_employee_details_view, name='download_employee_details'),
    path('download-daily-employee-details/', views.download_daily_employee_details_view, name='download_daily_employee_details'),
    path('permissions/', views.change_permission, name="permissions"),
    path('download_attendance/', views.download_attendance, name='download_attendance'),
    # path('download_attendance/', views.download_attendance, name='download_attendance'),
    path('take-attendence/', views.take_attendence, name='take_attendence'),
    path('transfer_daily_to_weekly/', views.transfer_daily_to_weekly_view),
]