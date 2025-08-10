"""
Inner Bloom Web Scraping Module
Scrapes content for user engagement, market research, and content aggregation
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import random
from urllib.parse import urljoin, urlparse
from datetime import datetime
import sqlite3
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InnerBloomScraper:
    def __init__(self, db_path="inner_bloom.db"):
        self.db_path = db_path
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.init_database()
    
    def init_database(self):
        """Initialize database tables for scraped content"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create scraped_content table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scraped_content (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE,
                title TEXT,
                content TEXT,
                category TEXT,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                sentiment_score REAL,
                keywords TEXT,
                source_domain TEXT
            )
        ''')
        
        # Create scraping_targets table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scraping_targets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE,
                category TEXT,
                frequency INTEGER DEFAULT 24,
                last_scraped TIMESTAMP,
                active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Create trending_topics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trending_topics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT,
                mentions INTEGER DEFAULT 1,
                sentiment REAL,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                category TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_scraping_target(self, url, category="general", frequency=24):
        """Add a new URL to scrape regularly"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO scraping_targets (url, category, frequency)
                VALUES (?, ?, ?)
            ''', (url, category, frequency))
            conn.commit()
            logger.info(f"Added scraping target: {url}")
            return True
        except Exception as e:
            logger.error(f"Error adding scraping target: {e}")
            return False
        finally:
            conn.close()
    
    def scrape_empowerment_content(self):
        """Scrape women's empowerment and spiritual content"""
        empowerment_sites = [
            "https://www.oprah.com/inspiration",
            "https://www.mindbodygreen.com/articles/spirituality",
            "https://www.huffpost.com/life/women",
            "https://www.forbes.com/sites/womensmedia/",
            "https://www.entrepreneur.com/topic/women-entrepreneurs"
        ]
        
        for url in empowerment_sites:
            self.add_scraping_target(url, "empowerment", 12)
        
        return self.scrape_all_targets()
    
    def scrape_url(self, url, category="general"):
        """Scrape content from a single URL"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title = soup.find('title')
            title = title.get_text().strip() if title else "No Title"
            
            # Extract main content
            content = self.extract_main_content(soup)
            
            # Extract keywords
            keywords = self.extract_keywords(soup, content)
            
            # Get domain
            domain = urlparse(url).netloc
            
            # Store in database
            self.store_scraped_content(url, title, content, category, keywords, domain)
            
            logger.info(f"Successfully scraped: {url}")
            return {
                'url': url,
                'title': title,
                'content': content[:500] + "..." if len(content) > 500 else content,
                'keywords': keywords,
                'domain': domain
            }
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            return None
    
    def extract_main_content(self, soup):
        """Extract main content from HTML"""
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Try to find main content areas
        content_selectors = [
            'article', 'main', '.content', '.post-content', 
            '.entry-content', '.article-body', '.story-body'
        ]
        
        content = ""
        for selector in content_selectors:
            elements = soup.select(selector)
            if elements:
                content = " ".join([elem.get_text().strip() for elem in elements])
                break
        
        # Fallback to body content
        if not content:
            body = soup.find('body')
            if body:
                content = body.get_text()
        
        # Clean up content
        content = " ".join(content.split())
        return content[:2000]  # Limit content length
    
    def extract_keywords(self, soup, content):
        """Extract keywords from meta tags and content"""
        keywords = []
        
        # Extract from meta keywords
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        if meta_keywords:
            keywords.extend([k.strip() for k in meta_keywords.get('content', '').split(',')])
        
        # Extract from meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            desc_words = meta_desc.get('content', '').split()
            keywords.extend([w.strip('.,!?') for w in desc_words if len(w) > 4])
        
        # Simple keyword extraction from content
        empowerment_keywords = [
            'empowerment', 'women', 'spiritual', 'growth', 'success', 
            'entrepreneur', 'leadership', 'confidence', 'purpose', 'faith',
            'business', 'money', 'financial', 'freedom', 'independence'
        ]
        
        content_lower = content.lower()
        for keyword in empowerment_keywords:
            if keyword in content_lower:
                keywords.append(keyword)
        
        return list(set(keywords[:10]))  # Return unique keywords, max 10
    
    def store_scraped_content(self, url, title, content, category, keywords, domain):
        """Store scraped content in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO scraped_content 
                (url, title, content, category, keywords, source_domain)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (url, title, content, category, json.dumps(keywords), domain))
            conn.commit()
        except Exception as e:
            logger.error(f"Error storing content: {e}")
        finally:
            conn.close()
    
    def scrape_all_targets(self):
        """Scrape all active targets"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT url, category FROM scraping_targets 
            WHERE active = 1
        ''')
        targets = cursor.fetchall()
        conn.close()
        
        results = []
        for url, category in targets:
            result = self.scrape_url(url, category)
            if result:
                results.append(result)
            
            # Be respectful - add delay between requests
            time.sleep(random.uniform(1, 3))
        
        return results
    
    def get_trending_topics(self, category=None, limit=10):
        """Get trending topics from scraped content"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if category:
            cursor.execute('''
                SELECT topic, mentions, sentiment FROM trending_topics 
                WHERE category = ? 
                ORDER BY mentions DESC, last_updated DESC 
                LIMIT ?
            ''', (category, limit))
        else:
            cursor.execute('''
                SELECT topic, mentions, sentiment FROM trending_topics 
                ORDER BY mentions DESC, last_updated DESC 
                LIMIT ?
            ''', (limit,))
        
        topics = cursor.fetchall()
        conn.close()
        
        return [{'topic': t[0], 'mentions': t[1], 'sentiment': t[2]} for t in topics]
    
    def get_content_for_ai(self, category=None, limit=5):
        """Get scraped content for AI companion to use"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if category:
            cursor.execute('''
                SELECT title, content, keywords FROM scraped_content 
                WHERE category = ? 
                ORDER BY scraped_at DESC 
                LIMIT ?
            ''', (category, limit))
        else:
            cursor.execute('''
                SELECT title, content, keywords FROM scraped_content 
                ORDER BY scraped_at DESC 
                LIMIT ?
            ''', (limit,))
        
        content = cursor.fetchall()
        conn.close()
        
        return [{
            'title': c[0], 
            'content': c[1], 
            'keywords': json.loads(c[2]) if c[2] else []
        } for c in content]
    
    def scrape_social_media_trends(self):
        """Scrape social media trends (Twitter-like content)"""
        # This would integrate with social media APIs
        # For now, we'll simulate trending topics
        trending_topics = [
            "women empowerment", "spiritual awakening", "financial freedom",
            "female entrepreneurs", "self love", "manifestation", 
            "girl boss", "divine feminine", "abundance mindset"
        ]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for topic in trending_topics:
            cursor.execute('''
                INSERT OR REPLACE INTO trending_topics (topic, mentions, category)
                VALUES (?, ?, ?)
            ''', (topic, random.randint(100, 1000), "empowerment"))
        
        conn.commit()
        conn.close()
        
        return trending_topics
    
    def get_content_suggestions(self, user_interests=None):
        """Get content suggestions based on scraped data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if user_interests:
            # Find content matching user interests
            interest_query = " OR ".join([f"keywords LIKE '%{interest}%'" for interest in user_interests])
            cursor.execute(f'''
                SELECT title, content, url FROM scraped_content 
                WHERE {interest_query}
                ORDER BY scraped_at DESC 
                LIMIT 5
            ''')
        else:
            cursor.execute('''
                SELECT title, content, url FROM scraped_content 
                ORDER BY scraped_at DESC 
                LIMIT 5
            ''')
        
        suggestions = cursor.fetchall()
        conn.close()
        
        return [{
            'title': s[0],
            'content': s[1][:200] + "..." if len(s[1]) > 200 else s[1],
            'url': s[2]
        } for s in suggestions]

# Initialize scraper instance
scraper = InnerBloomScraper()

def setup_default_targets():
    """Set up default scraping targets for Inner Bloom"""
    default_targets = [
        ("https://www.oprah.com/inspiration", "inspiration", 12),
        ("https://www.mindbodygreen.com/articles/spirituality", "spirituality", 12),
        ("https://www.entrepreneur.com/topic/women-entrepreneurs", "business", 24),
        ("https://www.forbes.com/sites/womensmedia/", "business", 24),
        ("https://www.huffpost.com/life/women", "lifestyle", 12)
    ]
    
    for url, category, frequency in default_targets:
        scraper.add_scraping_target(url, category, frequency)
    
    logger.info("Default scraping targets set up successfully")

if __name__ == "__main__":
    # Set up default targets and run initial scrape
    setup_default_targets()
    results = scraper.scrape_empowerment_content()
    print(f"Scraped {len(results)} articles successfully")

