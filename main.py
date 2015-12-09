import webapp2
from google.appengine.api import users, files, images
from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import mail
import time
import json
import database
import datetime

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Wo ai Baobao~~~\n')

class createprivatetask(webapp2.RequestHandler):
    def post(self):

        # position=self.request.params['latitude']+"%"+self.request.params['longitude']+")"

        taskname=self.request.params['taskname']
        creator=self.request.params['creator']
        due=self.request.params['due']
        # location=self.request.params['location']
        description=self.request.params['description']
        taskid=self.request.params['taskid']
        taskid=int(taskid)

        task=database.privatetask(finished=0,overdue=0,task_name=taskname,creator=creator,due=due,description=description,task_id=taskid)

        task.put()

class updateprivatetask(webapp2.RequestHandler):
    def post(self):

        taskid=self.request.params['taskid']
        taskid=int(taskid)
        task_query = database.privatetask.query(database.privatetask.task_id == taskid)
        tasks=task_query.fetch()

        for task in tasks:
            task.taskname=self.request.params['taskname']
            task.due=self.request.params['due']
            # task.location=self.request.params['location']
            task.description=self.request.params['description']
            task.put()

class deleteprivatetask(webapp2.RequestHandler):
    def post(self):

        taskid=self.request.params['taskid']
        taskid=int(taskid)
        task_query = database.privatetask.query(database.privatetask.task_id == taskid)
        tasks=task_query.fetch()

        for task in tasks:
            task.key.delete()

class finishprivatetask(webapp2.RequestHandler):
    def post(self):

        taskid=self.request.params['taskid']
        taskid=int(taskid)
        task_query = database.privatetask.query(database.privatetask.task_id == taskid)
        tasks=task_query.fetch()

        for task in tasks:
            task.finished=1
            task.put()

class createcommontask(webapp2.RequestHandler):
    def post(self):

        taskname=self.request.params['taskname']
        creator=self.request.params['creator']
        due=self.request.params['due']
        # location=self.request.params['location']
        description=self.request.params['description']
        taskid=self.request.params['taskid']
        taskid=int(taskid)

        task=database.commontask(finished=0,task_name=taskname,creator=creator,due=due,description=description,task_id=taskid,numofmember=0)

        task.put()

class updatecommontask(webapp2.RequestHandler):
    def post(self):

        taskid = self.request.get('taskid')

        task_query = database.commontask.query(database.commontask.task_id == taskid)
        tasks=task_query.fetch()

        for task in tasks:
            task.taskname=self.request.params['taskname']
            task.due=self.request.params['due']
            task.location=self.request.params['location']
            task.description=self.request.params['description']
            task.put()

class deletecommontask(webapp2.RequestHandler):
    def post(self):

        taskid=self.request.params['taskid']
        taskid=int(taskid)
        task_query = database.commontask.query(database.commontask.task_id == taskid)
        tasks=task_query.fetch()

        for task in tasks:
            task.key.delete()

class createcomment(webapp2.RequestHandler):
    def post(self):

        creator=self.request.params['creator']
        content=self.request.params['content']
        taskid=self.request.params['taskid']
        taskid=int(taskid)
        commentid=hash(content+str(taskid))

        comment=database.comment(task_id=taskid,creator=creator,comment_content=content,comment_id=commentid)

        comment.put()

class createreply(webapp2.RequestHandler):
    def post(self):

        creator=self.request.params['creator']
        content=self.request.params['content']
        commentid=self.request.params['commentid']
        replyid=hash(content)

        reply=database.reply(reply_id=replyid,creator=creator,reply_content=content,comment_id=commentid)

        reply.put()

class viewsinglecommontask(webapp2.RequestHandler):
    def get(self):
        taskid = self.request.get('taskid')
        taskid=int(taskid)

        task_query = database.commontask.query(database.commontask.task_id == taskid)
        tasks=task_query.fetch()

        for task in tasks:
            taskname=[task.task_name]
            creator=[task.creator]
            due=[task.due]
            location=[task.location]
            description=[task.description]
            create_time=[str(task.create_time)]
            numofmember=[task.numofmember]

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
            commentcreate_time.append(str(comment.create_time))
            commentcreator.append(comment.creator)

#get comment

        # reply_query = database.reply.query(ndb.AND(
        #     database.reply.comment_id in comment_id,database.reply.create_time!=None)).order(database.reply.create_time)
        # replys=reply_query.fetch()
        #
        # reply_content=[]
        # replycomment_id=[]
        # replycreate_time=[]
        # replycreator=[]
        #
        # for reply in replys:
        #     reply_content.append(reply.comment_content)
        #     replycomment_id.append(reply.comment_id)
        #     replycreate_time.append(reply.create_time)
        #     replycreator.append(reply.creator)

# get replys


        taskjson = {'taskname':taskname,'creator':creator,'due':due,'location':location,'description':description,'create_time':create_time,'numofmember':numofmember,'comment_content':comment_content,'comment_id':comment_id,'commentcreate_time':commentcreate_time,'commentcreator':commentcreator}
        jsonObj1 = json.dumps(taskjson, sort_keys=True,indent=4, separators=(',', ': '))
        self.response.write(jsonObj1)

        # commentjson = {'comment_content':comment_content,'comment_id':comment_id,'commentcreate_time':commentcreate_time,'commentcreator':commentcreator}
        # jsonObj2 = json.dumps(commentjson, sort_keys=True,indent=4, separators=(',', ': '))
        # self.response.write(jsonObj2)
        #
        # replyjson = {'reply_content':reply_content,' replycomment_id': replycomment_id,'replycreate_time':replycreate_time,'replycreator':replycreator}
        # jsonObj3 = json.dumps(replyjson, sort_keys=True,indent=4, separators=(',', ': '))
        # self.response.write(jsonObj3)

class viewsingleprivatetask(webapp2.RequestHandler):
    def get(self):
        taskid = self.request.get('taskid')
        taskid=int(taskid)

        task_query = database.privatetask.query(database.privatetask.task_id == taskid)
        tasks=task_query.fetch()

        taskname=[]
        creator=[]
        due=[]
        location=[]
        description=[]
        create_time=[]

        for task in tasks:
            taskname.append(task.task_name)
            creator.append(task.creator)
            due.append(task.due)
            location.append(task.location)
            description.append(task.description)
            time = str(task.create_time)
            create_time.append(time)

        dictPassed = {'taskname':taskname,'creator':creator,'due':due,'location':location,'description':description,'create_time':create_time}
        jsonObj = json.dumps(dictPassed, sort_keys=True,indent=4, separators=(',', ': '))
        self.response.write(jsonObj)

class viewmytask(webapp2.RequestHandler):
    def get(self):
        user_id = self.request.get('userid')

        privatetask_query = database.privatetask.query(database.commontask.creator == user_id)
        privatetasks=privatetask_query.fetch()

        pritaskname=[]
        pricreator=[]
        pridue=[]
        prilocation=[]
        pridescription=[]
        pritaskid=[]
        prifinished=[]
        prioverdue=[]

        for task in privatetasks:
            pritaskname.append(task.task_name)
            pricreator.append(task.creator)
            pridue.append(task.due)
            prilocation.append(task.location)
            pridescription.append(task.description)
            pritaskid.append(task.task_id)
            prifinished.append(task.finished)
            prioverdue.append(task.overdue)

        # pri = {'pritaskname':pritaskname,'pricreator':pricreator,'pridue':pridue,'prilocation':prilocation,'pridescription':pridescription,'pritaskid':pritaskid}
        # jsonObj1 = json.dumps(pri, sort_keys=True,indent=4, separators=(',', ': '))


        commontask_query = database.commontask.query(database.commontask.creator == user_id)
        commontasks=commontask_query.fetch()

        sub_query = database.subscribe.query(database.subscribe.user_id == user_id)
        subs=sub_query.fetch()
        subtaskid=[]
        for sub in subs:
            subtaskid.append(sub.task_id)

        subcommontask_query = database.commontask.query()
        subtasks=subcommontask_query.fetch()

        taskname=[]
        creator=[]
        due=[]
        location=[]
        description=[]
        numofmember=[]
        task_id=[]

        for task in commontasks:
            taskname.append(task.task_name)
            creator.append(task.creator)
            due.append(task.due)
            location.append(task.location)
            description.append(task.description)
            numofmember.append(task.numofmember)
            task_id.append(task.task_id)

        for tasks in subtasks:
            if tasks.task_id in subtaskid:
                taskname.append(tasks.task_name)
                creator.append(tasks.creator)
                due.append(tasks.due)
                location.append(tasks.location)
                description.append(tasks.description)
                numofmember.append(tasks.numofmember)
                task_id.append(tasks.tasks_id)

        commonjson = {'pritaskname':pritaskname,'pricreator':pricreator,'pridue':pridue,'prilocation':prilocation,'pridescription':pridescription,'pritaskid':pritaskid,'prifinished':prifinished,'prioverdue':prioverdue,'taskname':taskname,'creator':creator,'due':due,'location':location,'description':description,'numofmember':numofmember,'taskid':task_id}
        jsonObj2 = json.dumps(commonjson, sort_keys=True,indent=4, separators=(',', ': '))
        self.response.write(jsonObj2)

class viewallcommontask(webapp2.RequestHandler):
    def get(self):
        task_query = database.commontask.query()
        tasks=task_query.fetch()

        taskname=[]
        creator=[]
        due=[]
        location=[]
        description=[]
        numofmember=[]

        for task in tasks:
            taskname.append(task.task_name)
            creator.append(task.creator)
            due.append(task.due)
            location.append(task.location)
            description.append(task.description)
            numofmember.append(task.numofmember)

        taskjson = {'taskname':taskname,'creator':creator,'due':due,'location':location,'description':description,'numofmember':numofmember}
        jsonObj1 = json.dumps(taskjson, sort_keys=True,indent=4, separators=(',', ': '))
        self.response.write(jsonObj1)

class updateprivateedue(webapp2.RequestHandler):
    def get(self):
        task_query = database.privatetask.query()
        tasks=task_query.fetch()

        for task in tasks:
            due = task.due
            duesplit=due.split(" ")
            if len(duesplit)!=2:
                break
            date=duesplit[0]
            time=duesplit[1]
            datesplit = date.split("-")
            if len(datesplit)!=2:
                break
            year = datesplit[0]
            month = datesplit[1]
            day = datesplit[2]
            timesplit = time.split(":")
            if len(timesplit)!=2:
                break
            hour = timesplit[0]
            minute = timesplit[1]

            nowtime = str(datetime.datetime.now())
            nowyear = nowtime[:4]
            nowmonth= nowtime[5:7]
            nowday = nowtime[8:10]
            nowhour = nowtime[12:14]
            nowminute = nowtime[15:17]
            if int(nowyear)>int(year):
                task.overdue =1
            else:
                if int(nowmonth)>int(month):
                    task.overdue =1
                else:
                    if int(nowday)>int(day):
                        task.overdue =1
                    elif int(nowday)==int(day)-1 and nowhour==hour and nowminute==nowminute:
                        mail.send_mail(sender="TASK :: info <sunming2725@gmail.com>",
                        to=str(task.creator),
                        subject=task.name+"(Due Reminder From TASK)",
                        body="There is only 1 days left for "+task.name)
                    else:
                        if int(nowhour)>int(hour):
                            task.overdue =1
                        else:
                            if int(nowminute)>int(minute):
                                task.overdue =1
            task.put()


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
    ('/finishprivatetask', finishprivatetask),
    ('/updateprivateedue', updateprivateedue)

], debug=True)