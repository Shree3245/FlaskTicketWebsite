from mongoengine import *
from pprint import pprint
import datetime
import random

now = datetime.datetime.now()
db = connect('abh', host='localhost', port=27017)

class Ticket(Document):
    ticketID = IntField(required=True, max_length=200,default = "")
    uID = StringField(required=True, max_length=500,default = "")
    toID = ListField(required=True, max_length=5000000,default = "")
    ticket = StringField(required=True, max_length=20000,default = "")
    situation=StringField(default = "Not Yet Completed")
    published = DateTimeField(default=now)

class userInfo(Document):
    uID = StringField(required=True, max_length=500)
    userWholeName = StringField(required=True, max_length=500,default="X")
    username = StringField(required=True, max_length=500)
    hash = StringField(required=True, max_length=500)

def userInsert(UID,Name,username,hash):
    user=userInfo(
        uID=(UID),
        userWholeName=(Name),
        username=(username),  
        hash=(hash)       
    )
    user.save() 
    
def ticketInsert(ticketNum,UID,TID,ticket):
    #print(ticketNum,UID,TID,ticket,subject)
    ticketNum=Ticket(
        ticketID=(ticketNum),
        uID=(UID),
        toID=(TID),
        ticket=(ticket),         
    )
    ticketNum.save()       # This will perform an insert

def complete(ticketNum):
    temp = Ticket.objects.get(ticketID=ticketNum)
    temp.situation="Completed"
    temp.save()

def userFind(var,id):
    temp = userInfo.objects(var=id)
    x=temp.to_json()
    return x

def find(id):
    temp = Ticket.objects(uID=id)
    x=temp.to_json()
    return x
    #pprint("{}".format(x))

#Ticket.objects(uID='5a70b5731855790c9322fe4b').delete()

"""temp = Ticket.objects(uID='john')
for i in temp:
    x = i.to_json()
    print(x)
"""
def viewAll():
    posts = Ticket.objects
    return posts
"""
temp = len(Ticket.objects)

#x=temp.to_json()
print(Ticket.objects[temp-1].to_json())"""

