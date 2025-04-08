from datetime import datetime

from app import app
from models import db, Message

class TestApp:
    '''Flask application in app.py'''

    # Remove class-level deletion of seeded messages

    def test_has_correct_columns(self):
        with app.app_context():

            hello_from_liza = Message(
                body="Hello 👋",
                username="Liza")
            
            db.session.add(hello_from_liza)
            db.session.commit()

            assert(hello_from_liza.body == "Hello 👋")
            assert(hello_from_liza.username == "Liza")
            assert(type(hello_from_liza.created_at) == datetime)

            db.session.delete(hello_from_liza)
            db.session.commit()

    def test_returns_list_of_json_objects_for_all_messages_in_database(self):
        '''returns a list of JSON objects for all messages in the database.'''
        with app.app_context():
            response = app.test_client().get('/messages')
            records = Message.query.all()

            for message in response.json:
                assert(message['id'] in [record.id for record in records])
                assert(message['body'] in [record.body for record in records])

    def test_creates_new_message_in_the_database(self):
        '''creates a new message in the database.'''
        with app.app_context():

            app.test_client().post(
                '/messages',
                json={
                    "body":"Hello 👋",
                    "username":"Liza",
                }
            )

            h = Message.query.filter_by(body="Hello 👋").first()
            assert(h)

            db.session.delete(h)
            db.session.commit()

    def test_returns_data_for_newly_created_message_as_json(self):
        '''returns data for the newly created message as JSON.'''
        with app.app_context():

            response = app.test_client().post(
                '/messages',
                json={
                    "body":"Hello 👋",
                    "username":"Liza",
                }
            )

            assert(response.content_type == 'application/json')

            assert(response.json["body"] == "Hello 👋")
            assert(response.json["username"] == "Liza")

            h = Message.query.filter_by(body="Hello 👋").first()
            assert(h)

            db.session.delete(h)
            db.session.commit()


    def test_updates_body_of_message_in_database(self):
        '''updates the body of a message in the database.'''
        with app.app_context():
            # Create test message
            test_msg = Message(
                body="Test message",
                username="TestUser"
            )
            db.session.add(test_msg)
            db.session.commit()

            id = test_msg.id
            body = test_msg.body

            # Update the message
            app.test_client().patch(
                f'/messages/{id}',
                json={
                    "body":"Goodbye 👋",
                }
            )

            # Verify update
            updated = Message.query.get(id)
            assert(updated.body == "Goodbye 👋")

            # Clean up
            db.session.delete(updated)
            db.session.commit()

    def test_returns_data_for_updated_message_as_json(self):
        '''returns data for the updated message as JSON.'''
        with app.app_context():
            # Create test message
            test_msg = Message(
                body="Test message",
                username="TestUser"
            )
            db.session.add(test_msg)
            db.session.commit()

            id = test_msg.id

            # Update the message
            response = app.test_client().patch(
                f'/messages/{id}',
                json={
                    "body":"Goodbye 👋",
                }
            )

            # Verify response
            assert(response.content_type == 'application/json')
            assert(response.json["body"] == "Goodbye 👋")

            # Clean up
            db.session.delete(test_msg)
            db.session.commit()

    def test_deletes_message_from_database(self):
        '''deletes the message from the database.'''
        with app.app_context():

            hello_from_liza = Message(
                body="Hello 👋",
                username="Liza")
            
            db.session.add(hello_from_liza)
            db.session.commit()

            app.test_client().delete(
                f'/messages/{hello_from_liza.id}'
            )

            h = Message.query.filter_by(body="Hello 👋").first()
            assert(not h)