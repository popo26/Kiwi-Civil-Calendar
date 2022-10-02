from django import forms

from django.forms import ModelForm, DateInput
from todo.models import Event

class EventForm(ModelForm):
  
  class Meta:
    model = Event
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'title':forms.TextInput(attrs={"class":'form-control'}),
      'site':forms.TextInput(attrs={"class":'form-control'}),
      'start_time': DateInput(attrs={'type': 'datetime-local', "class":'form-control'}, format='%Y-%m-%dT%H:%M'),
      'end_time': DateInput(attrs={'type': 'datetime-local', "class":'form-control'}, format='%Y-%m-%dT%H:%M'),
      'user_name':forms.HiddenInput(),
      'description':forms.Textarea(attrs={"class":'form-control', 'cols':"10"}),
      
    }
    fields = '__all__'
    labels = {"title": "Todo", 'start_time': "Start", 'end_time':"End"}

  def __init__(self, *args, **kwargs):
    super(EventForm, self).__init__(*args, **kwargs)
    # input_formats to parse HTML5 datetime-local input to datetime field
    self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
    self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)
    

        
class SearchForm(forms.Form):
  search = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':"form-control", 'placeholder':"Search Keyword"}))

  
