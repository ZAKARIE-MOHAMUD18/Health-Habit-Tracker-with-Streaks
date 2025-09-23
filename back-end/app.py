from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, User, Habit, Challenge, HabitLog, UserChallenge
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///habit_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

# -------------------------------
# Validation Helpers
# -------------------------------
def validate_email(email):
    return "@" in email and "." in email

def validate_frequency(freq):
    return freq in ["daily", "weekly", "monthly"]

# -------------------------------
# USER ROUTES
# -------------------------------
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data.get("name") or not data.get("email") or not data.get("password"):
        return jsonify({"error": "name, email, and password required"}), 400
    if not validate_email(data["email"]):
        return jsonify({"error": "invalid email"}), 400
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "email already exists"}), 400

    user = User(
        name=data["name"],
        email=data["email"],
        password_hash=generate_password_hash(data["password"])
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict(rules=("-password_hash",))), 201

@app.route("/users", methods=["GET"])
def list_users():
    users = User.query.all()
    return jsonify([u.to_dict(rules=("-password_hash",)) for u in users]), 200

@app.route("/users/<int:id>", methods=["PATCH"])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    if "name" in data:
        user.name = data["name"]
    if "email" in data and validate_email(data["email"]):
        user.email = data["email"]
    if "password" in data:
        user.password_hash = generate_password_hash(data["password"])
    db.session.commit()
    return jsonify(user.to_dict(rules=("-password_hash",))), 200

@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200

# -------------------------------
# LOGIN
# -------------------------------
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"error": "email and password required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "invalid credentials"}), 401

    return jsonify({"message": "Login successful", "user": user.to_dict(rules=("-password_hash",))}), 200

# -------------------------------
# PROFILE
# -------------------------------
@app.route("/profile/<int:user_id>", methods=["GET"])
def profile(user_id):
    user = User.query.get_or_404(user_id)
    user_data = user.to_dict(rules=("-password_hash", "-habits.user", "-user_challenges.user"))
    user_data["habits"] = [h.to_dict(rules=("-user", "-logs.habit")) for h in user.habits]
    user_data["challenges"] = [uc.challenge.to_dict(rules=("-user_challenges.challenge",)) for uc in user.user_challenges]
    return jsonify(user_data), 200

# -------------------------------
# HABIT ROUTES
# -------------------------------
@app.route("/habits", methods=["POST"])
def create_habit():
    data = request.get_json()
    if not validate_frequency(data.get("frequency", "")):
        return jsonify({"error": "invalid frequency"}), 400

    habit = Habit(
        user_id=data["user_id"],
        title=data["title"],
        description=data.get("description"),
        frequency=data["frequency"],
        start_date=datetime.strptime(data["start_date"], "%Y-%m-%d").date()
    )
    db.session.add(habit)
    db.session.commit()
    return jsonify(habit.to_dict()), 201

@app.route("/habits", methods=["GET"])
def list_habits():
    habits = Habit.query.all()
    return jsonify([h.to_dict() for h in habits]), 200

@app.route("/habits/<int:id>", methods=["PATCH"])
def update_habit(id):
    habit = Habit.query.get_or_404(id)
    data = request.get_json()
    if "title" in data:
        habit.title = data["title"]
    if "frequency" in data and validate_frequency(data["frequency"]):
        habit.frequency = data["frequency"]
    db.session.commit()
    return jsonify(habit.to_dict()), 200

@app.route("/habits/<int:id>", methods=["DELETE"])
def delete_habit(id):
    habit = Habit.query.get_or_404(id)
    db.session.delete(habit)
    db.session.commit()
    return jsonify({"message": "Habit deleted"}), 200

# -------------------------------
# CHALLENGE ROUTES
# -------------------------------
@app.route("/challenges", methods=["POST"])
def create_challenge():
    data = request.get_json()
    challenge = Challenge(
        title=data["title"],
        description=data.get("description"),
        start_date=datetime.strptime(data["start_date"], "%Y-%m-%d").date(),
        end_date=datetime.strptime(data["end_date"], "%Y-%m-%d").date()
    )
    db.session.add(challenge)
    db.session.commit()
    return jsonify(challenge.to_dict()), 201

@app.route("/challenges", methods=["GET"])
def list_challenges():
    challenges = Challenge.query.all()
    return jsonify([c.to_dict() for c in challenges]), 200

@app.route("/challenges/<int:id>", methods=["PATCH"])
def update_challenge(id):
    challenge = Challenge.query.get_or_404(id)
    data = request.get_json()
    if "title" in data:
        challenge.title = data["title"]
    if "description" in data:
        challenge.description = data["description"]
    db.session.commit()
    return jsonify(challenge.to_dict()), 200

@app.route("/challenges/<int:id>", methods=["DELETE"])
def delete_challenge(id):
    challenge = Challenge.query.get_or_404(id)
    db.session.delete(challenge)
    db.session.commit()
    return jsonify({"message": "Challenge deleted"}), 200

# -------------------------------
# HABIT LOGS
# -------------------------------
@app.route("/habitlogs", methods=["POST"])
def create_log():
    data = request.get_json()
    log = HabitLog(
        habit_id=data["habit_id"],
        date=datetime.strptime(data["date"], "%Y-%m-%d").date(),
        status=data["status"],
        note=data.get("note")
    )
    db.session.add(log)
    db.session.commit()
    return jsonify(log.to_dict()), 201

@app.route("/habitlogs", methods=["GET"])
def list_logs():
    logs = HabitLog.query.all()
    return jsonify([l.to_dict() for l in logs]), 200

@app.route("/habitlogs/<int:id>", methods=["PATCH"])
def update_log(id):
    log = HabitLog.query.get_or_404(id)
    data = request.get_json()
    if "status" in data:
        log.status = data["status"]
    if "note" in data:
        log.note = data["note"]
    db.session.commit()
    return jsonify(log.to_dict()), 200

@app.route("/habitlogs/<int:id>", methods=["DELETE"])
def delete_log(id):
    log = HabitLog.query.get_or_404(id)
    db.session.delete(log)
    db.session.commit()
    return jsonify({"message": "Habit log deleted"}), 200

# -------------------------------
# USER CHALLENGES
# -------------------------------
@app.route("/user_challenges", methods=["POST"])
def join_challenge():
    data = request.get_json()
    uc = UserChallenge(
        user_id=data["user_id"],
        challenge_id=data["challenge_id"],
        join_date=datetime.strptime(data["join_date"], "%Y-%m-%d").date(),
        status=data.get("status", "active")
    )
    db.session.add(uc)
    db.session.commit()
    return jsonify(uc.to_dict()), 201

@app.route("/user_challenges", methods=["GET"])
def list_user_challenges():
    ucs = UserChallenge.query.all()
    return jsonify([uc.to_dict() for uc in ucs]), 200

@app.route("/user_challenges/<int:id>", methods=["PATCH"])
def update_user_challenge(id):
    uc = UserChallenge.query.get_or_404(id)
    data = request.get_json()
    if "status" in data:
        uc.status = data["status"]
    db.session.commit()
    return jsonify(uc.to_dict()), 200

@app.route("/user_challenges/<int:id>", methods=["DELETE"])
def delete_user_challenge(id):
    uc = UserChallenge.query.get_or_404(id)
    db.session.delete(uc)
    db.session.commit()
    return jsonify({"message": "User challenge deleted"}), 200

# -------------------------------
# RUN
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
