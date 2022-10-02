
import calendar
import datetime
import calendar
import requests
import os
from datetime import timedelta
from todo.models import Todo
from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.utils.safestring import mark_safe
from .models import *
from .utils import Calendar
from .utils2 import CalendarAll
from .forms import EventForm, SearchForm
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.template.defaulttags import register
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .templatetags.tags import reverseGeocode, tuple_cordinates
from accounts.models import CustomUser

  

app_name="todo"

NASA_API_KEY=os.getenv("NASA_API_KEY")

#To use dictionary as template variable
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


#Login/Logout counters added because request.user doesn't work outside views.py
@receiver(user_logged_in)
def on_login(sender, user, request, **kwargs):
    current_user = request.user
    current_user.login_status = True
    current_user.save()
   
    if current_user.logout_status == True:
        current_user.logout_status = False
        current_user.save()
 
    
@receiver(user_logged_out)
def on_logout(sender, user, request, **kwargs):
    current_user = request.user
    current_user.logout_status = True
    current_user.login_status = False
    current_user.save()

    

class CalendarView(LoginRequiredMixin, generic.ListView):
    model = Event
    template_name = 'todo/todo.html'
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True, user=self.request.user)
        now = datetime.now()
        user_session_id = self.request.session['_auth_user_id']
        user = CustomUser.objects.get(id=user_session_id)
        todos = Event.objects.filter(
            start_time__year=now.year, 
            start_time__month=now.month, 
            start_time__day=now.strftime('%d'), 
            username_id = user_session_id,
            )
        
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        context['todos'] = todos
        context['current_user'] = user
  
        if self.request.method == "POST":
            todo = self.request.POST.get['delete-todo']
            delete_todo = Event.object.get(id=todo.id)
            delete_todo.delete()
        
        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

class CalendarAllView(LoginRequiredMixin, generic.ListView):
    model = Event
    template_name = 'todo/family.html'
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = CalendarAll(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        now = datetime.now()
        # current_user=self.request.user
        # name=current_user.username
        todos = Event.objects.filter(
            start_time__year=now.year, 
            start_time__month=now.month, 
            start_time__day=now.strftime('%d')
            )
        
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        context['todos'] = todos
        
        return context

@login_required
def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()

    form = EventForm(request.POST or None, instance=instance, initial={"user_name":request.user.username})
    if request.POST and form.is_valid():
        current_user = request.user
        form.user_name = current_user.username
        form.save()
        return HttpResponseRedirect(reverse('todo:calendar'))
    return render(request, 'todo/event.html', {'form': form})

class EventDeleteView(LoginRequiredMixin,DeleteView):
    model = Event
    success_url = reverse_lazy("todo:calendar")

@login_required
def covid(request):
    today = datetime.today()
    y3 = today - timedelta(days=3)
    two_days_before_yesterday = y3.strftime('%Y-%m-%d')
    y2 = today - timedelta(days=2)
    day_before_yesterday = y2.strftime('%Y-%m-%d')
    # When testing locally cordinates defaults to Auckland, NZ
    country = reverseGeocode(coordinates=tuple_cordinates()).lower()
    country_name = country.replace(" ", "-")
   
    covid_url = f"https://api.covid19api.com/total/country/{country_name}/status/confirmed?from={two_days_before_yesterday}T00:00:00Z&to={day_before_yesterday}T00:00:00Z"
    response=requests.get(covid_url)
    data=response.json()
    
    two_days_before_yesterday_cases = int(data[1]['Cases'])
    day_before_yesterday_cases = int(data[0]['Cases'])
    confirmed_cases_till_now = two_days_before_yesterday_cases - day_before_yesterday_cases

    two_b_yesterday = y3.strftime('%d %b')
    day_b_yesterday = y2.strftime('%d %b')

    context = {
        'country_name': country,
        "confirmed_cases_till_now" : confirmed_cases_till_now,
        "two_days_before_yesterday": two_b_yesterday,
        "day_before_yesterday": day_b_yesterday,
    }
    
    return render(request, 'todo/covid.html', context=context)
    

@login_required
def nasa(request):
    nasa_apod_url=f'https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}'
    response=requests.get(nasa_apod_url)
    data=response.json()

    date = data["date"]
    title = data['title']
    explanation = data['explanation']
    img = data["url"]

    context = {
        "date": date,
        "title": title,
        "explanation": explanation,
        'img':img,
    }

    return render(request, 'todo/nasa.html', context=context)

@login_required
def trivia(request):
    trivia_url = "https://opentdb.com/api.php?amount=1&category=9&difficulty=medium&type=boolean"
    response = requests.get(trivia_url)
    data=response.json()

    results = data['results'][0]

    question = results['question']
    answer = results['correct_answer']

    context = {
        'question':question,
        'answer':answer,
    }
 
    return render(request, 'todo/trivia.html', context=context)

@login_required
def bored(request):
    bored_url = "http://www.boredapi.com/api/activity"
    response=requests.get(bored_url)
    data=response.json()

    activity = data['activity']
    return render(request, 'todo/bored.html', {"activity":activity})

@login_required
def news(request):
    form = SearchForm()
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            url = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/Search/ImageSearchAPI"
            search = request.POST.get('search')
            querystring = {"q":f"{search}","pageNumber":"1","pageSize":"10","autoCorrect":"true"}

            headers = {
                "X-RapidAPI-Key": os.getenv("RAPID_API_KEY"),
                "X-RapidAPI-Host": os.getenv('RAPIDAPI_HOST'),
            }

            response = requests.request("GET", url, headers=headers, params=querystring)

            data = response.json()
            all_data = data['value']
            results = []

            for item in all_data:
                results.append(item)

            context = {
                "results": results,
                'form':form,
            }

            return render(request, 'todo/news.html', context=context)
        else:
            print("FAIL!")

    return render(request, 'todo/news.html', {"form":form})

@login_required
def quote(request):
    quote_url = "https://zenquotes.io/api/random"
    response=requests.get(quote_url)
    data=response.json()

    quote = data[0]['q']
    author = data[0]['a']

    context = {
        "quote":quote,
        "author":author,
    }
    return render(request, 'todo/quote.html', context=context)



 