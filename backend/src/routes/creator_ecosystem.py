from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from src.models.creator_ecosystem import (
    TrendDetection, CreatorApplication, SponsoredCreator, BusinessAccelerator,
    NewsletterSubscriber, NewsletterCampaign, ContentRecommendation,
    detect_trending_content, generate_content_recommendations,
    calculate_creator_priority_score, create_newsletter_campaign, db
)
from src.models.user import User
from datetime import datetime, timedelta
import json

creator_ecosystem_bp = Blueprint('creator_ecosystem', __name__)

# Trend Detection Routes
@creator_ecosystem_bp.route('/trends', methods=['GET'])
@cross_origin()
def get_trends():
    """Get current trending content"""
    try:
        # Refresh trends (in production, this would be a scheduled job)
        detect_trending_content()
        
        platform = request.args.get('platform')
        category = request.args.get('category')
        
        query = TrendDetection.query.filter_by(status='detected')
        
        if platform:
            query = query.filter_by(platform=platform)
        if category:
            query = query.filter_by(category=category)
        
        trends = query.order_by(TrendDetection.engagement_score.desc()).limit(20).all()
        
        trends_data = [
            {
                'id': trend.id,
                'platform': trend.platform,
                'trend_type': trend.trend_type,
                'trend_name': trend.trend_name,
                'description': trend.trend_description,
                'engagement_score': trend.engagement_score,
                'growth_rate': trend.growth_rate,
                'category': trend.category,
                'target_audience': trend.target_audience,
                'monetization_potential': trend.monetization_potential,
                'relevance_score': trend.relevance_score,
                'detected_at': trend.detected_at.isoformat(),
                'expires_at': trend.expires_at.isoformat() if trend.expires_at else None
            }
            for trend in trends
        ]
        
        return jsonify({
            'trends': trends_data,
            'total_count': len(trends_data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@creator_ecosystem_bp.route('/trends/recommendations/<int:user_id>', methods=['GET'])
@cross_origin()
def get_user_recommendations(user_id):
    """Get personalized content recommendations for a user"""
    try:
        # Generate fresh recommendations
        recommendations = generate_content_recommendations(user_id)
        
        # Get existing recommendations
        existing_recommendations = ContentRecommendation.query.filter_by(
            user_id=user_id,
            status='active'
        ).order_by(ContentRecommendation.relevance_score.desc()).all()
        
        recommendations_data = [
            {
                'id': rec.id,
                'recommendation_type': rec.recommendation_type,
                'title': rec.title,
                'description': rec.description,
                'suggested_content': rec.suggested_content,
                'hashtags': rec.hashtags,
                'potential_earnings': rec.potential_earnings,
                'difficulty_level': rec.difficulty_level,
                'relevance_score': rec.relevance_score,
                'created_at': rec.created_at.isoformat(),
                'expires_at': rec.expires_at.isoformat() if rec.expires_at else None
            }
            for rec in existing_recommendations
        ]
        
        return jsonify({
            'recommendations': recommendations_data,
            'total_count': len(recommendations_data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Creator Portal Routes
@creator_ecosystem_bp.route('/creator/apply', methods=['POST'])
@cross_origin()
def submit_creator_application():
    """Submit creator application"""
    try:
        data = request.get_json()
        
        # Check if user already has an application
        existing_app = CreatorApplication.query.filter_by(user_id=data['user_id']).first()
        if existing_app:
            return jsonify({'error': 'Application already exists for this user'}), 409
        
        application = CreatorApplication(
            user_id=data['user_id'],
            creator_name=data['creator_name'],
            brand_name=data.get('brand_name'),
            niche=data['niche'],
            instagram_handle=data.get('instagram_handle'),
            instagram_followers=data.get('instagram_followers', 0),
            tiktok_handle=data.get('tiktok_handle'),
            tiktok_followers=data.get('tiktok_followers', 0),
            youtube_channel=data.get('youtube_channel'),
            youtube_subscribers=data.get('youtube_subscribers', 0),
            average_engagement_rate=data.get('average_engagement_rate', 0.0),
            content_frequency=data.get('content_frequency', 'weekly'),
            monthly_revenue=data.get('monthly_revenue', 0.0),
            business_goals=data.get('business_goals'),
            pitch_deck_url=data.get('pitch_deck_url'),
            portfolio_urls=data.get('portfolio_urls', []),
            media_kit_url=data.get('media_kit_url')
        )
        
        # Calculate priority score
        application.priority_score = calculate_creator_priority_score(application)
        
        db.session.add(application)
        db.session.commit()
        
        return jsonify({
            'message': 'Application submitted successfully',
            'application_id': application.id,
            'priority_score': application.priority_score
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@creator_ecosystem_bp.route('/creator/applications', methods=['GET'])
@cross_origin()
def get_creator_applications():
    """Get creator applications (admin only)"""
    try:
        status = request.args.get('status', 'pending')
        
        applications = CreatorApplication.query.filter_by(status=status)\
                                              .order_by(CreatorApplication.priority_score.desc())\
                                              .all()
        
        applications_data = [
            {
                'id': app.id,
                'user_id': app.user_id,
                'creator_name': app.creator_name,
                'brand_name': app.brand_name,
                'niche': app.niche,
                'total_followers': (app.instagram_followers or 0) + (app.tiktok_followers or 0) + (app.youtube_subscribers or 0),
                'engagement_rate': app.average_engagement_rate,
                'monthly_revenue': app.monthly_revenue,
                'priority_score': app.priority_score,
                'status': app.status,
                'applied_at': app.applied_at.isoformat()
            }
            for app in applications
        ]
        
        return jsonify({
            'applications': applications_data,
            'total_count': len(applications_data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@creator_ecosystem_bp.route('/creator/applications/<int:app_id>/approve', methods=['POST'])
@cross_origin()
def approve_creator_application(app_id):
    """Approve creator application and create sponsored creator"""
    try:
        data = request.get_json() or {}
        
        application = CreatorApplication.query.get_or_404(app_id)
        application.status = 'approved'
        application.reviewed_at = datetime.utcnow()
        application.review_notes = data.get('notes', '')
        
        # Create sponsored creator record
        sponsored_creator = SponsoredCreator(
            user_id=application.user_id,
            application_id=application.id,
            tier=data.get('tier', 'bronze'),
            monthly_support=data.get('monthly_support', 0.0),
            revenue_share_percentage=data.get('revenue_share', 10.0),
            spotlight_features=data.get('spotlight_features', 1),
            affiliate_boost_percentage=data.get('affiliate_boost', 5.0),
            priority_support=data.get('priority_support', False),
            contract_end=datetime.utcnow() + timedelta(days=365)  # 1 year contract
        )
        
        db.session.add(sponsored_creator)
        db.session.commit()
        
        return jsonify({
            'message': 'Creator application approved successfully',
            'sponsored_creator_id': sponsored_creator.id
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@creator_ecosystem_bp.route('/creator/sponsored', methods=['GET'])
@cross_origin()
def get_sponsored_creators():
    """Get sponsored creators"""
    try:
        sponsored_creators = db.session.query(
            SponsoredCreator,
            User.username,
            CreatorApplication.creator_name
        ).join(User, SponsoredCreator.user_id == User.id)\
         .join(CreatorApplication, SponsoredCreator.application_id == CreatorApplication.id)\
         .filter(SponsoredCreator.is_active == True)\
         .order_by(SponsoredCreator.performance_rating.desc()).all()
        
        creators_data = [
            {
                'id': creator.SponsoredCreator.id,
                'user_id': creator.SponsoredCreator.user_id,
                'username': creator.username,
                'creator_name': creator.creator_name,
                'tier': creator.SponsoredCreator.tier,
                'monthly_support': creator.SponsoredCreator.monthly_support,
                'revenue_share_percentage': creator.SponsoredCreator.revenue_share_percentage,
                'content_created': creator.SponsoredCreator.content_created,
                'revenue_generated': creator.SponsoredCreator.revenue_generated,
                'performance_rating': creator.SponsoredCreator.performance_rating,
                'contract_start': creator.SponsoredCreator.contract_start.isoformat(),
                'contract_end': creator.SponsoredCreator.contract_end.isoformat() if creator.SponsoredCreator.contract_end else None
            }
            for creator in sponsored_creators
        ]
        
        return jsonify({
            'sponsored_creators': creators_data,
            'total_count': len(creators_data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Business Accelerator Routes
@creator_ecosystem_bp.route('/accelerator/apply', methods=['POST'])
@cross_origin()
def apply_to_accelerator():
    """Apply to business accelerator program"""
    try:
        data = request.get_json()
        
        # Check if user already has an active accelerator application
        existing_app = BusinessAccelerator.query.filter_by(
            user_id=data['user_id'],
            status='active'
        ).first()
        
        if existing_app:
            return jsonify({'error': 'User already has an active accelerator application'}), 409
        
        accelerator_app = BusinessAccelerator(
            user_id=data['user_id'],
            business_name=data['business_name'],
            business_type=data['business_type'],
            industry=data['industry'],
            business_stage=data.get('business_stage', 'idea'),
            current_revenue=data.get('current_revenue', 0.0),
            revenue_goal=data.get('revenue_goal', 0.0),
            funding_needed=data.get('funding_needed', 0.0),
            program_type=data.get('program_type', 'standard'),
            milestones=data.get('milestones', [])
        )
        
        # Set program benefits based on type
        if accelerator_app.program_type == 'premium':
            accelerator_app.investment_amount = 5000.0
            accelerator_app.revenue_share_percentage = 15.0
            accelerator_app.mentorship_hours = 20
            accelerator_app.marketing_budget = 2000.0
        elif accelerator_app.program_type == 'vip':
            accelerator_app.investment_amount = 10000.0
            accelerator_app.revenue_share_percentage = 20.0
            accelerator_app.mentorship_hours = 40
            accelerator_app.marketing_budget = 5000.0
            accelerator_app.technical_support = True
            accelerator_app.audience_access = True
        
        db.session.add(accelerator_app)
        db.session.commit()
        
        return jsonify({
            'message': 'Accelerator application submitted successfully',
            'accelerator_id': accelerator_app.id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@creator_ecosystem_bp.route('/accelerator/companies', methods=['GET'])
@cross_origin()
def get_accelerator_companies():
    """Get accelerator companies"""
    try:
        companies = db.session.query(
            BusinessAccelerator,
            User.username
        ).join(User, BusinessAccelerator.user_id == User.id)\
         .filter(BusinessAccelerator.status == 'active')\
         .order_by(BusinessAccelerator.completion_percentage.desc()).all()
        
        companies_data = [
            {
                'id': company.BusinessAccelerator.id,
                'user_id': company.BusinessAccelerator.user_id,
                'username': company.username,
                'business_name': company.BusinessAccelerator.business_name,
                'business_type': company.BusinessAccelerator.business_type,
                'industry': company.BusinessAccelerator.industry,
                'business_stage': company.BusinessAccelerator.business_stage,
                'current_revenue': company.BusinessAccelerator.current_revenue,
                'revenue_goal': company.BusinessAccelerator.revenue_goal,
                'program_type': company.BusinessAccelerator.program_type,
                'investment_amount': company.BusinessAccelerator.investment_amount,
                'completion_percentage': company.BusinessAccelerator.completion_percentage,
                'revenue_growth': company.BusinessAccelerator.revenue_growth,
                'joined_at': company.BusinessAccelerator.joined_at.isoformat()
            }
            for company in companies
        ]
        
        return jsonify({
            'companies': companies_data,
            'total_count': len(companies_data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@creator_ecosystem_bp.route('/accelerator/<int:company_id>/milestone', methods=['POST'])
@cross_origin()
def update_milestone(company_id):
    """Update milestone progress"""
    try:
        data = request.get_json()
        
        company = BusinessAccelerator.query.get_or_404(company_id)
        
        milestone_id = data.get('milestone_id')
        completed = data.get('completed', False)
        
        # Update milestone in the milestones JSON
        milestones = company.milestones or []
        for milestone in milestones:
            if milestone.get('id') == milestone_id:
                milestone['completed'] = completed
                milestone['completed_at'] = datetime.utcnow().isoformat() if completed else None
                break
        
        company.milestones = milestones
        
        # Recalculate completion percentage
        total_milestones = len(milestones)
        completed_milestones = sum(1 for m in milestones if m.get('completed', False))
        company.completion_percentage = (completed_milestones / total_milestones * 100) if total_milestones > 0 else 0
        
        db.session.commit()
        
        return jsonify({
            'message': 'Milestone updated successfully',
            'completion_percentage': company.completion_percentage
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Newsletter Routes
@creator_ecosystem_bp.route('/newsletter/subscribe', methods=['POST'])
@cross_origin()
def subscribe_to_newsletter():
    """Subscribe to newsletter"""
    try:
        data = request.get_json()
        
        # Check if email already exists
        existing_subscriber = NewsletterSubscriber.query.filter_by(email=data['email']).first()
        if existing_subscriber:
            if existing_subscriber.is_active:
                return jsonify({'message': 'Email already subscribed'}), 200
            else:
                # Reactivate subscription
                existing_subscriber.is_active = True
                existing_subscriber.unsubscribed_at = None
                db.session.commit()
                return jsonify({'message': 'Subscription reactivated'}), 200
        
        subscriber = NewsletterSubscriber(
            email=data['email'],
            name=data.get('name'),
            subscriber_type=data.get('subscriber_type', 'general'),
            frequency=data.get('frequency', 'weekly'),
            interests=data.get('interests', [])
        )
        
        db.session.add(subscriber)
        db.session.commit()
        
        return jsonify({
            'message': 'Successfully subscribed to newsletter',
            'subscriber_id': subscriber.id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@creator_ecosystem_bp.route('/newsletter/campaigns', methods=['GET'])
@cross_origin()
def get_newsletter_campaigns():
    """Get newsletter campaigns"""
    try:
        campaigns = NewsletterCampaign.query.order_by(NewsletterCampaign.created_at.desc()).limit(20).all()
        
        campaigns_data = [
            {
                'id': campaign.id,
                'name': campaign.name,
                'subject': campaign.subject,
                'campaign_type': campaign.campaign_type,
                'target_audience': campaign.target_audience,
                'status': campaign.status,
                'recipients_count': campaign.recipients_count,
                'open_rate': campaign.open_rate,
                'click_rate': campaign.click_rate,
                'scheduled_at': campaign.scheduled_at.isoformat() if campaign.scheduled_at else None,
                'sent_at': campaign.sent_at.isoformat() if campaign.sent_at else None,
                'created_at': campaign.created_at.isoformat()
            }
            for campaign in campaigns
        ]
        
        return jsonify({
            'campaigns': campaigns_data,
            'total_count': len(campaigns_data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@creator_ecosystem_bp.route('/newsletter/campaigns/create', methods=['POST'])
@cross_origin()
def create_campaign():
    """Create newsletter campaign"""
    try:
        data = request.get_json()
        campaign_type = data.get('campaign_type', 'weekly_update')
        
        campaign = create_newsletter_campaign(campaign_type)
        
        return jsonify({
            'message': 'Campaign created successfully',
            'campaign_id': campaign.id,
            'scheduled_at': campaign.scheduled_at.isoformat()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Analytics Routes
@creator_ecosystem_bp.route('/analytics/ecosystem', methods=['GET'])
@cross_origin()
def get_ecosystem_analytics():
    """Get creator ecosystem analytics"""
    try:
        # Get ecosystem metrics
        total_trends = TrendDetection.query.count()
        active_trends = TrendDetection.query.filter_by(status='detected').count()
        
        total_applications = CreatorApplication.query.count()
        approved_creators = SponsoredCreator.query.filter_by(is_active=True).count()
        
        active_accelerator_companies = BusinessAccelerator.query.filter_by(status='active').count()
        newsletter_subscribers = NewsletterSubscriber.query.filter_by(is_active=True).count()
        
        # Get performance metrics
        avg_creator_performance = db.session.query(
            db.func.avg(SponsoredCreator.performance_rating)
        ).scalar() or 0.0
        
        total_creator_revenue = db.session.query(
            db.func.sum(SponsoredCreator.revenue_generated)
        ).scalar() or 0.0
        
        analytics_data = {
            'trends': {
                'total_trends': total_trends,
                'active_trends': active_trends,
                'trend_categories': ['fashion', 'wellness', 'business', 'lifestyle']
            },
            'creators': {
                'total_applications': total_applications,
                'approved_creators': approved_creators,
                'avg_performance_rating': round(avg_creator_performance, 2),
                'total_revenue_generated': total_creator_revenue
            },
            'accelerator': {
                'active_companies': active_accelerator_companies,
                'total_investment': db.session.query(db.func.sum(BusinessAccelerator.investment_amount)).scalar() or 0.0
            },
            'newsletter': {
                'total_subscribers': newsletter_subscribers,
                'campaigns_sent': NewsletterCampaign.query.filter_by(status='sent').count()
            }
        }
        
        return jsonify(analytics_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Health check
@creator_ecosystem_bp.route('/creator-ecosystem/health', methods=['GET'])
@cross_origin()
def creator_ecosystem_health():
    """Creator ecosystem health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    }), 200

