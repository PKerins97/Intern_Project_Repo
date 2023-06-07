from django import forms
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class RegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields = ['username','first_name','last_name','email','password1','password2']

        def clean_email(self):
            email= self.clean_data["email"]
            if User.objects.filter(email=email).exists():
                raise ValidationError("A user with this email already exists!")
            return email

class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)
    remember_me = forms.BooleanField(required=False)

class ManualPointsForm(forms.Form):
    cost_before = forms.DecimalField(decimal_places=2, min_value=0, required=True)
    cost_after = forms.DecimalField(decimal_places=2, required=True)
