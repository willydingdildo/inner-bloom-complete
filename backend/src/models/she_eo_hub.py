from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class BusinessProfile(db.Model):
    """User's business/entrepreneurial profile"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    business_stage = db.Column(db.String(50))  # "idea", "startup", "growth", "established"
    industry = db.Column(db.String(100))
    business_goals = db.Column(db.Text)  # JSON array of goals
    skills = db.Column(db.Text)  # JSON array of skills
    experience_level = db.Column(db.String(50))
    funding_status = db.Column(db.String(50))
    revenue_stage = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'business_stage': self.business_stage,
            'industry': self.industry,
            'business_goals': self.business_goals,
            'skills': self.skills,
            'experience_level': self.experience_level,
            'funding_status': self.funding_status,
            'revenue_stage': self.revenue_stage,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class BusinessPlan(db.Model):
    """AI-generated or user-created business plans"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    business_name = db.Column(db.String(200))
    business_idea = db.Column(db.Text)
    target_market = db.Column(db.Text)
    revenue_model = db.Column(db.Text)
    marketing_strategy = db.Column(db.Text)
    financial_projections = db.Column(db.Text)  # JSON data
    ai_generated = db.Column(db.Boolean, default=False)
    completion_status = db.Column(db.Float, default=0.0)  # Percentage complete
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'business_name': self.business_name,
            'business_idea': self.business_idea,
            'target_market': self.target_market,
            'revenue_model': self.revenue_model,
            'marketing_strategy': self.marketing_strategy,
            'financial_projections': self.financial_projections,
            'ai_generated': self.ai_generated,
            'completion_status': self.completion_status,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }

class MentorshipConnection(db.Model):
    """Connections between mentors and mentees"""
    id = db.Column(db.Integer, primary_key=True)
    mentor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mentee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    connection_status = db.Column(db.String(20))  # "pending", "active", "completed"
    focus_areas = db.Column(db.Text)  # JSON array of focus areas
    session_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'mentor_id': self.mentor_id,
            'mentee_id': self.mentee_id,
            'connection_status': self.connection_status,
            'focus_areas': self.focus_areas,
            'session_count': self.session_count,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class FinancialGoal(db.Model):
    """User's financial goals and tracking"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    goal_type = db.Column(db.String(50))  # "savings", "revenue", "investment", "debt_reduction"
    goal_amount = db.Column(db.Float)
    current_amount = db.Column(db.Float, default=0.0)
    target_date = db.Column(db.Date)
    description = db.Column(db.Text)
    is_achieved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'goal_type': self.goal_type,
            'goal_amount': self.goal_amount,
            'current_amount': self.current_amount,
            'target_date': self.target_date.isoformat() if self.target_date else None,
            'description': self.description,
            'is_achieved': self.is_achieved,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class CourseProgress(db.Model):
    """User progress through educational courses"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.String(100))  # Reference to course content
    course_title = db.Column(db.String(200))
    progress_percentage = db.Column(db.Float, default=0.0)
    completed_modules = db.Column(db.Text)  # JSON array of completed module IDs
    quiz_scores = db.Column(db.Text)  # JSON object of quiz results
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'course_id': self.course_id,
            'course_title': self.course_title,
            'progress_percentage': self.progress_percentage,
            'completed_modules': self.completed_modules,
            'quiz_scores': self.quiz_scores,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

class InvestorConnection(db.Model):
    """Connections between entrepreneurs and investors"""
    id = db.Column(db.Integer, primary_key=True)
    entrepreneur_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    investor_name = db.Column(db.String(200))
    investor_type = db.Column(db.String(50))  # "angel", "vc", "grant", "crowdfunding"
    connection_stage = db.Column(db.String(50))  # "introduction", "pitch", "due_diligence", "funded"
    funding_amount = db.Column(db.Float)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'entrepreneur_id': self.entrepreneur_id,
            'investor_name': self.investor_name,
            'investor_type': self.investor_type,
            'connection_stage': self.connection_stage,
            'funding_amount': self.funding_amount,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

