from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class DigitalWardrobe(db.Model):
    """User's digital wardrobe items"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50))  # e.g., "tops", "bottoms", "dresses", "accessories"
    color = db.Column(db.String(50))
    brand = db.Column(db.String(100))
    size = db.Column(db.String(20))
    image_url = db.Column(db.String(500))
    purchase_date = db.Column(db.Date)
    cost = db.Column(db.Float)
    sustainability_score = db.Column(db.Integer)  # 1-10 sustainability rating
    is_available = db.Column(db.Boolean, default=True)  # for swapping/selling
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'item_name': self.item_name,
            'category': self.category,
            'color': self.color,
            'brand': self.brand,
            'size': self.size,
            'image_url': self.image_url,
            'purchase_date': self.purchase_date.isoformat() if self.purchase_date else None,
            'cost': self.cost,
            'sustainability_score': self.sustainability_score,
            'is_available': self.is_available,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class OutfitCombination(db.Model):
    """AI-generated or user-created outfit combinations"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    outfit_name = db.Column(db.String(200))
    wardrobe_items = db.Column(db.Text)  # JSON array of wardrobe item IDs
    occasion = db.Column(db.String(100))  # e.g., "work", "casual", "date night"
    season = db.Column(db.String(20))
    ai_generated = db.Column(db.Boolean, default=False)
    likes_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'outfit_name': self.outfit_name,
            'wardrobe_items': self.wardrobe_items,
            'occasion': self.occasion,
            'season': self.season,
            'ai_generated': self.ai_generated,
            'likes_count': self.likes_count,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class StyleProfile(db.Model):
    """User's style preferences and body measurements"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    style_preferences = db.Column(db.Text)  # JSON of style tags
    body_measurements = db.Column(db.Text)  # JSON of measurements (encrypted)
    preferred_colors = db.Column(db.Text)  # JSON array
    budget_range = db.Column(db.String(50))
    sustainability_priority = db.Column(db.Integer)  # 1-10 scale
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'style_preferences': self.style_preferences,
            'body_measurements': self.body_measurements,
            'preferred_colors': self.preferred_colors,
            'budget_range': self.budget_range,
            'sustainability_priority': self.sustainability_priority,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }

class MarketplaceListing(db.Model):
    """Items listed for sale or swap in the peer-to-peer marketplace"""
    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    wardrobe_item_id = db.Column(db.Integer, db.ForeignKey('digital_wardrobe.id'), nullable=False)
    listing_type = db.Column(db.String(20))  # "sale" or "swap"
    price = db.Column(db.Float)  # for sales
    swap_preferences = db.Column(db.Text)  # JSON for swap criteria
    condition = db.Column(db.String(50))  # "new", "like new", "good", "fair"
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'seller_id': self.seller_id,
            'wardrobe_item_id': self.wardrobe_item_id,
            'listing_type': self.listing_type,
            'price': self.price,
            'swap_preferences': self.swap_preferences,
            'condition': self.condition,
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class StyleFeedback(db.Model):
    """Community feedback on outfits and style choices"""
    id = db.Column(db.Integer, primary_key=True)
    outfit_id = db.Column(db.Integer, db.ForeignKey('outfit_combination.id'), nullable=False)
    commenter_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    feedback_type = db.Column(db.String(20))  # "like", "love", "comment"
    comment_text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'outfit_id': self.outfit_id,
            'commenter_id': self.commenter_id,
            'feedback_type': self.feedback_type,
            'comment_text': self.comment_text,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

