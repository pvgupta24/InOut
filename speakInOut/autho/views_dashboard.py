from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from speakInOut.helper import parse_session, authentication_check, register_user
from .forms import LoginForm, AccountRegisterForm
from .models import Speech
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

import threading
import subprocess
import os
from textCompare import *
from eyeTrack import track

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
        name = request.POST.get("name")
        print(type(vd))
        path = default_storage.save('video/' + '123' + '.mp4', ContentFile(vd.read()))

        # task = ThreadTask()
        # task.save()
        t = threading.Thread(target=longTask,args=[path])
        t.setDaemon(True)
        t.start()

        user_obj = User.objects.get(username=request.user)
        speech_obj = Speech()
        speech_obj.name = name
        speech_obj.user = user_obj
        speech_obj.video = path
        speech_obj.audio = 'audio/' + '123' + '.wav'
        speech_obj.save()
        return HttpResponse(status=200)
    return render(request, 'dashboard.html', template_data)


# def startThreadTask(request):
#     task = ThreadTask()
#     task.save()
#     t = threading.Thread(target=longTask,args=[task.id])
#     t.setDaemon(True)
#     t.start()
#     return JsonResponse({'id':task.id})

# # Check status of long tash
# def checkThreadTask(request,id):
#     task = ThreadTask.objects.get(pk=id)
#     return JsonResponse({'is_done':task.is_done})

def longTask(video_path):
    print("Analyzing ",video_path)    
    track.analyzeFrames(video_path)
    
    print("Generating audio file")
    audio_file_name = os.path.basename(video_path).split('.')[0] + '.wav'
    command = "ffmpeg -i " + video_path + " -ab 160k -ac 2 -ar 44100 -vn audio/" + audio_file_name
    subprocess.call(command, shell=True)

    audio_path = "audio/" + audio_file_name
    text_from_audio = audioTranscript(audio_path)
    print(text_from_audio)
    # task = ThreadTask.objects.get(pk=id)
    # task.is_done = True
    # task.save()
    # print("Finished task",id)