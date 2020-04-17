from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

class ups_user(AbstractUser):
    user_name = models.CharField(max_length = 50, verbose_name = 'Your Name')

class ups_package(models.Model):
    package_id = models.IntegerField()
    x = models.IntegerField(default = 0)
    y = models.IntegerField(default = 0)
    owner = models.CharField(max_length = 50)
    status = models.CharField(max_length = 50)
    product_name = models.CharField(max_length = 50)
    truck_id = models.IntegerField()
    def get_absolute_url(self):
        return reverse('upsapp:detail', kwargs={'pk': self.pk})

class ups_truck(models.Model):
    truck_id = models.IntegerField()
    status = models.CharField(max_length = 50)