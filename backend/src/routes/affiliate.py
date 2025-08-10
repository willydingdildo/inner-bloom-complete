from flask import Blueprint, request, jsonify
import uuid
from datetime import datetime, timedelta
from src.models.affiliate import (
    AffiliateLink, AffiliateClick, AffiliateEarnings,
    affiliate_links_db, affiliate_clicks_db, affiliate_programs_db, affiliate_earnings_db
)

affiliate_bp = Blueprint('affiliate', __name__)

@affiliate_bp.route('/affiliate/programs', methods=['GET'])
def get_affiliate_programs():
    """Get all available affiliate programs"""
    programs = [program.to_dict() for program in affiliate_programs_db.values() if program.is_active]
    return jsonify({
        'success': True,
        'programs': programs
    })

@affiliate_bp.route('/affiliate/links', methods=['POST'])
def create_affiliate_link():
    """Create a new affiliate link"""
    data = request.get_json()
    
    required_fields = ['user_id', 'product_name', 'original_url', 'program_id']
    if not all(field in data for field in required_fields):
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400
    
    # Get the affiliate program
    program = affiliate_programs_db.get(data['program_id'])
    if not program:
        return jsonify({'success': False, 'error': 'Invalid affiliate program'}), 400
    
    # Generate affiliate link
    link_id = str(uuid.uuid4())
    affiliate_url = f"https://innerbloom.com/go/{link_id}"
    
    # Get user tier for commission rate
    user_earnings = affiliate_earnings_db.get(data['user_id'])
    user_tier = user_earnings.tier if user_earnings else 'bronze'
    commission_rate = program.get_commission_rate(user_tier)
    
    affiliate_link = AffiliateLink(
        link_id=link_id,
        user_id=data['user_id'],
        product_name=data['product_name'],
        original_url=data['original_url'],
        affiliate_url=affiliate_url,
        commission_rate=commission_rate,
        category=data.get('category', program.name)
    )
    
    affiliate_links_db[link_id] = affiliate_link
    
    return jsonify({
        'success': True,
        'link': affiliate_link.to_dict()
    })

@affiliate_bp.route('/affiliate/links/<user_id>', methods=['GET'])
def get_user_affiliate_links(user_id):
    """Get all affiliate links for a user"""
    user_links = [
        link.to_dict() for link in affiliate_links_db.values() 
        if link.user_id == user_id
    ]
    
    return jsonify({
        'success': True,
        'links': user_links
    })

@affiliate_bp.route('/affiliate/click/<link_id>', methods=['POST'])
def track_affiliate_click(link_id):
    """Track an affiliate link click"""
    affiliate_link = affiliate_links_db.get(link_id)
    if not affiliate_link:
        return jsonify({'success': False, 'error': 'Invalid affiliate link'}), 404
    
    if not affiliate_link.is_active:
        return jsonify({'success': False, 'error': 'Affiliate link is inactive'}), 400
    
    # Get click data
    ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR', ''))
    user_agent = request.environ.get('HTTP_USER_AGENT', '')
    referrer = request.environ.get('HTTP_REFERER', '')
    
    # Create click record
    click_id = str(uuid.uuid4())
    click = AffiliateClick(
        click_id=click_id,
        link_id=link_id,
        user_id=affiliate_link.user_id,
        ip_address=ip_address,
        user_agent=user_agent,
        referrer=referrer
    )
    
    affiliate_clicks_db[click_id] = click
    
    # Update link click count
    affiliate_link.clicks += 1
    
    # Update user earnings
    if affiliate_link.user_id not in affiliate_earnings_db:
        affiliate_earnings_db[affiliate_link.user_id] = AffiliateEarnings(affiliate_link.user_id)
    
    affiliate_earnings_db[affiliate_link.user_id].total_clicks += 1
    affiliate_earnings_db[affiliate_link.user_id].calculate_conversion_rate()
    
    return jsonify({
        'success': True,
        'redirect_url': affiliate_link.original_url,
        'click_id': click_id
    })

@affiliate_bp.route('/affiliate/conversion', methods=['POST'])
def track_conversion():
    """Track an affiliate conversion"""
    data = request.get_json()
    
    required_fields = ['click_id', 'conversion_value']
    if not all(field in data for field in required_fields):
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400
    
    click = affiliate_clicks_db.get(data['click_id'])
    if not click:
        return jsonify({'success': False, 'error': 'Invalid click ID'}), 404
    
    if click.converted:
        return jsonify({'success': False, 'error': 'Conversion already tracked'}), 400
    
    # Mark click as converted
    click.converted = True
    click.conversion_value = float(data['conversion_value'])
    
    # Update affiliate link
    affiliate_link = affiliate_links_db.get(click.link_id)
    if affiliate_link:
        affiliate_link.conversions += 1
        commission_earned = click.conversion_value * affiliate_link.commission_rate
        affiliate_link.earnings += commission_earned
        
        # Update user earnings
        user_earnings = affiliate_earnings_db.get(click.user_id)
        if user_earnings:
            user_earnings.total_conversions += 1
            user_earnings.total_earnings += commission_earned
            user_earnings.pending_earnings += commission_earned
            user_earnings.calculate_conversion_rate()
            user_earnings.update_tier()
    
    return jsonify({
        'success': True,
        'commission_earned': commission_earned
    })

@affiliate_bp.route('/affiliate/earnings/<user_id>', methods=['GET'])
def get_user_earnings(user_id):
    """Get affiliate earnings for a user"""
    user_earnings = affiliate_earnings_db.get(user_id)
    if not user_earnings:
        user_earnings = AffiliateEarnings(user_id)
        affiliate_earnings_db[user_id] = user_earnings
    
    return jsonify({
        'success': True,
        'earnings': user_earnings.to_dict()
    })

@affiliate_bp.route('/affiliate/analytics/<user_id>', methods=['GET'])
def get_affiliate_analytics(user_id):
    """Get detailed affiliate analytics for a user"""
    user_links = [
        link for link in affiliate_links_db.values() 
        if link.user_id == user_id
    ]
    
    user_clicks = [
        click for click in affiliate_clicks_db.values() 
        if click.user_id == user_id
    ]
    
    # Calculate analytics
    total_links = len(user_links)
    total_clicks = sum(link.clicks for link in user_links)
    total_conversions = sum(link.conversions for link in user_links)
    total_earnings = sum(link.earnings for link in user_links)
    
    # Top performing links
    top_links = sorted(user_links, key=lambda x: x.earnings, reverse=True)[:5]
    
    # Recent activity
    recent_clicks = sorted(user_clicks, key=lambda x: x.clicked_at, reverse=True)[:10]
    
    # Category breakdown
    category_stats = {}
    for link in user_links:
        if link.category not in category_stats:
            category_stats[link.category] = {
                'clicks': 0,
                'conversions': 0,
                'earnings': 0.0
            }
        category_stats[link.category]['clicks'] += link.clicks
        category_stats[link.category]['conversions'] += link.conversions
        category_stats[link.category]['earnings'] += link.earnings
    
    return jsonify({
        'success': True,
        'analytics': {
            'summary': {
                'total_links': total_links,
                'total_clicks': total_clicks,
                'total_conversions': total_conversions,
                'total_earnings': total_earnings,
                'conversion_rate': (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
            },
            'top_links': [link.to_dict() for link in top_links],
            'recent_clicks': [click.to_dict() for click in recent_clicks],
            'category_breakdown': category_stats
        }
    })

@affiliate_bp.route('/affiliate/payout', methods=['POST'])
def request_payout():
    """Request affiliate payout"""
    data = request.get_json()
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({'success': False, 'error': 'User ID required'}), 400
    
    user_earnings = affiliate_earnings_db.get(user_id)
    if not user_earnings:
        return jsonify({'success': False, 'error': 'No earnings found'}), 404
    
    if user_earnings.pending_earnings < 50:  # Minimum payout threshold
        return jsonify({
            'success': False, 
            'error': 'Minimum payout amount is $50'
        }), 400
    
    # Process payout (in real implementation, integrate with payment processor)
    payout_amount = user_earnings.pending_earnings
    user_earnings.paid_earnings += payout_amount
    user_earnings.pending_earnings = 0.0
    user_earnings.next_payout_date = datetime.utcnow() + timedelta(days=7)
    
    return jsonify({
        'success': True,
        'payout_amount': payout_amount,
        'message': 'Payout request submitted successfully'
    })

@affiliate_bp.route('/affiliate/share-tools', methods=['GET'])
def get_share_tools():
    """Get sharing tools and templates for viral marketing"""
    share_tools = {
        'social_templates': [
            {
                'platform': 'instagram',
                'template': "🌸 Just discovered Inner Bloom and I'm obsessed! This platform is helping me level up in every area of my life. Use my link to join the sisterhood! {affiliate_link} #InnerBloom #WomenEmpowerment #SelfGrowth",
                'hashtags': ['#InnerBloom', '#WomenEmpowerment', '#SelfGrowth', '#Sisterhood']
            },
            {
                'platform': 'facebook',
                'template': "Ladies, I found something amazing! 💕 Inner Bloom is like having a personal coach, stylist, and business mentor all in one. The community is incredible and the AI features are mind-blowing. Check it out: {affiliate_link}",
                'hashtags': ['#WomenSupport', '#PersonalGrowth', '#InnerBloom']
            },
            {
                'platform': 'twitter',
                'template': "Game-changer alert! 🚀 @InnerBloom is revolutionizing women's empowerment. From AI coaching to sustainable fashion to business building - it's all here. Join me: {affiliate_link} #InnerBloom #WomenInTech",
                'hashtags': ['#InnerBloom', '#WomenInTech', '#Empowerment']
            },
            {
                'platform': 'tiktok',
                'template': "POV: You found the app that's about to change your life 🌟 Inner Bloom has everything - AI coach, style advice, business tools, and the most supportive community ever! Link in bio ✨ #InnerBloom #GlowUp #WomenEmpowerment",
                'hashtags': ['#InnerBloom', '#GlowUp', '#WomenEmpowerment', '#SelfImprovement']
            }
        ],
        'email_templates': [
            {
                'subject': "You NEED to see this app! 💕",
                'body': "Hey gorgeous!\n\nI had to share this with you because I know you're always working on becoming your best self. I found this incredible platform called Inner Bloom and it's literally everything we've been looking for!\n\n✨ AI personal coach that actually gets you\n👗 Sustainable fashion marketplace\n💼 Business building tools\n🤗 The most supportive community of women\n\nI've been using it for [time period] and I'm already seeing amazing changes. The best part? You can earn money by sharing it too!\n\nCheck it out here: {affiliate_link}\n\nLet me know what you think!\n\nLove,\n[Your name]"
            }
        ],
        'content_ideas': [
            "Before & After: How Inner Bloom transformed my confidence",
            "5 ways Inner Bloom's AI coach changed my mindset",
            "Building my dream wardrobe sustainably with Inner Bloom",
            "From idea to launch: My business journey with Inner Bloom",
            "The sisterhood that's changing my life",
            "Why I'm obsessed with Inner Bloom's community features"
        ],
        'viral_challenges': [
            {
                'name': 'BloomGlowUp',
                'description': 'Share your transformation journey using Inner Bloom',
                'hashtag': '#BloomGlowUp',
                'prize': '$500 Inner Bloom credit'
            },
            {
                'name': 'SustainableStyle',
                'description': 'Show off your eco-friendly outfit from the marketplace',
                'hashtag': '#SustainableStyle',
                'prize': 'Featured on Inner Bloom social media'
            }
        ]
    }
    
    return jsonify({
        'success': True,
        'share_tools': share_tools
    })

# Viral referral tracking
@affiliate_bp.route('/affiliate/viral-share', methods=['POST'])
def track_viral_share():
    """Track viral sharing for bonus rewards"""
    data = request.get_json()
    
    required_fields = ['user_id', 'platform', 'content_type']
    if not all(field in data for field in required_fields):
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400
    
    # Award bonus points for viral sharing
    bonus_points = {
        'instagram': 50,
        'facebook': 30,
        'twitter': 25,
        'tiktok': 75,  # Higher reward for TikTok due to viral potential
        'email': 20
    }
    
    points_earned = bonus_points.get(data['platform'], 10)
    
    # In a real implementation, you'd update the user's points in the database
    # For now, we'll just return the points earned
    
    return jsonify({
        'success': True,
        'points_earned': points_earned,
        'message': f'Thanks for sharing! You earned {points_earned} points.'
    })

