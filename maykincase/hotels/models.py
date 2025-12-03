from django.db import models

class City(models.Model):
    code = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Cities"

    def __str__(self):
        return f"{self.name} ({self.code})"


class Hotel(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='hotels')

    def __str__(self):
        return f"{self.name} [{self.code}]"
