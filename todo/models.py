from django.db import models
from accounts.models import CustomUser
from django.urls import reverse

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    user_name = models.CharField(max_length=50)
    username = models.ForeignKey(CustomUser, on_delete=models.RESTRICT)
    site = models.TextField(default="Not specified")


    @property
    def get_html_url(self):
        url = reverse('todo:event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} ({self.user_name})</a>'

    @property
    def get_event_name(self):
        url = reverse('todo:event_edit', args=(self.id,))
        return f'{self.title} ({self.user_name})'


class Todo(models.Model):
    todo = models.CharField(max_length=200, null=False)
    date = models.DateField()

    def __str__(self):
        return self.todo
