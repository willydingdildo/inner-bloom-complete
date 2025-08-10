from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Subscription(db.Model):
    """User subscription management"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    plan_type = db.Column(db.String(50))  # "free", "premium", "vip"
    stripe_subscription_id = db.Column(db.String(200))
    stripe_customer_id = db.Column(db.String(200))
    status = db.Column(db.String(50))  # "active", "canceled", "past_due", "trialing"
    current_period_start = db.Column(db.DateTime)
    current_period_end = db.Column(db.DateTime)
    monthly_price = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'plan_type': self.plan_type,
            'stripe_subscription_id': self.stripe_subscription_id,
            'stripe_customer_id': self.stripe_customer_id,
            'status': self.status,
            'current_period_start': self.current_period_start.isoformat() if self.current_period_start else None,
            'current_period_end': self.current_period_end.isoformat() if self.current_period_end else None,
            'monthly_price': self.monthly_price,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class DigitalProduct(db.Model):
    """Digital products for sale"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100))  # "ebook", "course", "template", "meditation"
    price = db.Column(db.Float, nullable=False)
    stripe_price_id = db.Column(db.String(200))
    file_url = db.Column(db.String(500))  # URL to downloadable content
    preview_content = db.Column(db.Text)
    tags = db.Column(db.Text)  # JSON array of tags
    sales_count = db.Column(db.Integer, default=0)
    rating_average = db.Column(db.Float, default=0.0)
    rating_count = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'price': self.price,
            'stripe_price_id': self.stripe_price_id,
            'file_url': self.file_url,
            'preview_content': self.preview_content,
            'tags': self.tags,
            'sales_count': self.sales_count,
            'rating_average': self.rating_average,
            'rating_count': self.rating_count,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Purchase(db.Model):
    """Record of digital product purchases"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('digital_product.id'), nullable=False)
    stripe_payment_intent_id = db.Column(db.String(200))
    amount_paid = db.Column(db.Float)
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'stripe_payment_intent_id': self.stripe_payment_intent_id,
            'amount_paid': self.amount_paid,
            'purchase_date': self.purchase_date.isoformat() if self.purchase_date else None
        }

class AffiliateLink(db.Model):
    """Affiliate marketing links and tracking"""
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(200), nullable=False)
    affiliate_url = db.Column(db.String(500), nullable=False)
    commission_rate = db.Column(db.Float)  # Percentage
    category = db.Column(db.String(100))  # "wellness", "fashion", "business", "books"
    description = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    click_count = db.Column(db.Integer, default=0)
    conversion_count = db.Column(db.Integer, default=0)
    total_commission = db.Column(db.Float, default=0.0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_name': self.product_name,
            'affiliate_url': self.affiliate_url,
            'commission_rate': self.commission_rate,
            'category': self.category,
            'description': self.description,
            'image_url': self.image_url,
            'click_count': self.click_count,
            'conversion_count': self.conversion_count,
            'total_commission': self.total_commission,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class AffiliateClick(db.Model):
    """Track affiliate link clicks"""
    id = db.Column(db.Integer, primary_key=True)
    affiliate_link_id = db.Column(db.Integer, db.ForeignKey('affiliate_link.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # May be null for non-logged-in users
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    referrer = db.Column(db.String(500))
    clicked_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'affiliate_link_id': self.affiliate_link_id,
            'user_id': self.user_id,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'referrer': self.referrer,
            'clicked_at': self.clicked_at.isoformat() if self.clicked_at else None
        }

class ReferralProgram(db.Model):
    """User referral program tracking"""
    id = db.Column(db.Integer, primary_key=True)
    referrer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    referred_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    referral_code = db.Column(db.String(50), unique=True)
    commission_earned = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='pending')  # "pending", "confirmed", "paid"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'referrer_id': self.referrer_id,
            'referred_id': self.referred_id,
            'referral_code': self.referral_code,
            'commission_earned': self.commission_earned,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class RevenueMetrics(db.Model):
    """Daily revenue and metrics tracking"""
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, unique=True)
    subscription_revenue = db.Column(db.Float, default=0.0)
    digital_product_revenue = db.Column(db.Float, default=0.0)
    affiliate_commission = db.Column(db.Float, default=0.0)
    transaction_fees = db.Column(db.Float, default=0.0)
    total_revenue = db.Column(db.Float, default=0.0)
    new_subscribers = db.Column(db.Integer, default=0)
    canceled_subscriptions = db.Column(db.Integer, default=0)
    active_users = db.Column(db.Integer, default=0)
    
    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.isoformat() if self.date else None,
            'subscription_revenue': self.subscription_revenue,
            'digital_product_revenue': self.digital_product_revenue,
            'affiliate_commission': self.affiliate_commission,
            'transaction_fees': self.transaction_fees,
            'total_revenue': self.total_revenue,
            'new_subscribers': self.new_subscribers,
            'canceled_subscriptions': self.canceled_subscriptions,
            'active_users': self.active_users
        }

