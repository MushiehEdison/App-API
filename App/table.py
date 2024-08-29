from FlaskApp import app, db
from FlaskApp.models import User

def create_tables():
    with app.app_context():
        db.create_all()
        print("Tables created successfully.")

if __name__ == "__main__":
    create_tables()