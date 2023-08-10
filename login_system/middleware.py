from datetime import datetime, timedelta
from django.shortcuts import redirect

class UserInactivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity_time')
            if last_activity:
                inactive_duration = datetime.now() - last_activity
                max_inactive_duration = timedelta(minutes=30)
                if inactive_duration > max_inactive_duration:
                    # User is inactive, perform logout or other actions
                    # For example, you can clear the session and redirect to the login page
                    request.session.flush()
                    return redirect('login')

        response = self.get_response(request)

        if request.user.is_authenticated:
            request.session['last_activity_time'] = datetime.now()

        return response
    




# from datetime import time
# from django.contrib.auth import logout
# from django.utils import timezone

# class AutoLogoutMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         response = self.get_response(request)

#         # Check if the user is authenticated and is an employee
#         if request.user.is_authenticated and hasattr(request.user, 'employee'):
#             employee = request.user.employee
#             cutoff_time = time(17, 0)  # Specify the cutoff time (e.g., 5:00 PM)

#             # Convert the employee's last_login_at to an aware datetime
#             last_login_at_aware = timezone.make_aware(employee.last_login_at)

#             # Create a cutoff datetime using the same timezone as employee's last_login_at
#             cutoff_datetime = timezone.datetime.combine(
#                 last_login_at_aware.date(),
#                 cutoff_time,
#                 tzinfo=last_login_at_aware.tzinfo
#             )

#             # If the employee last logged in before the cutoff time, auto-logout
#             if last_login_at_aware and last_login_at_aware < cutoff_datetime:
#                 logout(request)

#         return response

