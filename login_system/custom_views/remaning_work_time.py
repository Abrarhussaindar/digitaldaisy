# authentication.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required(login_url='login')
def get_remaining_time(request):
    # ... your implementation ...
    emp = request.user
    remaining_time = emp.remaining_time
    formatted_remaining_time = str(remaining_time)
    return JsonResponse({'remaining_time': formatted_remaining_time})

