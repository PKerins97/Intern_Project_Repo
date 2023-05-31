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

class AddPointForm(forms.Form):
    # No fields are necessary since we're not expecting any input
    pass
