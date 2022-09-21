from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
   
    login_status = models.BooleanField(default=False)
    logout_status = models.BooleanField(default=False)

    def __str__(self):
        return self.username





        