"""
Inner Bloom Marketplace Model
Handles user listings, products, and sales
"""

import sqlite3
import json
from datetime import datetime
import uuid

class MarketplaceDB:
    def __init__(self, db_path="inner_bloom.db"):
        self.db_path = db_path
        self.init_tables()
    
    def init_tables(self):
        """Initialize marketplace tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Products table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id TEXT PRIMARY KEY,
                seller_id TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                category TEXT,
                image_url TEXT,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (seller_id) REFERENCES users (id)
            )
        """)
        
        # Sales table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id TEXT PRIMARY KEY,
                product_id TEXT NOT NULL,
                buyer_id TEXT NOT NULL,
                seller_id TEXT NOT NULL,
                amount REAL NOT NULL,
                commission REAL NOT NULL,
                status TEXT DEFAULT 'completed',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products (id),
                FOREIGN KEY (buyer_id) REFERENCES users (id),
                FOREIGN KEY (seller_id) REFERENCES users (id)
            )
        """)
        
        # Reviews table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id TEXT PRIMARY KEY,
                product_id TEXT NOT NULL,
                buyer_id TEXT NOT NULL,
                rating INTEGER NOT NULL,
                comment TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products (id),
                FOREIGN KEY (buyer_id) REFERENCES users (id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def create_product(self, seller_id, title, description, price, category, image_url=None):
        """Create a new product listing"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        product_id = str(uuid.uuid4())
        
        cursor.execute("""
            INSERT INTO products (id, seller_id, title, description, price, category, image_url)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (product_id, seller_id, title, description, price, category, image_url))
        
        conn.commit()
        conn.close()
        
        return product_id
    
    def get_products(self, category=None, limit=20, offset=0):
        """Get products with optional category filter"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if category:
            cursor.execute("""
                SELECT p.*, u.name as seller_name
                FROM products p
                JOIN users u ON p.seller_id = u.id
                WHERE p.status = 'active' AND p.category = ?
                ORDER BY p.created_at DESC
                LIMIT ? OFFSET ?
            """, (category, limit, offset))
        else:
            cursor.execute("""
                SELECT p.*, u.name as seller_name
                FROM products p
                JOIN users u ON p.seller_id = u.id
                WHERE p.status = 'active'
                ORDER BY p.created_at DESC
                LIMIT ? OFFSET ?
            """, (limit, offset))
        
        products = []
        for row in cursor.fetchall():
            products.append({
                'id': row[0],
                'seller_id': row[1],
                'title': row[2],
                'description': row[3],
                'price': row[4],
                'category': row[5],
                'image_url': row[6],
                'status': row[7],
                'created_at': row[8],
                'updated_at': row[9],
                'seller_name': row[10]
            })
        
        conn.close()
        return products
    
    def get_user_products(self, seller_id):
        """Get all products for a specific seller"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM products
            WHERE seller_id = ?
            ORDER BY created_at DESC
        """, (seller_id,))
        
        products = []
        for row in cursor.fetchall():
            products.append({
                'id': row[0],
                'seller_id': row[1],
                'title': row[2],
                'description': row[3],
                'price': row[4],
                'category': row[5],
                'image_url': row[6],
                'status': row[7],
                'created_at': row[8],
                'updated_at': row[9]
            })
        
        conn.close()
        return products
    
    def purchase_product(self, product_id, buyer_id):
        """Process a product purchase"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get product details
        cursor.execute("SELECT * FROM products WHERE id = ? AND status = 'active'", (product_id,))
        product = cursor.fetchone()
        
        if not product:
            conn.close()
            return None
        
        # Calculate commission (10% to platform)
        price = product[4]
        commission = price * 0.10
        seller_earnings = price - commission
        
        # Create sale record
        sale_id = str(uuid.uuid4())
        cursor.execute("""
            INSERT INTO sales (id, product_id, buyer_id, seller_id, amount, commission)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (sale_id, product_id, buyer_id, product[1], price, commission))
        
        # Update seller earnings
        cursor.execute("""
            UPDATE users SET total_earnings = total_earnings + ?
            WHERE id = ?
        """, (seller_earnings, product[1]))
        
        # Mark product as sold
        cursor.execute("""
            UPDATE products SET status = 'sold'
            WHERE id = ?
        """, (product_id,))
        
        conn.commit()
        conn.close()
        
        return {
            'sale_id': sale_id,
            'amount': price,
            'commission': commission,
            'seller_earnings': seller_earnings
        }
    
    def get_sales_stats(self, seller_id=None):
        """Get sales statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if seller_id:
            cursor.execute("""
                SELECT COUNT(*) as total_sales, SUM(amount - commission) as total_earnings
                FROM sales
                WHERE seller_id = ?
            """, (seller_id,))
        else:
            cursor.execute("""
                SELECT COUNT(*) as total_sales, SUM(amount) as total_revenue, SUM(commission) as total_commission
                FROM sales
            """)
        
        result = cursor.fetchone()
        conn.close()
        
        if seller_id:
            return {
                'total_sales': result[0] or 0,
                'total_earnings': result[1] or 0.0
            }
        else:
            return {
                'total_sales': result[0] or 0,
                'total_revenue': result[1] or 0.0,
                'total_commission': result[2] or 0.0
            }

# Initialize marketplace database
marketplace_db = MarketplaceDB()

# Seed some sample products
def seed_marketplace():
    """Add sample products to the marketplace"""
    sample_products = [
        {
            'seller_id': 'demo_user',
            'title': 'Empowerment Journal - Digital Download',
            'description': 'A beautiful 30-day empowerment journal to track your growth journey. Includes daily prompts, affirmations, and goal-setting pages.',
            'price': 29.99,
            'category': 'Digital Products',
            'image_url': '/api/placeholder/300/200'
        },
        {
            'seller_id': 'demo_user',
            'title': 'Manifestation Planner 2024',
            'description': 'Complete manifestation planner with moon phases, vision boards, and monthly goal tracking. Perfect for ambitious women.',
            'price': 49.99,
            'category': 'Planners',
            'image_url': '/api/placeholder/300/200'
        },
        {
            'seller_id': 'demo_user',
            'title': 'She-EO Business Templates Bundle',
            'description': 'Professional business templates including contracts, invoices, social media templates, and brand guidelines.',
            'price': 89.99,
            'category': 'Business Tools',
            'image_url': '/api/placeholder/300/200'
        },
        {
            'seller_id': 'demo_user',
            'title': 'Divine Feminine Energy Course',
            'description': 'Online course covering sacred feminine practices, energy healing, and spiritual empowerment. 8 modules included.',
            'price': 199.99,
            'category': 'Courses',
            'image_url': '/api/placeholder/300/200'
        },
        {
            'seller_id': 'demo_user',
            'title': 'Affirmation Card Deck - Printable',
            'description': '52 beautiful affirmation cards for daily inspiration. Print at home and start your empowerment practice today.',
            'price': 19.99,
            'category': 'Digital Products',
            'image_url': '/api/placeholder/300/200'
        }
    ]
    
    # Check if products already exist
    conn = sqlite3.connect("inner_bloom.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM products")
    count = cursor.fetchone()[0]
    conn.close()
    
    if count == 0:
        for product in sample_products:
            marketplace_db.create_product(**product)

# Seed the marketplace
seed_marketplace()

