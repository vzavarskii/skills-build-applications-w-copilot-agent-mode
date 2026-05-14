from django.core.management.base import BaseCommand
from django.conf import settings

import pymongo

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        client = pymongo.MongoClient('mongodb://localhost:27017')
        db = client['octofit_db']

        # Очистка коллекций
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Данные пользователей
        users = [
            {"name": "Superman", "email": "superman@dc.com", "team": "dc"},
            {"name": "Batman", "email": "batman@dc.com", "team": "dc"},
            {"name": "Wonder Woman", "email": "wonderwoman@dc.com", "team": "dc"},
            {"name": "Iron Man", "email": "ironman@marvel.com", "team": "marvel"},
            {"name": "Spider-Man", "email": "spiderman@marvel.com", "team": "marvel"},
            {"name": "Captain Marvel", "email": "captainmarvel@marvel.com", "team": "marvel"},
        ]
        db.users.insert_many(users)
        db.users.create_index([('email', pymongo.ASCENDING)], unique=True)

        # Данные команд
        teams = [
            {"name": "marvel", "members": ["Iron Man", "Spider-Man", "Captain Marvel"]},
            {"name": "dc", "members": ["Superman", "Batman", "Wonder Woman"]},
        ]
        db.teams.insert_many(teams)

        # Данные активностей
        activities = [
            {"user": "Superman", "activity": "Flight", "duration": 60},
            {"user": "Batman", "activity": "Martial Arts", "duration": 45},
            {"user": "Iron Man", "activity": "Suit Training", "duration": 50},
            {"user": "Spider-Man", "activity": "Web Swinging", "duration": 40},
        ]
        db.activities.insert_many(activities)

        # Данные лидерборда
        leaderboard = [
            {"user": "Superman", "score": 100},
            {"user": "Iron Man", "score": 95},
            {"user": "Batman", "score": 90},
        ]
        db.leaderboard.insert_many(leaderboard)

        # Данные тренировок
        workouts = [
            {"user": "Superman", "workout": "Strength", "reps": 100},
            {"user": "Wonder Woman", "workout": "Agility", "reps": 80},
            {"user": "Captain Marvel", "workout": "Endurance", "reps": 90},
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db успешно заполнена тестовыми данными!'))
