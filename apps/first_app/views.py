from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt
from datetime import date

def index(request):
    return render(request, 'first_app/index.html')


def process(request):
    # print(request.POST.get('action'))
    # using this if statement as there are two forms in the HTML file.
    # The submit button is hidden so you're able to use request.POST.get for register and login
    if request.POST.get('action') == 'registration':
        errors = User.objects.register_validator(request.POST)
        # check if there are any error messages to send
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            hash_userpw = bcrypt.hashpw(str(request.POST['password']).encode(), bcrypt.gensalt())
            # print(hash)
            # add the user into the DB
            user = User.objects.create()
            user.fname = request.POST['fname']
            user.lname = request.POST['lname']
            user.email = request.POST['email']
            user.b_date = request.POST['birthDate']
            user.password = hash_userpw
            user.save()
            # get the email info from the user
            email = request.POST['email']
            # search the fname in the DB where the email == email from the user (given from the form)
            # then you can check with email address belongs to which user firstname!!
            # at the end .fname gives you just the fname cell from the DB instead the whole user info
            user1 = User.objects.get(email = email)
            request.session['id'] = user1.id
            request.session['fname'] = user1.fname
            return redirect('/dashboard')

    if request.POST.get('action') == 'login':
        errors = User.objects.login_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        email = request.POST['email']
        user1 = User.objects.get(email = email)
        request.session['id'] = user1.id
        request.session['fname'] = user1.fname
        return redirect('/dashboard')
    
def logout(request):
    request.session.clear()
    return redirect('/')

def dashboard(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        this_user = User.objects.filter(id = request.session['id'])
        Trip.objects.filter(passengers = this_user)
        context = {
            'trips': Trip.objects.all().exclude(passengers = this_user),
            'my_trips': Trip.objects.filter(created_by = this_user),
            'joined_trips': Trip.objects.filter(passengers = this_user)
        }
        return render(request, 'first_app/dashboard.html', context)

def add_trip(request):
    return render(request, 'first_app/add_trip.html')

def adding(request):
    if request.method == 'POST':
        errors = Trip.objects.trip_validator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return render(request, 'first_app/add_trip.html')
        else:
            this_user = User.objects.get(id = request.session['id'])
            add_trip = Trip.objects.create(
                destination = request.POST['destination'],
                description = request.POST['desc'],
                depature = request.POST['depature'],
                arrival = request.POST['arrival'],
                travel_plan = request.POST['plans'],
                created_by = this_user)
        return redirect('/dashboard')

def back(request):
    return redirect('/dashboard')

def show_trip(request, trip_id):
    this_trip = Trip (id = trip_id)
    context = {
        'trips': Trip.objects.get(id = trip_id),
        'passengers': this_trip.passengers.all()
    }
    return render(request, 'first_app/show_trip.html', context)

def join(request, trip_id):
    this_user = User.objects.get(id = request.session['id'])
    add_to_travel_list = Trip.objects.get(id = trip_id)
    this_user.travel_buddy.add(add_to_travel_list)
    return redirect('/dashboard')

def cancel(request, trip_id):
    this_trip = Trip.objects.get(id = trip_id)
    user = User.objects.get(id = request.session['id'])
    user.travel_buddy.remove(this_trip)
    return redirect('/dashboard')

def delete(request, trip_id):
    delete_trip = Trip.objects.get(id = trip_id)
    delete_trip.delete()
    return redirect('/dashboard')

# def join(request, trip_id):
#     this_user = User.objects.get(id = request.session['id'])
#     add_to_travel_list = Trip.objects.get(id = trip_id)
#     this_user.travel_buddy.add(add_to_travel_list)
#     return redirect('/dashboard')

