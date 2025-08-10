from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    bloom_name = db.Column(db.String(100), nullable=True)
    bloom_backstory = db.Column(db.Text, nullable=True)
    title = db.Column(db.String(100), nullable=True) # New field for identity marker/title    
    # Referral tracking fields
    referred_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True) # ID of the user who referred this user
    referral_code_used = db.Column(db.String(50), nullable=True) # The specific referral code used by this user
    join_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'bloom_name': self.bloom_name,
            'bloom_backstory': self.bloom_backstory,
            'title': self.title,            'referred_by_id': self.referred_by_id,
            'referral_code_used': self.referral_code_used,
            'join_date': self.join_date.isoformat()
        }


