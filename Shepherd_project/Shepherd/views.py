from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as djlogin
from django.contrib.auth import logout as djlogout
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.template import loader
from django.utils import timezone
import random
import datetime
from django.contrib.auth.decorators import login_required
from mindee import Client, documents
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


from .forms import *
from .forms import FileEntryForm
from .models import *


# Create your views here.
def home(request):
    template = 'home.html'
    context = {}
    if (request.user.is_authenticated):
        context = {
            'user' : request.user,
            'mypoints': Points.objects.get(user_id=request.user.id).points,
            'form': ManualPointsForm()
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
                
                # return daily_login(request)
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
    topUsers = Points.objects.order_by('-points')
    context = {
        'champs': topUsers[:10]
    }
    this_user_id = topUsers.get(user=request.user)
    if (request.user.is_authenticated):
        context['current_user'] = request.user
        context['mypoints'] = Points.objects.get(user=request.user)
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

def manualPoints(request):
    if request.method == 'GET':
        template = 'manual_points.html'
        content = {
            'form': ManualPointsForm()
        }
        return render(request, template, content)
    else:
        form = ManualPointsForm(request.POST)
        if (form.is_valid()):
            print("form is valid")
            try:
                cashBefore = float(form['cost_before'].data)
                cashAfter = float(form['cost_after'].data)
            except ValueError:
                return redirect('manual')
            #TODO: decide which points system works
            p = Points.objects.get(user=request.user)
            p.points += (cashBefore-cashAfter)*100
            p.save()
            return redirect('home')
        else:
            return redirect('home')
    
def mindeeOCR(request):
    
    if request.method == 'GET':
        template = 'mindee_ocr.html'
        context = {
            'form': FileEntryForm()
        }
        return render(request, template, context)
    else:
        form = request.POST.get('file', '')
        print(form)
        form = FileEntryForm(request.POST, request.FILES)
        if form.is_valid():
            print(request.FILES["file"])
            return redirect('home')
        return redirect('leaderboard')
        # Init a new client
        # mindee_client = Client(api_key="229a21e30a51c7788f34d3b729a7775c")

        # Load a file from disk
        # input_doc = mindee_client.doc_from_path("/path/to/the/file.ext")

        # Parse the document as an invoice by passing the appropriate type
        # api_response = input_doc.parse(documents.TypeReceiptV5)

        # Print a brief summary of the parsed data
        # f = File('log.txt')
        # print(api_response.document)
        # print(api_response.document, file=f)
        # template = ''


def UserLoggedIn(request):
    if request.user.is_authenticated == True:
        username= request.user.username
    else:
        username = None
    return username

@login_required
def add_points(request):
    user_profile = get_object_or_404(Points, user=request.user)
    template = 'home.html'
    last_action_time = user_profile.last_action_time
    current_time = timezone.now()
    if last_action_time is not None:
        time_difference = current_time - last_action_time
        error_message = "You can only add points once a day."
        context = {
                'error_message': error_message,
                'mypoints': user_profile.points
            }
        return render(request, template, context)
    
    user_profile.points += 10
    user_profile.last_action_time = current_time
    user_profile.save()
    context = {}
    if (request.user.is_authenticated):
        context = {
            'mypoints': user_profile.points
       }
    else:
        context = { 'user' : request.user }
    return  render(request, template, context)

#driver = webdriver.Chrome('C:\Users\Paulk\Downloads\chromedriver')
#driver.get('https://www.tesco.ie/groceries/en-IE/promotions')
#offers = driver.find_elements_by_xpath('//*[@id="carouselWrapper"]/div[2]/div[2]/div[2]/div[1]/div/div[2]/div/ul/li[3]/div/div/div')

def congratulate(request):
    request
    
    return redirect('home')

def connect(request):
    pass