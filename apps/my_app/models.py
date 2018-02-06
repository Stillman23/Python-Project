from __future__ import unicode_literals
from django.db import models
from datetime import date, datetime
from time import strptime
import bcrypt
import re
Name_Regex = re.compile(r'^[A-Za-z ]+$')

# Create your models here.

class User(models.Model):
    user_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email_name = models.CharField(max_length=100, unique =True)
    password = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

class travelManager(models.Manager):
    def travelval(self, postData, id):
        errors=[]
        if len(postData['destination']) < 1 :
            errors.append("Destination field can not be empty")
        if len(postData['description']) < 1 :
            errors.append("Description field can not be empty")
        # try:
        #     str(datetime.strptime(postData["start"], "%d/%m/%Y"))
        # except ValueError:
        #     errors.append("Invalid date. Please input a date.")
        if str(date.today()) > str(postData['start']):
            errors.append("Please input a valid Date. Note: Start time can not be in the past.")
        if str(date.today()) > postData['end']:
            errors.append("Please input a valid Date. Note: End date must be in the future")
        if postData['start'] > postData['end']:
            errors.append("Travel Date From can not be in the future of Travel Date To")
        if len(errors) == 0:
            plan= Travel.objects.create(destination=postData['destination'],description=postData['description'], start=postData['start'],end=postData['end'], creator= User.objects.get(id=id))
            print "Successfully created new plan:"
            return (True, plan)
        else:
            print "Cannot input into Data"
            return (False, errors)

    def join(self, id, travel_id):
        if len(Travel.objects.filter(id=travel_id).filter(join__id=id))>0:
            return {'errors':'Oops - You already joined this'}
        else:
            joiner= User.objects.get(id=id)
            plan= self.get(id= travel_id)
            plan.join.add(joiner)
            return {}


class Travel(models.Model):
    destination = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    start= models.DateField()
    end= models.DateField()
    creator= models.ForeignKey(User, related_name= "planner")
    join= models.ManyToManyField(User, related_name="joiner") #holds on to instances of User
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = travelManager()