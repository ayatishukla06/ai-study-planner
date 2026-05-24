import os

class Config:
    # This creates a path for the database file in your main folder
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    # The 'Secret Key' is for security (like your Finance Buddy project)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-123'
    
    # This tells SQLAlchemy exactly where to create the 'study_planner.db'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'study_planner.db')
    
    # Keeps the app fast by not tracking every tiny change
    SQLALCHEMY_TRACK_MODIFICATIONS = False