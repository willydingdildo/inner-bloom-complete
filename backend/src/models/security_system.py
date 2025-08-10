from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import uuid
import hashlib
import secrets
import json
from enum import Enum

db = SQLAlchemy()

class SecurityEvent(db.Model):
    __tablename__ = 'security_events'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Event details
    event_type = db.Column(db.String(50), nullable=False)  # login_attempt, password_change, suspicious_activity, etc.
    event_category = db.Column(db.String(20), nullable=False)  # authentication, fraud, privacy, compliance
    severity = db.Column(db.String(10), default='low')  # low, medium, high, critical
    
    # Event data
    description = db.Column(db.Text)
    event_data = db.Column(db.JSON)  # Additional event-specific data
    
    # Source information
    ip_address = db.Column(db.String(45))  # IPv4 or IPv6
    user_agent = db.Column(db.Text)
    device_fingerprint = db.Column(db.String(255))
    geolocation = db.Column(db.JSON)  # Country, city, coordinates
    
    # Status and resolution
    status = db.Column(db.String(20), default='open')  # open, investigating, resolved, false_positive
    resolved_by = db.Column(db.Integer, db.ForeignKey('admin_users.id'))
    resolution_notes = db.Column(db.Text)
    
    # Timestamps
    occurred_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)

class FraudDetectionRule(db.Model):
    __tablename__ = 'fraud_detection_rules'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Rule details
    rule_name = db.Column(db.String(100), nullable=False)
    rule_type = db.Column(db.String(50), nullable=False)  # velocity, pattern, anomaly, blacklist
    description = db.Column(db.Text)
    
    # Rule configuration
    rule_config = db.Column(db.JSON, nullable=False)  # Rule-specific configuration
    threshold_value = db.Column(db.Float)  # Threshold for triggering
    time_window_minutes = db.Column(db.Integer)  # Time window for velocity rules
    
    # Scoring
    risk_score = db.Column(db.Integer, default=10)  # Risk score to add when triggered (1-100)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    priority = db.Column(db.Integer, default=1)  # 1-10, higher = more important
    
    # Performance tracking
    total_triggers = db.Column(db.Integer, default=0)
    false_positives = db.Column(db.Integer, default=0)
    true_positives = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class UserRiskProfile(db.Model):
    __tablename__ = 'user_risk_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    
    # Risk scoring
    current_risk_score = db.Column(db.Integer, default=0)  # 0-100
    max_risk_score = db.Column(db.Integer, default=0)  # Historical maximum
    risk_level = db.Column(db.String(10), default='low')  # low, medium, high, critical
    
    # Behavioral patterns
    typical_login_hours = db.Column(db.JSON)  # Array of typical login hours
    typical_locations = db.Column(db.JSON)  # Array of typical countries/cities
    typical_devices = db.Column(db.JSON)  # Array of device fingerprints
    
    # Account activity
    total_logins = db.Column(db.Integer, default=0)
    failed_login_attempts = db.Column(db.Integer, default=0)
    last_login_at = db.Column(db.DateTime)
    last_failed_login_at = db.Column(db.DateTime)
    
    # Financial activity
    total_earnings = db.Column(db.Float, default=0.0)
    total_payouts = db.Column(db.Float, default=0.0)
    suspicious_transactions = db.Column(db.Integer, default=0)
    
    # Verification status
    identity_verified = db.Column(db.Boolean, default=False)
    phone_verified = db.Column(db.Boolean, default=False)
    email_verified = db.Column(db.Boolean, default=False)
    bank_account_verified = db.Column(db.Boolean, default=False)
    
    # Flags and restrictions
    is_flagged = db.Column(db.Boolean, default=False)
    is_restricted = db.Column(db.Boolean, default=False)
    restriction_reason = db.Column(db.String(200))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class DigitalIDVerification(db.Model):
    __tablename__ = 'digital_id_verifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Verification request details
    verification_type = db.Column(db.String(20), nullable=False)  # government_id, selfie, address_proof
    document_type = db.Column(db.String(30))  # drivers_license, passport, national_id, utility_bill
    
    # Document information
    document_number = db.Column(db.String(100))  # Encrypted
    document_country = db.Column(db.String(2))  # ISO country code
    document_state = db.Column(db.String(10))  # State/province code
    expiry_date = db.Column(db.Date)
    
    # Extracted information
    full_name = db.Column(db.String(200))
    date_of_birth = db.Column(db.Date)
    address = db.Column(db.Text)
    
    # File storage
    document_image_path = db.Column(db.String(500))  # Encrypted storage path
    selfie_image_path = db.Column(db.String(500))  # Encrypted storage path
    
    # Verification results
    verification_status = db.Column(db.String(20), default='pending')  # pending, approved, rejected, expired
    confidence_score = db.Column(db.Float)  # 0.0-1.0 confidence from verification service
    
    # AI/ML verification results
    document_authentic = db.Column(db.Boolean)
    face_match_score = db.Column(db.Float)  # Selfie to ID photo match score
    liveness_check_passed = db.Column(db.Boolean)  # Anti-spoofing check
    
    # Manual review
    requires_manual_review = db.Column(db.Boolean, default=False)
    reviewed_by = db.Column(db.Integer, db.ForeignKey('admin_users.id'))
    review_notes = db.Column(db.Text)
    
    # Verification service details
    service_provider = db.Column(db.String(50))  # jumio, onfido, veriff, etc.
    external_verification_id = db.Column(db.String(100))
    
    # Timestamps
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    processed_at = db.Column(db.DateTime)
    reviewed_at = db.Column(db.DateTime)
    expires_at = db.Column(db.DateTime)  # When verification expires

class DeviceFingerprint(db.Model):
    __tablename__ = 'device_fingerprints'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Device identification
    fingerprint_hash = db.Column(db.String(255), nullable=False, unique=True)
    device_name = db.Column(db.String(100))  # User-defined device name
    
    # Device characteristics
    user_agent = db.Column(db.Text)
    screen_resolution = db.Column(db.String(20))
    timezone = db.Column(db.String(50))
    language = db.Column(db.String(10))
    platform = db.Column(db.String(50))
    
    # Browser/app characteristics
    browser_name = db.Column(db.String(50))
    browser_version = db.Column(db.String(20))
    plugins = db.Column(db.JSON)  # List of browser plugins
    
    # Network characteristics
    ip_address = db.Column(db.String(45))
    isp = db.Column(db.String(100))
    
    # Trust level
    trust_score = db.Column(db.Integer, default=50)  # 0-100
    is_trusted = db.Column(db.Boolean, default=False)
    is_blocked = db.Column(db.Boolean, default=False)
    
    # Usage statistics
    total_logins = db.Column(db.Integer, default=0)
    last_login_at = db.Column(db.DateTime)
    first_seen_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Geolocation
    country = db.Column(db.String(2))
    city = db.Column(db.String(100))
    coordinates = db.Column(db.JSON)  # [latitude, longitude]

class TwoFactorAuth(db.Model):
    __tablename__ = 'two_factor_auth'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    
    # 2FA configuration
    is_enabled = db.Column(db.Boolean, default=False)
    method = db.Column(db.String(20))  # totp, sms, email, backup_codes
    
    # TOTP (Time-based One-Time Password)
    totp_secret = db.Column(db.String(255))  # Encrypted
    totp_backup_codes = db.Column(db.JSON)  # Encrypted array of backup codes
    
    # SMS 2FA
    phone_number = db.Column(db.String(20))  # Encrypted
    phone_verified = db.Column(db.Boolean, default=False)
    
    # Recovery options
    recovery_email = db.Column(db.String(120))  # Encrypted
    recovery_questions = db.Column(db.JSON)  # Encrypted security questions
    
    # Usage tracking
    last_used_at = db.Column(db.DateTime)
    total_uses = db.Column(db.Integer, default=0)
    failed_attempts = db.Column(db.Integer, default=0)
    
    # Emergency access
    emergency_codes_used = db.Column(db.Integer, default=0)
    last_emergency_access = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class DataPrivacyConsent(db.Model):
    __tablename__ = 'data_privacy_consents'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Consent details
    consent_type = db.Column(db.String(50), nullable=False)  # gdpr, ccpa, marketing, analytics
    consent_version = db.Column(db.String(10), nullable=False)  # Version of privacy policy
    
    # Consent status
    is_granted = db.Column(db.Boolean, nullable=False)
    consent_method = db.Column(db.String(20))  # explicit, implicit, opt_out
    
    # Data processing purposes
    purposes = db.Column(db.JSON)  # Array of data processing purposes
    
    # Consent metadata
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    
    # Timestamps
    granted_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)  # When consent expires
    withdrawn_at = db.Column(db.DateTime)

class SecurityAuditLog(db.Model):
    __tablename__ = 'security_audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    admin_id = db.Column(db.Integer, db.ForeignKey('admin_users.id'))
    
    # Action details
    action_type = db.Column(db.String(50), nullable=False)  # login, logout, password_change, etc.
    action_category = db.Column(db.String(20), nullable=False)  # authentication, authorization, data_access
    resource_type = db.Column(db.String(50))  # user_profile, payment_method, etc.
    resource_id = db.Column(db.String(100))
    
    # Action result
    result = db.Column(db.String(20), nullable=False)  # success, failure, blocked
    failure_reason = db.Column(db.String(200))
    
    # Context information
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    device_fingerprint = db.Column(db.String(255))
    
    # Additional data
    audit_metadata = db.Column(db.JSON)  # Additional context-specific data
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UITheme(db.Model):
    __tablename__ = 'ui_themes'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Theme details
    theme_name = db.Column(db.String(50), nullable=False, unique=True)
    theme_type = db.Column(db.String(20), nullable=False)  # free, premium, vip, seasonal
    display_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    
    # Theme configuration
    color_palette = db.Column(db.JSON, nullable=False)  # Primary, secondary, accent colors
    typography = db.Column(db.JSON)  # Font families, sizes, weights
    layout_config = db.Column(db.JSON)  # Spacing, borders, shadows
    animation_config = db.Column(db.JSON)  # Animation preferences
    
    # Access control
    required_tier = db.Column(db.String(20), default='free')  # free, premium, vip
    is_seasonal = db.Column(db.Boolean, default=False)
    available_from = db.Column(db.DateTime)
    available_until = db.Column(db.DateTime)
    
    # Theme assets
    preview_image_url = db.Column(db.String(500))
    css_file_path = db.Column(db.String(500))
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    is_default = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class UserThemePreference(db.Model):
    __tablename__ = 'user_theme_preferences'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    theme_id = db.Column(db.Integer, db.ForeignKey('ui_themes.id'), nullable=False)
    
    # Customizations
    custom_colors = db.Column(db.JSON)  # User's custom color overrides
    dark_mode_enabled = db.Column(db.Boolean, default=False)
    
    # Accessibility preferences
    high_contrast = db.Column(db.Boolean, default=False)
    large_text = db.Column(db.Boolean, default=False)
    reduced_motion = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Utility functions for security system

def initialize_fraud_detection_rules():
    """Initialize default fraud detection rules"""
    default_rules = [
        {
            'rule_name': 'Multiple Failed Logins',
            'rule_type': 'velocity',
            'description': 'Detect multiple failed login attempts from same IP',
            'rule_config': {'action': 'failed_login', 'max_attempts': 5},
            'threshold_value': 5.0,
            'time_window_minutes': 15,
            'risk_score': 25
        },
        {
            'rule_name': 'Unusual Login Location',
            'rule_type': 'anomaly',
            'description': 'Detect logins from unusual geographic locations',
            'rule_config': {'check_type': 'geolocation', 'distance_threshold_km': 1000},
            'risk_score': 15
        },
        {
            'rule_name': 'High Velocity Referrals',
            'rule_type': 'velocity',
            'description': 'Detect unusually high referral creation rate',
            'rule_config': {'action': 'create_referral', 'max_referrals': 10},
            'threshold_value': 10.0,
            'time_window_minutes': 60,
            'risk_score': 30
        },
        {
            'rule_name': 'Suspicious Payout Pattern',
            'rule_type': 'pattern',
            'description': 'Detect suspicious payout request patterns',
            'rule_config': {'check_type': 'payout_velocity', 'max_amount': 1000},
            'threshold_value': 1000.0,
            'time_window_minutes': 1440,  # 24 hours
            'risk_score': 40
        },
        {
            'rule_name': 'Device Fingerprint Mismatch',
            'rule_type': 'anomaly',
            'description': 'Detect login from completely new device characteristics',
            'rule_config': {'check_type': 'device_fingerprint', 'similarity_threshold': 0.3},
            'risk_score': 20
        }
    ]
    
    for rule_data in default_rules:
        existing_rule = FraudDetectionRule.query.filter_by(rule_name=rule_data['rule_name']).first()
        if not existing_rule:
            rule = FraudDetectionRule(**rule_data)
            db.session.add(rule)
    
    db.session.commit()

def initialize_ui_themes():
    """Initialize default UI themes"""
    themes = [
        {
            'theme_name': 'inner_bloom_free',
            'theme_type': 'free',
            'display_name': 'Inner Bloom Classic',
            'description': 'Clean and elegant design for all users',
            'color_palette': {
                'primary': '#E91E63',
                'secondary': '#F8BBD9',
                'accent': '#FF4081',
                'background': '#FFFFFF',
                'surface': '#F5F5F5',
                'text': '#212121'
            },
            'typography': {
                'primary_font': 'Inter',
                'secondary_font': 'Poppins',
                'heading_sizes': {'h1': '2.5rem', 'h2': '2rem', 'h3': '1.5rem'},
                'body_size': '1rem'
            },
            'required_tier': 'free',
            'is_default': True
        },
        {
            'theme_name': 'inner_bloom_premium',
            'theme_type': 'premium',
            'display_name': 'Inner Bloom Premium',
            'description': 'Enhanced design with gradients and animations',
            'color_palette': {
                'primary': '#6366F1',
                'secondary': '#A5B4FC',
                'accent': '#F59E0B',
                'background': '#FFFFFF',
                'surface': '#F8FAFC',
                'text': '#1F2937',
                'gradient_start': '#6366F1',
                'gradient_end': '#EC4899'
            },
            'typography': {
                'primary_font': 'Montserrat',
                'secondary_font': 'Open Sans',
                'heading_sizes': {'h1': '3rem', 'h2': '2.25rem', 'h3': '1.75rem'},
                'body_size': '1.125rem'
            },
            'animation_config': {
                'enable_transitions': True,
                'hover_effects': True,
                'loading_animations': True
            },
            'required_tier': 'premium'
        },
        {
            'theme_name': 'inner_bloom_vip',
            'theme_type': 'vip',
            'display_name': 'Inner Bloom VIP - Royal Vintage',
            'description': 'Luxury vintage ornate theme with gold and black elegance',
            'color_palette': {
                'primary': '#000000',
                'secondary': '#FFD700',
                'accent': '#C9B037',
                'background': '#0A0A0A',
                'surface': '#1A1A1A',
                'text': '#FFD700',
                'text_secondary': '#E6E6E6',
                'border': '#FFD700',
                'shadow': 'rgba(255, 215, 0, 0.3)',
                'gradient_start': '#000000',
                'gradient_end': '#1A1A1A',
                'gold_metallic': '#D4AF37',
                'vintage_gold': '#B8860B'
            },
            'typography': {
                'primary_font': 'Playfair Display',
                'secondary_font': 'Crimson Text',
                'accent_font': 'Cinzel',
                'heading_sizes': {'h1': '4rem', 'h2': '3rem', 'h3': '2.25rem'},
                'body_size': '1.125rem',
                'letter_spacing': '0.05em'
            },
            'layout_config': {
                'border_style': 'ornate',
                'border_radius': '8px',
                'shadow_style': 'vintage',
                'ornate_borders': True,
                'vintage_patterns': True,
                'gold_accents': True
            },
            'animation_config': {
                'enable_transitions': True,
                'hover_effects': 'gold_glow',
                'loading_animations': 'vintage_fade',
                'scroll_effects': 'parallax',
                'ornate_animations': True
            },
            'required_tier': 'vip'
        },
        {
            'theme_name': 'dark_mode',
            'theme_type': 'free',
            'display_name': 'Dark Mode',
            'description': 'Dark theme for comfortable night viewing',
            'color_palette': {
                'primary': '#BB86FC',
                'secondary': '#3700B3',
                'accent': '#03DAC6',
                'background': '#121212',
                'surface': '#1E1E1E',
                'text': '#FFFFFF'
            },
            'typography': {
                'primary_font': 'Inter',
                'secondary_font': 'Roboto',
                'heading_sizes': {'h1': '2.5rem', 'h2': '2rem', 'h3': '1.5rem'},
                'body_size': '1rem'
            },
            'required_tier': 'free'
        }
    ]
    
    for theme_data in themes:
        existing_theme = UITheme.query.filter_by(theme_name=theme_data['theme_name']).first()
        if not existing_theme:
            theme = UITheme(**theme_data)
            db.session.add(theme)
    
    db.session.commit()

def calculate_risk_score(user_id, event_type, event_data):
    """Calculate risk score for a user event"""
    user_profile = UserRiskProfile.query.filter_by(user_id=user_id).first()
    if not user_profile:
        user_profile = create_user_risk_profile(user_id)
    
    total_risk_score = 0
    triggered_rules = []
    
    # Get active fraud detection rules
    active_rules = FraudDetectionRule.query.filter_by(is_active=True).all()
    
    for rule in active_rules:
        if evaluate_fraud_rule(rule, user_id, event_type, event_data):
            total_risk_score += rule.risk_score
            triggered_rules.append(rule.rule_name)
            
            # Update rule statistics
            rule.total_triggers += 1
    
    # Update user risk profile
    user_profile.current_risk_score = min(100, user_profile.current_risk_score + total_risk_score)
    user_profile.max_risk_score = max(user_profile.max_risk_score, user_profile.current_risk_score)
    
    # Update risk level
    if user_profile.current_risk_score >= 80:
        user_profile.risk_level = 'critical'
    elif user_profile.current_risk_score >= 60:
        user_profile.risk_level = 'high'
    elif user_profile.current_risk_score >= 30:
        user_profile.risk_level = 'medium'
    else:
        user_profile.risk_level = 'low'
    
    db.session.commit()
    
    return {
        'risk_score': user_profile.current_risk_score,
        'risk_level': user_profile.risk_level,
        'triggered_rules': triggered_rules
    }

def evaluate_fraud_rule(rule, user_id, event_type, event_data):
    """Evaluate if a fraud detection rule is triggered"""
    rule_config = rule.rule_config
    
    if rule.rule_type == 'velocity':
        return evaluate_velocity_rule(rule, user_id, event_type, event_data)
    elif rule.rule_type == 'anomaly':
        return evaluate_anomaly_rule(rule, user_id, event_type, event_data)
    elif rule.rule_type == 'pattern':
        return evaluate_pattern_rule(rule, user_id, event_type, event_data)
    elif rule.rule_type == 'blacklist':
        return evaluate_blacklist_rule(rule, user_id, event_type, event_data)
    
    return False

def evaluate_velocity_rule(rule, user_id, event_type, event_data):
    """Evaluate velocity-based fraud rule"""
    rule_config = rule.rule_config
    action = rule_config.get('action')
    
    if action != event_type:
        return False
    
    # Count events in time window
    time_window = datetime.utcnow() - timedelta(minutes=rule.time_window_minutes)
    
    if action == 'failed_login':
        count = SecurityEvent.query.filter(
            SecurityEvent.user_id == user_id,
            SecurityEvent.event_type == 'failed_login',
            SecurityEvent.occurred_at >= time_window
        ).count()
    elif action == 'create_referral':
        # This would check referral creation events
        count = SecurityEvent.query.filter(
            SecurityEvent.user_id == user_id,
            SecurityEvent.event_type == 'referral_created',
            SecurityEvent.occurred_at >= time_window
        ).count()
    else:
        return False
    
    return count >= rule.threshold_value

def evaluate_anomaly_rule(rule, user_id, event_type, event_data):
    """Evaluate anomaly-based fraud rule"""
    rule_config = rule.rule_config
    check_type = rule_config.get('check_type')
    
    user_profile = UserRiskProfile.query.filter_by(user_id=user_id).first()
    if not user_profile:
        return False
    
    if check_type == 'geolocation':
        # Check if login location is unusual
        current_location = event_data.get('geolocation', {})
        typical_locations = user_profile.typical_locations or []
        
        if not typical_locations:
            return False  # No baseline to compare
        
        # Simple distance check (in production, use proper geolocation library)
        for location in typical_locations:
            if location.get('country') == current_location.get('country'):
                return False
        
        return True  # Different country than usual
    
    elif check_type == 'device_fingerprint':
        # Check if device is significantly different
        current_fingerprint = event_data.get('device_fingerprint')
        typical_devices = user_profile.typical_devices or []
        
        if not typical_devices or not current_fingerprint:
            return False
        
        # Simple similarity check
        for device in typical_devices:
            if device == current_fingerprint:
                return False
        
        return True  # Completely new device
    
    return False

def evaluate_pattern_rule(rule, user_id, event_type, event_data):
    """Evaluate pattern-based fraud rule"""
    rule_config = rule.rule_config
    check_type = rule_config.get('check_type')
    
    if check_type == 'payout_velocity':
        # Check for suspicious payout patterns
        time_window = datetime.utcnow() - timedelta(minutes=rule.time_window_minutes)
        
        from src.models.banking_system import PayoutTransaction
        recent_payouts = PayoutTransaction.query.filter(
            PayoutTransaction.user_id == user_id,
            PayoutTransaction.created_at >= time_window
        ).all()
        
        total_amount = sum(payout.amount for payout in recent_payouts)
        return total_amount >= rule.threshold_value
    
    return False

def evaluate_blacklist_rule(rule, user_id, event_type, event_data):
    """Evaluate blacklist-based fraud rule"""
    rule_config = rule.rule_config
    blacklist_type = rule_config.get('blacklist_type')
    
    if blacklist_type == 'ip_address':
        ip_address = event_data.get('ip_address')
        blacklisted_ips = rule_config.get('blacklisted_ips', [])
        return ip_address in blacklisted_ips
    
    elif blacklist_type == 'email_domain':
        from src.models.user import User
        user = User.query.get(user_id)
        if user:
            email_domain = user.email.split('@')[1].lower()
            blacklisted_domains = rule_config.get('blacklisted_domains', [])
            return email_domain in blacklisted_domains
    
    return False

def create_user_risk_profile(user_id):
    """Create initial risk profile for user"""
    risk_profile = UserRiskProfile(user_id=user_id)
    db.session.add(risk_profile)
    db.session.commit()
    return risk_profile

def log_security_event(user_id, event_type, event_category, severity='low', description='', event_data=None, ip_address=None, user_agent=None):
    """Log a security event"""
    security_event = SecurityEvent(
        user_id=user_id,
        event_type=event_type,
        event_category=event_category,
        severity=severity,
        description=description,
        event_data=event_data or {},
        ip_address=ip_address,
        user_agent=user_agent
    )
    
    db.session.add(security_event)
    db.session.commit()
    
    # Calculate risk score for this event
    risk_result = calculate_risk_score(user_id, event_type, event_data or {})
    
    # If risk is high, flag for review
    if risk_result['risk_level'] in ['high', 'critical']:
        security_event.severity = 'high'
        security_event.status = 'investigating'
        
        # Auto-flag user if critical risk
        if risk_result['risk_level'] == 'critical':
            user_profile = UserRiskProfile.query.filter_by(user_id=user_id).first()
            if user_profile:
                user_profile.is_flagged = True
    
    db.session.commit()
    return security_event

def create_device_fingerprint(user_id, fingerprint_data):
    """Create or update device fingerprint"""
    fingerprint_hash = hashlib.sha256(json.dumps(fingerprint_data, sort_keys=True).encode()).hexdigest()
    
    existing_fingerprint = DeviceFingerprint.query.filter_by(fingerprint_hash=fingerprint_hash).first()
    
    if existing_fingerprint:
        # Update existing fingerprint
        existing_fingerprint.total_logins += 1
        existing_fingerprint.last_login_at = datetime.utcnow()
        existing_fingerprint.ip_address = fingerprint_data.get('ip_address')
        db.session.commit()
        return existing_fingerprint
    
    # Create new fingerprint
    device_fingerprint = DeviceFingerprint(
        user_id=user_id,
        fingerprint_hash=fingerprint_hash,
        user_agent=fingerprint_data.get('user_agent'),
        screen_resolution=fingerprint_data.get('screen_resolution'),
        timezone=fingerprint_data.get('timezone'),
        language=fingerprint_data.get('language'),
        platform=fingerprint_data.get('platform'),
        browser_name=fingerprint_data.get('browser_name'),
        browser_version=fingerprint_data.get('browser_version'),
        ip_address=fingerprint_data.get('ip_address'),
        country=fingerprint_data.get('country'),
        city=fingerprint_data.get('city'),
        total_logins=1,
        last_login_at=datetime.utcnow()
    )
    
    db.session.add(device_fingerprint)
    db.session.commit()
    return device_fingerprint

def verify_digital_id(user_id, verification_type, document_data, file_paths):
    """Create digital ID verification request"""
    verification = DigitalIDVerification(
        user_id=user_id,
        verification_type=verification_type,
        document_type=document_data.get('document_type'),
        document_number=document_data.get('document_number'),  # Should be encrypted
        document_country=document_data.get('document_country'),
        document_state=document_data.get('document_state'),
        expiry_date=document_data.get('expiry_date'),
        full_name=document_data.get('full_name'),
        date_of_birth=document_data.get('date_of_birth'),
        address=document_data.get('address'),
        document_image_path=file_paths.get('document_image'),
        selfie_image_path=file_paths.get('selfie_image'),
        service_provider='internal'  # In production, use external service
    )
    
    # Simulate verification process (in production, call external API)
    verification.confidence_score = 0.95  # Mock high confidence
    verification.document_authentic = True
    verification.face_match_score = 0.92
    verification.liveness_check_passed = True
    verification.verification_status = 'approved'
    verification.processed_at = datetime.utcnow()
    verification.expires_at = datetime.utcnow() + timedelta(days=365)  # 1 year validity
    
    db.session.add(verification)
    
    # Update user risk profile
    user_profile = UserRiskProfile.query.filter_by(user_id=user_id).first()
    if user_profile:
        user_profile.identity_verified = True
        user_profile.current_risk_score = max(0, user_profile.current_risk_score - 20)  # Reduce risk
    
    db.session.commit()
    return verification

def get_user_theme(user_id):
    """Get user's current theme"""
    user_preference = UserThemePreference.query.filter_by(user_id=user_id).first()
    
    if user_preference:
        theme = UITheme.query.get(user_preference.theme_id)
        if theme and theme.is_active:
            return {
                'theme': theme,
                'preferences': user_preference
            }
    
    # Return default theme
    default_theme = UITheme.query.filter_by(is_default=True, is_active=True).first()
    return {
        'theme': default_theme,
        'preferences': None
    }

def set_user_theme(user_id, theme_id, custom_options=None):
    """Set user's theme preference"""
    theme = UITheme.query.get(theme_id)
    if not theme or not theme.is_active:
        raise ValueError("Invalid or inactive theme")
    
    # Check if user has access to this theme
    from src.models.user import User
    user = User.query.get(user_id)
    if not user:
        raise ValueError("User not found")
    
    # Check tier access
    user_tier = getattr(user, 'subscription_tier', 'free')
    if theme.required_tier == 'premium' and user_tier not in ['premium', 'vip']:
        raise ValueError("Premium subscription required for this theme")
    elif theme.required_tier == 'vip' and user_tier != 'vip':
        raise ValueError("VIP subscription required for this theme")
    
    # Update or create preference
    user_preference = UserThemePreference.query.filter_by(user_id=user_id).first()
    if user_preference:
        user_preference.theme_id = theme_id
        user_preference.updated_at = datetime.utcnow()
    else:
        user_preference = UserThemePreference(
            user_id=user_id,
            theme_id=theme_id
        )
        db.session.add(user_preference)
    
    # Apply custom options
    if custom_options:
        user_preference.custom_colors = custom_options.get('custom_colors')
        user_preference.dark_mode_enabled = custom_options.get('dark_mode_enabled', False)
        user_preference.high_contrast = custom_options.get('high_contrast', False)
        user_preference.large_text = custom_options.get('large_text', False)
        user_preference.reduced_motion = custom_options.get('reduced_motion', False)
    
    db.session.commit()
    return user_preference

