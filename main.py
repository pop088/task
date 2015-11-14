import webapp2
from google.appengine.api import users, files, images
from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers
import time
import json
import database

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Wo ai Baobao~~~\n')

class createprivatetask(webapp2.RequestHandler):
    def post(self):

        # position=self.request.params['latitude']+"%"+self.request.params['longitude']+")"

        taskname=self.request.params['taskname']
        creator=self.request.params['creator']
        due=self.request.param['due']
        location=self.request.param['location']
        description=self.request.param['description']
        taskid=hash(taskname)

        task=database.privatetask(task_name=taskname,creator=creator,due=due,locaton=location,description=description,task_id=taskid)

        task.put()

class updateprivatetask(webapp2.RequestHandler):
    def post(self):

        taskid = self.request.get('taskid')

        task_query = database.privatetask.query(database.privatetask.task_id == taskid)
        tasks=task_query.fetch()

        for task in tasks:
            task.taskname=self.request.params['taskname']
            task.due=self.request.param['due']
            task.location=self.request.param['location']
            task.description=self.request.param['description']
            task.put()

class deleteprivatetask(webapp2.RequestHandler):
    def post(self):

        taskid = self.request.get('taskid')

        task_query = database.privatetask.query(database.privatetask.task_id == taskid)
        tasks=task_query.fetch()

        for task in tasks:
            task.key.delete()

class createcommontask(webapp2.RequestHandler):
    def post(self):

        # position=self.request.params['latitude']+"%"+self.request.params['longitude']+")"

        taskname=self.request.params['taskname']
        creator=self.request.params['creator']
        due=self.request.param['due']
        location=self.request.param['location']
        description=self.request.param['description']
        taskid=hash(taskname)

        task=database.privatetask(task_name=taskname,creator=creator,due=due,locaton=location,description=description,task_id=taskid,numofmember=1)

        task.put()

class updatecommontask(webapp2.RequestHandler):
    def post(self):

        taskid = self.request.get('taskid')

        task_query = database.commontask.query(database.commontask.task_id == taskid)
        tasks=task_query.fetch()

        for task in tasks:
            task.taskname=self.request.params['taskname']
            task.due=self.request.param['due']
            task.location=self.request.param['location']
            task.description=self.request.param['description']
            task.put()

class deletecommontask(webapp2.RequestHandler):
    def post(self):

        taskid = self.request.get('taskid')

        task_query = database.commontask.query(database.commontask.task_id == taskid)
        tasks=task_query.fetch()

        for task in tasks:
            task.key.delete()

class createcomment(webapp2.RequestHandler):
    def post(self):

        # position=self.request.params['latitude']+"%"+self.request.params['longitude']+")"


        creator=self.request.params['creator']
        content=self.request.params['content']
        taskid=self.request.param['taskid']
        commentid=hash(content)

        comment=database.comment(task_id=taskid,creator=creator,comment_content=content,comment_id=commentid)

        comment.put()

class createreply(webapp2.RequestHandler):
    def post(self):

        # position=self.request.params['latitude']+"%"+self.request.params['longitude']+")"

        creator=self.request.params['creator']
        content=self.request.params['content']
        commentid=self.request.param['commentid']
        replyid=hash(content)

        reply=database.reply(reply_id=replyid,creator=creator,reply_content=content,comment_id=commentid)

        reply.put()

class viewsinglecommontask(webapp2.RequestHandler):
    def get(self):
        taskid = self.request.get('taskid')

        task_query = database.commontask.query(database.commontask.task_id == taskid)
        tasks=task_query.fetch()

        for task in tasks:
            taskname=task.task_name
            creator=task.creator
            due=task.due
            location=task.location
            description=task.description
            create_time=task.create_time
            numofmember=task.numofmember

# get task

        comment_query = database.comment.query(ndb.AND(
            database.comment.task_id == taskid,database.comment.create_time!=None)).order(database.comment.create_time)
        comments=comment_query.fetch()

        comment_content=[]
        comment_id=[]
        commentcreate_time=[]
        commentcreator=[]

        for comment in comments:
            comment_content.append(comment.comment_content)
            comment_id.append(comment.comment_id)
            commentcreate_time.append(comment.create_time)
            commentcreator.append(comment.creator)
#get comment

        reply_query = database.reply.query(ndb.AND(
            database.reply.comment_id in comment_id,database.reply.create_time!=None)).order(database.reply.create_time)
        replys=reply_query.fetch()

        reply_content=[]
        replycomment_id=[]
        replycreate_time=[]
        replycreator=[]

        for reply in replys:
            reply_content.append(reply.comment_content)
            replycomment_id.append(reply.comment_id)
            replycreate_time.append(reply.create_time)
            replycreator.append(reply.creator)

# get replys


        taskjson = {'taskname':taskname,'creator':creator,'due':due,'location':location,'description':description,'create_time':create_time,'numofmember':numofmember}
        jsonObj1 = json.dumps(taskjson, sort_keys=True,indent=4, separators=(',', ': '))
        self.response.write(jsonObj1)

        commentjson = {'comment_content':comment_content,'comment_id':comment_id,'commentcreate_time':commentcreate_time,'commentcreator':commentcreator}
        jsonObj2 = json.dumps(commentjson, sort_keys=True,indent=4, separators=(',', ': '))
        self.response.write(jsonObj2)

        replyjson = {'reply_content':reply_content,' replycomment_id': replycomment_id,'replycreate_time':replycreate_time,'replycreator':replycreator}
        jsonObj3 = json.dumps(replyjson, sort_keys=True,indent=4, separators=(',', ': '))
        self.response.write(jsonObj3)

class viewsingleprivatetask(webapp2.RequestHandler):
    def get(self):
        taskid = self.request.get('taskid')

        task_query = database.privatetask.query(database.commontask.task_id == taskid)
        tasks=task_query.fetch()

        for task in tasks:
            taskname=task.task_name
            creator=task.creator
            due=task.due
            location=task.location
            description=task.description
            create_time=task.create_time

        dictPassed = {'taskname':taskname,'creator':creator,'due':due,'location':location,'description':description,'create_time':create_time}
        jsonObj = json.dumps(dictPassed, sort_keys=True,indent=4, separators=(',', ': '))
        self.response.write(jsonObj)

class viewmytask(webapp2.RequestHandler):
    def get(self):
        user_id = self.request.get('userid')

        privatetask_query = database.privatetask.query(database.commontask.creator == user_id)
        privatetasks=privatetask_query.fetch()

        for task in privatetasks:
            pritaskname=task.task_name
            pricreator=task.creator
            pridue=task.due
            prilocation=task.location
            pridescription=task.description
            pricreate_time=task.create_time

        pri = {'pritaskname':pritaskname,'pricreator':pricreator,'pridue':pridue,'prilocation':prilocation,'pridescription':pridescription,'pricreate_time':pricreate_time}
        jsonObj1 = json.dumps(pri, sort_keys=True,indent=4, separators=(',', ': '))
        self.response.write(jsonObj1)

        commontask_query = database.commontask.query(database.commontask.creator == user_id)
        commontasks=commontask_query.fetch()

        for task in commontasks:
            taskname=task.task_name
            creator=task.creator
            due=task.due
            location=task.location
            description=task.description
            create_time=task.create_time
            numofmember=task.numofmember

        commonjson = {'taskname':taskname,'creator':creator,'due':due,'location':location,'description':description,'create_time':create_time,'numofmember':numofmember}
        jsonObj2 = json.dumps(commonjson, sort_keys=True,indent=4, separators=(',', ': '))
        self.response.write(jsonObj2)

class viewallcommontask(webapp2.RequestHandler):
    def get(self):
        task_query = database.commontask.query()
        tasks=task_query.fetch()

        for task in tasks:
            taskname=task.task_name
            creator=task.creator
            due=task.due
            location=task.location
            description=task.description
            create_time=task.create_time
            numofmember=task.numofmember

        taskjson = {'taskname':taskname,'creator':creator,'due':due,'location':location,'description':description,'create_time':create_time,'numofmember':numofmember}
        jsonObj1 = json.dumps(taskjson, sort_keys=True,indent=4, separators=(',', ': '))
        self.response.write(jsonObj1)


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/createprivatetask',createprivatetask),
    ('/createcommontask', createcommontask),
    ('/createcomment', createcomment),
    ('/viewsinglecommontask', viewsinglecommontask),
    ('/viewsingleprivatetask', viewsingleprivatetask),
    ('/viewmytask', viewmytask),
    ('/viewallcommontask', viewallcommontask),
    ('/updateprivatetask', updateprivatetask),
    ('/updatecommontask', updatecommontask),
    ('/deleteprivatetask', deleteprivatetask),
    ('/deletecommontask', deletecommontask),
], debug=True)