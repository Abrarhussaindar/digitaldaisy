from django.urls import path
# from . import views, LoginView
from . import views
from .views import LoginView,home_api

urlpatterns = [
    path('home/', views.home, name="home"),
    path('', views.user_login, name="login"),
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
    # path('take-attendence/', views.take_attendence, name='take_attendence'),
    path('automate_attendance/', views.automate_attendance_view, name='automate_attendance'),


    path('api/login/', LoginView.as_view(), name='login'),
    path('api/homepage/', home_api, name='home-api'),
]