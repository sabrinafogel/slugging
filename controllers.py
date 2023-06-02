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

from py4web import action, request, abort, redirect, URL,Field
from yatl.helpers import A
from py4web.utils.form import Form, FormStyleBulma
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
def driver():
    results = []

    for user in db(db.user).select().as_list():
        if user['category'] == ("driver"):
            results.append(user)

    return dict(results=results)

# rider search
@action("rider")
@action.uses(db, 'rider.html')
def rider():
    results = []

    for user in db(db.user).select().as_list():
        if user['category'] == ("rider"):
            results.append(user)
    
    return dict(results=results)

@action("profile")
@action.uses(db, auth, 'profile.html')
def profile():
    rows = db(db.auth_user.email == get_user_email() ).select().as_list()
    return dict(rows=rows)
  

@action('editProfile/<user_id:int>', method=["GET","POST"])
@action.uses(db,auth, session, url_signer, "editProfile.html")
def editProfile(user_id=None):
    assert user_id is not None 
    form = Form(db.auth_user, record=user_id, formstyle=FormStyleBulma, csrf_session=session)
    if form.accepted:
       redirect(URL('profile'))
    #
    return dict(form=form, user_id=user_id)


@action('displayProfile/<id:int>', method=["GET","POST"])
@action.uses(db,"displayProfile.html")
def displayProfile(id=None):
    assert id is not None
    profile = db(db.user.id == id).select().as_list()
    print(profile)
    #form = Form(db.user, record=user_id, formstyle=FormStyleBulma, csrf_session=session)
    #if form.accepted:
    #   redirect(URL('profile'))
    #
    return dict(profile=profile)

@action('addSchedule/<user_id:int>' , method=["GET","POST"])
@action.uses(db,"addSchedule.html",session,auth)
def addSchedule(user_id=None):
    assert user_id is not None
    #get schedule for specific user 
        #s = db(db.schedule.user_id = user_id)
    form = Form([Field('day_of_week'), Field('available')], csrf_session=session,formstyle=FormStyleBulma)
    if form.accepted:
        #user_info = db(db.user.username == get_username()).select().first()
        #assert user_info is not None
        #db.schedule.insert(user_id=user_id, day_of_week=form.vars["Day of the Week"], available=form.vars["Time Available"])
        redirect(URL('editProfile',user_id))
        
    return dict(form=form)
    
@action('editSchedule/<user_id:int>' , method=["GET","POST"])
@action.uses(db,"editSchedule.html",session,auth)
def editSchedule(user_id=None):
    assert user_id is not None
    return dict()

@action("message")
@action.uses(db, 'message.html')
def profile():
    # rows = db(db.user.id == auth.user_id).select().as_list()
    # return dict(rows=rows)
    return dict()
