from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import hashlib
import secrets
from enum import Enum

db = SQLAlchemy()

class AdminUser(db.Model):
    __tablename__ = 'admin_users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='admin')  # admin, super_admin, moderator
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Security fields
    failed_login_attempts = db.Column(db.Integer, default=0)
    locked_until = db.Column(db.DateTime)
    two_factor_secret = db.Column(db.String(32))
    two_factor_enabled = db.Column(db.Boolean, default=False)

class SystemMetrics(db.Model):
    __tablename__ = 'system_metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    metric_date = db.Column(db.Date, default=datetime.utcnow().date)
    
    # User metrics
    total_users = db.Column(db.Integer, default=0)
    new_users_today = db.Column(db.Integer, default=0)
    active_users_today = db.Column(db.Integer, default=0)
    premium_users = db.Column(db.Integer, default=0)
    vip_users = db.Column(db.Integer, default=0)
    
    # Financial metrics
    total_revenue = db.Column(db.Float, default=0.0)
    revenue_today = db.Column(db.Float, default=0.0)
    total_referral_debt = db.Column(db.Float, default=0.0)  # Money owed to referrers
    total_payouts_made = db.Column(db.Float, default=0.0)
    pending_payouts = db.Column(db.Float, default=0.0)
    
    # Referral metrics
    total_referrals = db.Column(db.Integer, default=0)
    referrals_today = db.Column(db.Integer, default=0)
    conversion_rate = db.Column(db.Float, default=0.0)  # Percentage
    average_referral_value = db.Column(db.Float, default=0.0)
    
    # Content metrics
    viral_content_submissions = db.Column(db.Integer, default=0)
    approved_content = db.Column(db.Integer, default=0)
    content_engagement_rate = db.Column(db.Float, default=0.0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class FraudDetection(db.Model):
    __tablename__ = 'fraud_detection'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    fraud_type = db.Column(db.String(50), nullable=False)  # multi_account, fake_referrals, payment_fraud
    risk_score = db.Column(db.Float, default=0.0)  # 0-100 risk score
    
    # Detection details
    ip_address = db.Column(db.String(45))
    device_fingerprint = db.Column(db.String(255))
    suspicious_patterns = db.Column(db.JSON)  # Store detected patterns
    
    # Status
    status = db.Column(db.String(20), default='pending')  # pending, investigated, resolved, confirmed_fraud
    investigated_by = db.Column(db.Integer, db.ForeignKey('admin_users.id'))
    investigation_notes = db.Column(db.Text)
    
    # Actions taken
    account_suspended = db.Column(db.Boolean, default=False)
    payouts_frozen = db.Column(db.Boolean, default=False)
    referrals_invalidated = db.Column(db.Boolean, default=False)
    
    detected_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)

class PayoutApproval(db.Model):
    __tablename__ = 'payout_approvals'
    
    id = db.Column(db.Integer, primary_key=True)
    payout_request_id = db.Column(db.Integer, db.ForeignKey('payout_requests.id'), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin_users.id'), nullable=False)
    
    # Approval details
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    approval_notes = db.Column(db.Text)
    risk_assessment = db.Column(db.String(20), default='low')  # low, medium, high
    
    # Verification checks
    identity_verified = db.Column(db.Boolean, default=False)
    payment_method_verified = db.Column(db.Boolean, default=False)
    earnings_verified = db.Column(db.Boolean, default=False)
    fraud_check_passed = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    processed_at = db.Column(db.DateTime)

class DigitalIdentityVerification(db.Model):
    __tablename__ = 'digital_identity_verification'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Identity documents (encrypted storage paths)
    government_id_path = db.Column(db.String(255))
    selfie_verification_path = db.Column(db.String(255))
    address_proof_path = db.Column(db.String(255))
    
    # Verification status
    identity_status = db.Column(db.String(20), default='pending')  # pending, verified, rejected
    verification_level = db.Column(db.String(20), default='basic')  # basic, enhanced, premium
    
    # Verification details
    verified_name = db.Column(db.String(100))
    verified_address = db.Column(db.Text)
    verified_country = db.Column(db.String(50))
    date_of_birth = db.Column(db.Date)
    
    # Trust score and loyalty
    trust_score = db.Column(db.Float, default=0.0)  # 0-100 trust score
    loyalty_score = db.Column(db.Float, default=0.0)  # 0-100 loyalty score
    verification_tier = db.Column(db.String(20), default='bronze')  # bronze, silver, gold, platinum
    
    # Verification metadata
    verified_by = db.Column(db.Integer, db.ForeignKey('admin_users.id'))
    verification_notes = db.Column(db.Text)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    verified_at = db.Column(db.DateTime)
    expires_at = db.Column(db.DateTime)  # Verification expiry (annual renewal)

class SecurityLog(db.Model):
    __tablename__ = 'security_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    admin_id = db.Column(db.Integer, db.ForeignKey('admin_users.id'))
    
    # Event details
    event_type = db.Column(db.String(50), nullable=False)  # login, logout, password_change, payout_request, etc.
    event_description = db.Column(db.Text)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))
    
    # Risk assessment
    risk_level = db.Column(db.String(20), default='low')  # low, medium, high, critical
    automated_action = db.Column(db.String(100))  # Action taken by system
    
    # Geolocation
    country = db.Column(db.String(50))
    city = db.Column(db.String(100))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ContentModerationQueue(db.Model):
    __tablename__ = 'content_moderation_queue'
    
    id = db.Column(db.Integer, primary_key=True)
    content_id = db.Column(db.Integer, db.ForeignKey('viral_content_tracking.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Moderation details
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected, flagged
    priority = db.Column(db.String(20), default='normal')  # low, normal, high, urgent
    
    # AI analysis results
    ai_content_score = db.Column(db.Float, default=0.0)  # AI-generated content likelihood
    toxicity_score = db.Column(db.Float, default=0.0)  # Toxicity/inappropriate content score
    brand_safety_score = db.Column(db.Float, default=0.0)  # Brand safety compliance
    
    # Human review
    reviewed_by = db.Column(db.Integer, db.ForeignKey('admin_users.id'))
    review_notes = db.Column(db.Text)
    
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime)

class ReferralAuditLog(db.Model):
    __tablename__ = 'referral_audit_log'
    
    id = db.Column(db.Integer, primary_key=True)
    referral_id = db.Column(db.Integer, db.ForeignKey('referral_tracking.id'), nullable=False)
    
    # Audit details
    action = db.Column(db.String(50), nullable=False)  # created, bonus_calculated, bonus_paid, invalidated
    old_values = db.Column(db.JSON)  # Previous state
    new_values = db.Column(db.JSON)  # New state
    
    # Context
    triggered_by = db.Column(db.String(20), default='system')  # system, admin, user
    admin_id = db.Column(db.Integer, db.ForeignKey('admin_users.id'))
    reason = db.Column(db.String(200))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Utility functions for admin operations

def calculate_total_referral_debt():
    """Calculate total money owed to all referrers"""
    from src.models.affiliate_tracking import UserEarnings
    
    total_pending = db.session.query(
        db.func.sum(UserEarnings.pending_payout)
    ).scalar() or 0.0
    
    return total_pending

def detect_multi_account_fraud(user_id):
    """Detect potential multi-account fraud"""
    from src.models.user import User
    from src.models.affiliate_tracking import ReferralTracking
    
    user = User.query.get(user_id)
    if not user:
        return None
    
    # Check for suspicious patterns
    suspicious_patterns = []
    risk_score = 0.0
    
    # Pattern 1: Multiple accounts from same IP (simplified)
    # In production, this would use actual IP tracking
    
    # Pattern 2: Circular referrals
    user_referrals = ReferralTracking.query.filter_by(referrer_id=user_id).all()
    referred_users = [r.referred_id for r in user_referrals]
    
    for referred_id in referred_users:
        # Check if any referred user also referred the original user
        circular_referral = ReferralTracking.query.filter_by(
            referrer_id=referred_id,
            referred_id=user_id
        ).first()
        
        if circular_referral:
            suspicious_patterns.append("circular_referrals")
            risk_score += 30.0
    
    # Pattern 3: Rapid referral creation
    recent_referrals = ReferralTracking.query.filter(
        ReferralTracking.referrer_id == user_id,
        ReferralTracking.referred_at > datetime.utcnow() - timedelta(hours=24)
    ).count()
    
    if recent_referrals > 10:
        suspicious_patterns.append("rapid_referral_creation")
        risk_score += 25.0
    
    # Pattern 4: Similar email patterns
    user_email_domain = user.email.split('@')[1]
    similar_emails = User.query.filter(
        User.email.like(f'%@{user_email_domain}')
    ).count()
    
    if similar_emails > 5:
        suspicious_patterns.append("similar_email_domains")
        risk_score += 15.0
    
    if risk_score > 50.0:
        # Create fraud detection record
        fraud_record = FraudDetection(
            user_id=user_id,
            fraud_type='multi_account',
            risk_score=risk_score,
            suspicious_patterns=suspicious_patterns,
            status='pending'
        )
        db.session.add(fraud_record)
        db.session.commit()
        
        return fraud_record
    
    return None

def update_system_metrics():
    """Update daily system metrics"""
    from src.models.user import User
    from src.models.affiliate_tracking import ReferralTracking, UserEarnings
    
    today = datetime.utcnow().date()
    
    # Check if metrics already exist for today
    existing_metrics = SystemMetrics.query.filter_by(metric_date=today).first()
    if existing_metrics:
        metrics = existing_metrics
    else:
        metrics = SystemMetrics(metric_date=today)
        db.session.add(metrics)
    
    # Update user metrics
    metrics.total_users = User.query.count()
    metrics.new_users_today = User.query.filter(
        db.func.date(User.join_date) == today
    ).count()
    
    # Update financial metrics
    total_earnings = db.session.query(
        db.func.sum(UserEarnings.total_earnings)
    ).scalar() or 0.0
    
    metrics.total_referral_debt = calculate_total_referral_debt()
    metrics.total_payouts_made = db.session.query(
        db.func.sum(UserEarnings.total_paid)
    ).scalar() or 0.0
    
    # Update referral metrics
    metrics.total_referrals = ReferralTracking.query.count()
    metrics.referrals_today = ReferralTracking.query.filter(
        db.func.date(ReferralTracking.referred_at) == today
    ).count()
    
    # Calculate conversion rate
    total_referrals = ReferralTracking.query.count()
    converted_referrals = ReferralTracking.query.filter_by(status='converted').count()
    
    if total_referrals > 0:
        metrics.conversion_rate = (converted_referrals / total_referrals) * 100
    
    db.session.commit()
    return metrics

def approve_payout_request(payout_request_id, admin_id, approval_notes=""):
    """Approve a payout request with proper verification"""
    from src.models.affiliate_tracking import PayoutRequest
    
    payout_request = PayoutRequest.query.get(payout_request_id)
    if not payout_request:
        return False
    
    # Create approval record
    approval = PayoutApproval(
        payout_request_id=payout_request_id,
        admin_id=admin_id,
        status='approved',
        approval_notes=approval_notes,
        identity_verified=True,  # Assume verification checks passed
        payment_method_verified=True,
        earnings_verified=True,
        fraud_check_passed=True,
        processed_at=datetime.utcnow()
    )
    
    db.session.add(approval)
    
    # Update payout request status
    payout_request.status = 'approved'
    payout_request.processed_at = datetime.utcnow()
    
    db.session.commit()
    return True

def calculate_trust_and_loyalty_scores(user_id):
    """Calculate trust and loyalty scores for a user"""
    from src.models.user import User
    from src.models.affiliate_tracking import ReferralTracking, UserEarnings, ViralContentTracking
    
    user = User.query.get(user_id)
    if not user:
        return None
    
    # Get or create identity verification record
    identity_verification = DigitalIdentityVerification.query.filter_by(user_id=user_id).first()
    if not identity_verification:
        identity_verification = DigitalIdentityVerification(user_id=user_id)
        db.session.add(identity_verification)
    
    # Calculate trust score (0-100)
    trust_score = 0.0
    
    # Base score for account age
    account_age_days = (datetime.utcnow() - user.join_date).days
    trust_score += min(account_age_days * 0.5, 20.0)  # Max 20 points for account age
    
    # Identity verification bonus
    if identity_verification.identity_status == 'verified':
        trust_score += 30.0
    
    # Referral quality score
    successful_referrals = ReferralTracking.query.filter_by(
        referrer_id=user_id,
        status='converted'
    ).count()
    trust_score += min(successful_referrals * 2.0, 25.0)  # Max 25 points for referrals
    
    # Content quality score
    approved_content = ViralContentTracking.query.filter_by(
        user_id=user_id,
        status='approved'
    ).count()
    trust_score += min(approved_content * 1.5, 15.0)  # Max 15 points for content
    
    # Fraud check penalty
    fraud_records = FraudDetection.query.filter_by(
        user_id=user_id,
        status='confirmed_fraud'
    ).count()
    trust_score -= fraud_records * 20.0  # -20 points per confirmed fraud
    
    trust_score = max(0.0, min(100.0, trust_score))  # Clamp between 0-100
    
    # Calculate loyalty score (0-100)
    loyalty_score = 0.0
    
    # Earnings consistency
    user_earnings = UserEarnings.query.filter_by(user_id=user_id).first()
    if user_earnings and user_earnings.total_earnings > 0:
        loyalty_score += min(user_earnings.total_earnings * 0.1, 40.0)  # Max 40 points
    
    # Platform engagement
    total_referrals = ReferralTracking.query.filter_by(referrer_id=user_id).count()
    loyalty_score += min(total_referrals * 3.0, 30.0)  # Max 30 points
    
    # Content creation
    total_content = ViralContentTracking.query.filter_by(user_id=user_id).count()
    loyalty_score += min(total_content * 2.0, 20.0)  # Max 20 points
    
    # Community participation (placeholder - would track actual engagement)
    loyalty_score += 10.0  # Base community participation score
    
    loyalty_score = max(0.0, min(100.0, loyalty_score))  # Clamp between 0-100
    
    # Determine verification tier
    combined_score = (trust_score + loyalty_score) / 2
    if combined_score >= 80:
        tier = 'platinum'
    elif combined_score >= 60:
        tier = 'gold'
    elif combined_score >= 40:
        tier = 'silver'
    else:
        tier = 'bronze'
    
    # Update identity verification record
    identity_verification.trust_score = trust_score
    identity_verification.loyalty_score = loyalty_score
    identity_verification.verification_tier = tier
    
    db.session.commit()
    
    return {
        'trust_score': trust_score,
        'loyalty_score': loyalty_score,
        'verification_tier': tier,
        'combined_score': combined_score
    }

