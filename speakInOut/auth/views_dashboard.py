from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from speakInOut.helper import parse_session, authentication_check, register_user
from auth.forms import LoginForm, AccountRegisterForm
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def dashboard_view(request):
    # Authentication check. Users currently logged in cannot view this page.
    authentication_result = authentication_check(request)
    if authentication_result is not None:
        return authentication_result
    template_data = parse_session(request)
    # get template data from session
    template_data['profile'] = User.objects.get(username=request.user)
    template_data['dashboard'] = True
    if request.method == "POST":
    	print(request.FILES)
    return render(request, 'dashboard.html', template_data)