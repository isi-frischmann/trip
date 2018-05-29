from __future__ import unicode_literals
from django.db import models
from datetime import date 
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        # set variable today to today too check the birthdate
        today = str(date.today())
        print(today)

        if len(postData['fname']) < 2:
            errors['fname'] = 'First name needs to have more then 2 characters'
        
        if len(postData['lname']) < 2:
            errors['lname'] = 'Last name is too short. Needs to have at least two characters'

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Email needs to be a propper email address'
        
        # Check if email already exist!!!!
        # use .email to check the email cell in the DB!!!
        user1 = User.objects.filter(email = postData['email'])
        if len(user1):
            errors['email_exist'] = 'Use different email address'

        # if User.objects.get(email = postData['email']).email:
            
        
        # if len(postData['email']) > 1:
        #     user_email = User.objects.all()
        #     if user_email == postData['email']:
        #         errors['email_exist'] = 'Use different email address'


        if str(postData['birthDate']) >= today:
                errors['bdate'] = 'Invalid birthdate - please provide valid birthdate'

        if len(postData['password']) < 8:
            errors['password'] = 'Password needs to have more then eigth characters'
        
        if postData['password'] != postData['c_pw']:
            errors['c_pw'] = 'Confirmation Password needs to match your Password'
        return errors

    def login_validator(self, postData):
        errors = {}

        # check if email matches regex requirements
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Invalid email address'
         
        # check if email is greater then 0. And compare with the len of the user mail addresses stored in the DB.
        user1 = User.objects.filter(email = postData['email'])
        if len(user1):
            # get all users with the email address and check
            # check if password matches the bcrypt password in the DB. don't forget variable.encode()) != True
            if bcrypt.checkpw(postData['password'].encode(), user1[0].password.encode()) != True:
                errors['password'] = 'Password is not correct'
        else: 
            errors['email_not_exists'] = 'No email address found you need to register first'
        return errors

class TripManager(models.Manager):
    def trip_validator(self, postData):
        errors = {}
        pass
        # if len(postData['fname']) < 2:
        #     errors['fname'] =

class User(models.Model):
    fname = models.CharField(max_length = 40)
    lname = models.CharField(max_length = 40)
    email = models.CharField(max_length = 40)
    b_date = models.CharField(max_length = 10)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()

    def __repr__(self):
        return '<Object User: {} {} {} {} {}>'.format(self.fname, self.lname, self.email, self.b_date, self.password)

class Trip(models.Model):
    destination = models.CharField(max_length = 40)
    description = models.TextField()
    depature = models.DateTimeField()
    arrival = models.DateTimeField()
    travel_plan = models.TextField()
    created_by = models.ForeignKey(User, related_name = 'created_by')
    passengers = models.ManyToManyField(User, related_name = 'travel_buddy')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = TripManager()

    def __repr__(self):
        return '<Object Trip: {} {} {} {} {} {}>'.format(self.destination, self.description, self.depature, self.arrival, self.travel_plan)