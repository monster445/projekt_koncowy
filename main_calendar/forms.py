from django import forms
from main_calendar.models import CalendarOrder

class OrderForm(forms.ModelForm):
  class Meta:
    model = CalendarOrder
    widgets = {
      'start_time': forms.DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
      'end_time': forms.DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
    }
    fields = ('car','production_year','license_plate','client_name','damage_description','cost','start_time','end_time')

  def __init__(self, *args, **kwargs):
    super(OrderForm, self).__init__(*args, **kwargs)
    self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
    self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)

class CreateUserForm(forms.Form):
  username = forms.CharField(max_length=64)
  password = forms.CharField(max_length=64)
  repeat_password = forms.CharField(max_length=64)
  email = forms.CharField(max_length=128)

class LoginForm(forms.Form):
  username = forms.CharField(max_length=64)
  password = forms.CharField(max_length=64)