from flask import Flask, request
from models import db, User, Habit, HabitLog, Challenge, UserChallenge
from flask_migrate import Migrate
from flask_restful import Resource, Api, reqparse
from werkzeug.security import generate_password_hash
from datetime import datetime, date  

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///habit-tracker.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

# -------------------
# User Resource
# -------------------
class UserList(Resource):
    def get(self):
        users = User.query.all()
        return [u.to_dict(rules=("-habits", "-user_challenges", "-password_hash")) for u in users], 200

    def post(self):
        data = request.get_json()

        if not data.get("name") or not data.get("email") or not data.get("password"):
            return {"error": "name, email, and password are required"}, 400

        if User.query.filter_by(email=data["email"]).first():
            return {"error": "Email already exists"}, 400

        new_user = User(
            name=data["name"],
            email=data["email"],
            password_hash=generate_password_hash(data["password"])
        )

        db.session.add(new_user)
        db.session.commit()

        return new_user.to_dict(rules=("-habits", "-user_challenges", "-password_hash")), 201

# -------------------
# Habit Resource
# -------------------
class HabitList(Resource):
    def get(self):
        habits = Habit.query.all()
        return [h.to_dict() for h in habits], 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", type=int, required=True, help="user_id is required")
        parser.add_argument("title", type=str, required=True, help="title is required")
        parser.add_argument("description", type=str)
        parser.add_argument("frequency", type=str, required=True, help="frequency is required")
        parser.add_argument("start_date", type=str, required=False)
        args = parser.parse_args()

        if args["frequency"] not in ["daily", "weekly"]:
            return {"error": "frequency must be 'daily' or 'weekly'"}, 400

        user = User.query.get(args["user_id"])
        if not user:
            return {"error": "User not found"}, 404

        if args["start_date"]:
            try:
                start_date = datetime.strptime(args["start_date"], "%Y-%m-%d").date()
            except ValueError:
                return {"error": "start_date must be in YYYY-MM-DD format"}, 400
        else:
            start_date = date.today()

        habit = Habit(
            user_id=args["user_id"],
            title=args["title"],
            description=args["description"],
            frequency=args["frequency"],
            start_date=start_date,
        )

        db.session.add(habit)
        db.session.commit()

        return habit.to_dict(), 201

# -------------------
# HabitLog Resource
# -------------------
class HabitDetails(Resource):
    def get(self, habit_id):
        habit = HabitLog.query.get(habit_id)
        return habit.to_dict() if habit else {"error": "Habit not found"}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('habit_id', required=True)
        parser.add_argument('date', required=True)
        parser.add_argument('status', required=True)
        parser.add_argument('note')
        args = parser.parse_args()

        new_habit = HabitLog(
            habit_id=args['habit_id'],
            date=args['date'],
            status=args['status'],
            note=args.get('note')
        )
        db.session.add(new_habit)
        db.session.commit()
        return new_habit.to_dict(), 201

# -------------------
# Challenge Resource
# -------------------
class ChallengeDetails(Resource):
    def get(self, challenge_id):
        challenge = Challenge.query.get(challenge_id)
        return challenge.to_dict() if challenge else {"error": "Challenge not found"}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=True)
        parser.add_argument('description')
        parser.add_argument('start_date', required=True)
        parser.add_argument('end_date', required=True)
        args = parser.parse_args()

        new_challenge = Challenge(
            title=args['title'],
            description=args.get('description'),
            start_date=args['start_date'],
            end_date=args['end_date']
        )
        db.session.add(new_challenge)
        db.session.commit()
        return new_challenge.to_dict(), 201

# -------------------
# UserChallenge Resource
# -------------------
class UserChallengeDetails(Resource):
    def get(self, user_challenge_id):
        user_challenge = UserChallenge.query.get(user_challenge_id)
        return user_challenge.to_dict() if user_challenge else {"error": "Not found"}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', required=True, type=int)
        parser.add_argument('challenge_id', required=True, type=int)
        parser.add_argument('join_date', required=True)
        parser.add_argument('status', required=True)
        args = parser.parse_args()

        new_user_challenge = UserChallenge(
            user_id=args['user_id'],
            challenge_id=args['challenge_id'],
            join_date=args['join_date'],
            status=args['status']
        )
        db.session.add(new_user_challenge)
        db.session.commit()
        return new_user_challenge.to_dict(), 201

# -------------------
# Routes
# -------------------
api.add_resource(UserList, "/users")
api.add_resource(HabitList, "/habits")
api.add_resource(HabitDetails, "/habitdetails", "/habitdetails/<int:habit_id>")
api.add_resource(ChallengeDetails, "/challengedetails", "/challengedetails/<int:challenge_id>")
api.add_resource(UserChallengeDetails, "/userchallengedetails", "/userchallengedetails/<int:user_challenge_id>")
