from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader	
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout

# Create your views here.
def Shepherd(request):
    return HttpResponse("Hello World")

def home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

def signIn(request):

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
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)
                else:
                    request.session.set_expiry(1209600)
                return redirect('home')

        return render(request, 'login.html',{'form' : form})
    
def sign_out(request):
    logout(request)
    messages.success(request, f'you have been logged out.')
    return redirect('login')

def sign_up(request):
    if request.method =='GET':
        form =RegisterForm()
        return render (request, 'register.html', {'form' : form})
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have signed up successfully')
            login(request, user)
            return redirect ('home')
        else:
            return render(request, 'register.html',{'form' : form })
        
def UserLoggedIn(request):
    if request.user.is_authenticated == True:
        username= request.user.username
    else:
        username = None
    return username