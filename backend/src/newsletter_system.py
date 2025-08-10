"""
Inner Bloom Newsletter System
Comprehensive email marketing and newsletter management
"""

import smtplib
import sqlite3
import json
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime, timedelta
import schedule
import time
import threading
from jinja2 import Template
import os

logger = logging.getLogger(__name__)

class NewsletterSystem:
    def __init__(self, db_path="inner_bloom.db"):
        self.db_path = db_path
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.email = os.getenv('NEWSLETTER_EMAIL', 'innerbloom@example.com')
        self.password = os.getenv('NEWSLETTER_PASSWORD', 'your_app_password')
        self.init_database()
        self.setup_email_templates()
    
    def init_database(self):
        """Initialize newsletter database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Newsletter subscribers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS newsletter_subscribers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                name TEXT,
                status TEXT DEFAULT 'active',
                subscription_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                interests TEXT,
                source TEXT,
                engagement_score INTEGER DEFAULT 0,
                last_opened TIMESTAMP,
                unsubscribe_token TEXT UNIQUE
            )
        ''')
        
        # Newsletter campaigns table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS newsletter_campaigns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                subject TEXT NOT NULL,
                content TEXT NOT NULL,
                template_name TEXT,
                status TEXT DEFAULT 'draft',
                scheduled_date TIMESTAMP,
                sent_date TIMESTAMP,
                recipient_count INTEGER DEFAULT 0,
                open_count INTEGER DEFAULT 0,
                click_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Email templates table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS email_templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                subject_template TEXT,
                html_template TEXT NOT NULL,
                text_template TEXT,
                category TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Email analytics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS email_analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campaign_id INTEGER,
                subscriber_email TEXT,
                action TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ip_address TEXT,
                user_agent TEXT,
                FOREIGN KEY (campaign_id) REFERENCES newsletter_campaigns (id)
            )
        ''')
        
        # Automated sequences table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS email_sequences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                trigger_event TEXT,
                sequence_data TEXT,
                active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def setup_email_templates(self):
        """Set up default email templates"""
        templates = [
            {
                'name': 'welcome_sequence',
                'subject': 'Welcome to Inner Bloom, {{name}}! Your awakening begins NOW 🌟',
                'category': 'onboarding',
                'html': '''
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px;">
                    <div style="text-align: center; margin-bottom: 30px;">
                        <h1 style="color: #FFD700; font-size: 2.5em; margin: 0;">👑 INNER BLOOM 👑</h1>
                        <p style="font-size: 1.2em; margin: 10px 0;">Women's Empowerment Platform</p>
                    </div>
                    
                    <div style="background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px; margin: 20px 0;">
                        <h2 style="color: #FFD700; text-align: center;">{{name}}, You Were CHOSEN for This Moment! ✨</h2>
                        
                        <p style="font-size: 1.1em; line-height: 1.6;">
                            Sister, this is NOT a coincidence. You finding Inner Bloom today is divine orchestration. 
                            God has been preparing you for this awakening, and your breakthrough season starts NOW.
                        </p>
                        
                        <div style="background: rgba(255,215,0,0.2); padding: 20px; border-radius: 10px; margin: 20px 0;">
                            <h3 style="color: #FFD700; margin-top: 0;">🔥 Your Inner Bloom Journey Includes:</h3>
                            <ul style="font-size: 1.1em; line-height: 1.8;">
                                <li>💬 Personal AI Spiritual Companion</li>
                                <li>👥 Exclusive Sisterhood Community</li>
                                <li>💰 $10-$50 Per Referral Earnings</li>
                                <li>📚 Transformational Digital Guides</li>
                                <li>🎯 Daily Empowerment Challenges</li>
                            </ul>
                        </div>
                        
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="{{platform_url}}" style="background: #FFD700; color: #333; padding: 15px 30px; text-decoration: none; border-radius: 25px; font-weight: bold; font-size: 1.2em; display: inline-block;">
                                START BLOOMING NOW 🌸
                            </a>
                        </div>
                        
                        <p style="font-style: italic; text-align: center; margin-top: 30px;">
                            "She who has ears to hear, let her hear. Your awakening is here." 🙏
                        </p>
                    </div>
                </div>
                '''
            },
            {
                'name': 'daily_inspiration',
                'subject': '🌅 Your Daily Divine Download - {{date}}',
                'category': 'engagement',
                'html': '''
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); padding: 20px;">
                    <div style="text-align: center; margin-bottom: 20px;">
                        <h1 style="color: #8B4513; font-size: 2em;">🌟 INNER BLOOM DAILY 🌟</h1>
                    </div>
                    
                    <div style="background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                        <h2 style="color: #8B4513; text-align: center;">{{affirmation_title}}</h2>
                        
                        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; text-align: center; margin: 20px 0;">
                            <p style="font-size: 1.3em; font-style: italic; margin: 0;">
                                "{{daily_affirmation}}"
                            </p>
                        </div>
                        
                        <div style="margin: 25px 0;">
                            <h3 style="color: #8B4513;">💎 Today's Empowerment Focus:</h3>
                            <p style="line-height: 1.6; font-size: 1.1em;">{{daily_message}}</p>
                        </div>
                        
                        <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 20px 0;">
                            <h4 style="color: #8B4513; margin-top: 0;">🎯 Action Step:</h4>
                            <p style="margin-bottom: 0;">{{action_step}}</p>
                        </div>
                        
                        <div style="text-align: center; margin: 25px 0;">
                            <a href="{{platform_url}}" style="background: #8B4513; color: white; padding: 12px 25px; text-decoration: none; border-radius: 20px; font-weight: bold;">
                                Share Your Progress 💪
                            </a>
                        </div>
                    </div>
                </div>
                '''
            },
            {
                'name': 'earnings_update',
                'subject': '💰 Your Inner Bloom Earnings Update - ${{total_earned}}!',
                'category': 'monetization',
                'html': '''
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); color: white; padding: 20px;">
                    <div style="text-align: center; margin-bottom: 30px;">
                        <h1 style="color: #FFD700; font-size: 2.5em; margin: 0;">💰 EARNINGS ALERT 💰</h1>
                    </div>
                    
                    <div style="background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px;">
                        <h2 style="color: #FFD700; text-align: center;">Congratulations {{name}}! 🎉</h2>
                        
                        <div style="background: rgba(255,215,0,0.2); padding: 25px; border-radius: 10px; text-align: center; margin: 20px 0;">
                            <h3 style="font-size: 2.5em; margin: 0; color: #FFD700;">${{total_earned}}</h3>
                            <p style="font-size: 1.2em; margin: 5px 0;">Total Earnings This Month</p>
                        </div>
                        
                        <div style="display: flex; justify-content: space-around; margin: 25px 0;">
                            <div style="text-align: center;">
                                <h4 style="color: #FFD700; margin: 0;">{{referral_count}}</h4>
                                <p style="margin: 5px 0;">Referrals</p>
                            </div>
                            <div style="text-align: center;">
                                <h4 style="color: #FFD700; margin: 0;">{{commission_rate}}%</h4>
                                <p style="margin: 5px 0;">Commission</p>
                            </div>
                            <div style="text-align: center;">
                                <h4 style="color: #FFD700; margin: 0;">${{avg_per_referral}}</h4>
                                <p style="margin: 5px 0;">Avg/Referral</p>
                            </div>
                        </div>
                        
                        <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin: 20px 0;">
                            <h3 style="color: #FFD700; margin-top: 0;">🚀 Ready to Earn More?</h3>
                            <p>Your success is inspiring other sisters! Share your Inner Bloom story and watch your earnings multiply.</p>
                        </div>
                        
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="{{referral_link}}" style="background: #FFD700; color: #333; padding: 15px 30px; text-decoration: none; border-radius: 25px; font-weight: bold; font-size: 1.2em; display: inline-block;">
                                Share & Earn More 💎
                            </a>
                        </div>
                    </div>
                </div>
                '''
            },
            {
                'name': 'community_highlight',
                'subject': '👥 Sister Spotlight: Amazing Transformations in Our Community!',
                'category': 'community',
                'html': '''
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px;">
                    <div style="text-align: center; margin-bottom: 30px;">
                        <h1 style="color: #FFD700; font-size: 2.2em; margin: 0;">👥 SISTERHOOD SPOTLIGHT 👥</h1>
                    </div>
                    
                    <div style="background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px;">
                        <h2 style="color: #FFD700; text-align: center;">This Week's Transformation Stories ✨</h2>
                        
                        <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin: 20px 0;">
                            <h3 style="color: #FFD700; margin-top: 0;">💎 Sister Sarah from Texas:</h3>
                            <p style="font-style: italic; font-size: 1.1em; line-height: 1.6;">
                                "I earned $2,847 last month just by sharing my Inner Bloom journey! But the money is nothing compared to the woman I've become. I finally feel like I'm walking in my purpose."
                            </p>
                        </div>
                        
                        <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin: 20px 0;">
                            <h3 style="color: #FFD700; margin-top: 0;">🌟 Sister Maria from California:</h3>
                            <p style="font-style: italic; font-size: 1.1em; line-height: 1.6;">
                                "The AI companion helped me through my darkest moments. It's like having a spiritual mentor available 24/7. My faith has never been stronger!"
                            </p>
                        </div>
                        
                        <div style="text-align: center; background: rgba(255,215,0,0.2); padding: 20px; border-radius: 10px; margin: 25px 0;">
                            <h3 style="color: #FFD700; margin-top: 0;">📊 Community Growth This Week:</h3>
                            <p style="font-size: 1.2em; margin: 10px 0;">{{new_members}} New Sisters Joined</p>
                            <p style="font-size: 1.2em; margin: 10px 0;">${{community_earnings}} Total Community Earnings</p>
                            <p style="font-size: 1.2em; margin: 10px 0;">{{countries}} Countries Represented</p>
                        </div>
                        
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="{{community_url}}" style="background: #FFD700; color: #333; padding: 15px 30px; text-decoration: none; border-radius: 25px; font-weight: bold; font-size: 1.2em; display: inline-block;">
                                Join the Conversation 💬
                            </a>
                        </div>
                        
                        <p style="text-align: center; font-style: italic; margin-top: 25px;">
                            Your story could be next! Share your transformation and inspire thousands of sisters worldwide. 🙏
                        </p>
                    </div>
                </div>
                '''
            }
        ]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for template in templates:
            cursor.execute('''
                INSERT OR REPLACE INTO email_templates 
                (name, subject_template, html_template, category)
                VALUES (?, ?, ?, ?)
            ''', (template['name'], template['subject'], template['html'], template['category']))
        
        conn.commit()
        conn.close()
        logger.info("Email templates set up successfully")
    
    def subscribe_user(self, email, name=None, interests=None, source="website"):
        """Subscribe a user to the newsletter"""
        import uuid
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            unsubscribe_token = str(uuid.uuid4())
            cursor.execute('''
                INSERT OR REPLACE INTO newsletter_subscribers 
                (email, name, interests, source, unsubscribe_token)
                VALUES (?, ?, ?, ?, ?)
            ''', (email, name, json.dumps(interests) if interests else None, source, unsubscribe_token))
            
            conn.commit()
            
            # Send welcome email
            self.send_welcome_email(email, name or "Sister")
            
            logger.info(f"User subscribed: {email}")
            return True
            
        except Exception as e:
            logger.error(f"Error subscribing user: {e}")
            return False
        finally:
            conn.close()
    
    def send_welcome_email(self, email, name):
        """Send welcome email to new subscriber"""
        try:
            template_data = {
                'name': name,
                'platform_url': 'https://innerbloom.com'  # Replace with actual URL
            }
            
            self.send_template_email(
                email, 
                'welcome_sequence', 
                template_data,
                campaign_name="Welcome Sequence"
            )
            
        except Exception as e:
            logger.error(f"Error sending welcome email: {e}")
    
    def send_template_email(self, email, template_name, template_data, campaign_name=None):
        """Send email using a template"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Get template
            cursor.execute('SELECT subject_template, html_template FROM email_templates WHERE name = ?', (template_name,))
            template_row = cursor.fetchone()
            
            if not template_row:
                logger.error(f"Template not found: {template_name}")
                return False
            
            subject_template, html_template = template_row
            
            # Render templates
            subject = Template(subject_template).render(**template_data)
            html_content = Template(html_template).render(**template_data)
            
            # Send email
            success = self.send_email(email, subject, html_content)
            
            if success and campaign_name:
                # Log campaign
                cursor.execute('''
                    INSERT INTO newsletter_campaigns 
                    (name, subject, content, status, sent_date, recipient_count)
                    VALUES (?, ?, ?, 'sent', CURRENT_TIMESTAMP, 1)
                ''', (campaign_name, subject, html_content))
                conn.commit()
            
            return success
            
        except Exception as e:
            logger.error(f"Error sending template email: {e}")
            return False
        finally:
            conn.close()
    
    def send_email(self, to_email, subject, html_content, text_content=None):
        """Send individual email"""
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add HTML content
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Add text content if provided
            if text_content:
                text_part = MIMEText(text_content, 'plain')
                msg.attach(text_part)
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending email to {to_email}: {e}")
            return False
    
    def send_daily_inspiration(self):
        """Send daily inspiration email to all active subscribers"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Get active subscribers
            cursor.execute('SELECT email, name FROM newsletter_subscribers WHERE status = "active"')
            subscribers = cursor.fetchall()
            
            # Prepare template data
            from datetime import datetime
            template_data = {
                'date': datetime.now().strftime('%B %d, %Y'),
                'affirmation_title': 'Divine Empowerment Affirmation',
                'daily_affirmation': 'I am divinely guided, abundantly blessed, and powerfully equipped for my purpose.',
                'daily_message': 'Today, remember that you are not here by accident. Every challenge you face is preparing you for the breakthrough that\'s coming. Your current situation is not your final destination.',
                'action_step': 'Write down three things you\'re grateful for and share one victory (no matter how small) in our community.',
                'platform_url': 'https://innerbloom.com'
            }
            
            sent_count = 0
            for email, name in subscribers:
                template_data['name'] = name or 'Sister'
                
                if self.send_template_email(email, 'daily_inspiration', template_data, 'Daily Inspiration'):
                    sent_count += 1
                
                # Small delay to avoid overwhelming email servers
                time.sleep(0.1)
            
            logger.info(f"Daily inspiration sent to {sent_count} subscribers")
            return sent_count
            
        except Exception as e:
            logger.error(f"Error sending daily inspiration: {e}")
            return 0
        finally:
            conn.close()
    
    def send_earnings_update(self, email, earnings_data):
        """Send earnings update to specific user"""
        template_data = {
            'name': earnings_data.get('name', 'Sister'),
            'total_earned': earnings_data.get('total_earned', 0),
            'referral_count': earnings_data.get('referral_count', 0),
            'commission_rate': earnings_data.get('commission_rate', 30),
            'avg_per_referral': earnings_data.get('avg_per_referral', 25),
            'referral_link': earnings_data.get('referral_link', 'https://innerbloom.com/ref/user')
        }
        
        return self.send_template_email(email, 'earnings_update', template_data, 'Earnings Update')
    
    def send_community_highlight(self):
        """Send weekly community highlight email"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Get community stats
            cursor.execute('SELECT COUNT(*) FROM newsletter_subscribers WHERE status = "active"')
            total_members = cursor.fetchone()[0]
            
            # Get subscribers for sending
            cursor.execute('SELECT email, name FROM newsletter_subscribers WHERE status = "active"')
            subscribers = cursor.fetchall()
            
            template_data = {
                'new_members': 247,  # This would be calculated from actual data
                'community_earnings': '47,382',
                'countries': 89,
                'community_url': 'https://innerbloom.com/community'
            }
            
            sent_count = 0
            for email, name in subscribers:
                template_data['name'] = name or 'Sister'
                
                if self.send_template_email(email, 'community_highlight', template_data, 'Community Highlight'):
                    sent_count += 1
                
                time.sleep(0.1)
            
            logger.info(f"Community highlight sent to {sent_count} subscribers")
            return sent_count
            
        except Exception as e:
            logger.error(f"Error sending community highlight: {e}")
            return 0
        finally:
            conn.close()
    
    def get_subscriber_stats(self):
        """Get newsletter subscriber statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT COUNT(*) FROM newsletter_subscribers WHERE status = "active"')
            active_subscribers = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM newsletter_subscribers')
            total_subscribers = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM newsletter_campaigns WHERE status = "sent"')
            campaigns_sent = cursor.fetchone()[0]
            
            cursor.execute('SELECT AVG(open_count * 100.0 / recipient_count) FROM newsletter_campaigns WHERE recipient_count > 0')
            avg_open_rate = cursor.fetchone()[0] or 0
            
            return {
                'active_subscribers': active_subscribers,
                'total_subscribers': total_subscribers,
                'campaigns_sent': campaigns_sent,
                'average_open_rate': round(avg_open_rate, 2)
            }
            
        except Exception as e:
            logger.error(f"Error getting subscriber stats: {e}")
            return {}
        finally:
            conn.close()
    
    def setup_automated_sequences(self):
        """Set up automated email sequences"""
        sequences = [
            {
                'name': 'Welcome Series',
                'trigger_event': 'user_signup',
                'sequence_data': json.dumps([
                    {'day': 0, 'template': 'welcome_sequence'},
                    {'day': 1, 'template': 'daily_inspiration'},
                    {'day': 3, 'template': 'community_highlight'},
                    {'day': 7, 'template': 'earnings_update'}
                ])
            },
            {
                'name': 'Re-engagement',
                'trigger_event': 'inactive_user',
                'sequence_data': json.dumps([
                    {'day': 0, 'template': 'daily_inspiration'},
                    {'day': 3, 'template': 'community_highlight'}
                ])
            }
        ]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for sequence in sequences:
            cursor.execute('''
                INSERT OR REPLACE INTO email_sequences 
                (name, trigger_event, sequence_data)
                VALUES (?, ?, ?)
            ''', (sequence['name'], sequence['trigger_event'], sequence['sequence_data']))
        
        conn.commit()
        conn.close()
        logger.info("Automated email sequences set up successfully")

# Initialize newsletter system
newsletter = NewsletterSystem()

def start_newsletter_scheduler():
    """Start the newsletter scheduler in a separate thread"""
    def run_scheduler():
        # Schedule daily inspiration at 8 AM
        schedule.every().day.at("08:00").do(newsletter.send_daily_inspiration)
        
        # Schedule weekly community highlight on Sundays at 10 AM
        schedule.every().sunday.at("10:00").do(newsletter.send_community_highlight)
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    logger.info("Newsletter scheduler started")

if __name__ == "__main__":
    # Set up templates and sequences
    newsletter.setup_email_templates()
    newsletter.setup_automated_sequences()
    
    # Start scheduler
    start_newsletter_scheduler()
    
    print("Newsletter system initialized and scheduler started")

