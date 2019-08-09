from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class CalendarOrder(models.Model):
    car = models.CharField(max_length=100)
    production_year = models.IntegerField()
    license_plate = models.CharField(max_length=20)
    client_name = models.CharField(max_length=200)
    damage_description = models.TextField(null=True)
    cost = models.IntegerField(null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    @property
    def get_html_url(self):

        url = reverse('order_edit', args=(self.id,))
        return f'<a href="{url}"> {self.car} {self.license_plate} <br> {self.client_name}</a>'