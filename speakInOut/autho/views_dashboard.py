from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from speakInOut.helper import parse_session, authentication_check, register_user
from .forms import LoginForm, AccountRegisterForm
from .models import Speech
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


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
        vd = request.FILES.get("audiovideo", None)
        print(type(vd))
        path = default_storage.save('video/' + '123' + '.wav', ContentFile(vd.read()))
        user_obj = User.objects.get(username=request.user)
        speech_obj = Speech()
        speech_obj.user = user_obj
        speech_obj.video = path
        speech_obj.save()
        return HttpResponse(status=200)
    return render(request, 'dashboard.html', template_data)