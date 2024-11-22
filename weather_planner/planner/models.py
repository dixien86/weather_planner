# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests
from django.core.cache import cache
from django.db import models

# Create your models here.
from django.db import models
from rest_framework.decorators import action
from rest_framework.response import Response


class Destination(models.Model):
    """
    Destination
    """
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)


class Schedule(models.Model):
    """
    Schedule
    """
    name = models.CharField(max_length=255)
    destinations = models.ManyToManyField(Destination)
    created_at = models.DateTimeField(auto_now_add=True)
    

class Weather(models.Model):
    destination = models.OneToOneField("Destination", on_delete=models.CASCADE, related_name="weather")
    temperature = models.FloatField()
    windspeed = models.FloatField()
    winddirection = models.IntegerField()
    weathercode = models.IntegerField()
    is_day = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Weather for {self.destination.name} at {self.timestamp}"
    
   
