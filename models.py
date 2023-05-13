"""
This file defines the database models
"""

from .common import db, Field, auth
from pydal.validators import *

import datetime

def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None


### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later
#
# db.commit()
#
