from django.urls import path, re_path
from . import views

app_name = "todo"

urlpatterns = [
   
    path('', views.CalendarView.as_view(), name='calendar'),
    path('family/', views.CalendarAllView.as_view(), name='family-calendar'),
    re_path(r'^event/new/$', views.event, name='event_new'),
    re_path(r'^event/edit/(?P<event_id>\d+)/$', views.event, name='event_edit'),
    path("<int:pk>/delete/", views.EventDeleteView.as_view(), name='delete'),
    path("covid/", views.covid, name='covid'),
    path("nasa/", views.nasa, name='nasa'),
    path("trivia/", views.trivia, name='trivia'),
    path("bored/", views.bored, name='bored'),
    path("news/", views.news, name='news'),
    path("quote/", views.quote, name='quote'),
    
]