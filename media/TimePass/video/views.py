# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from .models import User, Video


def home(request):
    all_video = User.objects.all()
    return render(request,'video/home_page.html', {'all_video': all_video})


