#!/usr/bin/env python3

from random import choice as rc

from faker import Faker

from app import app
from models import db, Message


fake = Faker()

usernames = [fake.first_name() for i in range(4)]
if "Duane" not in usernames:
    usernames.append("Duane")

def seed_data():  # Renamed to match what conftest.py expects
    Message.query.delete()
    
    messages = [
        Message(
            body="Hello ",
            username="Liza"
        ),
        Message(
            body="Test message",
            username="TestUser"
        )
    ]

    # Add some random messages too
    for i in range(5):
        messages.append(Message(
            body=fake.sentence(),
            username=rc(usernames)
        ))

    db.session.add_all(messages)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        seed_data()
