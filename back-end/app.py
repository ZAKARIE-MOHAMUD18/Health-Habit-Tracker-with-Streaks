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
        parser.add_argument("user_id", type=int, required=True)
        parser.add_argument("title", type=str, required=True)
        parser.add_argument("description", type=str)
        parser.add_argument("frequency", type=str, required=True)
        parser.add_argument("start_date", type=str)
        args = parser.parse_args()

        if args["frequency"] not in ["daily", "weekly"]:
            return {"error": "frequency must be 'daily' or 'weekly'"}, 400

        user = User.query.get(args["user_id"])
        if not user:
            return {"error": "User not found"}, 404

        try:
            start_date = datetime.strptime(args["start_date"], "%Y-%m-%d").date() if args["start_date"] else date.today()
        except ValueError:
            return {"error": "start_date must be YYYY-MM-DD"}, 400

        habit = Habit(
            user_id=args["user_id"],
            title=args["title"],
            description=args.get("description"),
            frequency=args["frequency"],
            start_date=start_date,
        )

        db.session.add(habit)
        db.session.commit()

        return habit.to_dict(), 201


class HabitDetails(Resource):
    def get(self, habit_id):
        habit = Habit.query.get(habit_id)
        if not habit:
            return {"error": "Habit not found"}, 404
        return habit.to_dict(rules=("-user",)), 200


# -------------------
# HabitLog Resource
# -------------------
class HabitLogList(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("habit_id", type=int, required=True)
        parser.add_argument("date", type=str, required=True)
        parser.add_argument("status", type=bool, required=True)
        parser.add_argument("note")
        args = parser.parse_args()

        habit = Habit.query.get(args["habit_id"])
        if not habit:
            return {"error": "Habit not found"}, 404

        try:
            log_date = datetime.strptime(args["date"], "%Y-%m-%d").date()
        except ValueError:
            return {"error": "date must be YYYY-MM-DD"}, 400

        new_log = HabitLog(
            habit_id=args["habit_id"],
            date=log_date,
            status=args["status"],  # now Boolean in model
            note=args.get("note")
        )
        db.session.add(new_log)
        db.session.commit()
        return new_log.to_dict(), 201


class HabitLogDetails(Resource):
    def get(self, log_id):
        log = HabitLog.query.get(log_id)
        if not log:
            return {"error": "Log not found"}, 404
        return log.to_dict(), 200


# -------------------
# Challenge Resource
# -------------------
class ChallengeList(Resource):
    def get(self):
        challenges = Challenge.query.all()
        return [c.to_dict() for c in challenges], 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("title", required=True)
        parser.add_argument("description")
        parser.add_argument("start_date", required=True)
        parser.add_argument("end_date", required=True)
        args = parser.parse_args()

        try:
            start_date = datetime.strptime(args["start_date"], "%Y-%m-%d").date()
            end_date = datetime.strptime(args["end_date"], "%Y-%m-%d").date()
        except ValueError:
            return {"error": "dates must be YYYY-MM-DD"}, 400

        new_challenge = Challenge(
            title=args["title"],
            description=args.get("description"),
            start_date=start_date,
            end_date=end_date
        )
        db.session.add(new_challenge)
        db.session.commit()
        return new_challenge.to_dict(), 201


class ChallengeDetails(Resource):
    def get(self, challenge_id):
        challenge = Challenge.query.get(challenge_id)
        if not challenge:
            return {"error": "Challenge not found"}, 404
        return challenge.to_dict(), 200


# -------------------
# UserChallenge Resource
# -------------------
class UserChallengeList(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", type=int, required=True)
        parser.add_argument("challenge_id", type=int, required=True)
        parser.add_argument("status", type=str, required=True)  # match model
        parser.add_argument("join_date", type=str)
        args = parser.parse_args()

        user = User.query.get(args["user_id"])
        challenge = Challenge.query.get(args["challenge_id"])
        if not user or not challenge:
            return {"error": "User or Challenge not found"}, 404

        try:
            join_date = datetime.strptime(args["join_date"], "%Y-%m-%d").date() if args["join_date"] else date.today()
        except ValueError:
            return {"error": "join_date must be YYYY-MM-DD"}, 400

        new_uc = UserChallenge(
            user_id=args["user_id"],
            challenge_id=args["challenge_id"],
            join_date=join_date,
            status=args["status"]
        )
        db.session.add(new_uc)
        db.session.commit()
        return new_uc.to_dict(), 201


class UserChallengeDetails(Resource):
    def get(self, user_challenge_id):
        uc = UserChallenge.query.get(user_challenge_id)
        if not uc:
            return {"error": "Not found"}, 404
        return uc.to_dict(), 200


# -------------------
# Routes
# -------------------
api.add_resource(UserList, "/users")
api.add_resource(HabitList, "/habits")
api.add_resource(HabitDetails, "/habits/<int:habit_id>")
api.add_resource(HabitLogList, "/habitlogs")
api.add_resource(HabitLogDetails, "/habitlogs/<int:log_id>")
api.add_resource(ChallengeList, "/challenges")
api.add_resource(ChallengeDetails, "/challenges/<int:challenge_id>")
api.add_resource(UserChallengeList, "/userchallenges")
api.add_resource(UserChallengeDetails, "/userchallenges/<int:user_challenge_id>")
