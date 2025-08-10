from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from src.models.monetization import (
    Subscription, DigitalProduct, Purchase, AffiliateLink, 
    AffiliateClick, ReferralProgram, RevenueMetrics, db
)
import json
from datetime import datetime, date
import secrets
import string

monetization_bp = Blueprint('monetization', __name__)

@monetization_bp.route('/subscriptions/<int:user_id>', methods=['GET'])
@cross_origin()
def get_user_subscription(user_id):
    """Get user's current subscription"""
    subscription = Subscription.query.filter_by(user_id=user_id).first()
    if not subscription:
        # Create free subscription if none exists
        subscription = Subscription(
            user_id=user_id,
            plan_type='free',
            status='active',
            monthly_price=0.0
        )
        db.session.add(subscription)
        db.session.commit()
    
    return jsonify(subscription.to_dict())

@monetization_bp.route('/subscriptions', methods=['POST'])
@cross_origin()
def create_subscription():
    """Create or update a subscription"""
    data = request.json
    
    # Check if user already has a subscription
    existing = Subscription.query.filter_by(user_id=data['user_id']).first()
    if existing:
        # Update existing subscription
        existing.plan_type = data['plan_type']
        existing.stripe_subscription_id = data.get('stripe_subscription_id')
        existing.stripe_customer_id = data.get('stripe_customer_id')
        existing.status = data.get('status', 'active')
        existing.monthly_price = data.get('monthly_price', 0.0)
        if 'current_period_start' in data:
            existing.current_period_start = datetime.fromisoformat(data['current_period_start'])
        if 'current_period_end' in data:
            existing.current_period_end = datetime.fromisoformat(data['current_period_end'])
        
        db.session.commit()
        return jsonify(existing.to_dict())
    else:
        # Create new subscription
        subscription = Subscription(
            user_id=data['user_id'],
            plan_type=data['plan_type'],
            stripe_subscription_id=data.get('stripe_subscription_id'),
            stripe_customer_id=data.get('stripe_customer_id'),
            status=data.get('status', 'active'),
            monthly_price=data.get('monthly_price', 0.0)
        )
        
        if 'current_period_start' in data:
            subscription.current_period_start = datetime.fromisoformat(data['current_period_start'])
        if 'current_period_end' in data:
            subscription.current_period_end = datetime.fromisoformat(data['current_period_end'])
        
        db.session.add(subscription)
        db.session.commit()
        return jsonify(subscription.to_dict()), 201

@monetization_bp.route('/digital-products', methods=['GET'])
@cross_origin()
def get_digital_products():
    """Get all active digital products"""
    category = request.args.get('category')
    
    query = DigitalProduct.query.filter_by(is_active=True)
    if category:
        query = query.filter_by(category=category)
    
    products = query.order_by(DigitalProduct.created_at.desc()).all()
    return jsonify([product.to_dict() for product in products])

@monetization_bp.route('/digital-products', methods=['POST'])
@cross_origin()
def create_digital_product():
    """Create a new digital product"""
    data = request.json
    product = DigitalProduct(
        name=data['name'],
        description=data.get('description', ''),
        category=data['category'],
        price=data['price'],
        stripe_price_id=data.get('stripe_price_id'),
        file_url=data.get('file_url', ''),
        preview_content=data.get('preview_content', ''),
        tags=json.dumps(data.get('tags', []))
    )
    db.session.add(product)
    db.session.commit()
    
    return jsonify(product.to_dict()), 201

@monetization_bp.route('/digital-products/<int:product_id>', methods=['PUT'])
@cross_origin()
def update_digital_product(product_id):
    """Update a digital product"""
    product = DigitalProduct.query.get_or_404(product_id)
    data = request.json
    
    for field in ['name', 'description', 'category', 'price', 'stripe_price_id', 
                  'file_url', 'preview_content', 'is_active']:
        if field in data:
            if field == 'tags':
                setattr(product, field, json.dumps(data[field]))
            else:
                setattr(product, field, data[field])
    
    db.session.commit()
    return jsonify(product.to_dict())

@monetization_bp.route('/purchases', methods=['POST'])
@cross_origin()
def record_purchase():
    """Record a digital product purchase"""
    data = request.json
    purchase = Purchase(
        user_id=data['user_id'],
        product_id=data['product_id'],
        stripe_payment_intent_id=data.get('stripe_payment_intent_id'),
        amount_paid=data['amount_paid']
    )
    db.session.add(purchase)
    
    # Update product sales count
    product = DigitalProduct.query.get(data['product_id'])
    if product:
        product.sales_count += 1
    
    db.session.commit()
    
    return jsonify(purchase.to_dict()), 201

@monetization_bp.route('/purchases/<int:user_id>', methods=['GET'])
@cross_origin()
def get_user_purchases(user_id):
    """Get user's purchase history"""
    purchases = Purchase.query.filter_by(user_id=user_id)\
                             .order_by(Purchase.purchase_date.desc()).all()
    return jsonify([purchase.to_dict() for purchase in purchases])

@monetization_bp.route('/affiliate-links', methods=['GET'])
@cross_origin()
def get_affiliate_links():
    """Get all active affiliate links"""
    category = request.args.get('category')
    
    query = AffiliateLink.query.filter_by(is_active=True)
    if category:
        query = query.filter_by(category=category)
    
    links = query.order_by(AffiliateLink.created_at.desc()).all()
    return jsonify([link.to_dict() for link in links])

@monetization_bp.route('/affiliate-links', methods=['POST'])
@cross_origin()
def create_affiliate_link():
    """Create a new affiliate link"""
    data = request.json
    link = AffiliateLink(
        product_name=data['product_name'],
        affiliate_url=data['affiliate_url'],
        commission_rate=data.get('commission_rate', 0.0),
        category=data.get('category', ''),
        description=data.get('description', ''),
        image_url=data.get('image_url', '')
    )
    db.session.add(link)
    db.session.commit()
    
    return jsonify(link.to_dict()), 201

@monetization_bp.route('/affiliate-links/<int:link_id>/click', methods=['POST'])
@cross_origin()
def track_affiliate_click(link_id):
    """Track an affiliate link click"""
    data = request.json
    
    click = AffiliateClick(
        affiliate_link_id=link_id,
        user_id=data.get('user_id'),
        ip_address=data.get('ip_address', ''),
        user_agent=data.get('user_agent', ''),
        referrer=data.get('referrer', '')
    )
    db.session.add(click)
    
    # Update link click count
    link = AffiliateLink.query.get(link_id)
    if link:
        link.click_count += 1
    
    db.session.commit()
    
    return jsonify({'message': 'Click tracked', 'redirect_url': link.affiliate_url if link else None})

@monetization_bp.route('/referral-program/<int:user_id>', methods=['GET'])
@cross_origin()
def get_user_referrals(user_id):
    """Get user's referral information"""
    referrals = ReferralProgram.query.filter_by(referrer_id=user_id).all()
    
    # Generate referral code if user doesn't have one
    if not referrals:
        referral_code = generate_referral_code()
    else:
        referral_code = referrals[0].referral_code
    
    total_commission = sum(r.commission_earned for r in referrals)
    
    return jsonify({
        'referral_code': referral_code,
        'total_referrals': len(referrals),
        'total_commission': total_commission,
        'referrals': [r.to_dict() for r in referrals]
    })

@monetization_bp.route('/referral-program', methods=['POST'])
@cross_origin()
def create_referral():
    """Create a new referral"""
    data = request.json
    
    referral = ReferralProgram(
        referrer_id=data['referrer_id'],
        referred_id=data['referred_id'],
        referral_code=data['referral_code'],
        commission_earned=data.get('commission_earned', 0.0),
        status=data.get('status', 'pending')
    )
    db.session.add(referral)
    db.session.commit()
    
    return jsonify(referral.to_dict()), 201

@monetization_bp.route('/revenue-metrics', methods=['GET'])
@cross_origin()
def get_revenue_metrics():
    """Get revenue metrics"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = RevenueMetrics.query
    
    if start_date:
        query = query.filter(RevenueMetrics.date >= datetime.fromisoformat(start_date).date())
    if end_date:
        query = query.filter(RevenueMetrics.date <= datetime.fromisoformat(end_date).date())
    
    metrics = query.order_by(RevenueMetrics.date.desc()).all()
    return jsonify([metric.to_dict() for metric in metrics])

@monetization_bp.route('/revenue-metrics', methods=['POST'])
@cross_origin()
def update_revenue_metrics():
    """Update daily revenue metrics"""
    data = request.json
    metric_date = datetime.fromisoformat(data['date']).date()
    
    # Check if metrics for this date already exist
    existing = RevenueMetrics.query.filter_by(date=metric_date).first()
    
    if existing:
        # Update existing metrics
        for field in ['subscription_revenue', 'digital_product_revenue', 'affiliate_commission',
                     'transaction_fees', 'total_revenue', 'new_subscribers', 
                     'canceled_subscriptions', 'active_users']:
            if field in data:
                setattr(existing, field, data[field])
        db.session.commit()
        return jsonify(existing.to_dict())
    else:
        # Create new metrics
        metrics = RevenueMetrics(
            date=metric_date,
            subscription_revenue=data.get('subscription_revenue', 0.0),
            digital_product_revenue=data.get('digital_product_revenue', 0.0),
            affiliate_commission=data.get('affiliate_commission', 0.0),
            transaction_fees=data.get('transaction_fees', 0.0),
            total_revenue=data.get('total_revenue', 0.0),
            new_subscribers=data.get('new_subscribers', 0),
            canceled_subscriptions=data.get('canceled_subscriptions', 0),
            active_users=data.get('active_users', 0)
        )
        db.session.add(metrics)
        db.session.commit()
        return jsonify(metrics.to_dict()), 201

@monetization_bp.route('/subscription-plans', methods=['GET'])
@cross_origin()
def get_subscription_plans():
    """Get available subscription plans"""
    plans = [
        {
            'id': 'free',
            'name': 'Free',
            'price': 0,
            'features': [
                'Basic AI affirmations',
                'Limited community access',
                'Basic mood tracking',
                '5 journal entries per month'
            ]
        },
        {
            'id': 'premium',
            'name': 'Premium',
            'price': 29.99,
            'features': [
                'Full Bloom AI Companion',
                'Unlimited journaling',
                'Voice-activated journaling',
                'Personalized growth paths',
                'Premium community access',
                'Health data integration'
            ]
        },
        {
            'id': 'vip',
            'name': 'VIP',
            'price': 59.99,
            'features': [
                'Everything in Premium',
                'AI dream interpretation',
                'Advanced health insights',
                'Monthly coaching session',
                'Early access to features',
                'VIP community events'
            ]
        }
    ]
    
    return jsonify(plans)

def generate_referral_code():
    """Generate a unique referral code"""
    while True:
        code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))
        existing = ReferralProgram.query.filter_by(referral_code=code).first()
        if not existing:
            return code

