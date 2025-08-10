"""
Inner Bloom Community Posts Model
Handles real community posts, comments, and interactions
"""

import sqlite3
import json
from datetime import datetime
import uuid

class CommunityDB:
    def __init__(self, db_path="inner_bloom.db"):
        self.db_path = db_path
        self.init_tables()
    
    def init_tables(self):
        """Initialize community tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Posts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS community_posts (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                content TEXT NOT NULL,
                image_url TEXT,
                likes INTEGER DEFAULT 0,
                comments_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        # Comments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS post_comments (
                id TEXT PRIMARY KEY,
                post_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (post_id) REFERENCES community_posts (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        # Likes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS post_likes (
                id TEXT PRIMARY KEY,
                post_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(post_id, user_id),
                FOREIGN KEY (post_id) REFERENCES community_posts (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def create_post(self, user_id, content, image_url=None):
        """Create a new community post"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        post_id = str(uuid.uuid4())
        
        cursor.execute("""
            INSERT INTO community_posts (id, user_id, content, image_url)
            VALUES (?, ?, ?, ?)
        """, (post_id, user_id, content, image_url))
        
        conn.commit()
        conn.close()
        
        return post_id
    
    def get_posts(self, limit=20, offset=0):
        """Get community posts with user information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT p.*, u.name, u.bloom_name
            FROM community_posts p
            JOIN users u ON p.user_id = u.id
            ORDER BY p.created_at DESC
            LIMIT ? OFFSET ?
        """, (limit, offset))
        
        posts = []
        for row in cursor.fetchall():
            posts.append({
                'id': row[0],
                'user_id': row[1],
                'content': row[2],
                'image_url': row[3],
                'likes': row[4],
                'comments_count': row[5],
                'created_at': row[6],
                'updated_at': row[7],
                'user_name': row[8],
                'bloom_name': row[9] or row[8]
            })
        
        conn.close()
        return posts
    
    def like_post(self, post_id, user_id):
        """Like or unlike a post"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if already liked
        cursor.execute("""
            SELECT id FROM post_likes WHERE post_id = ? AND user_id = ?
        """, (post_id, user_id))
        
        existing_like = cursor.fetchone()
        
        if existing_like:
            # Unlike the post
            cursor.execute("""
                DELETE FROM post_likes WHERE post_id = ? AND user_id = ?
            """, (post_id, user_id))
            
            cursor.execute("""
                UPDATE community_posts SET likes = likes - 1 WHERE id = ?
            """, (post_id,))
            
            liked = False
        else:
            # Like the post
            like_id = str(uuid.uuid4())
            cursor.execute("""
                INSERT INTO post_likes (id, post_id, user_id)
                VALUES (?, ?, ?)
            """, (like_id, post_id, user_id))
            
            cursor.execute("""
                UPDATE community_posts SET likes = likes + 1 WHERE id = ?
            """, (post_id,))
            
            liked = True
        
        # Get updated like count
        cursor.execute("SELECT likes FROM community_posts WHERE id = ?", (post_id,))
        like_count = cursor.fetchone()[0]
        
        conn.commit()
        conn.close()
        
        return {
            'liked': liked,
            'like_count': like_count
        }
    
    def add_comment(self, post_id, user_id, content):
        """Add a comment to a post"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        comment_id = str(uuid.uuid4())
        
        cursor.execute("""
            INSERT INTO post_comments (id, post_id, user_id, content)
            VALUES (?, ?, ?, ?)
        """, (comment_id, post_id, user_id, content))
        
        # Update comment count
        cursor.execute("""
            UPDATE community_posts SET comments_count = comments_count + 1
            WHERE id = ?
        """, (post_id,))
        
        conn.commit()
        conn.close()
        
        return comment_id
    
    def get_post_comments(self, post_id):
        """Get comments for a specific post"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT c.*, u.name, u.bloom_name
            FROM post_comments c
            JOIN users u ON c.user_id = u.id
            WHERE c.post_id = ?
            ORDER BY c.created_at ASC
        """, (post_id,))
        
        comments = []
        for row in cursor.fetchall():
            comments.append({
                'id': row[0],
                'post_id': row[1],
                'user_id': row[2],
                'content': row[3],
                'created_at': row[4],
                'user_name': row[5],
                'bloom_name': row[6] or row[5]
            })
        
        conn.close()
        return comments
    
    def get_community_stats(self):
        """Get community statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM community_posts")
        total_posts = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM post_comments")
        total_comments = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM post_likes")
        total_likes = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT user_id) FROM community_posts")
        active_members = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_posts': total_posts,
            'total_comments': total_comments,
            'total_likes': total_likes,
            'active_members': active_members
        }

# Initialize community database
community_db = CommunityDB()

# Seed some sample posts
def seed_community():
    """Add sample community posts"""
    sample_posts = [
        {
            'user_id': 'demo_user',
            'content': '🌟 Just launched my first digital product on the marketplace! So excited to share my empowerment journal with all my sisters. The journey to creating this has been incredible - from idea to reality in just 30 days! 💪✨ #SheEO #Empowerment #DigitalProducts'
        },
        {
            'user_id': 'demo_user',
            'content': 'Morning affirmation: "I am worthy of abundance and success flows to me effortlessly." 🙏 Starting my day with gratitude and intention. What\'s your morning ritual, beautiful souls? 💕'
        },
        {
            'user_id': 'demo_user',
            'content': 'Hit my first $1000 month through the Inner Bloom marketplace! 🎉 To all the women doubting their potential - YOU CAN DO THIS! Your dreams are valid and your time is NOW. Thank you to this amazing community for the support! 💎'
        },
        {
            'user_id': 'demo_user',
            'content': 'Reminder: Your healing journey is not linear. Some days you\'ll feel like you\'re conquering the world, other days you\'ll need to rest and recharge. Both are sacred. Both are necessary. 🌸💚 #SelfLove #Healing'
        },
        {
            'user_id': 'demo_user',
            'content': 'Just finished my vision board for 2024! 📌✨ Manifesting: 6-figure business, dream home, spiritual retreat in Bali, and deeper connections with my soul tribe. What are you calling in, queens? 👑'
        }
    ]
    
    # Check if posts already exist
    conn = sqlite3.connect("inner_bloom.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM community_posts")
    count = cursor.fetchone()[0]
    conn.close()
    
    if count == 0:
        for post in sample_posts:
            community_db.create_post(**post)

# Seed the community
seed_community()

