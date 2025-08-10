from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class SisterhoodCircle(db.Model):
    """Private groups for deeper connection and accountability"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    max_members = db.Column(db.Integer, default=10)
    current_members = db.Column(db.Integer, default=1)
    focus_area = db.Column(db.String(100))  # e.g., "career", "wellness", "entrepreneurship"
    is_private = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'creator_id': self.creator_id,
            'max_members': self.max_members,
            'current_members': self.current_members,
            'focus_area': self.focus_area,
            'is_private': self.is_private,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class CircleMembership(db.Model):
    """Membership in sisterhood circles"""
    id = db.Column(db.Integer, primary_key=True)
    circle_id = db.Column(db.Integer, db.ForeignKey('sisterhood_circle.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role = db.Column(db.String(20), default='member')  # "creator", "moderator", "member"
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'circle_id': self.circle_id,
            'user_id': self.user_id,
            'role': self.role,
            'joined_at': self.joined_at.isoformat() if self.joined_at else None
        }

class CommunityPost(db.Model):
    """Posts in community forums and circles"""
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    circle_id = db.Column(db.Integer, db.ForeignKey('sisterhood_circle.id'))  # None for public posts
    title = db.Column(db.String(200))
    content = db.Column(db.Text, nullable=False)
    post_type = db.Column(db.String(50))  # "story", "question", "celebration", "support"
    tags = db.Column(db.Text)  # JSON array of tags
    likes_count = db.Column(db.Integer, default=0)
    comments_count = db.Column(db.Integer, default=0)
    is_anonymous = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'author_id': self.author_id,
            'circle_id': self.circle_id,
            'title': self.title,
            'content': self.content,
            'post_type': self.post_type,
            'tags': self.tags,
            'likes_count': self.likes_count,
            'comments_count': self.comments_count,
            'is_anonymous': self.is_anonymous,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class PostComment(db.Model):
    """Comments on community posts"""
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('community_post.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    parent_comment_id = db.Column(db.Integer, db.ForeignKey('post_comment.id'))  # For nested comments
    likes_count = db.Column(db.Integer, default=0)
    is_anonymous = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'post_id': self.post_id,
            'author_id': self.author_id,
            'content': self.content,
            'parent_comment_id': self.parent_comment_id,
            'likes_count': self.likes_count,
            'is_anonymous': self.is_anonymous,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class VirtualHug(db.Model):
    """Virtual hugs sent between users"""
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # None for anonymous hugs
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # None for global hugs
    message = db.Column(db.Text)
    hug_type = db.Column(db.String(50), default='general')  # "encouragement", "celebration", "support"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'sender_id': self.sender_id,
            'recipient_id': self.recipient_id,
            'message': self.message,
            'hug_type': self.hug_type,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class UserAchievement(db.Model):
    """User achievements and badges"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    achievement_type = db.Column(db.String(50))  # "streak", "milestone", "community", "growth"
    achievement_name = db.Column(db.String(200))
    description = db.Column(db.Text)
    badge_icon = db.Column(db.String(100))  # Icon identifier
    points_earned = db.Column(db.Integer, default=0)
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'achievement_type': self.achievement_type,
            'achievement_name': self.achievement_name,
            'description': self.description,
            'badge_icon': self.badge_icon,
            'points_earned': self.points_earned,
            'earned_at': self.earned_at.isoformat() if self.earned_at else None
        }

class UserEngagement(db.Model):
    """Track user engagement metrics"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    daily_streak = db.Column(db.Integer, default=0)
    total_points = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    last_active = db.Column(db.DateTime, default=datetime.utcnow)
    total_hugs_sent = db.Column(db.Integer, default=0)
    total_hugs_received = db.Column(db.Integer, default=0)
    posts_created = db.Column(db.Integer, default=0)
    comments_made = db.Column(db.Integer, default=0)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'daily_streak': self.daily_streak,
            'total_points': self.total_points,
            'level': self.level,
            'last_active': self.last_active.isoformat() if self.last_active else None,
            'total_hugs_sent': self.total_hugs_sent,
            'total_hugs_received': self.total_hugs_received,
            'posts_created': self.posts_created,
            'comments_made': self.comments_made
        }

class ShareableContent(db.Model):
    """Content designed for viral sharing"""
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content_type = db.Column(db.String(50))  # "growth_path", "outfit", "milestone", "quote"
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    content_data = db.Column(db.Text)  # JSON data specific to content type
    share_count = db.Column(db.Integer, default=0)
    view_count = db.Column(db.Integer, default=0)
    conversion_count = db.Column(db.Integer, default=0)  # How many viewers signed up
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'creator_id': self.creator_id,
            'content_type': self.content_type,
            'title': self.title,
            'description': self.description,
            'content_data': self.content_data,
            'share_count': self.share_count,
            'view_count': self.view_count,
            'conversion_count': self.conversion_count,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

