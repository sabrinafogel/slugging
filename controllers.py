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
from .models import get_user_email, get_time
import random

url_signer = URLSigner(session)

@action('index')
@action.uses('index.html', db, auth, url_signer, session)
def index():
    return dict(
        # COMPLETE: return here any signed URLs you need.
        my_callback_url = URL('my_callback', signer=url_signer)
    )

# driver search
@action("driver")
@action.uses(db, 'driver.html', auth, url_signer)
def driver():
    results = []

    for user in db(db.user).select().as_list():
        if user['category'] == ("driver"):
            results.append(user)

    # to get all the data needed to place markers
    markerList = [row for row in db().select(db.user.firstName, db.user.lastName, db.user.category, db.user.location)]
    
    # print to terminal for testing
    # print(markerList)

    return dict(results=results, markerList=markerList, driverURL = URL('driver'), getUserURL = URL('getUser'),
                url_signer=url_signer)

# rider search
@action("rider")
@action.uses(db, 'rider.html', auth, url_signer)
def rider():
    results = []

    for user in db(db.user).select().as_list():
        if user['category'] == ("rider"):
            results.append(user)
    
    return dict(results=results, riderURL = URL('rider'), url_signer=url_signer)

@action("profile")
@action.uses(db, 'profile.html', auth)
def profile():
    rows = db(db.auth_user.email == get_user_email() ).select().as_list()
    
    for r in rows:
       profile = db(db.user.firstName == r['first_name'] and db.user.lastName == r['last_name']).select().as_list()
       
    if len(profile) <=0:
        print("Add current user to user list")
        u_info = db(db.auth_user.email == get_user_email() ).select().first()
        assert u_info is not None
        username = "_%s%.2i" % (u_info.first_name.lower(),2)
        category = random.choice(["rider", "driver"])
        db.user.update_or_insert(firstName = u_info.first_name, lastName = u_info.last_name, username=username, category=category)
        profile = db(db.user.firstName == r['first_name'] and db.user.lastName == r['last_name']).select().as_list()
    
    schedule = db(db.schedule.user_email == get_user_email()).select()

    return dict(rows=rows, schedule=schedule, profile=profile)



@action('editProfile/<user_id:int>', method=["GET","POST"])
@action.uses(db, session, url_signer, "editProfile.html", auth)
def editProfile(user_id=None):
    assert user_id is not None 
    form = Form(db.user, record=user_id, formstyle=FormStyleBulma, csrf_session=session)
    a = db(db.user.id == user_id).select().first()
    if form.accepted:
       redirect(URL('profile'))
       
    rows = db(db.schedule.user_email == get_user_email()).select()
    
    return dict(rows=rows, account=a,form=form, user_id=user_id, url_signer=url_signer)


@action('schedule/<user_id:int>', method=["GET","POST"])
@action.uses(db, session, url_signer, "schedule.html", auth)
def schedule(user_id=None):
    assert user_id is not None 
       
    rows = db(db.schedule.user_email == get_user_email()).select()
    
    return dict(rows=rows, user_id=user_id, url_signer=url_signer)

@action('displayProfile/<id:int>', method=["GET","POST"])
@action.uses(db, "displayProfile.html", auth)
def displayProfile(id=None):
    assert id is not None
    profile = db(db.user.id == id).select().as_list()
    #form = Form(db.user, record=user_id, formstyle=FormStyleBulma, csrf_session=session)
    #if form.accepted:
    #   redirect(URL('profile'))
    #
    return dict(profile=profile)

# each message form is the id of the user you are messaging
@action('message/<id:int>')
@action.uses(db, 'message.html', auth, url_signer, auth.user, url_signer.verify())
def message(id = None):
    assert id is not None

    # get the info of the user i am messaging so that i can pass it to the message form for use
    profile = db(db.user.id == id).select().as_list()

    # rows = db(db.user.id == auth.user_id).select().as_list()
    # return dict(rows=rows)
    return dict(profile=profile, load_messages_url = URL('load_messages', signer=url_signer),
                add_messages_url = URL('add_messages', signer=url_signer),
                getUserURL = URL('getUser', signer=url_signer))

# This is our first message API function
@action("load_messages")
@action.uses(url_signer.verify(), db, auth.user)
def load_messages():
    # Retrieve the logged-in user's ID
    user_id = auth.current_user.get('id') #new

    # Get the user's username and profile picture
    # user = db.auth_user[user_id]

    # username = get_user_email() #new

    # username = auth.current_user.get('username') #new

    # comment_list = db(db.user_message).select().as_list()
    # comment_list = db(db.user_message.user_id == user_id).select().as_list()

    # get all message from logged in user and the user you are messaging
    # comment_list = db(db.user_message.user_id == user_id).select().as_list()

    # Add username and profile picture to each message
    # for comment in comment_list:
    #     comment['username'] = username#new

    # get the id of the user we are messaging
    otherUserId = request.query.get('id')
    # print(otherUserId)

    # get messages logged in user sent to person they are messaging, and vise versa
    comment_list = [row for row in db(((db.user_message.user_id == user_id) & (db.user_message.otherUserID == otherUserId)) | ((db.user_message.user_id == otherUserId) & (db.user_message.otherUserID == user_id))).select(db.user_message.user_id, db.user_message.text, db.user_message.timestamp, orderby=db.user_message.timestamp)]
    
    # this one is a placeholder, just gets any message logged in user has ever sent to anyone
    # comment_list = [row for row in db(db.user_message.user_id == user_id).select(db.user_message.user_id, db.user_message.timestamp, db.user_message.text, orderby=db.user_message.timestamp)]

    return dict(comment_list=comment_list)

@action("add_messages", method="POST")
@action.uses(url_signer.verify(), db, auth)
def add_messages():
    message = request.json.get('text')

    # Get the logged-in user's username
    # username = get_user_email() #new

    isoTime = get_time().isoformat()

    db.user_message.insert(
        user_id = auth.current_user.get('id'),  # NEW Store the user's ID instead of email
        # username=username,  # NEW Store the username
        timestamp = isoTime,
        text = message
    )
    db.commit()

@action('addSchedule', method = ["GET", "POST"])
@action.uses('addSchedule.html', db, auth)
def addSchedule():
    form = Form(db.schedule, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted: 
        redirect(URL('profile'))
    return dict(form = form)


@action('editSchedule/<schedule_id:int>', method=["GET", "POST"])
@action.uses('editSchedule.html', db, session,  auth.user, url_signer.verify(), url_signer)
def editSchedule(schedule_id = None):
    assert schedule_id is not None
    p = db.schedule[schedule_id]
    
    if p is None:
        redirect(URL('profile'))
        
    form = Form(db.schedule, record = p, csrf_session=session, formstyle=FormStyleBulma)
    
    if form.accepted:
        redirect(URL('profile'))
        
    return dict(form=form)

@action("getUser", method=["GET", "POST"])
@action.uses(db, auth.user)
def getUser():
    if request.method == 'POST':
        # get the user id being messaged

        # empty the db first, only want one temp at a time
        db.tempID.truncate()
        db.commit()

        id = request.json.get('id')
        db.tempID.insert(id=id)
        db.commit()

    id = db(db.tempID).select()
    print(id)

    return dict(id=id)

