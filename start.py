from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt
from auth import authenticate
from db import find, userInsert, userInfo,userFind, ticketInsert, Ticket, viewAll
import ast
import random 
# to run mongodb from cmd type in "C:\Program Files\MongoDB\Server\4.04\bin\mongod.exe" or mongod if in path
app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'mongologinexample2'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/myDatabase2'
def ticketGen():
    ticket = 0
    while ticket == 0:
        ticket= random.randint(1,999999999)

        outcome = find(ticket)
        if len(outcome) != 2 :
            ticket = 0
        else:
            break
        
    return ticket

mongo = PyMongo(app)

#this is the initial page. this is what you would see on startup which shows only the login page
@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('home'))

    return render_template('index.html')

#This is where the first step of the backend takes place. This is where the first step authentication
#with this database takes into place. This is the only authentication that is being used

@app.route("/login", methods = ['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
            session['username'] = request.form['username'].capitalize()
            return redirect(url_for('index'))

    return 'Invalid username/password combination'  

#this is the page that you redirect to after wanting to register
# here you use greenko username and password to login to setup an account
# authenticates with the test API at current specs 
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        
        user=request.form['username']
        password = request.form['pass']
        auth,uID,data = authenticate(user,password)
        if auth == 'success':
            userInsert(UID=uID,username= user.capitalize(),Surname= "y",FirstName="x")
            #num = usID
            #creating a unique url for every User
            return redirect(url_for("secondAuth", userID= uID))
        else:
            return render_template("register.html",hiddenText= "That username/password is not in the database. Try Again")
        

    return render_template('register.html')


#this is the secondAuth as I call it but it just takes in the users data to create a account
# if a username exists you must backtrack to the secondAuth page and try again
@app.route('/secondAuth', methods=['POST', 'GET'])
def secondAuth():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass1'].encode('utf-8'), bcrypt.gensalt())
            users.insert_one({'name' : request.form['username'], 'password' : hashpass})
            temp = userInfo.objects(username = request.form['username'])
            temp.userFirstName = request.form['firstName'].capitalize()
            temp.userSurname= request.form['Surname'].capitalize()
            session['username'] = request.form['username']
            
            return redirect(url_for('index'))
        
        return 'That username already exists!'

    return render_template('secondAuth.html')


#this is the main page where the user can either assign a ticket to multiple users or just view the tickets
@app.route("/home")
def home():
    if 'username' in session:
        return render_template('home.html',name = session['username'])
    else:
        return redirect(url_for('index'))

@app.route('/temp',methods=['POST'])
def temp():
    num = ticketGen()
    return redirect(url_for("assign",ticketID = num))
    
@app.route("/assign/<ticketID>",methods=['POST', 'GET'] )
def assign(ticketID):
    if 'username' in session:
        return render_template("assign.html",ticketID = ticketID)

@app.route('/ticketTemp/<ticketID>',methods=['POST', 'GET'])
def ticketTemp(ticketID):
    assignees = request.form['assign']
    ticket = request.form['ticket']
    ticketNum=ticketID
    return render_template("tempTicket.html",ticketNum=ticketNum,assignees=assignees,ticket=ticket)

@app.route("/confTicket/<ticketNum>/<assigned>/<ticket>" ,methods=['POST', 'GET'])
def confTicket(ticketNum, assigned, ticket): 
    temp=[]
    assigned=assigned.split(" ")
    for i in assigned:
        i=i.split("@")
        temp.extend(i)
    for i in temp:
        if i=='':
            temp.remove(i)
    assigned=temp
    temp = userInfo.objects(username= session['username'].capitalize())
    x = temp.to_json()
    X = ast.literal_eval(x)
    uID = X[0]["uID"]
    ticketInsert(ticketNum=ticketNum,UID=uID,TID=assigned,ticket=ticket)  
    return redirect(url_for('index'))

@app.route("/temp2",methods=['POST', 'GET'])
def temp2():
    
    #temp = temp.uID
    #return redirect(url_for("viewTicket",userID=temp))
    temp = viewAll()
    x = temp.to_json()
    X = ast.literal_eval(x)

    return render_template("viewTicket.html",dictionary = X)

@app.route('/viewTicket<userID>', methods=['GET'])
def viewTicket():
    temp = Ticket.objects(uID=id)
    x=temp.to_json()
    return "View"

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)