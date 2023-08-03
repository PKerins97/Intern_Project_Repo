from django.urls import path
from . import views
from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)


urlpatterns = [
    path('home/', views.home, name='home'),
    path('home/connect/', views.connect, name='connectHome'),
    path('register/', views.register, name='register'),
    path('', views.login, name='login'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('add-point/', views.add_points, name='add_point'),
    path('populate/', views.populate, name='populate'),
    path('product/', views.search_func, name='product'),
    path('map/', views.manualPoints, name='manual'),
    path('password-reset/', PasswordResetView.as_view(template_name='registration/password_reset.html'),name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),name='password_reset_complete'),
    
    path('history/', views.history, name='history'),
    
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('leaderboard/connect/', views.connect, name='connect'),
    path('leaderboard/congratulate/', views.congratulate, name='congratulate')
    
    #path('password-reset/',PasswordResetView.as_view(template_name='registration/password_reset.html',html_email_template_name='registration/password_reset_email.html'), name='password-reset')
]