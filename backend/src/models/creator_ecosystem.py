from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import json
import uuid

db = SQLAlchemy()

class TrendDetection(db.Model):
    __tablename__ = 'trend_detection'
    
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(50), nullable=False)  # tiktok, pinterest, instagram, youtube
    trend_type = db.Column(db.String(50), nullable=False)  # hashtag, audio, style, product, topic
    
    # Trend data
    trend_name = db.Column(db.String(200), nullable=False)
    trend_description = db.Column(db.Text)
    trend_url = db.Column(db.String(500))
    
    # Metrics
    engagement_score = db.Column(db.Float, default=0.0)  # 0-100 trending score
    growth_rate = db.Column(db.Float, default=0.0)  # Percentage growth
    estimated_reach = db.Column(db.Integer, default=0)
    
    # Categorization
    category = db.Column(db.String(50))  # fashion, wellness, business, lifestyle
    target_audience = db.Column(db.String(100))  # women_25_35, entrepreneurs, etc.
    monetization_potential = db.Column(db.String(20), default='medium')  # low, medium, high
    
    # AI analysis
    sentiment_score = db.Column(db.Float, default=0.0)  # -1 to 1 sentiment
    brand_safety_score = db.Column(db.Float, default=0.0)  # 0-100 brand safety
    relevance_score = db.Column(db.Float, default=0.0)  # 0-100 relevance to Inner Bloom
    
    # Status
    status = db.Column(db.String(20), default='detected')  # detected, analyzed, recommended, archived
    recommended_to_users = db.Column(db.Boolean, default=False)
    
    detected_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)  # When trend is no longer relevant

class CreatorApplication(db.Model):
    __tablename__ = 'creator_applications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Application details
    creator_name = db.Column(db.String(100), nullable=False)
    brand_name = db.Column(db.String(100))
    niche = db.Column(db.String(50), nullable=False)  # fashion, wellness, business, lifestyle
    
    # Social media presence
    instagram_handle = db.Column(db.String(100))
    instagram_followers = db.Column(db.Integer, default=0)
    tiktok_handle = db.Column(db.String(100))
    tiktok_followers = db.Column(db.Integer, default=0)
    youtube_channel = db.Column(db.String(200))
    youtube_subscribers = db.Column(db.Integer, default=0)
    other_platforms = db.Column(db.JSON)  # Store other platform data
    
    # Content metrics
    average_engagement_rate = db.Column(db.Float, default=0.0)
    content_frequency = db.Column(db.String(20))  # daily, weekly, monthly
    content_quality_score = db.Column(db.Float, default=0.0)  # 0-100 AI-assessed quality
    
    # Business information
    monthly_revenue = db.Column(db.Float, default=0.0)
    revenue_sources = db.Column(db.JSON)  # sponsorships, products, courses, etc.
    business_goals = db.Column(db.Text)
    
    # Pitch deck and portfolio
    pitch_deck_url = db.Column(db.String(500))
    portfolio_urls = db.Column(db.JSON)  # Array of portfolio links
    media_kit_url = db.Column(db.String(500))
    
    # Application status
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected, interview
    priority_score = db.Column(db.Float, default=0.0)  # 0-100 priority for review
    
    # Review process
    reviewed_by = db.Column(db.Integer, db.ForeignKey('admin_users.id'))
    review_notes = db.Column(db.Text)
    interview_scheduled = db.Column(db.DateTime)
    
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime)

class SponsoredCreator(db.Model):
    __tablename__ = 'sponsored_creators'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    application_id = db.Column(db.Integer, db.ForeignKey('creator_applications.id'), nullable=False)
    
    # Sponsorship details
    tier = db.Column(db.String(20), default='bronze')  # bronze, silver, gold, platinum
    monthly_support = db.Column(db.Float, default=0.0)  # Monthly financial support
    revenue_share_percentage = db.Column(db.Float, default=10.0)  # Platform's share of creator revenue
    
    # Benefits and perks
    spotlight_features = db.Column(db.Integer, default=0)  # Number of spotlight features
    affiliate_boost_percentage = db.Column(db.Float, default=0.0)  # Extra affiliate commission
    priority_support = db.Column(db.Boolean, default=False)
    exclusive_opportunities = db.Column(db.Boolean, default=False)
    
    # Performance tracking
    content_created = db.Column(db.Integer, default=0)
    total_engagement = db.Column(db.Integer, default=0)
    revenue_generated = db.Column(db.Float, default=0.0)
    referrals_brought = db.Column(db.Integer, default=0)
    
    # Contract details
    contract_start = db.Column(db.DateTime, default=datetime.utcnow)
    contract_end = db.Column(db.DateTime)
    auto_renewal = db.Column(db.Boolean, default=True)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    performance_rating = db.Column(db.Float, default=0.0)  # 0-5 star rating

class BusinessAccelerator(db.Model):
    __tablename__ = 'business_accelerator'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Business details
    business_name = db.Column(db.String(100), nullable=False)
    business_type = db.Column(db.String(50), nullable=False)  # podcast, course, coaching, product
    industry = db.Column(db.String(50), nullable=False)
    business_stage = db.Column(db.String(20), default='idea')  # idea, mvp, launch, growth, scale
    
    # Financial information
    current_revenue = db.Column(db.Float, default=0.0)
    revenue_goal = db.Column(db.Float, default=0.0)
    funding_needed = db.Column(db.Float, default=0.0)
    
    # Accelerator program details
    program_type = db.Column(db.String(20), default='standard')  # standard, premium, vip
    investment_amount = db.Column(db.Float, default=0.0)  # Platform investment
    equity_percentage = db.Column(db.Float, default=0.0)  # Platform equity stake
    revenue_share_percentage = db.Column(db.Float, default=20.0)  # Platform revenue share
    
    # Support provided
    mentorship_hours = db.Column(db.Integer, default=0)
    marketing_budget = db.Column(db.Float, default=0.0)
    technical_support = db.Column(db.Boolean, default=False)
    audience_access = db.Column(db.Boolean, default=False)  # Access to Inner Bloom audience
    
    # Milestones and progress
    milestones = db.Column(db.JSON)  # Array of milestone objects
    current_milestone = db.Column(db.Integer, default=1)
    completion_percentage = db.Column(db.Float, default=0.0)
    
    # Performance metrics
    revenue_growth = db.Column(db.Float, default=0.0)  # Percentage growth since joining
    audience_growth = db.Column(db.Float, default=0.0)
    engagement_improvement = db.Column(db.Float, default=0.0)
    
    # Program status
    status = db.Column(db.String(20), default='active')  # active, completed, terminated, paused
    graduation_date = db.Column(db.DateTime)
    
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class NewsletterSubscriber(db.Model):
    __tablename__ = 'newsletter_subscribers'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100))
    
    # Subscription preferences
    subscriber_type = db.Column(db.String(20), default='general')  # general, investor, creator, user
    frequency = db.Column(db.String(20), default='weekly')  # daily, weekly, monthly
    
    # Segmentation
    interests = db.Column(db.JSON)  # Array of interest categories
    engagement_score = db.Column(db.Float, default=0.0)  # 0-100 engagement score
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    confirmed = db.Column(db.Boolean, default=False)
    
    subscribed_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_email_sent = db.Column(db.DateTime)
    unsubscribed_at = db.Column(db.DateTime)

class NewsletterCampaign(db.Model):
    __tablename__ = 'newsletter_campaigns'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Campaign details
    name = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    campaign_type = db.Column(db.String(20), default='newsletter')  # newsletter, announcement, investor_update
    
    # Content
    html_content = db.Column(db.Text)
    text_content = db.Column(db.Text)
    template_id = db.Column(db.String(50))
    
    # Targeting
    target_audience = db.Column(db.String(20), default='all')  # all, users, creators, investors
    segment_filters = db.Column(db.JSON)  # Filtering criteria
    
    # Scheduling
    scheduled_at = db.Column(db.DateTime)
    sent_at = db.Column(db.DateTime)
    is_recurring = db.Column(db.Boolean, default=False)
    recurrence_pattern = db.Column(db.String(20))  # weekly, monthly
    
    # Performance metrics
    recipients_count = db.Column(db.Integer, default=0)
    delivered_count = db.Column(db.Integer, default=0)
    opened_count = db.Column(db.Integer, default=0)
    clicked_count = db.Column(db.Integer, default=0)
    unsubscribed_count = db.Column(db.Integer, default=0)
    
    # Calculated metrics
    delivery_rate = db.Column(db.Float, default=0.0)
    open_rate = db.Column(db.Float, default=0.0)
    click_rate = db.Column(db.Float, default=0.0)
    unsubscribe_rate = db.Column(db.Float, default=0.0)
    
    # Status
    status = db.Column(db.String(20), default='draft')  # draft, scheduled, sending, sent, failed
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ContentRecommendation(db.Model):
    __tablename__ = 'content_recommendations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    trend_id = db.Column(db.Integer, db.ForeignKey('trend_detection.id'))
    
    # Recommendation details
    recommendation_type = db.Column(db.String(20), nullable=False)  # trend, product, course, challenge
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # Content suggestions
    suggested_content = db.Column(db.JSON)  # Array of content ideas
    hashtags = db.Column(db.JSON)  # Recommended hashtags
    posting_times = db.Column(db.JSON)  # Optimal posting times
    
    # Monetization opportunities
    affiliate_products = db.Column(db.JSON)  # Relevant affiliate products
    potential_earnings = db.Column(db.Float, default=0.0)
    difficulty_level = db.Column(db.String(20), default='medium')  # easy, medium, hard
    
    # Personalization
    relevance_score = db.Column(db.Float, default=0.0)  # 0-100 relevance to user
    user_interests_match = db.Column(db.JSON)  # Matching user interests
    
    # Status
    status = db.Column(db.String(20), default='active')  # active, dismissed, completed
    viewed = db.Column(db.Boolean, default=False)
    acted_upon = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)

# Utility functions for creator ecosystem

def detect_trending_content():
    """Simulate trend detection from various platforms"""
    # In production, this would integrate with actual APIs
    # For now, we'll create sample trending data
    
    sample_trends = [
        {
            'platform': 'tiktok',
            'trend_type': 'hashtag',
            'trend_name': '#SelfCareRoutine',
            'description': 'Women sharing their morning and evening self-care routines',
            'engagement_score': 85.0,
            'category': 'wellness',
            'target_audience': 'women_25_35',
            'monetization_potential': 'high'
        },
        {
            'platform': 'pinterest',
            'trend_type': 'style',
            'trend_name': 'Sustainable Fashion Capsule Wardrobe',
            'description': 'Minimalist wardrobe with sustainable fashion pieces',
            'engagement_score': 78.0,
            'category': 'fashion',
            'target_audience': 'conscious_consumers',
            'monetization_potential': 'high'
        },
        {
            'platform': 'instagram',
            'trend_type': 'topic',
            'trend_name': 'Female Entrepreneur Stories',
            'description': 'Success stories and behind-the-scenes of female entrepreneurs',
            'engagement_score': 92.0,
            'category': 'business',
            'target_audience': 'entrepreneurs',
            'monetization_potential': 'medium'
        }
    ]
    
    for trend_data in sample_trends:
        existing_trend = TrendDetection.query.filter_by(
            platform=trend_data['platform'],
            trend_name=trend_data['trend_name']
        ).first()
        
        if not existing_trend:
            trend = TrendDetection(
                platform=trend_data['platform'],
                trend_type=trend_data['trend_type'],
                trend_name=trend_data['trend_name'],
                trend_description=trend_data['description'],
                engagement_score=trend_data['engagement_score'],
                category=trend_data['category'],
                target_audience=trend_data['target_audience'],
                monetization_potential=trend_data['monetization_potential'],
                relevance_score=85.0,  # High relevance to Inner Bloom
                brand_safety_score=95.0,  # High brand safety
                expires_at=datetime.utcnow() + timedelta(days=7)
            )
            db.session.add(trend)
    
    db.session.commit()
    return TrendDetection.query.filter_by(status='detected').all()

def generate_content_recommendations(user_id):
    """Generate personalized content recommendations for a user"""
    from src.models.user import User
    
    user = User.query.get(user_id)
    if not user:
        return []
    
    # Get active trends
    active_trends = TrendDetection.query.filter_by(status='detected').all()
    recommendations = []
    
    for trend in active_trends:
        # Create personalized recommendation
        recommendation = ContentRecommendation(
            user_id=user_id,
            trend_id=trend.id,
            recommendation_type='trend',
            title=f"Create content around: {trend.trend_name}",
            description=f"This trend is gaining traction on {trend.platform.title()} with {trend.engagement_score}% engagement score.",
            suggested_content=[
                f"Share your take on {trend.trend_name}",
                f"Create a tutorial related to {trend.trend_name}",
                f"Start a challenge around {trend.trend_name}"
            ],
            hashtags=[trend.trend_name, '#InnerBloom', '#WomenEmpowerment'],
            potential_earnings=50.0 if trend.monetization_potential == 'high' else 25.0,
            relevance_score=trend.relevance_score,
            expires_at=trend.expires_at
        )
        
        db.session.add(recommendation)
        recommendations.append(recommendation)
    
    db.session.commit()
    return recommendations

def calculate_creator_priority_score(application):
    """Calculate priority score for creator application review"""
    score = 0.0
    
    # Follower count scoring
    total_followers = (application.instagram_followers or 0) + \
                     (application.tiktok_followers or 0) + \
                     (application.youtube_subscribers or 0)
    
    if total_followers > 100000:
        score += 30.0
    elif total_followers > 50000:
        score += 25.0
    elif total_followers > 10000:
        score += 20.0
    elif total_followers > 1000:
        score += 15.0
    else:
        score += 10.0
    
    # Engagement rate scoring
    if application.average_engagement_rate > 5.0:
        score += 25.0
    elif application.average_engagement_rate > 3.0:
        score += 20.0
    elif application.average_engagement_rate > 1.0:
        score += 15.0
    else:
        score += 10.0
    
    # Revenue scoring
    if application.monthly_revenue > 10000:
        score += 20.0
    elif application.monthly_revenue > 5000:
        score += 15.0
    elif application.monthly_revenue > 1000:
        score += 10.0
    else:
        score += 5.0
    
    # Content quality scoring
    score += application.content_quality_score * 0.25  # Max 25 points
    
    return min(100.0, score)

def create_newsletter_campaign(campaign_type='weekly_update'):
    """Create automated newsletter campaign"""
    from src.models.affiliate_tracking import UserEarnings
    from src.models.user import User
    
    # Get top performers for the week
    top_earners = db.session.query(
        User.username,
        UserEarnings.total_earnings
    ).join(UserEarnings, User.id == UserEarnings.user_id)\
     .order_by(UserEarnings.total_earnings.desc())\
     .limit(5).all()
    
    # Get latest trends
    trending_content = TrendDetection.query.filter_by(status='detected')\
                                          .order_by(TrendDetection.engagement_score.desc())\
                                          .limit(3).all()
    
    # Generate content based on campaign type
    if campaign_type == 'weekly_update':
        subject = f"Inner Bloom Weekly: Top Earners & Trending Content - {datetime.now().strftime('%B %d')}"
        
        html_content = f"""
        <h1>🌸 Inner Bloom Weekly Update</h1>
        
        <h2>💰 Top Earners This Week</h2>
        <ul>
        {''.join([f'<li>{earner.username}: ${earner.total_earnings:.2f}</li>' for earner in top_earners])}
        </ul>
        
        <h2>🔥 Trending Content Opportunities</h2>
        <ul>
        {''.join([f'<li><strong>{trend.trend_name}</strong> on {trend.platform.title()} - {trend.engagement_score}% engagement</li>' for trend in trending_content])}
        </ul>
        
        <h2>🚀 This Week's Challenge</h2>
        <p>Share your biggest win from this week using #InnerBloomWins for a chance to win $500!</p>
        
        <p>Keep blooming! 🌸<br>The Inner Bloom Team</p>
        """
    
    elif campaign_type == 'investor_update':
        total_users = User.query.count()
        total_revenue = db.session.query(db.func.sum(UserEarnings.total_earnings)).scalar() or 0
        
        subject = f"Inner Bloom Investor Update - {datetime.now().strftime('%B %Y')}"
        
        html_content = f"""
        <h1>📊 Inner Bloom Investor Update</h1>
        
        <h2>Key Metrics</h2>
        <ul>
            <li>Total Users: {total_users:,}</li>
            <li>Total Revenue Generated: ${total_revenue:,.2f}</li>
            <li>Active Creators: {SponsoredCreator.query.filter_by(is_active=True).count()}</li>
            <li>Accelerator Companies: {BusinessAccelerator.query.filter_by(status='active').count()}</li>
        </ul>
        
        <h2>Growth Highlights</h2>
        <p>Platform continues to show strong growth in user acquisition and revenue generation.</p>
        
        <h2>Upcoming Initiatives</h2>
        <ul>
            <li>Crypto payment integration</li>
            <li>Enhanced AI trend detection</li>
            <li>International expansion</li>
        </ul>
        
        <p>Best regards,<br>Inner Bloom Leadership Team</p>
        """
    
    # Create campaign
    campaign = NewsletterCampaign(
        name=f"{campaign_type.replace('_', ' ').title()} - {datetime.now().strftime('%Y-%m-%d')}",
        subject=subject,
        campaign_type=campaign_type,
        html_content=html_content,
        target_audience='all' if campaign_type == 'weekly_update' else 'investors',
        scheduled_at=datetime.utcnow() + timedelta(hours=1),  # Send in 1 hour
        is_recurring=True,
        recurrence_pattern='weekly' if campaign_type == 'weekly_update' else 'monthly'
    )
    
    db.session.add(campaign)
    db.session.commit()
    
    return campaign

