from __future__ import unicode_literals

import os
import zipfile

import time
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver

from judge import config


def get_image_path(instance, filename):
    return os.path.join(str(instance.id), filename)


class Problem(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=30)
    content = models.TextField()
    file = models.FileField(upload_to=get_image_path)
    memory_limit = models.IntegerField(null=True)
    time_limit = models.IntegerField()
    upload_date = models.DateField()
    submit_times = models.IntegerField(default=0)
    accept_times = models.IntegerField(default=0)
    input_request = models.TextField()
    output_request = models.TextField()
    input_sample = models.TextField()
    output_sample = models.TextField()
    source = models.CharField(max_length=30)
    level = models.CharField(max_length=30)
    classify = models.CharField(max_length=30)

@receiver(post_save, sender=Problem, dispatch_uid="unzip")
def unzip(sender, instance, **kwargs):
    try:
        data_dir = os.path.join('data_dir', '%s'%instance.id)
    except:
        pass
    file_list = os.listdir(data_dir)
    for file_name in file_list:
        if os.path.splitext(file_name)[1] == '.zip':
            zip_path = os.path.join('data_dir', '%s' % instance.id, file_name)
            file_zip = zipfile.ZipFile(zip_path, 'r')
            for file in file_zip.namelist():
                file_zip.extract(file, data_dir)
            file_zip.close()
            os.remove(zip_path)


class Submit(models.Model):
    problem_id = models.ForeignKey(Problem)
    user_id = models.ForeignKey(User)
    submit_time = models.TimeField(auto_now=True)
    language = models.CharField(max_length=10)
    take_time = models.IntegerField(default=0)
    take_memory = models.IntegerField(default=0)
    result = models.CharField(max_length=10)
    code = models.TextField()
    codeLength = models.CharField(max_length=10)
    status = models.IntegerField(default=0)