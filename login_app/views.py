from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt
# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "POST":
        errors = User.objects.register_validator(request.POST)
        if len(errors):
            for key, value in errors.items(): 
                messages.error(request, value)
            return redirect('/')
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hashed_pw
        )
        request.session['user_id'] = user.id
        request.session['greeting'] = user.first_name
        return redirect('/dashboard')

def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            user = User.objects.get(email=request.POST['email'])
            request.session['user_id'] = user.id
            request.session['greeting'] = user.first_name
            return redirect('/dashboard')

def dashboard(request):
    if 'user_id' not in request.session:
        return redirect("/")
    user = User.objects.get(id = request.session['user_id'])
    context = {
		"user": user,
		"user_trips":Trip.objects.filter(creator = user),
        "joined_trips" : Trip.objects.filter(joined=user),
		"other_trips": Trip.objects.all().exclude(creator=user).exclude(joined=user),
	}
    return render(request,"trips.html",context)

def new(request):
    if 'user_id' not in request.session:
        return redirect("/")
    context = {
        "user": User.objects.get(id=request.session['user_id']),
    }
    return render(request,"newtrip.html",context)

def create(request):
    if request.method == "POST":
        errors = Trip.objects.trip_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/trips/new")
        Trip.objects.create(
            destination =request.POST['destination'],
            start_date = request.POST['start_date'],
            end_date = request.POST['end_date'],
            plan=request.POST['plan'],
            creator=User.objects.get(id=request.session['user_id'])
        )
    return redirect("/dashboard")

def show(request, id):
    context={
        'trip':Trip.objects.get(id=id)
    }
    return render(request,"display.html",context)

def edit(request, id):
    context={
        'trip':Trip.objects.get(id=id)
    }
    return render(request,"edit.html",context)

def update(request, id):
    if request.method == "POST":
        errors = Trip.objects.trip_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f"/trips/edit/{id}")
        else:
            trip=Trip.objects.get(id=id)
            trip.destination=request.POST['destination']
            trip.plan=request.POST['plan']
            trip.save()
    return redirect('/dashboard')

def join(request, id):
    user = User.objects.get(id=request.session['user_id'])
    trip = Trip.objects.get(id=id)
    user.joined_trips.add(trip)
    return redirect("/dashboard")

def delete(request, id):
    trip = Trip.objects.get(id=id)
    trip.delete()
    return redirect("/dashboard")

def cancel(request, id):
    user = User.objects.get(id=request.session['user_id'])
    trip = Trip.objects.get(id=id)
    user.joined_trips.remove(trip)
    return redirect("/dashboard")

def logout(request):
    request.session.flush()
    return redirect('/')