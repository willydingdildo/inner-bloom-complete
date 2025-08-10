from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from src.models.admin import (
    AdminUser, SystemMetrics, FraudDetection, PayoutApproval, 
    DigitalIdentityVerification, SecurityLog, ContentModerationQueue,
    ReferralAuditLog, calculate_total_referral_debt, detect_multi_account_fraud,
    update_system_metrics, approve_payout_request, calculate_trust_and_loyalty_scores,
    db
)
from src.models.user import User
from src.models.affiliate_tracking import (
    ReferralTracking, UserEarnings, PayoutRequest, ViralContentTracking
)
from datetime import datetime, timedelta
import json

admin_bp = Blueprint('admin', __name__)

# Dashboard Routes
@admin_bp.route('/admin/dashboard', methods=['GET'])
@cross_origin()
def get_admin_dashboard():
    """Get comprehensive admin dashboard data"""
    try:
        # Update system metrics
        metrics = update_system_metrics()
        
        # Get recent activity
        recent_users = User.query.order_by(User.join_date.desc()).limit(10).all()
        recent_referrals = ReferralTracking.query.order_by(ReferralTracking.referred_at.desc()).limit(10).all()
        pending_payouts = PayoutRequest.query.filter_by(status='pending').limit(10).all()
        
        # Get fraud alerts
        fraud_alerts = FraudDetection.query.filter_by(status='pending').order_by(FraudDetection.detected_at.desc()).limit(5).all()
        
        # Calculate key metrics
        total_referral_debt = calculate_total_referral_debt()
        
        dashboard_data = {
            'metrics': {
                'total_users': metrics.total_users,
                'new_users_today': metrics.new_users_today,
                'active_users_today': metrics.active_users_today,
                'total_revenue': metrics.total_revenue,
                'revenue_today': metrics.revenue_today,
                'total_referral_debt': total_referral_debt,
                'pending_payouts': metrics.pending_payouts,
                'total_referrals': metrics.total_referrals,
                'referrals_today': metrics.referrals_today,
                'conversion_rate': metrics.conversion_rate
            },
            'recent_activity': {
                'new_users': [
                    {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'join_date': user.join_date.isoformat(),
                        'referred_by_id': user.referred_by_id
                    }
                    for user in recent_users
                ],
                'recent_referrals': [
                    {
                        'id': ref.id,
                        'referrer_id': ref.referrer_id,
                        'referred_id': ref.referred_id,
                        'level': ref.level,
                        'bonus': ref.referral_bonus,
                        'status': ref.status,
                        'referred_at': ref.referred_at.isoformat()
                    }
                    for ref in recent_referrals
                ],
                'pending_payouts': [
                    {
                        'id': payout.id,
                        'user_id': payout.user_id,
                        'amount': payout.amount,
                        'payment_method': payout.payment_method,
                        'requested_at': payout.requested_at.isoformat()
                    }
                    for payout in pending_payouts
                ]
            },
            'fraud_alerts': [
                {
                    'id': fraud.id,
                    'user_id': fraud.user_id,
                    'fraud_type': fraud.fraud_type,
                    'risk_score': fraud.risk_score,
                    'detected_at': fraud.detected_at.isoformat(),
                    'suspicious_patterns': fraud.suspicious_patterns
                }
                for fraud in fraud_alerts
            ]
        }
        
        return jsonify(dashboard_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/referrals', methods=['GET'])
@cross_origin()
def get_referral_overview():
    """Get detailed referral system overview"""
    try:
        # Get referral statistics by tier
        referral_stats = db.session.query(
            ReferralTracking.level,
            db.func.count(ReferralTracking.id).label('count'),
            db.func.sum(ReferralTracking.referral_bonus).label('total_bonus'),
            db.func.avg(ReferralTracking.referral_bonus).label('avg_bonus')
        ).group_by(ReferralTracking.level).all()
        
        # Get top referrers
        top_referrers = db.session.query(
            ReferralTracking.referrer_id,
            User.username,
            db.func.count(ReferralTracking.id).label('referral_count'),
            db.func.sum(ReferralTracking.referral_bonus).label('total_earned')
        ).join(User, ReferralTracking.referrer_id == User.id)\
         .group_by(ReferralTracking.referrer_id, User.username)\
         .order_by(db.func.sum(ReferralTracking.referral_bonus).desc())\
         .limit(20).all()
        
        # Get conversion funnel data
        total_referrals = ReferralTracking.query.count()
        converted_referrals = ReferralTracking.query.filter_by(payment_status='completed').count()
        paid_bonuses = ReferralTracking.query.filter_by(status='bonus_paid').count()
        
        referral_data = {
            'statistics': {
                'total_referrals': total_referrals,
                'converted_referrals': converted_referrals,
                'paid_bonuses': paid_bonuses,
                'conversion_rate': (converted_referrals / total_referrals * 100) if total_referrals > 0 else 0,
                'payout_rate': (paid_bonuses / converted_referrals * 100) if converted_referrals > 0 else 0
            },
            'level_breakdown': [
                {
                    'level': stat.level,
                    'count': stat.count,
                    'total_bonus': float(stat.total_bonus or 0),
                    'avg_bonus': float(stat.avg_bonus or 0)
                }
                for stat in referral_stats
            ],
            'top_referrers': [
                {
                    'user_id': ref.referrer_id,
                    'username': ref.username,
                    'referral_count': ref.referral_count,
                    'total_earned': float(ref.total_earned or 0)
                }
                for ref in top_referrers
            ]
        }
        
        return jsonify(referral_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/payouts', methods=['GET'])
@cross_origin()
def get_payout_management():
    """Get payout management data"""
    try:
        # Get pending payout requests
        pending_payouts = db.session.query(
            PayoutRequest,
            User.username,
            UserEarnings.total_earnings,
            UserEarnings.pending_payout
        ).join(User, PayoutRequest.user_id == User.id)\
         .join(UserEarnings, PayoutRequest.user_id == UserEarnings.user_id)\
         .filter(PayoutRequest.status == 'pending')\
         .order_by(PayoutRequest.requested_at.desc()).all()
        
        # Get payout history
        payout_history = db.session.query(
            PayoutRequest,
            User.username
        ).join(User, PayoutRequest.user_id == User.id)\
         .filter(PayoutRequest.status.in_(['completed', 'failed']))\
         .order_by(PayoutRequest.processed_at.desc())\
         .limit(50).all()
        
        # Calculate payout statistics
        total_pending_amount = db.session.query(
            db.func.sum(PayoutRequest.amount)
        ).filter(PayoutRequest.status == 'pending').scalar() or 0
        
        total_paid_amount = db.session.query(
            db.func.sum(PayoutRequest.amount)
        ).filter(PayoutRequest.status == 'completed').scalar() or 0
        
        payout_data = {
            'statistics': {
                'total_pending_requests': len(pending_payouts),
                'total_pending_amount': float(total_pending_amount),
                'total_paid_amount': float(total_paid_amount),
                'total_referral_debt': calculate_total_referral_debt()
            },
            'pending_payouts': [
                {
                    'id': payout.PayoutRequest.id,
                    'user_id': payout.PayoutRequest.user_id,
                    'username': payout.username,
                    'amount': payout.PayoutRequest.amount,
                    'payment_method': payout.PayoutRequest.payment_method,
                    'total_earnings': payout.total_earnings,
                    'pending_payout': payout.pending_payout,
                    'requested_at': payout.PayoutRequest.requested_at.isoformat()
                }
                for payout in pending_payouts
            ],
            'payout_history': [
                {
                    'id': payout.PayoutRequest.id,
                    'user_id': payout.PayoutRequest.user_id,
                    'username': payout.username,
                    'amount': payout.PayoutRequest.amount,
                    'status': payout.PayoutRequest.status,
                    'payment_method': payout.PayoutRequest.payment_method,
                    'processed_at': payout.PayoutRequest.processed_at.isoformat() if payout.PayoutRequest.processed_at else None
                }
                for payout in payout_history
            ]
        }
        
        return jsonify(payout_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/payouts/<int:payout_id>/approve', methods=['POST'])
@cross_origin()
def approve_payout(payout_id):
    """Approve a payout request"""
    try:
        data = request.get_json() or {}
        admin_id = data.get('admin_id', 1)  # Default admin ID for demo
        approval_notes = data.get('notes', '')
        
        success = approve_payout_request(payout_id, admin_id, approval_notes)
        
        if success:
            return jsonify({'message': 'Payout approved successfully'}), 200
        else:
            return jsonify({'error': 'Payout request not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/fraud-detection', methods=['GET'])
@cross_origin()
def get_fraud_detection():
    """Get fraud detection overview"""
    try:
        # Get fraud alerts
        fraud_alerts = db.session.query(
            FraudDetection,
            User.username
        ).join(User, FraudDetection.user_id == User.id)\
         .order_by(FraudDetection.detected_at.desc())\
         .limit(50).all()
        
        # Get fraud statistics
        fraud_stats = db.session.query(
            FraudDetection.fraud_type,
            db.func.count(FraudDetection.id).label('count'),
            db.func.avg(FraudDetection.risk_score).label('avg_risk_score')
        ).group_by(FraudDetection.fraud_type).all()
        
        fraud_data = {
            'statistics': {
                'total_alerts': len(fraud_alerts),
                'pending_investigations': FraudDetection.query.filter_by(status='pending').count(),
                'confirmed_fraud': FraudDetection.query.filter_by(status='confirmed_fraud').count(),
                'resolved_cases': FraudDetection.query.filter_by(status='resolved').count()
            },
            'fraud_types': [
                {
                    'type': stat.fraud_type,
                    'count': stat.count,
                    'avg_risk_score': float(stat.avg_risk_score or 0)
                }
                for stat in fraud_stats
            ],
            'recent_alerts': [
                {
                    'id': alert.FraudDetection.id,
                    'user_id': alert.FraudDetection.user_id,
                    'username': alert.username,
                    'fraud_type': alert.FraudDetection.fraud_type,
                    'risk_score': alert.FraudDetection.risk_score,
                    'status': alert.FraudDetection.status,
                    'suspicious_patterns': alert.FraudDetection.suspicious_patterns,
                    'detected_at': alert.FraudDetection.detected_at.isoformat()
                }
                for alert in fraud_alerts
            ]
        }
        
        return jsonify(fraud_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/users/<int:user_id>/fraud-check', methods=['POST'])
@cross_origin()
def run_fraud_check(user_id):
    """Run fraud detection on a specific user"""
    try:
        fraud_record = detect_multi_account_fraud(user_id)
        
        if fraud_record:
            return jsonify({
                'fraud_detected': True,
                'risk_score': fraud_record.risk_score,
                'suspicious_patterns': fraud_record.suspicious_patterns,
                'fraud_id': fraud_record.id
            }), 200
        else:
            return jsonify({
                'fraud_detected': False,
                'message': 'No suspicious activity detected'
            }), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/users/<int:user_id>/trust-score', methods=['GET'])
@cross_origin()
def get_user_trust_score(user_id):
    """Get user trust and loyalty scores"""
    try:
        scores = calculate_trust_and_loyalty_scores(user_id)
        
        if scores:
            return jsonify(scores), 200
        else:
            return jsonify({'error': 'User not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/content-moderation', methods=['GET'])
@cross_origin()
def get_content_moderation():
    """Get content moderation queue"""
    try:
        # Get pending content for review
        pending_content = db.session.query(
            ContentModerationQueue,
            User.username,
            ViralContentTracking.content_type,
            ViralContentTracking.platform_url
        ).join(User, ContentModerationQueue.user_id == User.id)\
         .join(ViralContentTracking, ContentModerationQueue.content_id == ViralContentTracking.id)\
         .filter(ContentModerationQueue.status == 'pending')\
         .order_by(ContentModerationQueue.submitted_at.desc()).all()
        
        moderation_data = {
            'pending_content': [
                {
                    'id': content.ContentModerationQueue.id,
                    'content_id': content.ContentModerationQueue.content_id,
                    'user_id': content.ContentModerationQueue.user_id,
                    'username': content.username,
                    'content_type': content.content_type,
                    'platform_url': content.platform_url,
                    'ai_content_score': content.ContentModerationQueue.ai_content_score,
                    'toxicity_score': content.ContentModerationQueue.toxicity_score,
                    'brand_safety_score': content.ContentModerationQueue.brand_safety_score,
                    'priority': content.ContentModerationQueue.priority,
                    'submitted_at': content.ContentModerationQueue.submitted_at.isoformat()
                }
                for content in pending_content
            ]
        }
        
        return jsonify(moderation_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/analytics', methods=['GET'])
@cross_origin()
def get_analytics():
    """Get comprehensive analytics data"""
    try:
        # Get date range from query params
        days = request.args.get('days', 30, type=int)
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # User growth analytics
        user_growth = db.session.query(
            db.func.date(User.join_date).label('date'),
            db.func.count(User.id).label('new_users')
        ).filter(User.join_date >= start_date)\
         .group_by(db.func.date(User.join_date))\
         .order_by(db.func.date(User.join_date)).all()
        
        # Revenue analytics
        revenue_data = db.session.query(
            db.func.date(ReferralTracking.converted_at).label('date'),
            db.func.sum(ReferralTracking.referral_bonus).label('revenue')
        ).filter(
            ReferralTracking.converted_at >= start_date,
            ReferralTracking.payment_status == 'completed'
        ).group_by(db.func.date(ReferralTracking.converted_at))\
         .order_by(db.func.date(ReferralTracking.converted_at)).all()
        
        # Referral conversion funnel
        funnel_data = {
            'total_signups': User.query.filter(User.join_date >= start_date).count(),
            'referred_signups': User.query.filter(
                User.join_date >= start_date,
                User.referred_by_id.isnot(None)
            ).count(),
            'converted_referrals': ReferralTracking.query.filter(
                ReferralTracking.referred_at >= start_date,
                ReferralTracking.payment_status == 'completed'
            ).count(),
            'paid_bonuses': ReferralTracking.query.filter(
                ReferralTracking.referred_at >= start_date,
                ReferralTracking.status == 'bonus_paid'
            ).count()
        }
        
        analytics_data = {
            'user_growth': [
                {
                    'date': growth.date.isoformat(),
                    'new_users': growth.new_users
                }
                for growth in user_growth
            ],
            'revenue_data': [
                {
                    'date': revenue.date.isoformat(),
                    'revenue': float(revenue.revenue or 0)
                }
                for revenue in revenue_data
            ],
            'conversion_funnel': funnel_data
        }
        
        return jsonify(analytics_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Security and audit routes
@admin_bp.route('/admin/security-logs', methods=['GET'])
@cross_origin()
def get_security_logs():
    """Get security logs"""
    try:
        logs = SecurityLog.query.order_by(SecurityLog.created_at.desc()).limit(100).all()
        
        security_data = {
            'logs': [
                {
                    'id': log.id,
                    'user_id': log.user_id,
                    'event_type': log.event_type,
                    'event_description': log.event_description,
                    'ip_address': log.ip_address,
                    'risk_level': log.risk_level,
                    'created_at': log.created_at.isoformat()
                }
                for log in logs
            ]
        }
        
        return jsonify(security_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/audit-logs', methods=['GET'])
@cross_origin()
def get_audit_logs():
    """Get referral audit logs"""
    try:
        logs = ReferralAuditLog.query.order_by(ReferralAuditLog.created_at.desc()).limit(100).all()
        
        audit_data = {
            'logs': [
                {
                    'id': log.id,
                    'referral_id': log.referral_id,
                    'action': log.action,
                    'old_values': log.old_values,
                    'new_values': log.new_values,
                    'triggered_by': log.triggered_by,
                    'reason': log.reason,
                    'created_at': log.created_at.isoformat()
                }
                for log in logs
            ]
        }
        
        return jsonify(audit_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Health check
@admin_bp.route('/admin/health', methods=['GET'])
@cross_origin()
def admin_health_check():
    """Admin API health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    }), 200

