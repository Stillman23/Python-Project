# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-08-24 22:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Travel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=255)),
                ('start', models.DateField()),
                ('end', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email_name', models.CharField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='travel',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='planner', to='my_app.User'),
        ),
        migrations.AddField(
            model_name='travel',
            name='join',
            field=models.ManyToManyField(related_name='joiner', to='my_app.User'),
        ),
    ]
