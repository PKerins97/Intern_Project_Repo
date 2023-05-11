from django.urls import path
from . import views


urlpatterns = [
    path('Shepherd/',views.Shepherd,name='Shepherd'),
    path('home/', views.home, name='home'),
    path('register/', views.sign_up, name='register'),
    path('', views.signIn, name='login'),
    path('logout/', views.sign_out, name='logout'),
    
]