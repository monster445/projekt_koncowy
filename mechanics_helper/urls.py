from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from main_calendar.views import CalendarView, order, CreateUserView, LoginView, HomepageView, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^homepage/$', HomepageView.as_view(), name='homepage'),
    url(r'^create_user/$', CreateUserView.as_view(), name='create_user'),
    url(r'^calendar/$', CalendarView.as_view(), name='calendar'),
    url(r'^order/new/$', order, name='order_new'),
    url(r'^order/edit/(?P<order_id>\d+)/$', order, name='order_edit'),
]
