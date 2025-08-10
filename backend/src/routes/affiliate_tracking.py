from flask import Blueprint, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import requests
import json
from ..models.affiliate_tracking import *
from ..models.user import User

affiliate_bp = Blueprint('affiliate_tracking', __name__, url_prefix='/api/affiliate')

@affiliate_bp.route('/programs', methods=['GET'])
def get_affiliate_programs():
    """Get all available affiliate programs"""
    try:
        category = request.args.get('category')
        
        query = AffiliateProgram.query.filter_by(is_active=True)
        if category:
            query = query.filter_by(category=category)
        
        programs = query.all()
        
        return jsonify({
            'success': True,
            'programs': [{
                'id': p.id,
                'name': p.name,
                'company': p.company,
                'commission_rate': p.commission_rate,
                'commission_type': p.commission_type,
                'category': p.category,
                'description': p.description,
                'minimum_payout': p.minimum_payout,
                'payment_schedule': p.payment_schedule
            } for p in programs]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@affiliate_bp.route('/link/create', methods=['POST'])
def create_user_affiliate_link():
    """Create an affiliate link for a user"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        program_id = data.get('program_id')
        custom_params = data.get('custom_params', {})
        
        if not user_id or not program_id:
            return jsonify({'success': False, 'error': 'User ID and Program ID required'}), 400
        
        user_link = create_affiliate_link(user_id, program_id, custom_params)
        
        if not user_link:
            return jsonify({'success': False, 'error': 'Program not found'}), 404
        
        return jsonify({
            'success': True,
            'link': {
                'id': user_link.id,
                'unique_code': user_link.unique_code,
                'custom_url': user_link.custom_url,
                'total_clicks': user_link.total_clicks,
                'total_conversions': user_link.total_conversions,
                'total_earnings': user_link.total_earnings
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@affiliate_bp.route('/click/<link_code>', methods=['GET'])
def track_click(link_code):
    """Track affiliate link click and redirect"""
    try:
        user_link = UserAffiliateLink.query.filter_by(unique_code=link_code).first()
        
        if not user_link or not user_link.is_active:
            return jsonify({'success': False, 'error': 'Invalid link'}), 404
        
        # Collect visitor data
        visitor_data = {
            'ip': request.remote_addr,
            'user_agent': request.headers.get('User-Agent'),
            'referrer': request.headers.get('Referer'),
            'session_id': request.headers.get('X-Session-ID')
        }
        
        # Track the click
        click = track_affiliate_click(user_link.id, visitor_data)
        
        # Redirect to the actual affiliate URL
        return redirect(user_link.custom_url)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@affiliate_bp.route('/conversion', methods=['POST'])
def record_conversion():
    """Record an affiliate conversion"""
    try:
        data = request.get_json()
        link_code = data.get('link_code')
        conversion_value = data.get('conversion_value')
        transaction_id = data.get('transaction_id')
        
        user_link = UserAffiliateLink.query.filter_by(unique_code=link_code).first()
        
        if not user_link:
            return jsonify({'success': False, 'error': 'Invalid link code'}), 404
        
        conversion = record_affiliate_conversion(
            user_link.id, 
            conversion_value, 
            transaction_id
        )
        
        return jsonify({
            'success': True,
            'conversion': {
                'id': conversion.id,
                'commission_earned': conversion.commission_earned,
                'status': conversion.status
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@affiliate_bp.route('/earnings/<int:user_id>', methods=['GET'])
def get_user_earnings(user_id):
    """Get user's earnings breakdown"""
    try:
        user_earnings = UserEarnings.query.filter_by(user_id=user_id).first()
        
        if not user_earnings:
            user_earnings = UserEarnings(user_id=user_id)
            db.session.add(user_earnings)
            db.session.commit()
        
        # Get recent conversions
        recent_conversions = db.session.query(AffiliateConversion)\
            .join(UserAffiliateLink)\
            .filter(UserAffiliateLink.user_id == user_id)\
            .order_by(AffiliateConversion.conversion_timestamp.desc())\
            .limit(10).all()
        
        # Get referral stats
        referral_count = ReferralTracking.query.filter_by(
            referrer_id=user_id, 
            status='converted'
        ).count()
        
        return jsonify({
            'success': True,
            'earnings': {
                'referral_earnings': user_earnings.referral_earnings,
                'affiliate_earnings': user_earnings.affiliate_earnings,
                'content_earnings': user_earnings.content_earnings,
                'community_earnings': user_earnings.community_earnings,
                'total_earnings': user_earnings.total_earnings,
                'total_paid': user_earnings.total_paid,
                'pending_payout': user_earnings.pending_payout,
                'last_payout_date': user_earnings.last_payout_date.isoformat() if user_earnings.last_payout_date else None,
                'payment_method': user_earnings.payment_method,
                'referral_count': referral_count
            },
            'recent_conversions': [{
                'id': c.id,
                'commission_earned': c.commission_earned,
                'conversion_timestamp': c.conversion_timestamp.isoformat(),
                'status': c.status
            } for c in recent_conversions]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@affiliate_bp.route('/payout/request', methods=['POST'])
def request_payout():
    """Request a payout"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        amount = data.get('amount')
        payment_method = data.get('payment_method')
        payment_details = data.get('payment_details')
        
        user_earnings = UserEarnings.query.filter_by(user_id=user_id).first()
        
        if not user_earnings:
            return jsonify({'success': False, 'error': 'No earnings found'}), 404
        
        if amount > user_earnings.pending_payout:
            return jsonify({'success': False, 'error': 'Insufficient balance'}), 400
        
        if amount < 25.0:  # Minimum payout
            return jsonify({'success': False, 'error': 'Minimum payout is $25'}), 400
        
        # Create payout request
        payout_request = PayoutRequest(
            user_id=user_id,
            amount=amount,
            payment_method=payment_method,
            payment_details=payment_details
        )
        
        db.session.add(payout_request)
        
        # Update pending payout
        user_earnings.pending_payout -= amount
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'payout_request': {
                'id': payout_request.id,
                'amount': payout_request.amount,
                'status': payout_request.status,
                'requested_at': payout_request.requested_at.isoformat()
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@affiliate_bp.route('/viral-content/submit', methods=['POST'])
def submit_viral_content():
    """Submit viral content for reward"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        content_type = data.get('content_type')
        platform_url = data.get('platform_url')
        content_description = data.get('content_description')
        
        # Create content tracking record
        content_tracking = ViralContentTracking(
            user_id=user_id,
            content_type=content_type,
            platform_url=platform_url,
            content_description=content_description
        )
        
        db.session.add(content_tracking)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'content_id': content_tracking.id,
            'status': 'submitted',
            'message': 'Content submitted for review. Rewards will be processed within 24-48 hours.'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@affiliate_bp.route('/viral-content/approve', methods=['POST'])
def approve_viral_content():
    """Approve viral content and process reward (admin only)"""
    try:
        data = request.get_json()
        content_id = data.get('content_id')
        performance_metrics = data.get('performance_metrics', {})
        
        content = ViralContentTracking.query.get(content_id)
        if not content:
            return jsonify({'success': False, 'error': 'Content not found'}), 404
        
        # Process reward
        total_reward = process_viral_content_reward(
            content.user_id,
            content.content_type,
            performance_metrics
        )
        
        # Update content record
        content.status = 'approved'
        content.reviewed_at = datetime.utcnow()
        content.total_earned = total_reward
        
        # Update performance metrics
        for key, value in performance_metrics.items():
            if hasattr(content, key):
                setattr(content, key, value)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'total_reward': total_reward,
            'status': 'approved'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@affiliate_bp.route('/referral/track', methods=['POST'])
def track_referral():
    """Track a new referral"""
    try:
        data = request.get_json()
        referrer_id = data.get('referrer_id')
        referred_id = data.get('referred_id')
        referral_code = data.get('referral_code')
        
        # Create referral tracking
        referral = ReferralTracking(
            referrer_id=referrer_id,
            referred_id=referred_id,
            referral_code=referral_code
        )
        
        db.session.add(referral)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'referral_id': referral.id
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@affiliate_bp.route('/referral/convert', methods=['POST'])
def convert_referral():
    """Convert a referral to paying customer"""
    try:
        data = request.get_json()
        referred_id = data.get('referred_id')
        subscription_type = data.get('subscription_type')
        
        referral = ReferralTracking.query.filter_by(
            referred_id=referred_id,
            status='pending'
        ).first()
        
        if not referral:
            return jsonify({'success': False, 'error': 'Referral not found'}), 404
        
        # Update referral status
        referral.status = 'converted'
        referral.converted_at = datetime.utcnow()
        referral.subscription_type = subscription_type
        
        # Calculate and award bonus
        bonus, tier = calculate_referral_bonus(referral.referrer_id, subscription_type)
        referral.referral_bonus = bonus
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'bonus_awarded': bonus,
            'referrer_tier': tier
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@affiliate_bp.route('/stats/<int:user_id>', methods=['GET'])
def get_affiliate_stats(user_id):
    """Get comprehensive affiliate stats for a user"""
    try:
        # Get user's affiliate links
        user_links = UserAffiliateLink.query.filter_by(user_id=user_id).all()
        
        # Get earnings
        user_earnings = UserEarnings.query.filter_by(user_id=user_id).first()
        
        # Get referral stats
        referrals = ReferralTracking.query.filter_by(referrer_id=user_id).all()
        
        # Get viral content stats
        viral_content = ViralContentTracking.query.filter_by(user_id=user_id).all()
        
        return jsonify({
            'success': True,
            'stats': {
                'affiliate_links': len(user_links),
                'total_clicks': sum(link.total_clicks for link in user_links),
                'total_conversions': sum(link.total_conversions for link in user_links),
                'total_earnings': user_earnings.total_earnings if user_earnings else 0,
                'pending_payout': user_earnings.pending_payout if user_earnings else 0,
                'referrals_made': len(referrals),
                'referrals_converted': len([r for r in referrals if r.status == 'converted']),
                'viral_content_pieces': len(viral_content),
                'viral_content_approved': len([v for v in viral_content if v.status == 'approved'])
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Initialize default affiliate programs
def init_affiliate_programs():
    """Initialize default affiliate programs"""
    default_programs = [
        {
            'name': 'Tony Robbins Programs',
            'company': 'Tony Robbins',
            'commission_rate': 40.0,
            'category': 'personal_development',
            'description': 'Life coaching and personal development programs',
            'affiliate_url': 'https://www.tonyrobbins.com/affiliate-link',
            'minimum_payout': 50.0
        },
        {
            'name': 'Mindvalley Courses',
            'company': 'Mindvalley',
            'commission_rate': 40.0,
            'category': 'personal_development',
            'description': 'Personal growth courses and meditation programs',
            'affiliate_url': 'https://www.mindvalley.com/affiliate',
            'minimum_payout': 25.0
        },
        {
            'name': 'Everlane Fashion',
            'company': 'Everlane',
            'commission_rate': 8.0,
            'category': 'fashion',
            'description': 'Sustainable and transparent fashion',
            'affiliate_url': 'https://www.everlane.com/affiliate',
            'minimum_payout': 25.0
        },
        {
            'name': 'Ritual Vitamins',
            'company': 'Ritual',
            'commission_rate': 25.0,
            'category': 'wellness',
            'description': 'Women\'s health supplements',
            'affiliate_url': 'https://ritual.com/affiliate',
            'minimum_payout': 25.0
        },
        {
            'name': 'Shopify',
            'company': 'Shopify',
            'commission_rate': 200.0,
            'commission_type': 'fixed',
            'category': 'business',
            'description': 'E-commerce platform for entrepreneurs',
            'affiliate_url': 'https://www.shopify.com/affiliates',
            'minimum_payout': 25.0
        }
    ]
    
    for program_data in default_programs:
        existing = AffiliateProgram.query.filter_by(name=program_data['name']).first()
        if not existing:
            program = AffiliateProgram(**program_data)
            db.session.add(program)
    
    db.session.commit()

