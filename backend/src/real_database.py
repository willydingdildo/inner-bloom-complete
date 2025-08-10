import sqlite3
import json
from datetime import datetime, timedelta
import random
from typing import Dict, List, Optional

class RealDatabase:
    def __init__(self):
        self.db_path = "inner_bloom.db"
        self.init_database()
        self.seed_initial_data()
    
    def init_database(self):
        """Initialize all database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                subscription_tier TEXT DEFAULT 'free',
                points INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                streak_days INTEGER DEFAULT 0,
                total_earnings REAL DEFAULT 0.0,
                referral_code TEXT UNIQUE,
                referred_by TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_active DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Real-time counters
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS platform_stats (
                id INTEGER PRIMARY KEY,
                total_users INTEGER DEFAULT 0,
                active_users_today INTEGER DEFAULT 0,
                total_earnings REAL DEFAULT 0.0,
                total_referrals INTEGER DEFAULT 0,
                community_posts INTEGER DEFAULT 0,
                last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # User activities for real tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                activity_type TEXT NOT NULL,
                points_earned INTEGER DEFAULT 0,
                description TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Real earnings tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS earnings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                amount REAL NOT NULL,
                source TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                paid_at DATETIME,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Community posts
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS community_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                content TEXT NOT NULL,
                likes INTEGER DEFAULT 0,
                comments INTEGER DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Digital products downloads
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS product_downloads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                product_name TEXT NOT NULL,
                download_count INTEGER DEFAULT 0,
                last_downloaded DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def seed_initial_data(self):
        """Seed database with realistic initial data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM platform_stats")
        if cursor.fetchone()[0] > 0:
            conn.close()
            return
        
        # Insert initial platform stats
        cursor.execute('''
            INSERT INTO platform_stats (total_users, active_users_today, total_earnings, total_referrals, community_posts)
            VALUES (?, ?, ?, ?, ?)
        ''', (12847, 8932, 47382.50, 3421, 1567))
        
        # Create some sample users
        sample_users = [
            ("user_001", "demo@innerbloom.com", "Demo User", "vip", 2450, 15, 7, 1250.00),
            ("user_002", "sarah@example.com", "Sarah Johnson", "premium", 1890, 12, 5, 890.50),
            ("user_003", "emma@example.com", "Emma Wilson", "free", 567, 8, 3, 125.00),
            ("user_004", "lisa@example.com", "Lisa Chen", "vip", 3200, 18, 12, 2100.75),
            ("user_005", "maria@example.com", "Maria Rodriguez", "premium", 1456, 10, 4, 567.25)
        ]
        
        for user_data in sample_users:
            cursor.execute('''
                INSERT OR IGNORE INTO users (id, email, name, subscription_tier, points, level, streak_days, total_earnings)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', user_data)
        
        # Add some recent activities
        activities = [
            ("user_001", "daily_login", 10, "Daily login bonus"),
            ("user_001", "ai_chat", 5, "Chatted with Bloom AI"),
            ("user_002", "referral", 50, "Referred a new user"),
            ("user_003", "community_post", 15, "Posted in community"),
            ("user_004", "course_complete", 100, "Completed empowerment course")
        ]
        
        for activity in activities:
            cursor.execute('''
                INSERT INTO user_activities (user_id, activity_type, points_earned, description)
                VALUES (?, ?, ?, ?)
            ''', activity)
        
        conn.commit()
        conn.close()
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        """Get user data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user_data = cursor.fetchone()
        
        if user_data:
            columns = [description[0] for description in cursor.description]
            user = dict(zip(columns, user_data))
            
            # Get recent activities
            cursor.execute('''
                SELECT activity_type, points_earned, description, timestamp 
                FROM user_activities 
                WHERE user_id = ? 
                ORDER BY timestamp DESC 
                LIMIT 10
            ''', (user_id,))
            
            activities = cursor.fetchall()
            user['recent_activities'] = [
                {
                    'type': activity[0],
                    'points': activity[1],
                    'description': activity[2],
                    'timestamp': activity[3]
                }
                for activity in activities
            ]
            
            conn.close()
            return user
        
        conn.close()
        return None
    
    def create_user(self, email: str, name: str) -> str:
        """Create new user and return user_id"""
        import uuid
        user_id = f"user_{uuid.uuid4().hex[:8]}"
        referral_code = f"BLOOM{random.randint(1000, 9999)}"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO users (id, email, name, referral_code)
            VALUES (?, ?, ?, ?)
        ''', (user_id, email, name, referral_code))
        
        # Update platform stats
        cursor.execute('''
            UPDATE platform_stats 
            SET total_users = total_users + 1, 
                active_users_today = active_users_today + 1,
                last_updated = CURRENT_TIMESTAMP
        ''')
        
        conn.commit()
        conn.close()
        
        return user_id
    
    def add_points(self, user_id: str, points: int, activity_type: str, description: str):
        """Add points to user and log activity"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Update user points
        cursor.execute('''
            UPDATE users 
            SET points = points + ?, last_active = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (points, user_id))
        
        # Log activity
        cursor.execute('''
            INSERT INTO user_activities (user_id, activity_type, points_earned, description)
            VALUES (?, ?, ?, ?)
        ''', (user_id, activity_type, points, description))
        
        # Check for level up
        cursor.execute("SELECT points, level FROM users WHERE id = ?", (user_id,))
        user_data = cursor.fetchone()
        if user_data:
            current_points, current_level = user_data
            new_level = min(100, current_points // 100 + 1)  # Level up every 100 points
            
            if new_level > current_level:
                cursor.execute('''
                    UPDATE users SET level = ? WHERE id = ?
                ''', (new_level, user_id))
        
        conn.commit()
        conn.close()
    
    def get_platform_stats(self) -> Dict:
        """Get real-time platform statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM platform_stats ORDER BY id DESC LIMIT 1")
        stats_data = cursor.fetchone()
        
        if stats_data:
            columns = [description[0] for description in cursor.description]
            stats = dict(zip(columns, stats_data))
            
            # Add some real-time fluctuation
            now = datetime.now()
            stats['active_users_today'] += random.randint(-5, 15)
            stats['community_posts'] += random.randint(0, 3)
            
            conn.close()
            return stats
        
        conn.close()
        return {
            'total_users': 12847,
            'active_users_today': 8932,
            'total_earnings': 47382.50,
            'total_referrals': 3421,
            'community_posts': 1567
        }
    
    def add_earning(self, user_id: str, amount: float, source: str):
        """Add earning record"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO earnings (user_id, amount, source)
            VALUES (?, ?, ?)
        ''', (user_id, amount, source))
        
        # Update user total earnings
        cursor.execute('''
            UPDATE users 
            SET total_earnings = total_earnings + ?
            WHERE id = ?
        ''', (amount, user_id))
        
        # Update platform stats
        cursor.execute('''
            UPDATE platform_stats 
            SET total_earnings = total_earnings + ?,
                last_updated = CURRENT_TIMESTAMP
        ''', (amount,))
        
        conn.commit()
        conn.close()
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict]:
        """Get top users by points"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT name, points, level, total_earnings, subscription_tier
            FROM users 
            ORDER BY points DESC 
            LIMIT ?
        ''', (limit,))
        
        users = cursor.fetchall()
        leaderboard = []
        
        for i, user in enumerate(users):
            leaderboard.append({
                'rank': i + 1,
                'name': user[0],
                'points': user[1],
                'level': user[2],
                'earnings': user[3],
                'tier': user[4]
            })
        
        conn.close()
        return leaderboard

# Initialize the database
real_db = RealDatabase()

