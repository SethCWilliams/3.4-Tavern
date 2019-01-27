from django.db import models
from django.utils import timezone

class Lunch(models.Model):
    nickname = models.CharField(max_length=255)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nickname


class Location(models.Model):
    lunch = models.ForeignKey(Lunch, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default='generic')
    description = models.TextField(default=True)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.title
