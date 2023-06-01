"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from .models import get_user_email

url_signer = URLSigner(session)

@action('index')
@action.uses('index.html', db, auth, url_signer)
def index():
    return dict(
        # COMPLETE: return here any signed URLs you need.
        my_callback_url = URL('my_callback', signer=url_signer),
    )

# driver search
@action("driver")
@action.uses(db, 'driver.html')
def edit_phones():


    return dict()

# rider search
@action("rider")
@action.uses(db, 'rider.html')
def edit_phones():


    return dict()

@action("profile")
@action.uses(db, 'profile.html')
def profile():
    # rows = db(db.user.id == auth.user_id).select().as_list()
    # return dict(rows=rows)
    return dict()

@action('editProfile', method=["GET","POST"])
@action.uses(db,"editProfile.html")
def editProfile():
    
    #form = Form(db.user, record=user_id, formstyle=FormStyleBulma, csrf_session=session)
    #if form.accepted:
    #   redirect(URL('profile'))
    #
    return dict()

@action('displayProfile', method=["GET","POST"])
@action.uses(db,"displayProfile.html")
def displayProfile():
    
    #form = Form(db.user, record=user_id, formstyle=FormStyleBulma, csrf_session=session)
    #if form.accepted:
    #   redirect(URL('profile'))
    #
    return dict()

@action('addSchedule', method=["GET","POST"])
@action.uses(db,"addSchedule.html",session,auth)
def addSchedule():
    # assert user_id is not None
    #get schedule for specific user 
        #s = db(db.schedule.user_id = user_id)
    form = Form([Field('day_of_week'), Field('available')], csrf_session=session,formstyle=FormStyleBulma)
    if form.accepted:
        #user_info = db(db.user.username == get_username()).select().first()
        #assert user_info is not None
        #db.schedule.insert(user_id=user_id, day_of_wwek=form.vars["Day of the Week"], available=form.vars["Time Available"])
        redirect(URL('editProfile'))
        
    return dict(form=form)
    
@action('editSchedule', method=["GET","POST"])
@action.uses(db,"editSchedule.html")
def editSchedule():
    
    return dict()

@action("message")
@action.uses(db, 'message.html')
def profile():
    # rows = db(db.user.id == auth.user_id).select().as_list()
    # return dict(rows=rows)
    return dict()