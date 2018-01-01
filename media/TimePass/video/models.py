from __future__ import unicode_literals

from django.db import models


class User(models.Model):
    user_name = models.CharField(max_length=250)
    email = models.CharField(max_length=300)
    password = models.CharField(max_length=300)

    def __str__(self):
        return self.user_name


class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    Description = models.CharField(max_length=1000)
    thumbnail = models.CharField(max_length=2000)
    video = models.CharField(max_length=2000)

    def __str__(self):
        return self.title