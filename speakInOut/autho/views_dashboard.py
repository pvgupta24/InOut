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
import json
import os
from textCompare import *
from eyeTrack import track
from fillerWordAnalyzer import analyze_text
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
        request.session['video_name'] = name
        # task = ThreadTask()
        # task.save()
        t = threading.Thread(target=longTask,args=[path,request,name])
        t.setDaemon(True)
        t.start()

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

def longTask(video_path, request,name):
    print("Analyzing ",video_path)    
    conf = track.analyzeFrames(video_path)
    
    print("Generating audio file")
    audio_file_name = os.path.basename(video_path).split('.')[0] + '.wav'
    command = "ffmpeg -i " + video_path + " -ab 160k -ac 2 -ar 44100 -vn audio/" + audio_file_name
    subprocess.call(command, shell=True)

    #Generating text from audio.
    audio_path = "audio/" + audio_file_name
    text_from_audio = audioTranscript(audio_path)
    print(text_from_audio)

    #Generating questions from text.
    questions = generateQuestionsFromText(text_from_audio)
    print(questions)
    final_quest = ""
    for i in range(8):
        if i< len(questions):
            final_quest += questions[i]+","
    print("Final questions is" + final_quest)
    #Analysing filler words
    filler_percent = analyze_text.filler_percentage(text_from_audio)
    print(filler_percent)

    user_obj = User.objects.get(username=request.user)
    speech_obj = Speech()
    speech_obj.name = name
    speech_obj.user = user_obj
    speech_obj.video = video_path
    speech_obj.audio = audio_path
    speech_obj.filler_per = filler_percent
    speech_obj.gaze_count = conf
    speech_obj.generated_questions = final_quest
    speech_obj.speech2text = text_from_audio
    speech_obj.save()
    # task = ThreadTask.objects.get(pk=id)
    # task.is_done = True
    # task.save()
    # print("Finished task",id)

def show_analysis(request):
    authentication_result = authentication_check(request)
    if authentication_result is not None:
        return authentication_result
    template_data = parse_session(request)
    # get template data from session
    template_data['profile'] = User.objects.get(username=request.user)
    template_data['dashboard'] = True
    
    name = template_data['video_name']
    obj = Speech.objects.get(name = name, user = request.user)
    print("Printing")
    print(obj)
    template_data['obj'] = obj
    template_data['obj'].generated_questions_string = obj.generated_questions.split(",")
    print(template_data['obj'].name)
   
    return render(request, "dashboard.html", template_data)


