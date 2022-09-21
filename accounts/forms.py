from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm

from .models import CustomUser
# from django.forms import TextInput, EmailField, PasswordInput

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")

        widgets = {
        'username':forms.TextInput(attrs={"class":'form-control text-center', 'placeholder': 'Username: LETTERS, DIGITS AND @/./+/-/_ ONLY.'}),
        'email':forms.EmailInput(attrs={"class":'form-control text-center', 'placeholder': 'Email'}),
        }    

        
class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email")

        widgets = {
        'username':forms.TextInput(attrs={"class":'form-control', 'placeholder': 'Username'}),
        'password':forms.PasswordInput(attrs={"class":'form-control', 'placeholder': 'Password'}),
        }
      
        def __init__(self, *args, **kwargs):
            super(CustomUserCreationForm, self).__init__(*args, **kwargs)
            self.fields['username'].widget.attrs = {'class': 'form-control', 'placeholder': 'Password','required': 'required'}
            self.fields['password1'].widget.attrs = {'class': 'form-control', 'placeholder': 'Confirm password','required': 'required'}


class CustomUserPasswordChangeForm(PasswordChangeForm):

    class Meta:
        model = CustomUser
        fields = '__all__'
            
       