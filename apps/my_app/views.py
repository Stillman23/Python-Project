from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from .models import User, Travel


# Create your views here.
def index(request):
    return render(request, 'my_app/index.html')

def registration_process(request):
    if request.method == 'POST':
        user_name = request.POST['user_name']
        last_name = request.POST['last_name']
        email_name = request.POST['email_name']
        password = request.POST['password']

        isValid = True
        minValName = 2
        minValPass = 8

    if len(request.POST['user_name']) < minValName:
        messages.error(request, 'Name must be at least 2 characters!')
        isValid = False

    if len(request.POST['last_name']) < minValName:
        messages.error(request, 'Alias must be at least 2 characters!')
        isValid = False
    
    if len(request.POST['email_name']) < minValName:
        messages.error(request, 'Email is Required!')
        isValid = False
    
    if request.POST['email_name'] != email_name:
        messages.error(request, 'This email is already registered!')
        isValid = False
    
    if len(request.POST['password']) < minValName:
        messages.error(request, 'Password is required!')
        isValid = False
    
    if request.POST['confirm_password'] != request.POST['password']:
        messages.error(request, 'Password confirmation failed!')
        isValid = False
        
    if not isValid:
        return redirect('/')

    if request.POST['confirm_password'] == password:

        try:
            user = User.objects.create(user_name=user_name, last_name = last_name, email_name=email_name,password=password)

        except IntegrityError:

            messages.error(request, 'This Email is already registered!')
            return redirect('/')

        request.session['user_id'] = user.id
    return redirect('/travels')


def login_process(request):
    if request.method == "POST":
        email_name = request.POST['email_name']
        password = request.POST['password']
        isValid = True
        minVal = 2

    if len(request.POST['email_name']) < minVal:
        messages.error(request, "Email is required!")
        isValid = False

    if len(request.POST['password']) < minVal:
        messages.error(request, "password is required!")
        isValid = False

    try:
        User.objects.get(email_name= request.POST['email_name'], password= request.POST['password'])

    except ObjectDoesNotExist:
        messages.error(request, "email and password don't match")
        isValid = False
    else:
        messages.error(request, "YOU ARE NOW LOGGED IN!")
        
    if not isValid:
        return redirect('/')
    else:
        request.session['user_id']= (User.objects.get(email_name= request.POST['email_name'])).id
        return redirect('/travels')

def travels(request):
    if 'user_id' in request.session.keys():
        user= User.objects.get(id=request.session['user_id'])
    context={
        'user': user,
        'travels' : Travel.objects.all(),
        'others': Travel.objects.all().exclude(join__id=request.session['user_id'])
    }
    return render(request, 'my_app/travels.html', context)

def addplan(request):
    if 'user_id' not in request.session:
        return redirect ("/")
    else:
        context= {
            "user":User.objects.get(id=request.session['user_id']),
        }
        return render(request, 'my_app/addplan.html', context)
   

def logout(request):
    request.session.clear()
    return redirect('/')

def createplan(request):
    if request.method != 'POST':
        return redirect ("/addplan")
    newplan= Travel.objects.travelval(request.POST, request.session["user_id"])
    if newplan[0] == True:
        return redirect('/travels')
    else:
        for message in newplan[1]:
            messages.error(request, message)
        return redirect('/addplan')

def show(request, travel_id):
    try:
        travel= Travel.objects.get(id=travel_id)
    except Travel.DoesNotExist:
        messages.info(request,"Travel Not Found")
        return redirect('/travels')
    context={
        "travel": travel,
        "user":User.objects.get(id=request.session['user_id']),
        "others": User.objects.filter(joiner__id=travel.id).exclude(id=travel.creator.id),
    }
    return render(request, 'my_app/showdetail.html', context)

def join(request, travel_id):
    if request.method == "GET":
        messages.error(request,"What trip?")
        return redirect('/')
    joiner= Travel.objects.join(request.session["user_id"], travel_id)
    print 80 * ('*'), joiner
    if 'errors' in joiner:
        messages.error(request, joiner['errors'])
    return redirect('/travels')

def delete(request, id):
    try:
        target= Travel.objects.get(id=id)
    except Travel.DoesNotExist:
        messages.info(request,"Message Not Found")
        return redirect('/travels')
    target.delete()
    return redirect('/travels')