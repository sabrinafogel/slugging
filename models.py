"""
This file defines the database models
"""

from .common import db, Field, auth
from pydal.validators import *

import datetime

def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None


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
                Field('id'),
                Field('username'),
                Field('password'),
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
### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later
#
# db.commit()
#
