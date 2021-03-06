# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-05 07:06
from __future__ import unicode_literals

import app_problem.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=30)),
                ('content', models.TextField()),
                ('file', models.FileField(upload_to=app_problem.models.get_image_path)),
                ('memory_limit', models.IntegerField(null=True)),
                ('time_limit', models.IntegerField()),
                ('upload_date', models.DateField()),
                ('submit_times', models.IntegerField(default=0)),
                ('accept_times', models.IntegerField(default=0)),
                ('input_request', models.TextField()),
                ('output_request', models.TextField()),
                ('input_sample', models.TextField()),
                ('output_sample', models.TextField()),
                ('source', models.CharField(max_length=30)),
                ('level', models.CharField(max_length=30)),
                ('classify', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Submit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submit_time', models.TimeField(auto_now=True)),
                ('language', models.CharField(max_length=10)),
                ('take_time', models.IntegerField(default=0)),
                ('take_memory', models.IntegerField(default=0)),
                ('result', models.CharField(max_length=10)),
                ('code', models.TextField()),
                ('codeLength', models.CharField(max_length=10)),
                ('status', models.IntegerField(default=0)),
                ('problem_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_problem.Problem')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
