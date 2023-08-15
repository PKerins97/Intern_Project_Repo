from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate,login as djlogin
from django.contrib.auth import logout as djlogout
from django.contrib.auth.views import LogoutView
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.template import loader
from django.utils import timezone
import random
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session



from .forms import *
from .forms import FileEntryForm
from .models import *


# Create your views here.
@login_required
def home(request):
    template = 'home.html'
    context = {}
    if (request.user.is_authenticated):

        context = {
            'user' : request.user,
            'mypoints': Points.objects.get(user_id=request.user.id).points,
            'form': ManualPointsForm()
            }
        messages = Message.objects.filter(receiver=request.user).filter(consumed=False)
        print(messages)
        if (messages==None):
            context['has_messages'] = False
        else:
            context['has_messages'] = True
            context['messages'] = list(messages)
            messages.update(consumed=True)
        
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
            login_error = "Invaild Username or Password! Try again!"
            user = authenticate(request, username=username, password=password)
            if user is not None:
                djlogin(request, user)
            else:
                if request.method =='POST':
                    form = LoginForm()
                    template = 'login.html'
                    login_error = "Invaild Username or Password! Please try again!"
                    # context={
                    #     'login_error':login_error
                    # }
                return render(request,template,{'form': form})
                
            if not remember_me:
                request.session.set_expiry(0)
                return redirect('login')
            else:
                request.session.set_expiry(1209600)

            
        return render(request, 'login.html', {'form': form})
    
def logout(request):
     djlogout(request)
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
    topUsers = Points.objects.order_by('-points')[:10]
    messages = Message.objects.filter(message="-connect")
    if (request.user.is_authenticated):
        for user in topUsers:
            user.user.i_sent = messages.filter(sender=request.user, receiver=user.user).exists()
            user.user.sent_me = messages.filter(sender=user.user, receiver=request.user).exists()
            
    context = {
        'champs': topUsers
    }
    if (request.user.is_authenticated):
        context['current_user'] = request.user
        context['mypoints'] = Points.objects.get(user=request.user).points
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
        template = 'manual_points.html'
        context = {}
        if (form.is_valid()):
            try:
                cashBefore = float(form['cost_before'].data)
                cashAfter = float(form['cost_after'].data)
            except ValueError:
                return redirect('manual')
            description = form['description'].data
            cap_description = description.capitalize()
            display_description = cap_description
            shop = form['shop'].data
            #TODO: decide which points system works
            p = Points.objects.get(user=request.user)
            p.points += (cashBefore-cashAfter)*100
            p.save()
            purchase = Purchase(
                user = request.user,
                money_before = cashBefore,
                money_after = cashAfter,
                description = display_description,
                shop = shop
            )
            purchase.save()
            
            # Create success message
            context['message'] = 'success'
        else:
            # Create failure message
            context['message'] = 'fail'
            
        context['form'] = ManualPointsForm()
        return render(request, template, context)

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


def search_func(request):
    if request.method == "POST":
        search_query = request.POST.get('search_query', None)
        if search_query:
            # Perform the search using the 'description__icontains' filter
            results = Items.objects.filter(description__icontains=search_query)
            for result in results:
               
                result.image_url = result.image.url  

            return render(request, 'product.html', {"results": results})

    # If no search is performed or the request is not POST, render the template without results
    return render(request, 'product.html')

def congratulate(request):
    
    receiver_name = request.GET['receiver']
    receiver = User.objects.get(username=receiver_name)
    
    message = Message(sender=request.user, receiver=receiver, message='-congrats', consumed=False)
    message.save()
    
    messages = Message.objects.filter(receiver=request.user).filter(consumed=False)
    print(messages)
    return redirect('leaderboard')

def connect(request):
    
    receiver_name = request.GET['receiver']
    redirect_to = request.GET['src']
    print(receiver_name)
    receiver = User.objects.get(username=receiver_name)
    
    # If not message has been sent from the user to that user before, do so
    if (not Message.objects.filter(sender=request.user, receiver=receiver, message='-connect').exists()):
        message = Message(sender=request.user, receiver=receiver, message='-connect', consumed=False)
        message.save()
    # If it is an acceptance message
    else:
        pass
    
    return redirect(redirect_to)


def history(request):
    template = 'history.html'
    orders = Purchase.objects.filter(user=request.user)
    for order in orders:
        order.points = 100 * (order.money_before - order.money_after)
        
    context = {
        'mypoints': Points.objects.get(user_id=request.user.id).points,
        'my_orders': orders
    }
    return render(request, template, context)

def audio_view(request):
    audio_url = "static/Intern_project_recording.mp3"  # Replace with the actual URL of your audio file
    context = {'audio_url': audio_url}
    return render(request, 'home.html', context)
