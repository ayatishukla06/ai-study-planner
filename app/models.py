from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    daily_limit = db.Column(db.Integer, default=4)  # Default 4 hours/day
    subjects = db.relationship('Subject', backref='owner', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    topics = db.relationship('Topic', backref='subject', lazy=True)
    def get_progress(self):
        total = len(self.topics)
        if total == 0:
            return 0
        completed = len([t for t in self.topics if t.is_completed])
        return int((completed / total) * 100)

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    priority = db.Column(db.Integer, default=1) # 1=Low, 3=High
    estimated_time = db.Column(db.Integer) # In minutes
    is_completed = db.Column(db.Boolean, default=False)

class StudyPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)
    scheduled_date = db.Column(db.Date, nullable=False)
    topic = db.relationship('Topic', backref='planned_dates')

class ProgressLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow)
    completion_rate = db.Column(db.Float) # e.g., 0.85 for 85%

class User(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False) 
    password_hash = db.Column(db.String(128), nullable=False)

    # Helper methods for hashing
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)