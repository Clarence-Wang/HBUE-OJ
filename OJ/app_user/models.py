# coding:utf-8
from __future__ import unicode_literals

from django.db import models
# Create your models here.

from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    real_name = models.CharField(max_length=20)
    student_id = models.CharField(max_length=9)
    student_class = models.CharField(max_length=30)
    ac_times = models.IntegerField(default=0)
    submit_times = models.IntegerField(default=0)
    ranking = models.IntegerField(default=0)