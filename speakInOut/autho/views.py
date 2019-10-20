from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from speakInOut.helper import parse_session, authentication_check, register_user
from .forms import LoginForm, AccountRegisterForm


def setup_view(request):
    if User.objects.all().count() > 0:
        return HttpResponseRedirect('/')
    # Get template data from the session
    template_data = parse_session(request,{'form_button':"Register"})
    # Proceed with rest of the view
    if request.method == 'POST':
        form = AccountRegisterForm(request.POST)
        if form.is_valid():
            register_user(
                form.cleaned_data['email'],
                form.cleaned_data['password_first'],
                form.cleaned_data['firstname'],
                form.cleaned_data['lastname']
            )
            user = authenticate(
                username=form.cleaned_data['email'].lower(),  # Make sure it's lowercase
                password=form.cleaned_data['password_first']
            )
            login(request, user)
            return HttpResponseRedirect('/dashboard/')
    else:
        form = AccountRegisterForm()
    template_data['form'] = form
    return render(request, 'setup.html', template_data)


def logout_view(request):
    # Django deletes the session on logout, so we need to preserve any alerts currently waiting to be displayed
    logout(request)
    return HttpResponseRedirect('/')


def login_view(request):
    # Authentication check. Users currently logged in cannot view this page.
    if request.user.is_authenticated:
        return HttpResponseRedirect('/dashboard/')
    elif User.objects.all().count() == 0:
        return HttpResponseRedirect('/setup/')
    # get template data from session
    template_data = parse_session(request, {'form_button':"Login"})
    # Proceed with the rest of view
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username = form.cleaned_data['email'].lower(),
                password = form.cleaned_data['password']
            )
            userInfo = User.objects.get(username=form.cleaned_data['email'].lower())
            if userInfo is not None:
                login(request,user)
                return HttpResponseRedirect('/dashboard/')
            else:
                return HttpResponseRedirect('/register/')
    else:
        form = LoginForm()
    template_data['form'] = form
    return render(request, 'login.html', template_data)


def register_view(request):
    # Authentication check. Users logged in cannot view this page.
    if request.user.is_authenticated:
        return HttpResponseRedirect('/dashboard/')
    elif User.objects.all().count() == 0:
        return HttpResponseRedirect('/setup/')
    # Get template data from session
    template_data = parse_session(request, {'form_button': "Register"})
    # Proceed with rest of the view
    if request.method == 'POST':
        form = AccountRegisterForm(request.POST)
        if form.is_valid():
            register_user(
                form.cleaned_data['email'],
                form.cleaned_data['password_first'],
                form.cleaned_data['firstname'],
                form.cleaned_data['lastname']
            )
            user = authenticate(
                username = form.cleaned_data['email'].lower(),
                password = form.cleaned_data['password_first']
            )
            login(request,user)
            return HttpResponseRedirect('/dashboard/')
    else:
        form = AccountRegisterForm()
    template_data['form'] = form
    return render(request,'signup.html',template_data)