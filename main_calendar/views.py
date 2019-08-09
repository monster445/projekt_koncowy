from main_calendar.models import CalendarOrder
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe
from django.views import generic, View
from datetime import datetime, date, timedelta
from main_calendar.calendar import Calendar
from main_calendar.forms import OrderForm, CreateUserForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import calendar
from django.contrib.auth.mixins import LoginRequiredMixin


class CalendarView(LoginRequiredMixin, generic.ListView):
    login_url = '/login/'
    model = CalendarOrder
    template_name = 'calendar.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


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



def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()



def order(request, order_id=None):

    if order_id:
        instance = get_object_or_404(CalendarOrder, pk=order_id)
    else:
        instance = CalendarOrder()

    form = OrderForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('calendar'))
    return render(request, 'calendar_order.html', {'form': form})



class CreateUserView(View):
    def get(self, request):

        form = CreateUserForm()

        return render(request, 'create_user.html', {'form':form})

    def post(self, request):

        form = CreateUserForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            email = form.cleaned_data['email']

            if not "@" in email or password != repeat_password:
                return redirect('/create_user/')
            else:
                User.objects.create_user(username, email, password)
                return redirect('/login/')

class LoginView(View):
    def get(self, request):

        form = LoginForm()

        return render(request, 'login_form.html', {'form':form})

    def post(self, request):

        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user=user)
                return redirect('/homepage/')
            else:
                return redirect('/login/')


class HomepageView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):

        return render(request, 'homepage.html', {'logged_user':request.user})

def logout_view(request):
    logout(request)
    return redirect('/login/')

def get_user(request):
    logged_user = request.user
    return logged_user

