from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as djlogin
from django.contrib.auth import logout as djlogout
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.utils import timezone
import random

from .forms import LoginForm, RegisterForm
from .models import *


# Create your views here.
def home(request):
    template = 'home.html'
    context = {}
    if (request.user.is_authenticated):
        context = {
            'user' : request.user,
            'mypoints': Points.objects.get(user_id=request.user.id).points
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
   
def leaderboard(request):
    template = 'leaderboard.html'
    context = {
        'top_users': []
    }
    if (request.user.is_authenticated):
        context['current_user'] = request.user
    return render(request, template, context)
         
def populate(request):
    random.seed()
    n = request.GET.get('n','10')
    n = int(n)
    template = 'home.html'
    for i in range(n):
        id=random.randint(11, 999)
        user = User(username='robot'+str(id), first_name='John '+str(id), last_name='Doe'+str(id))
        points = Points(user=user, points = random.randint(0,999))
        user.save()
        points.save()
    return redirect('home')
    
def UserLoggedIn(request):
    if request.user.is_authenticated == True:
        username= request.user.username
    else:
        username = None
    return username