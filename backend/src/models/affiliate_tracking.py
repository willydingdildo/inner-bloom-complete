from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import uuid
import hashlib
import secrets

db = SQLAlchemy()

class AffiliateProgram(db.Model):
    __tablename__ = 'affiliate_programs'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    commission_rate = db.Column(db.Float, nullable=False)  # Percentage
    commission_type = db.Column(db.String(20), default='percentage')  # percentage, fixed
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    affiliate_url = db.Column(db.String(500), nullable=False)
    tracking_method = db.Column(db.String(50), default='url_param')  # url_param, pixel, api
    cookie_duration = db.Column(db.Integer, default=30)  # days
    minimum_payout = db.Column(db.Float, default=25.0)
    payment_schedule = db.Column(db.String(20), default='monthly')  # weekly, monthly, quarterly
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    clicks = db.relationship('AffiliateClick', backref='program', lazy=True)
    conversions = db.relationship('AffiliateConversion', backref='program', lazy=True)

class UserAffiliateLink(db.Model):
    __tablename__ = 'user_affiliate_links'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey('affiliate_programs.id'), nullable=False)
    unique_code = db.Column(db.String(50), unique=True, nullable=False)
    custom_url = db.Column(db.String(500))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Performance metrics
    total_clicks = db.Column(db.Integer, default=0)
    total_conversions = db.Column(db.Integer, default=0)
    total_earnings = db.Column(db.Float, default=0.0)
    
    # Relationships
    clicks = db.relationship('AffiliateClick', backref='user_link', lazy=True)
    conversions = db.relationship('AffiliateConversion', backref='user_link', lazy=True)
    
    def __init__(self, **kwargs):
        super(UserAffiliateLink, self).__init__(**kwargs)
        if not self.unique_code:
            self.unique_code = self.generate_unique_code()
    
    def generate_unique_code(self):
        """Generate a unique tracking code for the user"""
        base_string = f"{self.user_id}_{self.program_id}_{datetime.utcnow().timestamp()}"
        return hashlib.md5(base_string.encode()).hexdigest()[:12].upper()

class AffiliateClick(db.Model):
    __tablename__ = 'affiliate_clicks'
    
    id = db.Column(db.Integer, primary_key=True)
    user_link_id = db.Column(db.Integer, db.ForeignKey('user_affiliate_links.id'), nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey('affiliate_programs.id'), nullable=False)
    visitor_ip = db.Column(db.String(45))
    visitor_user_agent = db.Column(db.String(500))
    referrer_url = db.Column(db.String(500))
    click_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    session_id = db.Column(db.String(100))
    converted = db.Column(db.Boolean, default=False)
    conversion_value = db.Column(db.Float, default=0.0)

class AffiliateConversion(db.Model):
    __tablename__ = 'affiliate_conversions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_link_id = db.Column(db.Integer, db.ForeignKey('user_affiliate_links.id'), nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey('affiliate_programs.id'), nullable=False)
    click_id = db.Column(db.Integer, db.ForeignKey('affiliate_clicks.id'))
    
    # Conversion details
    conversion_value = db.Column(db.Float, nullable=False)
    commission_earned = db.Column(db.Float, nullable=False)
    conversion_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    external_transaction_id = db.Column(db.String(100))
    
    # Status tracking
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected, paid
    approved_at = db.Column(db.DateTime)
    paid_at = db.Column(db.DateTime)
    rejection_reason = db.Column(db.String(200))

class UserEarnings(db.Model):
    __tablename__ = 'user_earnings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Earnings breakdown
    referral_earnings = db.Column(db.Float, default=0.0)
    affiliate_earnings = db.Column(db.Float, default=0.0)
    content_earnings = db.Column(db.Float, default=0.0)
    community_earnings = db.Column(db.Float, default=0.0)
    total_earnings = db.Column(db.Float, default=0.0)
    
    # Payout tracking
    total_paid = db.Column(db.Float, default=0.0)
    pending_payout = db.Column(db.Float, default=0.0)
    last_payout_date = db.Column(db.DateTime)
    
    # Payment preferences
    payment_method = db.Column(db.String(20), default='paypal')  # paypal, venmo, bank, crypto
    payment_email = db.Column(db.String(100))
    payment_details = db.Column(db.JSON)  # Store encrypted payment info (e.g., bank details, crypto wallet)
    payout_frequency = db.Column(db.String(20), default='monthly') # weekly, monthly

    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PayoutRequest(db.Model):
    __tablename__ = 'payout_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(20), nullable=False)
    payment_details = db.Column(db.JSON)
    
    # Status tracking
    status = db.Column(db.String(20), default='pending')  # pending, processing, completed, failed
    requested_at = db.Column(db.DateTime, default=datetime.utcnow)
    processed_at = db.Column(db.DateTime)
    transaction_id = db.Column(db.String(100))
    notes = db.Column(db.Text)

class ViralContentTracking(db.Model):
    __tablename__ = 'viral_content_tracking'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content_type = db.Column(db.String(50), nullable=False)  # instagram, tiktok, youtube, blog
    platform_url = db.Column(db.String(500))
    content_description = db.Column(db.Text)
    
    # Performance metrics
    views = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)
    shares = db.Column(db.Integer, default=0)
    comments = db.Column(db.Integer, default=0)
    click_throughs = db.Column(db.Integer, default=0)
    
    # Earnings
    base_reward = db.Column(db.Float, default=0.0)
    performance_bonus = db.Column(db.Float, default=0.0)
    total_earned = db.Column(db.Float, default=0.0)
    
    # Status
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected, paid
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime)
    paid_at = db.Column(db.DateTime)

class ReferralTracking(db.Model):
    __tablename__ = 'referral_tracking'
    
    id = db.Column(db.Integer, primary_key=True)
    referrer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    referred_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    referral_code = db.Column(db.String(50), nullable=False)
    
    # Multi-level tracking
    level = db.Column(db.Integer, default=1)  # 1st, 2nd, 3rd level referral
    parent_referral_id = db.Column(db.Integer, db.ForeignKey('referral_tracking.id'), nullable=True)
    
    # Conversion tracking
    referred_at = db.Column(db.DateTime, default=datetime.utcnow)
    converted_at = db.Column(db.DateTime)  # When they became paying customer
    subscription_type = db.Column(db.String(20))  # free, premium, vip, product_purchase
    payment_status = db.Column(db.String(20), default='pending') # pending, completed, refunded
    refund_period_ends_at = db.Column(db.DateTime, nullable=True)
    
    # Earnings
    referral_bonus = db.Column(db.Float, default=0.0)
    lifetime_value = db.Column(db.Float, default=0.0)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    status = db.Column(db.String(20), default='pending')  # pending, converted, churned, bonus_paid

# Utility functions for affiliate tracking

def create_affiliate_link(user_id, program_id, custom_params=None):
    """Create a tracked affiliate link for a user"""
    program = AffiliateProgram.query.get(program_id)
    if not program:
        return None
    
    # Check if user already has a link for this program
    existing_link = UserAffiliateLink.query.filter_by(
        user_id=user_id, 
        program_id=program_id
    ).first()
    
    if existing_link:
        return existing_link
    
    # Create new affiliate link
    user_link = UserAffiliateLink(
        user_id=user_id,
        program_id=program_id
    )
    
    db.session.add(user_link)
    db.session.commit()
    
    # Generate the actual tracking URL
    base_url = program.affiliate_url
    tracking_param = f"ib_ref={user_link.unique_code}"
    
    if '?' in base_url:
        user_link.custom_url = f"{base_url}&{tracking_param}"
    else:
        user_link.custom_url = f"{base_url}?{tracking_param}"
    
    if custom_params:
        for key, value in custom_params.items():
            user_link.custom_url += f"&{key}={value}"
    
    db.session.commit()
    return user_link

def track_affiliate_click(user_link_id, visitor_data):
    """Track an affiliate link click"""
    click = AffiliateClick(
        user_link_id=user_link_id,
        program_id=UserAffiliateLink.query.get(user_link_id).program_id,
        visitor_ip=visitor_data.get('ip'),
        visitor_user_agent=visitor_data.get('user_agent'),
        referrer_url=visitor_data.get('referrer'),
        session_id=visitor_data.get('session_id')
    )
    
    db.session.add(click)
    
    # Update click count
    user_link = UserAffiliateLink.query.get(user_link_id)
    user_link.total_clicks += 1
    
    db.session.commit()
    return click

def record_affiliate_conversion(user_link_id, conversion_value, external_transaction_id=None):
    """Record an affiliate conversion"""
    user_link = UserAffiliateLink.query.get(user_link_id)
    program = user_link.program
    
    # Calculate commission
    if program.commission_type == 'percentage':
        commission = conversion_value * (program.commission_rate / 100)
    else:
        commission = program.commission_rate
    
    # Create conversion record
    conversion = AffiliateConversion(
        user_link_id=user_link_id,
        program_id=program.id,
        conversion_value=conversion_value,
        commission_earned=commission,
        external_transaction_id=external_transaction_id
    )
    
    db.session.add(conversion)
    
    # Update user link stats
    user_link.total_conversions += 1
    user_link.total_earnings += commission
    
    # Update user earnings
    user_earnings = UserEarnings.query.filter_by(user_id=user_link.user_id).first()
    if not user_earnings:
        user_earnings = UserEarnings(user_id=user_link.user_id)
        db.session.add(user_earnings)
    
    user_earnings.affiliate_earnings += commission
    user_earnings.total_earnings += commission
    user_earnings.pending_payout += commission
    
    db.session.commit()
    return conversion

def calculate_referral_bonus(referrer_id, referred_user_id, subscription_type, parent_referral_id=None):
    """Calculate and award referral bonuses based on tier system and Sister Circle logic"""
    # Get referrer's current converted referral count (excluding the current one if it's a new conversion)
    referrer_converted_count = ReferralTracking.query.filter_by(
        referrer_id=referrer_id, 
        payment_status='completed'
    ).count()
    
    # Determine tier and base bonus amount
    if referrer_converted_count < 4:
        bonus = 10.0  # Bronze
    elif referrer_converted_count < 14:
        bonus = 15.0  # Silver
    elif referrer_converted_count < 29:
        bonus = 25.0  # Gold
    else:
        bonus = 50.0  # Platinum
    
    # Sister Circle (3-level depth)
    current_level = 1
    current_referrer_id = referrer_id
    
    while current_level <= 3 and current_referrer_id:
        referral_bonus_amount = bonus
        if current_level == 2: # 50% bonus for level 2
            referral_bonus_amount *= 0.5
        elif current_level == 3: # 25% bonus for level 3
            referral_bonus_amount *= 0.25

        # Create or update ReferralTracking entry
        referral_entry = ReferralTracking.query.filter_by(
            referrer_id=current_referrer_id,
            referred_id=referred_user_id,
            level=current_level
        ).first()

        if not referral_entry:
            referral_entry = ReferralTracking(
                referrer_id=current_referrer_id,
                referred_id=referred_user_id,
                referral_code=f"REF{current_referrer_id}{referred_user_id}{secrets.token_hex(4)}",
                level=current_level,
                parent_referral_id=parent_referral_id if current_level > 1 else None,
                subscription_type=subscription_type,
                payment_status='completed', # Assuming this function is called after payment
                converted_at=datetime.utcnow(),
                referral_bonus=referral_bonus_amount,
                refund_period_ends_at=datetime.utcnow() + timedelta(days=7) # Example 7-day refund period
            )
            db.session.add(referral_entry)
        else:
            referral_entry.referral_bonus += referral_bonus_amount # Add to existing if already tracked
            referral_entry.payment_status = 'completed'
            referral_entry.converted_at = datetime.utcnow()
            referral_entry.subscription_type = subscription_type
            referral_entry.refund_period_ends_at = datetime.utcnow() + timedelta(days=7)

        # Update user earnings for the current referrer
        user_earnings = UserEarnings.query.filter_by(user_id=current_referrer_id).first()
        if not user_earnings:
            user_earnings = UserEarnings(user_id=current_referrer_id)
            db.session.add(user_earnings)
        
        user_earnings.referral_earnings += referral_bonus_amount
        user_earnings.total_earnings += referral_bonus_amount
        user_earnings.pending_payout += referral_bonus_amount # Funds held in pending
        
        db.session.commit()

        # Move to the next level referrer
        if current_level < 3: # Only proceed if there's a next level
            # Find the referrer of the current_referrer_id
            parent_referral_entry = ReferralTracking.query.filter_by(referred_id=current_referrer_id, level=1).first()
            if parent_referral_entry: # Check if the current_referrer_id was itself referred
                parent_referral_id = parent_referral_entry.id # Pass the ID of the parent referral entry
                current_referrer_id = parent_referral_entry.referrer_id
                current_level += 1
            else:
                current_referrer_id = None # No more referrers in the chain
        else:
            current_referrer_id = None # Max level reached

    return bonus

def process_viral_content_reward(user_id, content_type, performance_metrics):
    """Process rewards for viral content creation"""
    base_rewards = {
        'instagram': 5.0,
        'tiktok': 15.0,
        'youtube': 50.0,
        'blog': 25.0,
        'podcast': 100.0
    }
    
    base_reward = base_rewards.get(content_type, 5.0)
    
    # Performance bonus calculation
    performance_bonus = 0.0
    if performance_metrics.get('views', 0) > 1000:
        performance_bonus += 10.0
    if performance_metrics.get('shares', 0) > 100:
        performance_bonus += 15.0
    if performance_metrics.get('click_throughs', 0) > 50:
        performance_bonus += 20.0
    
    total_reward = base_reward + performance_bonus
    
    # Create tracking record
    content_tracking = ViralContentTracking(
        user_id=user_id,
        content_type=content_type,
        base_reward=base_reward,
        performance_bonus=performance_bonus,
        total_earned=total_reward,
        **performance_metrics
    )
    
    db.session.add(content_tracking)
    
    # Update user earnings
    user_earnings = UserEarnings.query.filter_by(user_id=user_id).first()
    if not user_earnings:
        user_earnings = UserEarnings(user_id=user_id)
        db.session.add(user_earnings)
    
    user_earnings.content_earnings += total_reward
    user_earnings.total_earnings += total_reward
    user_earnings.pending_payout += total_reward
    
    db.session.commit()
    return total_reward

# Function to check and process payouts based on thresholds and refund periods
def check_and_process_payouts():
    """Checks pending payouts and processes them if conditions are met"""
    users_with_pending_payouts = UserEarnings.query.filter(UserEarnings.pending_payout >= 25.0).all()
    
    for user_earnings in users_with_pending_payouts:
        # Check if all associated conversions/referrals have passed their refund period
        eligible_for_payout = True
        
        # Check affiliate conversions
        pending_affiliate_conversions = AffiliateConversion.query.filter(
            AffiliateConversion.user_link.has(user_id=user_earnings.user_id),
            AffiliateConversion.status == 'pending'
        ).all()
        
        for conv in pending_affiliate_conversions:
            # Assuming a refund period for affiliate conversions as well, or they are approved by admin
            # For simplicity, let's assume 'pending' means waiting for admin approval or refund period
            # If status is 'pending' and not yet approved, it's not eligible
            if conv.status == 'pending': # This needs to be updated by an admin process or automated check
                eligible_for_payout = False
                break
        
        if not eligible_for_payout: continue

        # Check referral bonuses
        pending_referrals = ReferralTracking.query.filter(
            ReferralTracking.referrer_id == user_earnings.user_id,
            ReferralTracking.payment_status == 'completed', # Payment completed by referred user
            ReferralTracking.status != 'bonus_paid' # Not yet paid out
        ).all()

        for ref in pending_referrals:
            if ref.refund_period_ends_at and datetime.utcnow() < ref.refund_period_ends_at:
                eligible_for_payout = False
                break
        
        if not eligible_for_payout: continue

        # If all checks pass, move pending to total_paid and reset pending
        if eligible_for_payout:
            payout_amount = user_earnings.pending_payout
            user_earnings.total_paid += payout_amount
            user_earnings.pending_payout = 0.0
            user_earnings.last_payout_date = datetime.utcnow()
            
            # Mark processed referrals as paid
            for ref in pending_referrals:
                ref.status = 'bonus_paid'

            # Create a payout request record
            payout_request = PayoutRequest(
                user_id=user_earnings.user_id,
                amount=payout_amount,
                payment_method=user_earnings.payment_method,
                payment_details=user_earnings.payment_details,
                status='processing'
            )
            db.session.add(payout_request)
            db.session.commit()
            print(f"Processed payout of ${payout_amount:.2f} for user {user_earnings.user_id}")

# Note on South African VAT:
# The system will not explicitly prevent SA users from using it.
# Instead, a disclaimer will be added during registration and in the terms of service
# advising users of their own tax obligations based on their location and earnings.
# For users exceeding the R1 million threshold, it will be their responsibility to comply with SA VAT laws.
# The platform will provide exportable earnings statements to assist users with their tax filings.
# This avoids complex geo-blocking and ensures global accessibility while placing responsibility on the user.

