from flask import Flask, request,jsonify
from flask_restful import Resource, Api,reqparse
from json import dumps
from auth import authenticate
from db import find, userInsert, userInfo,userFind, ticketInsert, Ticket, viewAll
import jwt
import ast

app = Flask(__name__)
api = Api(app)


def abort_if_todo_doesnt_exist(ticket_id):
    if len(Ticket.objects(ticketID =ticket_id ))==0 :
        abort(404, message="Ticket {} doesn't exist".format(ticket_id))

class TicketsAll(Resource):
    def get(self):
        temp = viewAll()
        x = temp.to_json()
        X = ast.literal_eval(x)
        return jsonify(X)

class Employees_Name(Resource):
    def get(self, username,password):
        output,uID,data = authenticate(username,password)
        
                
        if output=='success':
            temp = userInfo.objects(username= username)
            x = temp.to_json()
            X = ast.literal_eval(x)
            

            if len(X)==0:
                name =  data['data']['name']
                access_hash = jwt.encode({username: password}, 'secret', algorithm='HS256')
                tempHash = {"access_Hash":access_hash}
                
                userInsert(UID=uID,username= username,Name=name,hash=access_hash) 
                return data,tempHash
            else:
                tempHash = {'Info':data,"access_Hash":temp[0]['hash']}

                return jsonify(tempHash)
        else:
            return "username/password combination is wrong"        


class Ticket(Resource):
    def get(self, ticket_id):
        abort_if_todo_doesnt_exist(ticket_id)
        temp = (Ticket.objects(ticketID =ticket_id ))
        x = temp.to_json()
        X = ast.literal_eval(x)
        return jsonify(X)

    def delete(self, ticket_id):
        abort_if_todo_doesnt_exist(ticket_id)
        Ticket.objects(ticketID =ticket_id ).delete()
        return '', 204

    def put(self, ticket_id):
        temp = Ticket.objects(ticketID=ticket_id)
        args = parser.parse_args()
        toList= args['toID']
        temp.toID= toList
        return toList, 201

parser = reqparse.RequestParser()
parser.add_argument('ticketID')
parser.add_argument("uID")
parser.add_argument("toID")
parser.add_argument('ticket')
parser.add_argument('situation')
parser.add_argument('published ')

class TicketAdd(Resource):
    def post(self):
        ticketID = len(Ticket.objects)
        args = parser.parse_args()
        if len(args['toID'])==0:
            ticketInsert(ticketID,TID=[""],ticket=args['ticket'],UID=args["UID"])
        else:
            ticketInsert(ticketID,TID=args['toID'],ticket=args['ticket'],UID=args["UID"])
        myDict = []

        return TODOS[ticket_id], 201

api.add_resource(TicketsAll, '/tickets') # Route_1
api.add_resource(Employees_Name, '/employees/user=<username>/password=<password>') # Route_2

if __name__ == '__main__':
    app.run(debug=True)