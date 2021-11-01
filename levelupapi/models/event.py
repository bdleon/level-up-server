from django.db import models

class Event(models.Model):
    game = models.IntegerField()
    description = models.TextField()