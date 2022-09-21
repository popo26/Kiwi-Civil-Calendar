from django.urls import path

from .views import PasswordResetByUser, SignUpView



urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),   
]