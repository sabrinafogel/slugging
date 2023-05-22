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

from py4web import action, request, abort, redirect, URL, Field
from py4web.utils.form import Form, FormStyleBulma
from py4web.utils.url_signer import URLSigner
from .models import get_user_email

from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash, signed_url


@action("index")
@action.uses("index.html", auth, T)
def index():
    user = auth.get_user()
    message = T("Hello {first_name}".format(**user) if user else "Hello")
    actions = {"allowed_actions": auth.param.allowed_actions}
    return dict(message=message, actions=actions)

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
    
@action('editSchedule', method=["GET","POST"])
@action.uses(db,"editSchedule.html")
def editProfile():
    
    return dict()
    
@action('addProfile', method=["GET","POST"])
@action.uses(db,"addSchedule.html")
def editProfile():
    
    return dict()

    
