from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import UniqueConstraint
from datetime import date, datetime

db = SQLAlchemy()


class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)  # fixed length

    # Relationships
    habits = db.relationship("Habit", back_populates="user", cascade="all, delete-orphan")
    user_challenges = db.relationship("UserChallenge", back_populates="user", cascade="all, delete-orphan")

    # Exclude password hash from API responses
    serialize_rules = ("-password_hash", "-habits.user", "-user_challenges.user")


class Habit(db.Model, SerializerMixin):
    __tablename__ = "habits"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    frequency = db.Column(db.String(20), nullable=False)  # validate in app layer
    start_date = db.Column(db.Date, nullable=False)

    # Relationships
    user = db.relationship("User", back_populates="habits")
    logs = db.relationship("HabitLog", back_populates="habit", cascade="all, delete-orphan")

    serialize_rules = ("-user.habits", "-logs.habit")


class HabitLog(db.Model, SerializerMixin):
    __tablename__ = "habitlogs"

    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey("habits.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    note = db.Column(db.Text)

    # Relationships
    habit = db.relationship("Habit", back_populates="logs")

    # Ensure no duplicate logs for the same day
    __table_args__ = (UniqueConstraint("habit_id", "date", name="unique_habit_date"),)

    serialize_rules = ("-habit.logs",)


class Challenge(db.Model, SerializerMixin):
    __tablename__ = "challenges"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    # Many-to-Many via UserChallenge
    user_challenges = db.relationship("UserChallenge", back_populates="challenge", cascade="all, delete-orphan")

    serialize_rules = ("-user_challenges.challenge",)


class UserChallenge(db.Model, SerializerMixin):
    __tablename__ = "user_challenges"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey("challenges.id"), nullable=False)
    join_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False)

    # Relationships
    user = db.relationship("User", back_populates="user_challenges")
    challenge = db.relationship("Challenge", back_populates="user_challenges")

    serialize_rules = ("-user.user_challenges", "-challenge.user_challenges")
