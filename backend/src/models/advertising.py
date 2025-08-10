from datetime import datetime
from typing import Optional, List, Dict, Any
import random

class AdNetwork:
    def __init__(self, network_id: str, name: str, description: str, 
                 revenue_share: float, min_payout: float = 100.0):
        self.network_id = network_id
        self.name = name
        self.description = description
        self.revenue_share = revenue_share  # Percentage of ad revenue shared with platform
        self.min_payout = min_payout
        self.is_active = True
        self.created_at = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        return {
            'network_id': self.network_id,
            'name': self.name,
            'description': self.description,
            'revenue_share': self.revenue_share,
            'min_payout': self.min_payout,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat()
        }

class AdPlacement:
    def __init__(self, placement_id: str, name: str, location: str, 
                 ad_type: str, dimensions: str):
        self.placement_id = placement_id
        self.name = name
        self.location = location  # e.g., 'homepage_banner', 'sidebar', 'feed_native'
        self.ad_type = ad_type    # e.g., 'banner', 'native', 'video', 'sponsored_post'
        self.dimensions = dimensions  # e.g., '728x90', '300x250', 'responsive'
        self.is_active = True
        self.created_at = datetime.utcnow()
        
        # Performance metrics
        self.impressions = 0
        self.clicks = 0
        self.revenue = 0.0
        self.ctr = 0.0  # Click-through rate

    def calculate_ctr(self):
        if self.impressions > 0:
            self.ctr = (self.clicks / self.impressions) * 100
        else:
            self.ctr = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            'placement_id': self.placement_id,
            'name': self.name,
            'location': self.location,
            'ad_type': self.ad_type,
            'dimensions': self.dimensions,
            'is_active': self.is_active,
            'impressions': self.impressions,
            'clicks': self.clicks,
            'revenue': self.revenue,
            'ctr': self.ctr,
            'created_at': self.created_at.isoformat()
        }

class SponsoredContent:
    def __init__(self, content_id: str, advertiser: str, title: str, 
                 description: str, image_url: str, target_url: str,
                 budget: float, target_audience: Dict[str, Any]):
        self.content_id = content_id
        self.advertiser = advertiser
        self.title = title
        self.description = description
        self.image_url = image_url
        self.target_url = target_url
        self.budget = budget
        self.spent = 0.0
        self.target_audience = target_audience
        self.is_active = True
        self.created_at = datetime.utcnow()
        
        # Performance metrics
        self.impressions = 0
        self.clicks = 0
        self.conversions = 0
        self.cost_per_click = 0.0
        self.cost_per_conversion = 0.0

    def calculate_metrics(self):
        if self.clicks > 0:
            self.cost_per_click = self.spent / self.clicks
        if self.conversions > 0:
            self.cost_per_conversion = self.spent / self.conversions

    def to_dict(self) -> Dict[str, Any]:
        return {
            'content_id': self.content_id,
            'advertiser': self.advertiser,
            'title': self.title,
            'description': self.description,
            'image_url': self.image_url,
            'target_url': self.target_url,
            'budget': self.budget,
            'spent': self.spent,
            'target_audience': self.target_audience,
            'is_active': self.is_active,
            'impressions': self.impressions,
            'clicks': self.clicks,
            'conversions': self.conversions,
            'cost_per_click': self.cost_per_click,
            'cost_per_conversion': self.cost_per_conversion,
            'created_at': self.created_at.isoformat()
        }

class AdRevenue:
    def __init__(self, user_id: str = None):
        self.user_id = user_id  # None for platform-wide revenue
        self.total_revenue = 0.0
        self.pending_revenue = 0.0
        self.paid_revenue = 0.0
        self.total_impressions = 0
        self.total_clicks = 0
        self.average_ctr = 0.0
        self.last_updated = datetime.utcnow()

    def calculate_average_ctr(self):
        if self.total_impressions > 0:
            self.average_ctr = (self.total_clicks / self.total_impressions) * 100
        else:
            self.average_ctr = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            'user_id': self.user_id,
            'total_revenue': self.total_revenue,
            'pending_revenue': self.pending_revenue,
            'paid_revenue': self.paid_revenue,
            'total_impressions': self.total_impressions,
            'total_clicks': self.total_clicks,
            'average_ctr': self.average_ctr,
            'last_updated': self.last_updated.isoformat()
        }

# In-memory storage for demo purposes
ad_networks_db = {}
ad_placements_db = {}
sponsored_content_db = {}
ad_revenue_db = {}

# Initialize sample ad networks
sample_networks = [
    AdNetwork(
        "google_adsense",
        "Google AdSense",
        "Premium display advertising network with high-quality ads",
        0.68  # 68% revenue share
    ),
    AdNetwork(
        "media_net",
        "Media.net",
        "Contextual advertising network powered by Yahoo and Bing",
        0.70  # 70% revenue share
    ),
    AdNetwork(
        "amazon_associates",
        "Amazon Associates",
        "Product recommendation and affiliate advertising",
        0.75  # 75% revenue share
    ),
    AdNetwork(
        "native_ads",
        "Native Ads Network",
        "Native advertising that blends with content",
        0.65  # 65% revenue share
    )
]

for network in sample_networks:
    ad_networks_db[network.network_id] = network

# Initialize sample ad placements
sample_placements = [
    AdPlacement(
        "homepage_hero",
        "Homepage Hero Banner",
        "homepage_banner",
        "banner",
        "1200x300"
    ),
    AdPlacement(
        "sidebar_square",
        "Sidebar Square Ad",
        "sidebar",
        "banner",
        "300x300"
    ),
    AdPlacement(
        "feed_native",
        "Community Feed Native Ad",
        "feed_native",
        "native",
        "responsive"
    ),
    AdPlacement(
        "article_inline",
        "Article Inline Ad",
        "article_inline",
        "banner",
        "728x90"
    ),
    AdPlacement(
        "mobile_banner",
        "Mobile Banner",
        "mobile_banner",
        "banner",
        "320x50"
    )
]

for placement in sample_placements:
    ad_placements_db[placement.placement_id] = placement

# Initialize sample sponsored content
sample_sponsored_content = [
    SponsoredContent(
        "wellness_brand_1",
        "Glow Wellness Co.",
        "Transform Your Morning Routine",
        "Discover the power of our organic wellness products designed specifically for empowered women.",
        "https://example.com/wellness-ad.jpg",
        "https://glowwellness.com/inner-bloom",
        5000.0,
        {
            "age_range": [25, 45],
            "interests": ["wellness", "self-care", "personal-growth"],
            "subscription_tier": ["premium", "vip"]
        }
    ),
    SponsoredContent(
        "fashion_brand_1",
        "Sustainable Style Co.",
        "Ethical Fashion That Empowers",
        "Shop our collection of sustainable, ethically-made clothing that makes you look and feel amazing.",
        "https://example.com/fashion-ad.jpg",
        "https://sustainablestyle.com/inner-bloom",
        3000.0,
        {
            "age_range": [22, 40],
            "interests": ["fashion", "sustainability", "style"],
            "subscription_tier": ["free", "premium", "vip"]
        }
    ),
    SponsoredContent(
        "business_course_1",
        "Entrepreneur Academy",
        "Launch Your Dream Business",
        "Join thousands of women who've built successful businesses with our proven framework.",
        "https://example.com/business-ad.jpg",
        "https://entrepreneuracademy.com/inner-bloom",
        7500.0,
        {
            "age_range": [25, 50],
            "interests": ["entrepreneurship", "business", "career"],
            "subscription_tier": ["premium", "vip"]
        }
    )
]

for content in sample_sponsored_content:
    sponsored_content_db[content.content_id] = content

# Initialize platform revenue tracking
platform_revenue = AdRevenue()
ad_revenue_db['platform'] = platform_revenue

