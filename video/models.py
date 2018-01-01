# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
# from myapplication.essay.models import Essay
# from django.contrib import admin

# Create your models here.


class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=1000)
    thumbnail = models.FileField(max_length=1000)
    video_path = models.FileField(max_length=1000)
    is_favorite = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('video:details', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class UserFeedback(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    comment = models.CharField(max_length=1000)
    like = models.PositiveSmallIntegerField(default=0)
    dislike = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return "Comment:-" + self.comment
