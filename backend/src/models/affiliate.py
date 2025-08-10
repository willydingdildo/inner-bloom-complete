from datetime import datetime
from typing import Optional, List, Dict, Any

class AffiliateLink:
    def __init__(self, link_id: str, user_id: str, product_name: str, 
                 original_url: str, affiliate_url: str, commission_rate: float,
                 category: str = "general"):
        self.link_id = link_id
        self.user_id = user_id
        self.product_name = product_name
        self.original_url = original_url
        self.affiliate_url = affiliate_url
        self.commission_rate = commission_rate
        self.category = category
        self.created_at = datetime.utcnow()
        self.clicks = 0
        self.conversions = 0
        self.earnings = 0.0
        self.is_active = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            'link_id': self.link_id,
            'user_id': self.user_id,
            'product_name': self.product_name,
            'original_url': self.original_url,
            'affiliate_url': self.affiliate_url,
            'commission_rate': self.commission_rate,
            'category': self.category,
            'created_at': self.created_at.isoformat(),
            'clicks': self.clicks,
            'conversions': self.conversions,
            'earnings': self.earnings,
            'is_active': self.is_active
        }

class AffiliateClick:
    def __init__(self, click_id: str, link_id: str, user_id: str, 
                 ip_address: str, user_agent: str, referrer: str = ""):
        self.click_id = click_id
        self.link_id = link_id
        self.user_id = user_id
        self.ip_address = ip_address
        self.user_agent = user_agent
        self.referrer = referrer
        self.clicked_at = datetime.utcnow()
        self.converted = False
        self.conversion_value = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            'click_id': self.click_id,
            'link_id': self.link_id,
            'user_id': self.user_id,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'referrer': self.referrer,
            'clicked_at': self.clicked_at.isoformat(),
            'converted': self.converted,
            'conversion_value': self.conversion_value
        }

class AffiliateProgram:
    def __init__(self, program_id: str, name: str, description: str,
                 base_commission_rate: float, cookie_duration: int = 30):
        self.program_id = program_id
        self.name = name
        self.description = description
        self.base_commission_rate = base_commission_rate
        self.cookie_duration = cookie_duration
        self.is_active = True
        self.created_at = datetime.utcnow()
        
        # Tier-based commission rates
        self.tier_rates = {
            'bronze': base_commission_rate,
            'silver': base_commission_rate * 1.2,
            'gold': base_commission_rate * 1.5,
            'platinum': base_commission_rate * 2.0
        }

    def get_commission_rate(self, user_tier: str = 'bronze') -> float:
        return self.tier_rates.get(user_tier, self.base_commission_rate)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'program_id': self.program_id,
            'name': self.name,
            'description': self.description,
            'base_commission_rate': self.base_commission_rate,
            'cookie_duration': self.cookie_duration,
            'tier_rates': self.tier_rates,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat()
        }

class AffiliateEarnings:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.total_earnings = 0.0
        self.pending_earnings = 0.0
        self.paid_earnings = 0.0
        self.total_clicks = 0
        self.total_conversions = 0
        self.conversion_rate = 0.0
        self.tier = 'bronze'
        self.next_payout_date = None
        self.payment_method = None

    def calculate_conversion_rate(self):
        if self.total_clicks > 0:
            self.conversion_rate = (self.total_conversions / self.total_clicks) * 100
        else:
            self.conversion_rate = 0.0

    def update_tier(self):
        """Update user tier based on performance"""
        if self.total_earnings >= 10000:
            self.tier = 'platinum'
        elif self.total_earnings >= 5000:
            self.tier = 'gold'
        elif self.total_earnings >= 1000:
            self.tier = 'silver'
        else:
            self.tier = 'bronze'

    def to_dict(self) -> Dict[str, Any]:
        return {
            'user_id': self.user_id,
            'total_earnings': self.total_earnings,
            'pending_earnings': self.pending_earnings,
            'paid_earnings': self.paid_earnings,
            'total_clicks': self.total_clicks,
            'total_conversions': self.total_conversions,
            'conversion_rate': self.conversion_rate,
            'tier': self.tier,
            'next_payout_date': self.next_payout_date.isoformat() if self.next_payout_date else None,
            'payment_method': self.payment_method
        }

# In-memory storage for demo purposes
affiliate_links_db = {}
affiliate_clicks_db = {}
affiliate_programs_db = {}
affiliate_earnings_db = {}

# Initialize some sample affiliate programs
sample_programs = [
    AffiliateProgram(
        "fashion_forward", 
        "Fashion Forward", 
        "Sustainable fashion brands and accessories",
        0.08  # 8% commission
    ),
    AffiliateProgram(
        "wellness_world", 
        "Wellness World", 
        "Health, wellness, and self-care products",
        0.12  # 12% commission
    ),
    AffiliateProgram(
        "business_boost", 
        "Business Boost", 
        "Business tools, courses, and entrepreneurship resources",
        0.15  # 15% commission
    ),
    AffiliateProgram(
        "beauty_bloom", 
        "Beauty Bloom", 
        "Clean beauty and skincare products",
        0.10  # 10% commission
    )
]

for program in sample_programs:
    affiliate_programs_db[program.program_id] = program

