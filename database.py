__author__ = 'sm'

from google.appengine.ext import ndb
from google.appengine.ext import blobstore

class imagedata(ndb.Model):
     user_id = ndb.StringProperty()
     blob_key= ndb.BlobKeyProperty()
     comment_id = ndb.StringProperty()
     task_id=ndb.StringProperty()
     date = ndb.DateTimeProperty(auto_now_add=True)
     url = ndb.StringProperty()
     name = ndb.StringProperty()
     position=ndb.StringProperty()

class subscribe(ndb.Model):
    commontask_id=ndb.IntegerProperty()
    user_id=ndb.StringProperty()
    overdue=ndb.IntegerProperty()
    finished=ndb.IntegerProperty()
    remind=ndb.StringProperty()

class commontask(ndb.Model):
    task_id = ndb.IntegerProperty()
    creator=ndb.StringProperty()
    numofmember = ndb.IntegerProperty()
    last_update = ndb.StringProperty()
    task_name = ndb.StringProperty()
    create_time = ndb.DateTimeProperty(auto_now_add=True)
    location=ndb.StringProperty()
    due=ndb.StringProperty()
    description=ndb.StringProperty()
    finished=ndb.IntegerProperty()

class privatetask(ndb.Model):
    task_id = ndb.IntegerProperty()
    creator=ndb.StringProperty()
    due=ndb.StringProperty()
    task_name = ndb.StringProperty()
    create_time = ndb.DateTimeProperty(auto_now_add=True)
    location=ndb.StringProperty()
    description=ndb.StringProperty()
    finished=ndb.IntegerProperty()
    overdue=ndb.IntegerProperty()
    remind=ndb.StringProperty()

class comment(ndb.Model):
    task_id=ndb.IntegerProperty()
    comment_id = ndb.IntegerProperty()
    creator=ndb.StringProperty()
    comment_content = ndb.StringProperty()
    create_time = ndb.DateTimeProperty(auto_now_add=True)

class reply(ndb.Model):
    task_id=ndb.IntegerProperty()
    comment_id = ndb.IntegerProperty()
    reply_id = ndb.IntegerProperty()
    creator=ndb.StringProperty()
    reply_content = ndb.StringProperty()
    create_time = ndb.DateTimeProperty(auto_now_add=True)
    replyto=ndb.StringProperty()

class setting(ndb.Model):
    email_notification = ndb.IntegerProperty()

    email_visible = ndb.IntegerProperty()
    email=ndb.StringProperty()

    user_id=ndb.StringProperty()
    profileurl=ndb.StringProperty()

    gender=ndb.StringProperty()
    gender_visible=ndb.IntegerProperty()
    dob=ndb.StringProperty()
    dob_visible=ndb.IntegerProperty()

class replyremind(ndb.Model):
    sender=ndb.StringProperty()
    receiver=ndb.StringProperty()
    taskid=ndb.IntegerProperty()
    groupposition=ndb.IntegerProperty()


