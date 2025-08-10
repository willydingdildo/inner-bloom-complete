from flask import Blueprint, request, jsonify
import uuid
import random
from datetime import datetime, timedelta
from src.models.advertising import (
    AdNetwork, AdPlacement, SponsoredContent, AdRevenue,
    ad_networks_db, ad_placements_db, sponsored_content_db, ad_revenue_db
)

advertising_bp = Blueprint('advertising', __name__)

@advertising_bp.route('/ads/networks', methods=['GET'])
def get_ad_networks():
    """Get all available ad networks"""
    networks = [network.to_dict() for network in ad_networks_db.values() if network.is_active]
    return jsonify({
        'success': True,
        'networks': networks
    })

@advertising_bp.route('/ads/placements', methods=['GET'])
def get_ad_placements():
    """Get all ad placements"""
    placements = [placement.to_dict() for placement in ad_placements_db.values() if placement.is_active]
    return jsonify({
        'success': True,
        'placements': placements
    })

@advertising_bp.route('/ads/content/<location>', methods=['GET'])
def get_ads_for_location(location):
    """Get ads for a specific location/placement"""
    user_id = request.args.get('user_id')
    user_tier = request.args.get('user_tier', 'free')
    
    # Find placement
    placement = None
    for p in ad_placements_db.values():
        if p.location == location and p.is_active:
            placement = p
            break
    
    if not placement:
        return jsonify({'success': False, 'error': 'Invalid placement location'}), 404
    
    # Get relevant sponsored content
    relevant_ads = []
    for content in sponsored_content_db.values():
        if not content.is_active or content.spent >= content.budget:
            continue
            
        # Check if user matches target audience
        target = content.target_audience
        if user_tier not in target.get('subscription_tier', ['free', 'premium', 'vip']):
            continue
            
        relevant_ads.append(content)
    
    # Select ads based on budget and targeting
    selected_ads = sorted(relevant_ads, key=lambda x: x.budget - x.spent, reverse=True)[:3]
    
    # Simulate ad serving
    ads_to_serve = []
    for ad in selected_ads:
        # Simulate impression
        ad.impressions += 1
        placement.impressions += 1
        
        # Update revenue tracking
        platform_revenue = ad_revenue_db.get('platform')
        if platform_revenue:
            platform_revenue.total_impressions += 1
            platform_revenue.calculate_average_ctr()
        
        ads_to_serve.append({
            'content_id': ad.content_id,
            'title': ad.title,
            'description': ad.description,
            'image_url': ad.image_url,
            'target_url': f"/ads/click/{ad.content_id}",  # Tracking URL
            'advertiser': ad.advertiser,
            'ad_type': placement.ad_type
        })
    
    return jsonify({
        'success': True,
        'ads': ads_to_serve,
        'placement': {
            'id': placement.placement_id,
            'type': placement.ad_type,
            'dimensions': placement.dimensions
        }
    })

@advertising_bp.route('/ads/click/<content_id>', methods=['POST'])
def track_ad_click(content_id):
    """Track ad click and redirect"""
    content = sponsored_content_db.get(content_id)
    if not content:
        return jsonify({'success': False, 'error': 'Invalid content ID'}), 404
    
    # Track click
    content.clicks += 1
    
    # Calculate cost (simplified - in reality this would be more complex)
    click_cost = random.uniform(0.50, 2.00)  # $0.50 - $2.00 per click
    content.spent += click_cost
    content.calculate_metrics()
    
    # Update placement metrics
    for placement in ad_placements_db.values():
        if placement.location in ['feed_native', 'homepage_banner', 'sidebar']:  # Simplified
            placement.clicks += 1
            placement.revenue += click_cost * 0.7  # 70% revenue share
            placement.calculate_ctr()
            break
    
    # Update platform revenue
    platform_revenue = ad_revenue_db.get('platform')
    if platform_revenue:
        platform_revenue.total_clicks += 1
        platform_revenue.total_revenue += click_cost * 0.7
        platform_revenue.pending_revenue += click_cost * 0.7
        platform_revenue.calculate_average_ctr()
        platform_revenue.last_updated = datetime.utcnow()
    
    return jsonify({
        'success': True,
        'redirect_url': content.target_url,
        'click_tracked': True
    })

@advertising_bp.route('/ads/revenue', methods=['GET'])
def get_ad_revenue():
    """Get advertising revenue analytics"""
    platform_revenue = ad_revenue_db.get('platform')
    if not platform_revenue:
        return jsonify({'success': False, 'error': 'No revenue data found'}), 404
    
    # Calculate daily/weekly/monthly revenue
    today_revenue = random.uniform(150, 300)  # Simulated daily revenue
    weekly_revenue = today_revenue * 7 * random.uniform(0.8, 1.2)
    monthly_revenue = weekly_revenue * 4.3 * random.uniform(0.9, 1.1)
    
    # Top performing placements
    top_placements = sorted(
        ad_placements_db.values(), 
        key=lambda x: x.revenue, 
        reverse=True
    )[:5]
    
    # Network performance
    network_performance = {}
    for network in ad_networks_db.values():
        network_performance[network.name] = {
            'revenue_share': network.revenue_share,
            'estimated_revenue': random.uniform(50, 200),
            'impressions': random.randint(1000, 5000),
            'clicks': random.randint(50, 200)
        }
    
    return jsonify({
        'success': True,
        'revenue': {
            'total': platform_revenue.total_revenue,
            'pending': platform_revenue.pending_revenue,
            'paid': platform_revenue.paid_revenue,
            'today': today_revenue,
            'weekly': weekly_revenue,
            'monthly': monthly_revenue
        },
        'metrics': {
            'total_impressions': platform_revenue.total_impressions,
            'total_clicks': platform_revenue.total_clicks,
            'average_ctr': platform_revenue.average_ctr,
            'last_updated': platform_revenue.last_updated
        },
        'top_placements': [p.to_dict() for p in top_placements],
        'network_performance': network_performance
    })

@advertising_bp.route('/ads/sponsored-content', methods=['POST'])
def create_sponsored_content():
    """Create new sponsored content (for advertisers)"""
    data = request.get_json()
    
    required_fields = ['advertiser', 'title', 'description', 'target_url', 'budget']
    if not all(field in data for field in required_fields):
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400
    
    content_id = str(uuid.uuid4())
    sponsored_content = SponsoredContent(
        content_id=content_id,
        advertiser=data['advertiser'],
        title=data['title'],
        description=data['description'],
        image_url=data.get('image_url', ''),
        target_url=data['target_url'],
        budget=float(data['budget']),
        target_audience=data.get('target_audience', {})
    )
    
    sponsored_content_db[content_id] = sponsored_content
    
    return jsonify({
        'success': True,
        'content': sponsored_content.to_dict()
    })

@advertising_bp.route('/ads/sponsored-content', methods=['GET'])
def get_sponsored_content():
    """Get all sponsored content"""
    content_list = [content.to_dict() for content in sponsored_content_db.values()]
    return jsonify({
        'success': True,
        'content': content_list
    })

@advertising_bp.route('/ads/analytics', methods=['GET'])
def get_advertising_analytics():
    """Get comprehensive advertising analytics"""
    # Calculate overall performance
    total_impressions = sum(p.impressions for p in ad_placements_db.values())
    total_clicks = sum(p.clicks for p in ad_placements_db.values())
    total_revenue = sum(p.revenue for p in ad_placements_db.values())
    
    # Calculate trends (simulated)
    daily_trends = []
    for i in range(30):
        date = datetime.utcnow() - timedelta(days=i)
        daily_trends.append({
            'date': date.strftime('%Y-%m-%d'),
            'impressions': random.randint(800, 1500),
            'clicks': random.randint(40, 100),
            'revenue': random.uniform(20, 80)
        })
    
    # Top advertisers
    advertiser_performance = {}
    for content in sponsored_content_db.values():
        if content.advertiser not in advertiser_performance:
            advertiser_performance[content.advertiser] = {
                'total_spent': 0,
                'total_impressions': 0,
                'total_clicks': 0,
                'campaigns': 0
            }
        
        advertiser_performance[content.advertiser]['total_spent'] += content.spent
        advertiser_performance[content.advertiser]['total_impressions'] += content.impressions
        advertiser_performance[content.advertiser]['total_clicks'] += content.clicks
        advertiser_performance[content.advertiser]['campaigns'] += 1
    
    # Revenue by category
    category_revenue = {
        'wellness': random.uniform(200, 400),
        'fashion': random.uniform(150, 350),
        'business': random.uniform(300, 500),
        'beauty': random.uniform(100, 250),
        'lifestyle': random.uniform(80, 200)
    }
    
    return jsonify({
        'success': True,
        'analytics': {
            'overview': {
                'total_impressions': total_impressions,
                'total_clicks': total_clicks,
                'total_revenue': total_revenue,
                'average_ctr': (total_clicks / total_impressions * 100) if total_impressions > 0 else 0,
                'average_cpm': (total_revenue / total_impressions * 1000) if total_impressions > 0 else 0
            },
            'daily_trends': daily_trends,
            'advertiser_performance': advertiser_performance,
            'category_revenue': category_revenue,
            'placement_performance': [p.to_dict() for p in ad_placements_db.values()]
        }
    })

@advertising_bp.route('/ads/optimize', methods=['POST'])
def optimize_ad_placements():
    """AI-powered ad placement optimization"""
    data = request.get_json()
    user_profile = data.get('user_profile', {})
    
    # Simulate AI optimization based on user profile
    recommendations = []
    
    # Analyze user interests and behavior
    interests = user_profile.get('interests', [])
    subscription_tier = user_profile.get('subscription_tier', 'free')
    engagement_score = user_profile.get('engagement_score', 50)
    
    # Generate personalized ad recommendations
    if 'wellness' in interests:
        recommendations.append({
            'placement': 'sidebar_square',
            'content_type': 'wellness',
            'expected_ctr': 3.2,
            'expected_revenue': 1.50
        })
    
    if 'fashion' in interests:
        recommendations.append({
            'placement': 'feed_native',
            'content_type': 'fashion',
            'expected_ctr': 2.8,
            'expected_revenue': 1.20
        })
    
    if subscription_tier in ['premium', 'vip']:
        recommendations.append({
            'placement': 'article_inline',
            'content_type': 'business',
            'expected_ctr': 4.1,
            'expected_revenue': 2.30
        })
    
    # Optimize based on engagement
    if engagement_score > 70:
        recommendations.append({
            'placement': 'homepage_hero',
            'content_type': 'premium_brand',
            'expected_ctr': 5.2,
            'expected_revenue': 3.10
        })
    
    return jsonify({
        'success': True,
        'recommendations': recommendations,
        'optimization_score': random.uniform(75, 95),
        'estimated_revenue_increase': random.uniform(15, 35)
    })

@advertising_bp.route('/ads/user-revenue/<user_id>', methods=['GET'])
def get_user_ad_revenue(user_id):
    """Get ad revenue sharing for specific user (for premium features)"""
    # In a real implementation, users might get a share of ad revenue
    # based on their content engagement or premium subscription
    
    user_revenue = ad_revenue_db.get(user_id)
    if not user_revenue:
        user_revenue = AdRevenue(user_id)
        # Simulate some revenue for premium users
        user_revenue.total_revenue = random.uniform(10, 50)
        user_revenue.pending_revenue = random.uniform(5, 25)
        ad_revenue_db[user_id] = user_revenue
    
    return jsonify({
        'success': True,
        'revenue': user_revenue.to_dict(),
        'revenue_share_rate': 0.10,  # 10% of platform ad revenue shared with premium users
        'next_payout': (datetime.utcnow() + timedelta(days=30)).isoformat()
    })

