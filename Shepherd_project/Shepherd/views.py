from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as djlogin
from django.contrib.auth import logout as djlogout
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, RegisterForm
from .models import *


# Create your views here.
def home(request):
    template = 'home.html'
    context = {
        'user' : request.user,
        'mypoints': Points.objects.get(user_id=request.user.id).points
    }
    context = {}
    if (request.user.is_authenticated):
        context = {
            'user' : request.user,
            'mypoints': Points.objects.get(user_id=request.user.id).points
            #'daily_login':DailyLogin.objects.get(login_date = request.user.id).login_date,
            
        }
    else:
        context = { 'user' : request.user }
    return  render(request, template, context)

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
            return redirect('login')
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
            points = Points(user=user, points=0)
            user.save()
            points.save()
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

from datetime import date
from .models import DailyLogin

@login_required
def login_view(request):
    # Check if the user already has a daily login record for today
    today = date.today()
    daily_login = DailyLogin.objects.filter(user=request.user, login_date=today).first()

    if not daily_login:
        # User hasn't logged in today, create a new daily login record
        daily_login = DailyLogin(user=request.user, login_date=today)
        daily_login.save()

        # Give rewards to the user
        daily_login.points  = ('points')+1  # Adds one point to points as long in bonus 
        daily_login.save()

    # Pass the daily login record to the template for display
    return render(request, 'home.html', {'daily_login': daily_login})