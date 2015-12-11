import webapp2
from google.appengine.api import users, files, images
from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import mail
from google.appengine.ext import db
import time
import json
import database
import datetime
import os
import pytz

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

        task=database.privatetask(finished=0,overdue=0,task_name=taskname,creator=creator,due=due,description=description,
                                  task_id=taskid)

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
        taskid=self.request.params['taskid']
        replyto=self.request.params['replyto']
        taskid=int(taskid)
        commentid=int(commentid)
        replyid=hash(content+str(taskid))

        reply=database.reply(reply_id=replyid,creator=creator,reply_content=content,comment_id=commentid,task_id=taskid,replyto=replyto)

        reply.put()

class viewsinglecommontask(webapp2.RequestHandler):
    def get(self):
        taskid = self.request.get('taskid')
        taskid=int(taskid)

        task_query = database.commontask.query(database.commontask.task_id == taskid)
        tasks=task_query.fetch()

        taskname=[]
        creator=[]
        due=[]
        location=[]
        description=[]
        create_time=[]
        numofmember=[]

        for task in tasks:
            taskname.append(task.task_name)
            creator.append(task.creator)
            due.append(task.due)
            # location=[task.location]
            description.append(task.description)
            finals=transtime(task.create_time)
            create_time.append(finals)
            numofmember.append(task.numofmember)

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
            finalsss=transtime(comment.create_time)
            commentcreate_time.append(finalsss)
            commentcreator.append(comment.creator)

#get comment

        reply_query = database.reply.query(ndb.AND(
            database.reply.task_id == taskid,database.reply.create_time!=None)).order(database.reply.create_time)
        replys=reply_query.fetch()

        reply_content=[]
        replycomment_id=[]
        replycreate_time=[]
        replycreator=[]
        replyto=[]

        for reply in replys:
            reply_content.append(reply.reply_content)
            replycomment_id.append(reply.comment_id)
            finalss=transtime(reply.create_time)
            replycreate_time.append(finalss)
            replycreator.append(reply.creator)
            replyto.append(reply.replyto)
# get replys


        taskjson = {'taskname':taskname,'creator':creator,'due':due,'location':location,'description':description,'create_time':create_time,'numofmember':numofmember,
                    'comment_content':comment_content,'comment_id':comment_id,'commentcreate_time':commentcreate_time,'commentcreator':commentcreator,
                    'reply_content':reply_content,'replycomment_id': replycomment_id,'replycreate_time':replycreate_time,'replycreator':replycreator,'replyto':replyto}
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

        privatetask_query = database.privatetask.query(database.privatetask.creator == user_id)
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

        jointaskname=[]
        joincreator=[]
        joindue=[]
        joinlocation=[]
        joindescription=[]
        joinnumofmember=[]
        jointask_id=[]

        for tasks in subtasks:
            if tasks.task_id in subtaskid:
                jointaskname.append(tasks.task_name)
                joincreator.append(tasks.creator)
                joindue.append(tasks.due)
                joinlocation.append(tasks.location)
                joindescription.append(tasks.description)
                joinnumofmember.append(tasks.numofmember)
                jointask_id.append(tasks.tasks_id)


        commonjson = {'pritaskname':pritaskname,'pricreator':pricreator,'pridue':pridue,'prilocation':prilocation,'pridescription':pridescription,
                      'pritaskid':pritaskid,'prifinished':prifinished,'prioverdue':prioverdue,'taskname':taskname,'creator':creator,'due':due,
                      'location':location,'description':description,'numofmember':numofmember,'taskid':task_id,'jointaskname':jointaskname,'joincreator':joincreator,
                      'joindue':joindue,'joinlocation':joinlocation,'joindescription':joindescription,'joinnumofmember':joinnumofmember,'jointaskid':jointask_id}
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

class viewreply(webapp2.RequestHandler):
    def get(self):
        commentid = self.request.get('commentid')
        commentid=int(commentid)

        reply_query = database.reply.query(ndb.AND(
            database.reply.comment_id == commentid,database.reply.create_time!=None)).order(database.reply.create_time)
        replys=reply_query.fetch()

        reply_content=[]
        replycomment_id=[]
        replycreate_time=[]
        replycreator=[]
        replyto=[]

        for reply in replys:
            reply_content.append(reply.reply_content)
            replycomment_id.append(reply.comment_id)
            finals=transtime(reply.create_time)
            replycreate_time.append(finals)
            replycreator.append(reply.creator)
            replyto.append(reply.replyto)
# get replys


        taskjson = {'reply_content':reply_content,'replycomment_id': replycomment_id,'replycreate_time':replycreate_time,'replycreator':replycreator,'replyto':replyto}
        jsonObj1 = json.dumps(taskjson, sort_keys=True,indent=4, separators=(',', ': '))
        self.response.write(jsonObj1)

class searchtask(webapp2.RequestHandler):
    def get(self):

        searchname=self.request.get('searchname')

        task_query = database.commontask.query()
        tasks=task_query.fetch()

        taskname=[]
        taskid=[]

        for task in tasks:
            if searchname in task.description or searchname in task.task_name:
                taskname.append(task.task_name)
                taskid.append(task.task_id)


        taskjson = {'taskname':taskname,'taskid':taskid}
        jsonObj1 = json.dumps(taskjson, sort_keys=True,indent=4, separators=(',', ': '))
        self.response.write(jsonObj1)

class suggest(webapp2.RequestHandler):
    def get(self):
        user_id = self.request.get('userid')

        mytask_query = database.commontask.query(database.commontask.creator == user_id)
        mytasks=mytask_query.fetch()
        mytaskname=[]

# join part
        alltask_query = database.commontask.query()
        alltask=alltask_query.fetch()
        alltaskname=[]

        for tasks in alltask:
            alltaskname.append(tasks.task_name)
        for ta in mytasks:
            mytaskname.append(ta.task_name)

        finaltaskname=[]
        for task in mytaskname:
            init=0
            tmp=""
            for i in alltaskname:
                if le(task,i)<1 and le(task,i)>init and i not in finaltaskname:
                    tmp=i
                    init=le(task,i)
            finaltaskname.append(tmp)


        taskname=[]
        creator=[]
        due=[]
        numofmember=[]
        task_id=[]

        for t in alltask:
            if t.task_name in finaltaskname:
                taskname.append(t.task_name)
                creator.append(t.creator)
                due.append(t.due)
                numofmember.append(t.numofmember)
                task_id.append(t.task_id)

        commonjson = {'taskname':taskname,'creator':creator,'due':due,'numofmember':numofmember,'taskid':task_id}
        jsonObj2 = json.dumps(commonjson, sort_keys=True,indent=4, separators=(',', ': '))
        self.response.write(jsonObj2)

def transtime(time):
        time2=str(time)
        time3=time2[:19]
        t4=time3.split(" ")
        day=t4[0][8:10]
        hour=t4[1][:2]
        inthour=int(hour)
        intday=int(day)
        if inthour>=6:
            inthour-=6
        else:
            inthour=inthour+24-6
            intday-=1

        newhour=str(inthour)
        if inthour<10:
            newhour="0"+str(inthour)

        newday=str(intday)

        finals=t4[0][:8]+newday+" "+newhour+t4[1][2:5]
        return finals

def le(input_x, input_y):
        xlen = len(input_x) + 1
        ylen = len(input_y) + 1

        dp = []
        for p in range(xlen):
            dp.append([])
            for q in range(ylen):
                dp[p].append(0)

        for i in range(0, xlen):
            dp[i][0] = i
        for j in range(0, ylen):
            dp[0][j] = j

        for i in range(1, xlen):
            for j in range(1, ylen):
                if input_x[i - 1] == input_y[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
        similarity = 1.0-float(dp[xlen-1][ylen-1])/float(max(xlen-1,ylen-1))
        return similarity


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/createprivatetask',createprivatetask),
    ('/createcommontask', createcommontask),
    ('/createcomment', createcomment),
    ('/createreply', createreply),
    ('/viewsinglecommontask', viewsinglecommontask),
    ('/viewsingleprivatetask', viewsingleprivatetask),
    ('/viewmytask', viewmytask),
    ('/viewallcommontask', viewallcommontask),
    ('/viewreply', viewreply),
    ('/updateprivatetask', updateprivatetask),
    ('/updatecommontask', updatecommontask),
    ('/deleteprivatetask', deleteprivatetask),
    ('/deletecommontask', deletecommontask),
    ('/finishprivatetask', finishprivatetask),
    ('/updateprivateedue', updateprivateedue),
    ('/searchtask', searchtask),
    ('/suggest', suggest)

], debug=True)