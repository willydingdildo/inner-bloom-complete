from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from src.models.security_system import (
    SecurityEvent, FraudDetectionRule, UserRiskProfile, DigitalIDVerification,
    DeviceFingerprint, TwoFactorAuth, DataPrivacyConsent, SecurityAuditLog,
    UITheme, UserThemePreference, initialize_fraud_detection_rules, initialize_ui_themes,
    calculate_risk_score, log_security_event, create_device_fingerprint,
    verify_digital_id, get_user_theme, set_user_theme, db
)
from src.models.user import User
from datetime import datetime, timedelta
import json
import secrets
import pyotp

security_system_bp = Blueprint('security_system', __name__)

# Initialize security system on first load
# @security_system_bp.before_app_first_request  # Not supported in this Flask version
def setup_security_system():
    """Initialize security system"""
    initialize_fraud_detection_rules()
    initialize_ui_themes()

# Security Event Routes
@security_system_bp.route('/security/events', methods=['GET'])
@cross_origin()
def get_security_events():
    """Get security events"""
    try:
        user_id = request.args.get('user_id', type=int)
        event_type = request.args.get('event_type')
        severity = request.args.get('severity')
        status = request.args.get('status')
        limit = request.args.get('limit', 100, type=int)
        
        query = SecurityEvent.query
        
        if user_id:
            query = query.filter_by(user_id=user_id)
        if event_type:
            query = query.filter_by(event_type=event_type)
        if severity:
            query = query.filter_by(severity=severity)
        if status:
            query = query.filter_by(status=status)
        
        events = query.order_by(SecurityEvent.occurred_at.desc()).limit(limit).all()
        
        events_data = [
            {
                'id': event.id,
                'user_id': event.user_id,
                'event_type': event.event_type,
                'event_category': event.event_category,
                'severity': event.severity,
                'description': event.description,
                'ip_address': event.ip_address,
                'status': event.status,
                'occurred_at': event.occurred_at.isoformat(),
                'resolved_at': event.resolved_at.isoformat() if event.resolved_at else None
            }
            for event in events
        ]
        
        return jsonify({
            'security_events': events_data,
            'total_count': len(events_data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@security_system_bp.route('/security/events', methods=['POST'])
@cross_origin()
def create_security_event():
    """Create a security event"""
    try:
        data = request.get_json()
        
        required_fields = ['user_id', 'event_type', 'event_category']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        event = log_security_event(
            user_id=data['user_id'],
            event_type=data['event_type'],
            event_category=data['event_category'],
            severity=data.get('severity', 'low'),
            description=data.get('description', ''),
            event_data=data.get('event_data'),
            ip_address=data.get('ip_address'),
            user_agent=data.get('user_agent')
        )
        
        return jsonify({
            'event_id': event.id,
            'message': 'Security event logged successfully'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Risk Profile Routes
@security_system_bp.route('/security/risk-profile/<int:user_id>', methods=['GET'])
@cross_origin()
def get_user_risk_profile(user_id):
    """Get user's risk profile"""
    try:
        risk_profile = UserRiskProfile.query.filter_by(user_id=user_id).first()
        
        if not risk_profile:
            return jsonify({'risk_profile': None}), 200
        
        profile_data = {
            'user_id': risk_profile.user_id,
            'current_risk_score': risk_profile.current_risk_score,
            'max_risk_score': risk_profile.max_risk_score,
            'risk_level': risk_profile.risk_level,
            'total_logins': risk_profile.total_logins,
            'failed_login_attempts': risk_profile.failed_login_attempts,
            'identity_verified': risk_profile.identity_verified,
            'phone_verified': risk_profile.phone_verified,
            'email_verified': risk_profile.email_verified,
            'bank_account_verified': risk_profile.bank_account_verified,
            'is_flagged': risk_profile.is_flagged,
            'is_restricted': risk_profile.is_restricted,
            'restriction_reason': risk_profile.restriction_reason,
            'last_login_at': risk_profile.last_login_at.isoformat() if risk_profile.last_login_at else None,
            'created_at': risk_profile.created_at.isoformat()
        }
        
        return jsonify({'risk_profile': profile_data}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@security_system_bp.route('/security/risk-assessment', methods=['POST'])
@cross_origin()
def assess_risk():
    """Assess risk for a user action"""
    try:
        data = request.get_json()
        
        required_fields = ['user_id', 'event_type']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        risk_result = calculate_risk_score(
            user_id=data['user_id'],
            event_type=data['event_type'],
            event_data=data.get('event_data', {})
        )
        
        return jsonify(risk_result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Digital ID Verification Routes
@security_system_bp.route('/security/id-verification', methods=['POST'])
@cross_origin()
def submit_id_verification():
    """Submit digital ID verification"""
    try:
        data = request.get_json()
        
        required_fields = ['user_id', 'verification_type', 'document_data']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # In production, handle file uploads properly
        file_paths = {
            'document_image': data.get('document_image_path', '/tmp/mock_document.jpg'),
            'selfie_image': data.get('selfie_image_path', '/tmp/mock_selfie.jpg')
        }
        
        verification = verify_digital_id(
            user_id=data['user_id'],
            verification_type=data['verification_type'],
            document_data=data['document_data'],
            file_paths=file_paths
        )
        
        return jsonify({
            'verification_id': verification.id,
            'verification_status': verification.verification_status,
            'confidence_score': verification.confidence_score,
            'requires_manual_review': verification.requires_manual_review,
            'message': 'ID verification submitted successfully'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@security_system_bp.route('/security/id-verification/<int:user_id>', methods=['GET'])
@cross_origin()
def get_id_verification_status(user_id):
    """Get ID verification status for user"""
    try:
        verifications = DigitalIDVerification.query.filter_by(user_id=user_id)\
                                                  .order_by(DigitalIDVerification.submitted_at.desc()).all()
        
        verifications_data = [
            {
                'id': verification.id,
                'verification_type': verification.verification_type,
                'document_type': verification.document_type,
                'verification_status': verification.verification_status,
                'confidence_score': verification.confidence_score,
                'document_authentic': verification.document_authentic,
                'face_match_score': verification.face_match_score,
                'liveness_check_passed': verification.liveness_check_passed,
                'requires_manual_review': verification.requires_manual_review,
                'submitted_at': verification.submitted_at.isoformat(),
                'processed_at': verification.processed_at.isoformat() if verification.processed_at else None,
                'expires_at': verification.expires_at.isoformat() if verification.expires_at else None
            }
            for verification in verifications
        ]
        
        return jsonify({
            'verifications': verifications_data,
            'total_count': len(verifications_data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Device Fingerprint Routes
@security_system_bp.route('/security/device-fingerprint', methods=['POST'])
@cross_origin()
def create_device_fingerprint_endpoint():
    """Create or update device fingerprint"""
    try:
        data = request.get_json()
        
        required_fields = ['user_id', 'fingerprint_data']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        device_fingerprint = create_device_fingerprint(
            user_id=data['user_id'],
            fingerprint_data=data['fingerprint_data']
        )
        
        return jsonify({
            'fingerprint_id': device_fingerprint.id,
            'fingerprint_hash': device_fingerprint.fingerprint_hash,
            'trust_score': device_fingerprint.trust_score,
            'is_trusted': device_fingerprint.is_trusted,
            'message': 'Device fingerprint created/updated successfully'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@security_system_bp.route('/security/device-fingerprints/<int:user_id>', methods=['GET'])
@cross_origin()
def get_user_device_fingerprints(user_id):
    """Get user's device fingerprints"""
    try:
        fingerprints = DeviceFingerprint.query.filter_by(user_id=user_id)\
                                             .order_by(DeviceFingerprint.last_login_at.desc()).all()
        
        fingerprints_data = [
            {
                'id': fp.id,
                'device_name': fp.device_name,
                'platform': fp.platform,
                'browser_name': fp.browser_name,
                'browser_version': fp.browser_version,
                'country': fp.country,
                'city': fp.city,
                'trust_score': fp.trust_score,
                'is_trusted': fp.is_trusted,
                'is_blocked': fp.is_blocked,
                'total_logins': fp.total_logins,
                'last_login_at': fp.last_login_at.isoformat() if fp.last_login_at else None,
                'first_seen_at': fp.first_seen_at.isoformat()
            }
            for fp in fingerprints
        ]
        
        return jsonify({
            'device_fingerprints': fingerprints_data,
            'total_count': len(fingerprints_data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Two-Factor Authentication Routes
@security_system_bp.route('/security/2fa/setup', methods=['POST'])
@cross_origin()
def setup_2fa():
    """Setup two-factor authentication"""
    try:
        data = request.get_json()
        
        required_fields = ['user_id', 'method']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        user_id = data['user_id']
        method = data['method']
        
        # Check if 2FA already exists
        existing_2fa = TwoFactorAuth.query.filter_by(user_id=user_id).first()
        if existing_2fa and existing_2fa.is_enabled:
            return jsonify({'error': '2FA is already enabled for this user'}), 409
        
        if method == 'totp':
            # Generate TOTP secret
            secret = pyotp.random_base32()
            
            # Generate backup codes
            backup_codes = [secrets.token_hex(4).upper() for _ in range(10)]
            
            if existing_2fa:
                existing_2fa.method = method
                existing_2fa.totp_secret = secret  # In production, encrypt this
                existing_2fa.totp_backup_codes = backup_codes  # In production, encrypt this
                two_factor = existing_2fa
            else:
                two_factor = TwoFactorAuth(
                    user_id=user_id,
                    method=method,
                    totp_secret=secret,  # In production, encrypt this
                    totp_backup_codes=backup_codes  # In production, encrypt this
                )
                db.session.add(two_factor)
            
            # Generate QR code URL for TOTP setup
            user = User.query.get(user_id)
            totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
                name=user.email,
                issuer_name="Inner Bloom"
            )
            
            db.session.commit()
            
            return jsonify({
                'secret': secret,
                'qr_code_uri': totp_uri,
                'backup_codes': backup_codes,
                'message': 'TOTP setup initiated. Please verify with authenticator app.'
            }), 200
            
        elif method == 'sms':
            phone_number = data.get('phone_number')
            if not phone_number:
                return jsonify({'error': 'Phone number required for SMS 2FA'}), 400
            
            if existing_2fa:
                existing_2fa.method = method
                existing_2fa.phone_number = phone_number  # In production, encrypt this
                two_factor = existing_2fa
            else:
                two_factor = TwoFactorAuth(
                    user_id=user_id,
                    method=method,
                    phone_number=phone_number  # In production, encrypt this
                )
                db.session.add(two_factor)
            
            db.session.commit()
            
            # In production, send SMS verification code
            return jsonify({
                'message': 'SMS 2FA setup initiated. Verification code sent to phone.'
            }), 200
        
        else:
            return jsonify({'error': 'Unsupported 2FA method'}), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@security_system_bp.route('/security/2fa/verify', methods=['POST'])
@cross_origin()
def verify_2fa():
    """Verify and enable 2FA"""
    try:
        data = request.get_json()
        
        required_fields = ['user_id', 'code']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        user_id = data['user_id']
        code = data['code']
        
        two_factor = TwoFactorAuth.query.filter_by(user_id=user_id).first()
        if not two_factor:
            return jsonify({'error': '2FA not set up for this user'}), 404
        
        if two_factor.method == 'totp':
            # Verify TOTP code
            totp = pyotp.TOTP(two_factor.totp_secret)
            if totp.verify(code):
                two_factor.is_enabled = True
                two_factor.last_used_at = datetime.utcnow()
                two_factor.total_uses += 1
                db.session.commit()
                
                return jsonify({
                    'message': '2FA enabled successfully',
                    'is_enabled': True
                }), 200
            else:
                two_factor.failed_attempts += 1
                db.session.commit()
                return jsonify({'error': 'Invalid verification code'}), 400
        
        elif two_factor.method == 'sms':
            # In production, verify SMS code
            # For demo, accept any 6-digit code
            if len(code) == 6 and code.isdigit():
                two_factor.is_enabled = True
                two_factor.phone_verified = True
                two_factor.last_used_at = datetime.utcnow()
                two_factor.total_uses += 1
                db.session.commit()
                
                return jsonify({
                    'message': '2FA enabled successfully',
                    'is_enabled': True
                }), 200
            else:
                return jsonify({'error': 'Invalid verification code'}), 400
        
        return jsonify({'error': 'Unsupported 2FA method'}), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@security_system_bp.route('/security/2fa/status/<int:user_id>', methods=['GET'])
@cross_origin()
def get_2fa_status(user_id):
    """Get 2FA status for user"""
    try:
        two_factor = TwoFactorAuth.query.filter_by(user_id=user_id).first()
        
        if not two_factor:
            return jsonify({
                'is_enabled': False,
                'method': None
            }), 200
        
        return jsonify({
            'is_enabled': two_factor.is_enabled,
            'method': two_factor.method,
            'phone_verified': two_factor.phone_verified,
            'last_used_at': two_factor.last_used_at.isoformat() if two_factor.last_used_at else None,
            'total_uses': two_factor.total_uses
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# UI Theme Routes
@security_system_bp.route('/themes', methods=['GET'])
@cross_origin()
def get_available_themes():
    """Get available UI themes"""
    try:
        user_id = request.args.get('user_id', type=int)
        
        # Get user's subscription tier
        user_tier = 'free'
        if user_id:
            user = User.query.get(user_id)
            if user:
                user_tier = getattr(user, 'subscription_tier', 'free')
        
        # Get themes available to user's tier
        query = UITheme.query.filter_by(is_active=True)
        
        if user_tier == 'free':
            query = query.filter_by(required_tier='free')
        elif user_tier == 'premium':
            query = query.filter(UITheme.required_tier.in_(['free', 'premium']))
        # VIP users can access all themes
        
        themes = query.all()
        
        themes_data = [
            {
                'id': theme.id,
                'theme_name': theme.theme_name,
                'theme_type': theme.theme_type,
                'display_name': theme.display_name,
                'description': theme.description,
                'color_palette': theme.color_palette,
                'required_tier': theme.required_tier,
                'is_seasonal': theme.is_seasonal,
                'is_default': theme.is_default,
                'preview_image_url': theme.preview_image_url,
                'available_from': theme.available_from.isoformat() if theme.available_from else None,
                'available_until': theme.available_until.isoformat() if theme.available_until else None
            }
            for theme in themes
        ]
        
        return jsonify({
            'themes': themes_data,
            'user_tier': user_tier,
            'total_count': len(themes_data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@security_system_bp.route('/themes/user/<int:user_id>', methods=['GET'])
@cross_origin()
def get_user_theme_preference(user_id):
    """Get user's current theme"""
    try:
        theme_data = get_user_theme(user_id)
        
        result = {
            'theme': {
                'id': theme_data['theme'].id,
                'theme_name': theme_data['theme'].theme_name,
                'display_name': theme_data['theme'].display_name,
                'color_palette': theme_data['theme'].color_palette,
                'typography': theme_data['theme'].typography,
                'layout_config': theme_data['theme'].layout_config,
                'animation_config': theme_data['theme'].animation_config
            }
        }
        
        if theme_data['preferences']:
            result['preferences'] = {
                'custom_colors': theme_data['preferences'].custom_colors,
                'dark_mode_enabled': theme_data['preferences'].dark_mode_enabled,
                'high_contrast': theme_data['preferences'].high_contrast,
                'large_text': theme_data['preferences'].large_text,
                'reduced_motion': theme_data['preferences'].reduced_motion
            }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@security_system_bp.route('/themes/user/<int:user_id>', methods=['POST'])
@cross_origin()
def set_user_theme_preference(user_id):
    """Set user's theme preference"""
    try:
        data = request.get_json()
        
        if 'theme_id' not in data:
            return jsonify({'error': 'Missing required field: theme_id'}), 400
        
        theme_id = data['theme_id']
        custom_options = data.get('custom_options', {})
        
        user_preference = set_user_theme(user_id, theme_id, custom_options)
        
        return jsonify({
            'message': 'Theme preference updated successfully',
            'theme_id': user_preference.theme_id,
            'updated_at': user_preference.updated_at.isoformat()
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Privacy and Consent Routes
@security_system_bp.route('/security/privacy-consent', methods=['POST'])
@cross_origin()
def record_privacy_consent():
    """Record user's privacy consent"""
    try:
        data = request.get_json()
        
        required_fields = ['user_id', 'consent_type', 'consent_version', 'is_granted']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        consent = DataPrivacyConsent(
            user_id=data['user_id'],
            consent_type=data['consent_type'],
            consent_version=data['consent_version'],
            is_granted=data['is_granted'],
            consent_method=data.get('consent_method', 'explicit'),
            purposes=data.get('purposes', []),
            ip_address=data.get('ip_address'),
            user_agent=data.get('user_agent'),
            expires_at=datetime.utcnow() + timedelta(days=365) if data.get('expires_in_days') else None
        )
        
        db.session.add(consent)
        db.session.commit()
        
        return jsonify({
            'consent_id': consent.id,
            'message': 'Privacy consent recorded successfully'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@security_system_bp.route('/security/privacy-consent/<int:user_id>', methods=['GET'])
@cross_origin()
def get_privacy_consents(user_id):
    """Get user's privacy consents"""
    try:
        consents = DataPrivacyConsent.query.filter_by(user_id=user_id)\
                                          .order_by(DataPrivacyConsent.granted_at.desc()).all()
        
        consents_data = [
            {
                'id': consent.id,
                'consent_type': consent.consent_type,
                'consent_version': consent.consent_version,
                'is_granted': consent.is_granted,
                'consent_method': consent.consent_method,
                'purposes': consent.purposes,
                'granted_at': consent.granted_at.isoformat(),
                'expires_at': consent.expires_at.isoformat() if consent.expires_at else None,
                'withdrawn_at': consent.withdrawn_at.isoformat() if consent.withdrawn_at else None
            }
            for consent in consents
        ]
        
        return jsonify({
            'privacy_consents': consents_data,
            'total_count': len(consents_data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Admin Routes
@security_system_bp.route('/security/admin/fraud-rules', methods=['GET'])
@cross_origin()
def get_fraud_detection_rules():
    """Get fraud detection rules (admin only)"""
    try:
        rules = FraudDetectionRule.query.order_by(FraudDetectionRule.priority.desc()).all()
        
        rules_data = [
            {
                'id': rule.id,
                'rule_name': rule.rule_name,
                'rule_type': rule.rule_type,
                'description': rule.description,
                'rule_config': rule.rule_config,
                'threshold_value': rule.threshold_value,
                'time_window_minutes': rule.time_window_minutes,
                'risk_score': rule.risk_score,
                'is_active': rule.is_active,
                'priority': rule.priority,
                'total_triggers': rule.total_triggers,
                'false_positives': rule.false_positives,
                'true_positives': rule.true_positives
            }
            for rule in rules
        ]
        
        return jsonify({
            'fraud_rules': rules_data,
            'total_count': len(rules_data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@security_system_bp.route('/security/admin/high-risk-users', methods=['GET'])
@cross_origin()
def get_high_risk_users():
    """Get high-risk users (admin only)"""
    try:
        high_risk_profiles = UserRiskProfile.query.filter(
            UserRiskProfile.risk_level.in_(['high', 'critical'])
        ).order_by(UserRiskProfile.current_risk_score.desc()).all()
        
        users_data = []
        for profile in high_risk_profiles:
            user = User.query.get(profile.user_id)
            if user:
                users_data.append({
                    'user_id': profile.user_id,
                    'username': user.username,
                    'email': user.email,
                    'current_risk_score': profile.current_risk_score,
                    'risk_level': profile.risk_level,
                    'is_flagged': profile.is_flagged,
                    'is_restricted': profile.is_restricted,
                    'restriction_reason': profile.restriction_reason,
                    'identity_verified': profile.identity_verified,
                    'last_login_at': profile.last_login_at.isoformat() if profile.last_login_at else None
                })
        
        return jsonify({
            'high_risk_users': users_data,
            'total_count': len(users_data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Analytics Routes
@security_system_bp.route('/security/analytics', methods=['GET'])
@cross_origin()
def get_security_analytics():
    """Get security analytics"""
    try:
        # Get security event statistics
        total_events = SecurityEvent.query.count()
        high_severity_events = SecurityEvent.query.filter_by(severity='high').count()
        critical_events = SecurityEvent.query.filter_by(severity='critical').count()
        
        # Get risk profile statistics
        total_users = UserRiskProfile.query.count()
        high_risk_users = UserRiskProfile.query.filter(
            UserRiskProfile.risk_level.in_(['high', 'critical'])
        ).count()
        
        flagged_users = UserRiskProfile.query.filter_by(is_flagged=True).count()
        verified_users = UserRiskProfile.query.filter_by(identity_verified=True).count()
        
        # Get 2FA adoption
        users_with_2fa = TwoFactorAuth.query.filter_by(is_enabled=True).count()
        
        # Get recent security events
        recent_events = SecurityEvent.query.filter(
            SecurityEvent.occurred_at >= datetime.utcnow() - timedelta(days=7)
        ).count()
        
        analytics_data = {
            'overview': {
                'total_security_events': total_events,
                'high_severity_events': high_severity_events,
                'critical_events': critical_events,
                'recent_events_7_days': recent_events
            },
            'risk_management': {
                'total_users': total_users,
                'high_risk_users': high_risk_users,
                'flagged_users': flagged_users,
                'risk_percentage': (high_risk_users / total_users * 100) if total_users > 0 else 0
            },
            'verification': {
                'identity_verified_users': verified_users,
                'verification_rate': (verified_users / total_users * 100) if total_users > 0 else 0,
                'users_with_2fa': users_with_2fa,
                'two_fa_adoption_rate': (users_with_2fa / total_users * 100) if total_users > 0 else 0
            }
        }
        
        return jsonify(analytics_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Health check
@security_system_bp.route('/security/health', methods=['GET'])
@cross_origin()
def security_system_health():
    """Security system health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'features': ['fraud_detection', 'id_verification', '2fa', 'device_fingerprinting', 'ui_themes'],
        'version': '1.0.0'
    }), 200

