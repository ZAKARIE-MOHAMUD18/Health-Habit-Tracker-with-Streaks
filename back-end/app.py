from app import app, db
from models import Habitlog, Challange, UserChallange,User
from flask_restful import Resource, Api, reqparse

api = Api(app)

class Habitdetails(Resource):
    def get(self, habit_id):
        habit = Habitlog.query.get(habit_id)
        return habit
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('habit_id', required=True)
        parser.add_argument('date', required=True)
        parser.add_argument('status', required=True)
        parser.add_argument('note')
        args = parser.parse_args()

        new_habit = Habitlog(
            habit_id=args['habit_id'],
            date=args['date'],
            status=args['status'],
            note=args.get('note')
        )
        db.session.add(new_habit)
        db.session.commit()
        return new_habit, 201   
    
api.add_resource(Habitdetails, '/habitdetails', '/habitdetails/<string:habit_id>')  

class Challangedetails(Resource):
    def get(self, challange_id):
        challange = Challange.query.get(challange_id)
        return challange
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=True)
        parser.add_argument('description')
        parser.add_argument('start_date', required=True)
        parser.add_argument('end_date', required=True)
        args = parser.parse_args()

        new_challange = Challange(
            title=args['title'],
            description=args.get('description'),
            start_date=args['start_date'],
            end_date=args['end_date']
        )
        db.session.add(new_challange)
        db.session.commit()
        return new_challange, 201
api.add_resource(Challangedetails, '/challangedetails', '/challangedetails/<int:challange_id>')

class UserChallangedetails(Resource):
    def get(self, user_challange_id):
        user_challange = UserChallange.query.get(user_challange_id)
        return user_challange
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', required=True)
        parser.add_argument('challange_id', required=True)
        parser.add_argument('join_date', required=True)
        parser.add_argument('status', required=True)
        args = parser.parse_args()

        new_user_challange = UserChallange(
            user_id=args['user_id'],
            challange_id=args['challange_id'],
            join_date=args['join_date'],
            status=args['status']
        )
        db.session.add(new_user_challange)
        db.session.commit()
        return new_user_challange, 201
api.add_resource(UserChallangedetails, '/userchallangedetails', '/userchallangedetails/<int:user_challange_id>')