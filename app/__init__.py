from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# Initialize extensions outside the factory
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    # Adding instance_relative_config=True helps locate the DB file easily
    app = Flask(__name__, instance_relative_config=True)

    # 1. SECURITY & DATABASE CONFIG
    app.config['SECRET_KEY'] = 'dev-key-123-change-this-later' 
    
    # We use os.path to make sure the DB is created in your main project folder
    basedir = os.path.abspath(os.path.dirname(__file__))
    # Database is placed in the root directory
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(basedir), 'study_planner.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 2. INITIALIZE EXTENSIONS
    db.init_app(app)
    login_manager.init_app(app)
    
    # Tells Flask-Login which route handles logging in
    login_manager.login_view = 'login' 
    login_manager.login_message_category = 'info' 

    with app.app_context():
        # Import models and routes INSIDE context to prevent SAWarning
        from . import models, routes
        
        # Create tables only if they don't exist
        db.create_all()

    return app

# Move the user_loader OUTSIDE create_app to keep the factory clean
@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))