from django.db import models

class Hotel(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    city = models.ForeignKey()

class City(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=100)
