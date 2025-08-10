"""
Inner Bloom Newsletter API Routes
Provides endpoints for newsletter management and subscriber interactions
"""

from flask import Blueprint, jsonify, request
from ..newsletter_system import newsletter, start_newsletter_scheduler
import logging

logger = logging.getLogger(__name__)

newsletter_bp = Blueprint('newsletter', __name__)

@newsletter_bp.route('/newsletter/subscribe', methods=['POST'])
def subscribe_to_newsletter():
    """Subscribe user to newsletter"""
    try:
        data = request.get_json()
        email = data.get('email')
        name = data.get('name')
        interests = data.get('interests', [])
        source = data.get('source', 'website')
        
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        success = newsletter.subscribe_user(email, name, interests, source)
        
        if success:
            return jsonify({
                'message': 'Successfully subscribed to Inner Bloom newsletter!',
                'email': email,
                'welcome_email_sent': True,
                'status': 'active'
            })
        else:
            return jsonify({'error': 'Failed to subscribe'}), 500
            
    except Exception as e:
        logger.error(f"Error subscribing to newsletter: {e}")
        return jsonify({'error': str(e)}), 500

@newsletter_bp.route('/newsletter/stats', methods=['GET'])
def get_newsletter_stats():
    """Get newsletter statistics"""
    try:
        stats = newsletter.get_subscriber_stats()
        
        return jsonify({
            'newsletter_stats': stats,
            'status': 'active',
            'last_updated': 'real-time'
        })
    except Exception as e:
        logger.error(f"Error getting newsletter stats: {e}")
        return jsonify({'error': str(e)}), 500

@newsletter_bp.route('/newsletter/send-daily', methods=['POST'])
def send_daily_inspiration():
    """Manually trigger daily inspiration email"""
    try:
        sent_count = newsletter.send_daily_inspiration()
        
        return jsonify({
            'message': 'Daily inspiration emails sent successfully',
            'recipients': sent_count,
            'type': 'daily_inspiration'
        })
    except Exception as e:
        logger.error(f"Error sending daily inspiration: {e}")
        return jsonify({'error': str(e)}), 500

@newsletter_bp.route('/newsletter/send-community', methods=['POST'])
def send_community_highlight():
    """Manually trigger community highlight email"""
    try:
        sent_count = newsletter.send_community_highlight()
        
        return jsonify({
            'message': 'Community highlight emails sent successfully',
            'recipients': sent_count,
            'type': 'community_highlight'
        })
    except Exception as e:
        logger.error(f"Error sending community highlight: {e}")
        return jsonify({'error': str(e)}), 500

@newsletter_bp.route('/newsletter/send-earnings', methods=['POST'])
def send_earnings_update():
    """Send earnings update to specific user"""
    try:
        data = request.get_json()
        email = data.get('email')
        earnings_data = data.get('earnings_data', {})
        
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        success = newsletter.send_earnings_update(email, earnings_data)
        
        if success:
            return jsonify({
                'message': 'Earnings update sent successfully',
                'email': email,
                'earnings': earnings_data.get('total_earned', 0)
            })
        else:
            return jsonify({'error': 'Failed to send earnings update'}), 500
            
    except Exception as e:
        logger.error(f"Error sending earnings update: {e}")
        return jsonify({'error': str(e)}), 500

@newsletter_bp.route('/newsletter/templates', methods=['GET'])
def get_email_templates():
    """Get available email templates"""
    try:
        import sqlite3
        conn = sqlite3.connect(newsletter.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT name, subject_template, category FROM email_templates')
        templates = cursor.fetchall()
        conn.close()
        
        template_list = [{
            'name': t[0],
            'subject': t[1],
            'category': t[2]
        } for t in templates]
        
        return jsonify({
            'templates': template_list,
            'count': len(template_list)
        })
    except Exception as e:
        logger.error(f"Error getting email templates: {e}")
        return jsonify({'error': str(e)}), 500

@newsletter_bp.route('/newsletter/campaigns', methods=['GET'])
def get_campaigns():
    """Get newsletter campaign history"""
    try:
        import sqlite3
        conn = sqlite3.connect(newsletter.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT name, subject, status, sent_date, recipient_count, open_count, click_count
            FROM newsletter_campaigns 
            ORDER BY created_at DESC 
            LIMIT 20
        ''')
        campaigns = cursor.fetchall()
        conn.close()
        
        campaign_list = [{
            'name': c[0],
            'subject': c[1],
            'status': c[2],
            'sent_date': c[3],
            'recipients': c[4],
            'opens': c[5],
            'clicks': c[6],
            'open_rate': round((c[5] / c[4] * 100) if c[4] > 0 else 0, 2)
        } for c in campaigns]
        
        return jsonify({
            'campaigns': campaign_list,
            'count': len(campaign_list)
        })
    except Exception as e:
        logger.error(f"Error getting campaigns: {e}")
        return jsonify({'error': str(e)}), 500

@newsletter_bp.route('/newsletter/subscribers', methods=['GET'])
def get_subscribers():
    """Get subscriber list with pagination"""
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 50))
        status = request.args.get('status', 'active')
        
        offset = (page - 1) * limit
        
        import sqlite3
        conn = sqlite3.connect(newsletter.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT email, name, subscription_date, engagement_score, last_opened
            FROM newsletter_subscribers 
            WHERE status = ?
            ORDER BY subscription_date DESC 
            LIMIT ? OFFSET ?
        ''', (status, limit, offset))
        subscribers = cursor.fetchall()
        
        cursor.execute('SELECT COUNT(*) FROM newsletter_subscribers WHERE status = ?', (status,))
        total_count = cursor.fetchone()[0]
        
        conn.close()
        
        subscriber_list = [{
            'email': s[0],
            'name': s[1],
            'subscription_date': s[2],
            'engagement_score': s[3],
            'last_opened': s[4]
        } for s in subscribers]
        
        return jsonify({
            'subscribers': subscriber_list,
            'pagination': {
                'page': page,
                'limit': limit,
                'total': total_count,
                'pages': (total_count + limit - 1) // limit
            }
        })
    except Exception as e:
        logger.error(f"Error getting subscribers: {e}")
        return jsonify({'error': str(e)}), 500

@newsletter_bp.route('/newsletter/test-email', methods=['POST'])
def send_test_email():
    """Send test email"""
    try:
        data = request.get_json()
        email = data.get('email')
        template_name = data.get('template', 'welcome_sequence')
        
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        template_data = {
            'name': 'Test User',
            'platform_url': 'https://innerbloom.com',
            'date': 'Today',
            'affirmation_title': 'Test Affirmation',
            'daily_affirmation': 'This is a test affirmation for Inner Bloom.',
            'daily_message': 'This is a test message to verify email functionality.',
            'action_step': 'Check that this email displays correctly.',
            'total_earned': 100,
            'referral_count': 5,
            'commission_rate': 30,
            'avg_per_referral': 20,
            'referral_link': 'https://innerbloom.com/ref/test',
            'new_members': 50,
            'community_earnings': '5,000',
            'countries': 25,
            'community_url': 'https://innerbloom.com/community'
        }
        
        success = newsletter.send_template_email(email, template_name, template_data, 'Test Email')
        
        if success:
            return jsonify({
                'message': 'Test email sent successfully',
                'email': email,
                'template': template_name
            })
        else:
            return jsonify({'error': 'Failed to send test email'}), 500
            
    except Exception as e:
        logger.error(f"Error sending test email: {e}")
        return jsonify({'error': str(e)}), 500

@newsletter_bp.route('/newsletter/start-scheduler', methods=['POST'])
def start_scheduler():
    """Start the newsletter scheduler"""
    try:
        start_newsletter_scheduler()
        
        return jsonify({
            'message': 'Newsletter scheduler started successfully',
            'scheduled_tasks': [
                'Daily inspiration at 8:00 AM',
                'Weekly community highlight on Sundays at 10:00 AM'
            ]
        })
    except Exception as e:
        logger.error(f"Error starting scheduler: {e}")
        return jsonify({'error': str(e)}), 500

@newsletter_bp.route('/newsletter/unsubscribe/<token>', methods=['GET'])
def unsubscribe(token):
    """Unsubscribe user using token"""
    try:
        import sqlite3
        conn = sqlite3.connect(newsletter.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE newsletter_subscribers 
            SET status = 'unsubscribed' 
            WHERE unsubscribe_token = ?
        ''', (token,))
        
        if cursor.rowcount > 0:
            conn.commit()
            conn.close()
            return jsonify({
                'message': 'Successfully unsubscribed from Inner Bloom newsletter',
                'status': 'unsubscribed'
            })
        else:
            conn.close()
            return jsonify({'error': 'Invalid unsubscribe token'}), 400
            
    except Exception as e:
        logger.error(f"Error unsubscribing: {e}")
        return jsonify({'error': str(e)}), 500

@newsletter_bp.route('/newsletter/engagement/<email>', methods=['POST'])
def track_engagement(email):
    """Track email engagement (opens, clicks)"""
    try:
        data = request.get_json()
        action = data.get('action', 'open')  # 'open' or 'click'
        campaign_id = data.get('campaign_id')
        
        import sqlite3
        conn = sqlite3.connect(newsletter.db_path)
        cursor = conn.cursor()
        
        # Log engagement
        cursor.execute('''
            INSERT INTO email_analytics 
            (campaign_id, subscriber_email, action, ip_address, user_agent)
            VALUES (?, ?, ?, ?, ?)
        ''', (campaign_id, email, action, request.remote_addr, request.headers.get('User-Agent')))
        
        # Update subscriber engagement score
        cursor.execute('''
            UPDATE newsletter_subscribers 
            SET engagement_score = engagement_score + 1,
                last_opened = CURRENT_TIMESTAMP
            WHERE email = ?
        ''', (email,))
        
        # Update campaign stats
        if action == 'open':
            cursor.execute('''
                UPDATE newsletter_campaigns 
                SET open_count = open_count + 1 
                WHERE id = ?
            ''', (campaign_id,))
        elif action == 'click':
            cursor.execute('''
                UPDATE newsletter_campaigns 
                SET click_count = click_count + 1 
                WHERE id = ?
            ''', (campaign_id,))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'message': 'Engagement tracked successfully',
            'action': action,
            'email': email
        })
        
    except Exception as e:
        logger.error(f"Error tracking engagement: {e}")
        return jsonify({'error': str(e)}), 500

