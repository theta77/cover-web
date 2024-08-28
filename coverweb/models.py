from django.db import models
from django.contrib.auth.models import AbstractUser
from typing import Any

# Create your models here.
class User(AbstractUser):
    idx = models.AutoField(primary_key=True)
    nick = models.CharField(max_length=20)
    info = models.CharField(max_length=200, blank=True)
    sub = models.CharField(max_length=100000, blank=True)
    video = models.CharField(max_length=100000, blank=True)

    def __str__(self):
        return self.username
    
class Video(models.Model):
    idx = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    sub = models.CharField(max_length=100)
    info = models.CharField(max_length=10000, blank=True)
    view = models.IntegerField(default=0)
    like = models.CharField(max_length=100000, blank=True)
    date = models.DateField(auto_now_add=True)
    thumbnail = models.FileField(upload_to=f'video/', blank=True)
    video = models.FileField(upload_to=f'video/', blank=True)
    genre = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.sub
    
class VideoBackUp(models.Model):
    idx = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    sub = models.CharField(max_length=100)
    info = models.CharField(max_length=10000, blank=True)
    view = models.IntegerField(default=0)
    like = models.CharField(max_length=100000, blank=True)
    date = models.DateField(auto_now_add=True)
    thumbnail = models.FileField(upload_to=f'backup/', blank=True)
    video = models.FileField(upload_to=f'backup/', blank=True)
    genre = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.sub