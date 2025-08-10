"""
Inner Bloom Web Scraping API Routes
Provides endpoints for managing and accessing scraped content
"""

from flask import Blueprint, jsonify, request
from ..web_scraper import scraper, setup_default_targets
import logging

logger = logging.getLogger(__name__)

scraper_bp = Blueprint('scraper', __name__)

@scraper_bp.route('/scraper/status', methods=['GET'])
def scraper_status():
    """Get scraper status and statistics"""
    try:
        # Get content count by category
        import sqlite3
        conn = sqlite3.connect(scraper.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM scraped_content')
        total_content = cursor.fetchone()[0]
        
        cursor.execute('SELECT category, COUNT(*) FROM scraped_content GROUP BY category')
        category_counts = dict(cursor.fetchall())
        
        cursor.execute('SELECT COUNT(*) FROM scraping_targets WHERE active = 1')
        active_targets = cursor.fetchone()[0]
        
        conn.close()
        
        return jsonify({
            'status': 'active',
            'total_content': total_content,
            'category_breakdown': category_counts,
            'active_targets': active_targets,
            'last_updated': 'real-time'
        })
    except Exception as e:
        logger.error(f"Error getting scraper status: {e}")
        return jsonify({'error': str(e)}), 500

@scraper_bp.route('/scraper/trending', methods=['GET'])
def get_trending_topics():
    """Get trending topics from scraped content"""
    try:
        category = request.args.get('category')
        limit = int(request.args.get('limit', 10))
        
        topics = scraper.get_trending_topics(category, limit)
        
        return jsonify({
            'trending_topics': topics,
            'category': category or 'all',
            'count': len(topics)
        })
    except Exception as e:
        logger.error(f"Error getting trending topics: {e}")
        return jsonify({'error': str(e)}), 500

@scraper_bp.route('/scraper/content', methods=['GET'])
def get_scraped_content():
    """Get scraped content for AI or user consumption"""
    try:
        category = request.args.get('category')
        limit = int(request.args.get('limit', 5))
        
        content = scraper.get_content_for_ai(category, limit)
        
        return jsonify({
            'content': content,
            'category': category or 'all',
            'count': len(content)
        })
    except Exception as e:
        logger.error(f"Error getting scraped content: {e}")
        return jsonify({'error': str(e)}), 500

@scraper_bp.route('/scraper/suggestions', methods=['GET'])
def get_content_suggestions():
    """Get personalized content suggestions"""
    try:
        interests = request.args.getlist('interests')
        
        suggestions = scraper.get_content_suggestions(interests if interests else None)
        
        return jsonify({
            'suggestions': suggestions,
            'based_on': interests or 'general',
            'count': len(suggestions)
        })
    except Exception as e:
        logger.error(f"Error getting content suggestions: {e}")
        return jsonify({'error': str(e)}), 500

@scraper_bp.route('/scraper/add-target', methods=['POST'])
def add_scraping_target():
    """Add a new URL to scrape"""
    try:
        data = request.get_json()
        url = data.get('url')
        category = data.get('category', 'general')
        frequency = data.get('frequency', 24)
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        success = scraper.add_scraping_target(url, category, frequency)
        
        if success:
            return jsonify({
                'message': 'Scraping target added successfully',
                'url': url,
                'category': category,
                'frequency': frequency
            })
        else:
            return jsonify({'error': 'Failed to add scraping target'}), 500
            
    except Exception as e:
        logger.error(f"Error adding scraping target: {e}")
        return jsonify({'error': str(e)}), 500

@scraper_bp.route('/scraper/scrape-now', methods=['POST'])
def scrape_now():
    """Trigger immediate scraping of all targets"""
    try:
        results = scraper.scrape_all_targets()
        
        return jsonify({
            'message': 'Scraping completed',
            'scraped_count': len(results),
            'results': results[:5]  # Return first 5 results as preview
        })
    except Exception as e:
        logger.error(f"Error during scraping: {e}")
        return jsonify({'error': str(e)}), 500

@scraper_bp.route('/scraper/setup-defaults', methods=['POST'])
def setup_defaults():
    """Set up default scraping targets"""
    try:
        setup_default_targets()
        
        return jsonify({
            'message': 'Default scraping targets set up successfully',
            'targets': [
                'Oprah Inspiration',
                'MindBodyGreen Spirituality', 
                'Entrepreneur Women',
                'Forbes Women Media',
                'HuffPost Women'
            ]
        })
    except Exception as e:
        logger.error(f"Error setting up defaults: {e}")
        return jsonify({'error': str(e)}), 500

@scraper_bp.route('/scraper/social-trends', methods=['GET'])
def get_social_trends():
    """Get social media trends"""
    try:
        trends = scraper.scrape_social_media_trends()
        
        return jsonify({
            'social_trends': trends,
            'count': len(trends),
            'category': 'empowerment'
        })
    except Exception as e:
        logger.error(f"Error getting social trends: {e}")
        return jsonify({'error': str(e)}), 500

@scraper_bp.route('/scraper/ai-content', methods=['GET'])
def get_ai_content():
    """Get content specifically formatted for AI companion"""
    try:
        category = request.args.get('category', 'empowerment')
        limit = int(request.args.get('limit', 3))
        
        content = scraper.get_content_for_ai(category, limit)
        
        # Format for AI companion
        ai_formatted = []
        for item in content:
            ai_formatted.append({
                'title': item['title'],
                'summary': item['content'][:300] + "..." if len(item['content']) > 300 else item['content'],
                'keywords': item['keywords'],
                'inspiration_level': 'high' if any(word in item['content'].lower() for word in ['empower', 'success', 'achieve', 'dream']) else 'medium'
            })
        
        return jsonify({
            'ai_content': ai_formatted,
            'category': category,
            'count': len(ai_formatted),
            'usage': 'AI companion inspiration and guidance'
        })
    except Exception as e:
        logger.error(f"Error getting AI content: {e}")
        return jsonify({'error': str(e)}), 500

