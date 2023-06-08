"""
This file defines the database models
"""

import datetime
import random
from py4web.utils.populate import FIRST_NAMES, LAST_NAMES, IUP
from .common import db, Field, auth
from pydal.validators import *


def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()

# For table 'user':
# username = the user's username
# password = the user's password
# firstName = the user's first name
# lastName = the user's last name
# category = if the user is a rider or driver
# carMake, carModel = the user's car's make and model
# numSeats = the user's car's number of seats
# location = the user's nearest ideal pickup location
# schedule = a list of the user's on-campus schedule

db.define_table('user',
                Field('user_id', 'reference auth_user'),
                Field('username'),
                Field('password'),
                Field('profilePic'),
                Field('firstName'),
                Field('lastName'),
                Field('category'),
                Field('carMake'),
                Field('carModel'),
                Field('numSeats'),
                Field('location'),
                Field('schedule')
                )

db.define_table(
    'user_schedule',
    Field('user_id', 'reference: user'),
    Field('day_of_week'),
    Field('available_time')
    )

db.commit()


locationList = ["Porter", "College 9", "Kresge", "College 10", "Stevenson",
"Merril", "Crown", "Cowell", "Nobel", "Escalona", "Downtown", "Natural Bridges", 
"WatsonVille", "Seabright", "Capitola", "Ocean st", "Soquel", "Scotts Valley"]

model = ["Ford F150", "Ford F350", "Honda Civic", "Honda Accord", "Honda CRV",
"Toyota Supra", "Toyota Corolla", "Toyota Camry", "Toyota Prius", "Subaru WRX", 
"Lambrogini", "Rolls Royce Phantom" ]

days_of_week = ["Monday", "Tuesday","Wednesday", "Thursday","Friday", "Saturday", "Sunday"]

r_times = ["9:00 am" , "10:00 am", "11:00 am", "12:00 pm", "1:00 pm", "2:00 pm","3:00 pm", "4:00 pm"]

def add_users_for_testing(num_users):
    # Test user names begin with "_".
    # Counts how many users we need to add.
    db(db.user.username.startswith("_")).delete()
    num_test_users = db(db.user.username.startswith("_")).count()
    num_new_users = num_users - num_test_users
    print("Adding", num_new_users, "users.")
    for k in range(num_test_users, num_users):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        username = "_%s%.2i" % (first_name.lower(), k)
        category = random.choice(["rider", "driver"])
        numSeats = random.randint(2,5)
        carModel = random.choice(model)
        carMake = random.randint(2000,2022)
        location = random.choice(locationList)
        user_info = dict(
            username=username,
            #email=username + "@ucsc.edu",
            firstName=first_name,
            lastName=last_name,
            password=username,  # To facilitate testing.
            category=category,
            numSeats=numSeats,
            carModel=carModel,
            carMake=carMake,
            location=location
        )
        #auth.register(user_info, send=False)
        # Adds some content for each user.
        db.user.insert(**user_info)
    users = db(db.user).select()
    for u in users:
        user_schedule = dict(
        user_id = u.id,
        day_of_week = random.choice(days_of_week),
        available_time = random.choice(r_times)  
        )
        db.user_schedule.insert(**user_schedule) 
       
       
    db.commit()
    

#adds the amount of mock users, the value can always be changed 
add_users_for_testing(6)
