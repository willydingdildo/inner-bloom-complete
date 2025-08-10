from flask import Blueprint, jsonify, request
import random
from datetime import datetime, timedelta
import json

social_proof_bp = Blueprint('social_proof', __name__)

# Fake user names for social proof
SISTER_NAMES = [
    'Divine Rose', 'Sacred Luna', 'Golden Goddess', 'Radiant Star', 'Mystic Dawn',
    'Celestial Grace', 'Bloom Queen', 'Sacred Fire', 'Divine Light', 'Eternal Bloom',
    'Goddess Aria', 'Sacred Willow', 'Divine Phoenix', 'Radiant Moon', 'Golden Spirit',
    'Celestial Rose', 'Sacred Ember', 'Divine Aurora', 'Mystic Sage', 'Bloom Angel'
]

SUCCESS_STORIES = [
    "I manifested my dream job within 30 days of joining Inner Bloom! The sisterhood energy is REAL! 💫",
    "Lost 25 pounds and found my confidence again. This community saved my life! 🌟",
    "Started my own business and made $10K in my first month. Inner Bloom changed everything! 💎",
    "Met my soulmate after working on self-love. The universe really does conspire for us! ❤️",
    "Healed my relationship with my mother after years of pain. The transformation is miraculous! 🙏",
    "Doubled my income and bought my dream house. Manifestation works when you have sisters supporting you! 🏡",
    "Overcame depression and anxiety. I'm finally living my purpose! This sisterhood is everything! ✨",
    "Left my toxic relationship and found inner peace. I'm a completely new woman! 🦋"
]

ACTIVITIES = [
    "completed the Sacred Morning Ritual",
    "shared a transformation story",
    "earned the Golden Goddess badge",
    "joined the VIP Sister Circle",
    "manifested a major breakthrough",
    "completed the 7-day challenge",
    "unlocked exclusive content",
    "reached Level 5 transformation",
    "sent healing energy to the community",
    "celebrated a major milestone"
]

@social_proof_bp.route('/live-activity', methods=['GET'])
def get_live_activity():
    """Get real-time activity feed for social proof"""
    
    # Generate fake but believable activity
    activities = []
    for i in range(15):
        activity = {
            'id': f"activity_{i}",
            'sister_name': random.choice(SISTER_NAMES),
            'action': random.choice(ACTIVITIES),
            'timestamp': (datetime.now() - timedelta(minutes=random.randint(1, 120))).isoformat(),
            'points_earned': random.choice([25, 50, 75, 100, 150, 200]),
            'location': random.choice(['New York', 'Los Angeles', 'Chicago', 'Miami', 'Seattle', 'Austin', 'Denver']),
            'achievement_unlocked': random.choice([None, None, None, 'Rising Star', 'Divine Warrior', 'Sacred Queen'])
        }
        activities.append(activity)
    
    return jsonify({
        'success': True,
        'activities': activities,
        'total_active_now': random.randint(847, 1247),
        'total_transformations_today': random.randint(156, 289)
    })

@social_proof_bp.route('/success-testimonials', methods=['GET'])
def get_success_testimonials():
    """Get rotating success testimonials for FOMO"""
    
    testimonials = []
    for i in range(8):
        testimonial = {
            'id': f"testimonial_{i}",
            'sister_name': random.choice(SISTER_NAMES),
            'story': random.choice(SUCCESS_STORIES),
            'transformation_area': random.choice(['Financial', 'Relationships', 'Health', 'Career', 'Spiritual', 'Self-Love']),
            'time_to_result': random.choice(['2 weeks', '1 month', '3 months', '6 months']),
            'before_rating': random.randint(2, 4),
            'after_rating': random.randint(8, 10),
            'verified': True,
            'featured': random.choice([True, False, False, False])  # 25% chance of being featured
        }
        testimonials.append(testimonial)
    
    return jsonify({
        'success': True,
        'testimonials': testimonials,
        'total_success_stories': random.randint(2847, 3156)
    })

@social_proof_bp.route('/urgency-metrics', methods=['GET'])
def get_urgency_metrics():
    """Get urgency-inducing metrics and counters"""
    
    metrics = {
        'sisters_joined_today': random.randint(47, 89),
        'sisters_joined_this_hour': random.randint(3, 12),
        'transformations_in_progress': random.randint(234, 456),
        'success_stories_shared_today': random.randint(23, 67),
        'total_community_size': random.randint(12847, 15234),
        'average_transformation_time': '21 days',
        'success_rate': '94%',
        'spots_remaining_vip': random.randint(7, 23),
        'limited_offer_expires_in': random.randint(3600, 86400),  # 1 hour to 24 hours in seconds
        'sisters_online_now': random.randint(156, 289),
        'current_energy_level': random.randint(85, 98),  # Community energy percentage
        'manifestations_today': random.randint(34, 78)
    }
    
    return jsonify({
        'success': True,
        'metrics': metrics,
        'trending_hashtags': ['#InnerBloomTransformation', '#SacredSisterhood', '#ManifestationMagic', '#DivineFeminine']
    })

@social_proof_bp.route('/peer-pressure', methods=['GET'])
def get_peer_pressure_messages():
    """Get peer pressure messages to encourage engagement"""
    
    messages = [
        {
            'type': 'challenge_participation',
            'message': f"{random.randint(234, 567)} sisters have already completed today's challenge. Will you join them?",
            'urgency': 'high',
            'action_text': 'Join Challenge Now'
        },
        {
            'type': 'community_activity',
            'message': f"Your sister circle is 73% more active than you this week. Time to catch up!",
            'urgency': 'medium',
            'action_text': 'Get Active'
        },
        {
            'type': 'milestone_pressure',
            'message': f"{random.choice(SISTER_NAMES)} just reached Level 5! You're only {random.randint(2, 4)} levels behind.",
            'urgency': 'medium',
            'action_text': 'Level Up'
        },
        {
            'type': 'exclusive_access',
            'message': f"Only {random.randint(12, 34)} VIP spots left this month. Your sisters are securing theirs!",
            'urgency': 'high',
            'action_text': 'Claim VIP Access'
        },
        {
            'type': 'transformation_fomo',
            'message': f"{random.randint(45, 89)} sisters transformed their lives this month. What are you waiting for?",
            'urgency': 'high',
            'action_text': 'Start Transformation'
        }
    ]
    
    return jsonify({
        'success': True,
        'messages': random.sample(messages, 3),  # Return 3 random messages
        'community_pressure_level': random.randint(75, 95)
    })

@social_proof_bp.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    """Get leaderboard for competitive social pressure"""
    
    leaderboard = []
    for i in range(20):
        entry = {
            'rank': i + 1,
            'sister_name': random.choice(SISTER_NAMES),
            'points': random.randint(500, 5000),
            'level': random.randint(3, 15),
            'streak': random.randint(7, 180),
            'transformation_score': random.randint(65, 98),
            'is_current_user': i == 7,  # Make user rank 8th for motivation
            'tier': random.choice(['Novice', 'Intermediate', 'Advanced', 'Legendary']),
            'recent_achievement': random.choice([None, 'Sacred Warrior', 'Divine Queen', 'Transformation Master'])
        }
        leaderboard.append(entry)
    
    # Sort by points descending
    leaderboard.sort(key=lambda x: x['points'], reverse=True)
    
    # Update ranks
    for i, entry in enumerate(leaderboard):
        entry['rank'] = i + 1
    
    return jsonify({
        'success': True,
        'leaderboard': leaderboard,
        'user_rank': 8,
        'points_to_next_rank': random.randint(150, 400),
        'total_participants': len(leaderboard) + random.randint(200, 500)
    })

@social_proof_bp.route('/scarcity-alerts', methods=['GET'])
def get_scarcity_alerts():
    """Get scarcity-based alerts to create FOMO"""
    
    alerts = [
        {
            'type': 'limited_spots',
            'title': 'VIP Circle Almost Full!',
            'message': f'Only {random.randint(3, 15)} spots remaining in this month\'s VIP Sister Circle',
            'urgency_level': 'critical',
            'expires_in_hours': random.randint(6, 48),
            'claimed_count': random.randint(87, 97),
            'total_spots': 100
        },
        {
            'type': 'exclusive_content',
            'title': 'Sacred Wisdom Disappearing Soon!',
            'message': 'Exclusive masterclass access expires in 24 hours',
            'urgency_level': 'high',
            'expires_in_hours': random.randint(12, 24),
            'claimed_count': random.randint(234, 456),
            'total_spots': 500
        },
        {
            'type': 'bonus_points',
            'title': 'Double Points Ending!',
            'message': 'Last chance to earn double transformation points',
            'urgency_level': 'medium',
            'expires_in_hours': random.randint(2, 8),
            'claimed_count': random.randint(123, 234),
            'total_spots': 300
        }
    ]
    
    return jsonify({
        'success': True,
        'alerts': alerts,
        'total_active_offers': len(alerts),
        'sisters_taking_action_now': random.randint(23, 67)
    })

@social_proof_bp.route('/community-energy', methods=['GET'])
def get_community_energy():
    """Get community energy levels for collective motivation"""
    
    energy_data = {
        'current_energy': random.randint(78, 96),
        'energy_trend': random.choice(['rising', 'stable', 'peak']),
        'peak_hours': ['6:00 AM - 9:00 AM', '6:00 PM - 9:00 PM'],
        'most_active_regions': ['California', 'New York', 'Texas', 'Florida'],
        'collective_manifestations': random.randint(45, 89),
        'group_challenges_active': random.randint(3, 7),
        'sisters_meditating_now': random.randint(23, 67),
        'positive_vibes_sent': random.randint(234, 567),
        'transformation_momentum': random.randint(85, 98),
        'next_energy_boost': f"Full Moon Ceremony in {random.randint(3, 14)} days"
    }
    
    return jsonify({
        'success': True,
        'energy': energy_data,
        'message': 'The sisterhood energy is at an all-time high! Perfect time for manifestation! ✨'
    })

