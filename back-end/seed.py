from app import app, db
from models import User, Habit, HabitLog, Challenge, UserChallenge
from datetime import date, timedelta
from faker import Faker
import random

fake = Faker()

with app.app_context():
    db.drop_all()
    db.create_all()

    try:
        # --- USERS ---
        users = [
            User(
                name=fake.name(),
                email=fake.unique.email(),
                password_hash="hashed_pw"  # for demo only
            )
            for _ in range(5)
        ]
        db.session.add_all(users)
        db.session.commit()
        print("Users seeded:", User.query.count())

        # --- HABITS ---
        habits = []
        for user in users:
            for _ in range(2):  # each user gets 2 habits
                habits.append(
                    Habit(
                        user_id=user.id,
                        title=fake.word().capitalize(),
                        description=fake.sentence(),
                        frequency=random.choice(["daily", "weekly"]),
                        start_date=date.today() - timedelta(days=random.randint(1, 30)),
                    )
                )
        db.session.add_all(habits)
        db.session.commit()
        print("Habits seeded:", Habit.query.count())

        # --- HABIT LOGS ---
        habitlogs = []
        for habit in habits:
            for i in range(5):  # 5 logs per habit
                habitlogs.append(
                    HabitLog(
                        habit_id=habit.id,
                        date=date.today() - timedelta(days=i),
                        status=random.choice(["completed", "missed"]),
                        note=fake.sentence(),
                    )
                )
        db.session.add_all(habitlogs)
        db.session.commit()
        print("HabitLogs seeded:", HabitLog.query.count())

        # --- CHALLENGES ---
        challenges = [
            Challenge(
                title=fake.catch_phrase(),
                description=fake.paragraph(),
                start_date=date.today(),
                end_date=date.today() + timedelta(days=30),
            )
            for _ in range(3)
        ]
        db.session.add_all(challenges)
        db.session.commit()
        print("Challenges seeded:", Challenge.query.count())

        # --- USER CHALLENGES ---
        userchallenges = []
        for user in users:
            challenge = random.choice(challenges)
            userchallenges.append(
                UserChallenge(
                    user_id=user.id,
                    challenge_id=challenge.id,
                    join_date=date.today(),
                    status=random.choice(["active", "completed"]),
                )
            )
        db.session.add_all(userchallenges)
        db.session.commit()
        print("UserChallenges seeded:", UserChallenge.query.count())

    except Exception as e:
        db.session.rollback()
        print("Seeding failed:", e)
