from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User
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
            return redirect('/success')

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
        return redirect('/success')
    
def logout(request):
    request.session.clear()
    return redirect('/')

def success(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        return render(request, 'first_app/success.html')
