from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as djlogin
from django.contrib.auth import logout as djlogout
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.utils import timezone

from .forms import LoginForm, RegisterForm
from .models import *


# Create your views here.
def home(request):
    template = 'home.html'
    context = {
        'user' : request.user,
    }
    return render(request, template, context)

def login(request):

    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method =='GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    
    elif request.method =='POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data['remember_me']
            user = authenticate(request, username = username, password = password)
            if user:
                djlogin(request, user)
                if not remember_me:
                    request.session.set_expiry(0)
                    return redirect ('home')
                else:
                    request.session.set_expiry(1209600)
            return redirect('home')

        return render(request, 'login.html',{'form' : form})
    
def logout(request):
    djlogout(request)
    messages.success(request, f'you have been logged out.')
    return redirect('login')

def register(request):
    if request.method =='GET':
        form =RegisterForm()
        return render (request, 'register.html', {'form' : form})
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            djlogin(request, user)
            return redirect ('home')
        else:
            return render(request, 'register.html',{'form' : form })
        
def UserLoggedIn(request):
    if request.user.is_authenticated == True:
        username= request.user.username
    else:
        username = None
    return username