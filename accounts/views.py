from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView

from .forms import CustomUserCreationForm, CustomUserPasswordChangeForm

app_name="accounts"

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

class PasswordResetByUser(PasswordChangeView):
    form_class = CustomUserPasswordChangeForm
    template_name = 'registration/password_change_form.html'
    success_url = "/"

class PasswordResetDoneByUser(PasswordChangeDoneView):
    template_name = "registration/password_change_done.html"

