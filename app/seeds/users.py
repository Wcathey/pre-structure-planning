from app.models import db, User, environment, SCHEMA
from sqlalchemy.sql import text


# Adds a demo user, you can add other users here if you want
def seed_users():
    first_client = User(
        first_name="John", last_name="Doe", username='Client1', email='client1@aa.io', phone_number='210-555-5555', password='password', user_type="CLIENT", isDemo=True)
    second_client = User(
        first_name="Jane", last_name="Dawn", username='Client2', email='client2.io', phone_number='210-555-4545', password='password', user_type="CLIENT", isDemo=True)
    first_preserver = User(
        first_name="Scanner", last_name="Jim", username='Preserver1', email='preserver1@aa.io', phone_number='830-545-6245', password='password', user_type="PRESERVER", isDemo=True)
    second_preserver = User(
        first_name="Scanner", last_name="Bob", username='Preserver2', email='preserver2@aa.io', phone_number='756-622-6280', password='password', user_type="PRESERVER", isDemo=True)

    demo_admin = User(
        first_name="Peter", last_name="Parker", username='Admin1', email='admin@smh.io', phone_number='756-888-8888', password='password', user_type="ADMIN", isDemo=True)

    db.session.add(first_client)
    db.session.add(second_client)
    db.session.add(first_preserver)
    db.session.add(second_preserver)
    db.session.add(demo_admin)
    db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the users table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_users():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.users RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM users"))

    db.session.commit()
