from flask import Blueprint, jsonify, request
import random
from datetime import datetime, timedelta
import json

addiction_bp = Blueprint('addiction', __name__)

# Unpredictable reward system
@addiction_bp.route('/random-reward', methods=['POST'])
def get_random_reward():
    """Generate unpredictable rewards with variable schedules"""
    
    # Define reward types with different rarities
    rewards = {
        'common': [
            {'type': 'points', 'amount': 25, 'icon': '⭐', 'message': 'Daily Shine!', 'rarity': 'common'},
            {'type': 'points', 'amount': 50, 'icon': '✨', 'message': 'Sparkle Bonus!', 'rarity': 'common'},
            {'type': 'affirmation', 'icon': '💫', 'message': 'Divine Affirmation!', 'content': 'You are exactly where you need to be, sister.', 'rarity': 'common'},
        ],
        'uncommon': [
            {'type': 'points', 'amount': 100, 'icon': '🌟', 'message': 'Star Power!', 'rarity': 'uncommon'},
            {'type': 'title', 'icon': '👑', 'message': 'New Title Unlocked!', 'title': 'Rising Star', 'rarity': 'uncommon'},
            {'type': 'exclusive_content', 'icon': '🔮', 'message': 'Secret Wisdom Unlocked!', 'content': 'The universe conspires to help those who help themselves.', 'rarity': 'uncommon'},
        ],
        'rare': [
            {'type': 'points', 'amount': 250, 'icon': '💎', 'message': 'Diamond Blessing!', 'rarity': 'rare'},
            {'type': 'title', 'icon': '🦋', 'message': 'Transformation Complete!', 'title': 'Butterfly Sister', 'rarity': 'rare'},
            {'type': 'special_badge', 'icon': '🏆', 'message': 'Divine Recognition!', 'badge': 'Chosen One', 'rarity': 'rare'},
        ],
        'legendary': [
            {'type': 'points', 'amount': 500, 'icon': '🌈', 'message': 'Rainbow Miracle!', 'rarity': 'legendary'},
            {'type': 'title', 'icon': '👸', 'message': 'Ascension Achieved!', 'title': 'Inner Bloom Queen', 'rarity': 'legendary'},
            {'type': 'exclusive_access', 'icon': '🗝️', 'message': 'Sacred Chamber Unlocked!', 'access': 'VIP_LOUNGE', 'rarity': 'legendary'},
        ]
    }
    
    # Determine rarity based on weighted probability
    rand = random.random()
    if rand < 0.60:  # 60% common
        rarity = 'common'
    elif rand < 0.85:  # 25% uncommon
        rarity = 'uncommon'
    elif rand < 0.97:  # 12% rare
        rarity = 'rare'
    else:  # 3% legendary
        rarity = 'legendary'
    
    # Select random reward from chosen rarity
    reward = random.choice(rewards[rarity])
    
    return jsonify({
        'success': True,
        'reward': reward,
        'timestamp': datetime.now().isoformat()
    })

# Achievement system with emotional validation
@addiction_bp.route('/achievements', methods=['GET'])
def get_achievements():
    """Get available achievements with emotional triggers"""
    
    achievements = [
        {
            'id': 'first_bloom',
            'name': 'First Bloom',
            'description': 'You took the first step into your transformation',
            'icon': '🌱',
            'emotional_message': 'Every mighty oak was once a tiny acorn. You\'ve planted your seed.',
            'points': 50,
            'category': 'journey'
        },
        {
            'id': 'daily_warrior',
            'name': 'Daily Warrior',
            'description': 'Maintained a 7-day streak',
            'icon': '⚔️',
            'emotional_message': 'Your consistency is your superpower. You\'re becoming unstoppable.',
            'points': 150,
            'category': 'consistency'
        },
        {
            'id': 'point_collector',
            'name': 'Point Collector',
            'description': 'Earned 500 points',
            'icon': '💎',
            'emotional_message': 'Each point represents a moment you chose growth over comfort.',
            'points': 100,
            'category': 'progress'
        },
        {
            'id': 'sister_supporter',
            'name': 'Sister Supporter',
            'description': 'Helped 5 sisters in the community',
            'icon': '🤝',
            'emotional_message': 'Your light helps others find their way. You\'re a beacon of hope.',
            'points': 200,
            'category': 'community'
        },
        {
            'id': 'transformation_queen',
            'name': 'Transformation Queen',
            'description': 'Completed your first major milestone',
            'icon': '👑',
            'emotional_message': 'You\'ve shed your old skin and emerged as royalty. Bow to no one.',
            'points': 300,
            'category': 'transformation'
        }
    ]
    
    return jsonify({
        'success': True,
        'achievements': achievements
    })

# Daily challenges with social pressure
@addiction_bp.route('/daily-challenge', methods=['GET'])
def get_daily_challenge():
    """Get today's challenge with social pressure elements"""
    
    challenges = [
        {
            'id': 'morning_affirmation',
            'title': 'Morning Goddess Ritual',
            'description': 'Start your day with 3 powerful affirmations',
            'icon': '🌅',
            'points': 75,
            'social_message': '847 sisters have already completed this challenge today. Will you join them?',
            'urgency': 'Only 6 hours left to complete today\'s challenge!'
        },
        {
            'id': 'gratitude_share',
            'title': 'Gratitude Overflow',
            'description': 'Share 3 things you\'re grateful for with the community',
            'icon': '🙏',
            'points': 100,
            'social_message': 'Your sisters are waiting to celebrate your blessings with you.',
            'urgency': 'Limited time: Share your gratitude before midnight!'
        },
        {
            'id': 'self_love_moment',
            'title': 'Self-Love Sunday',
            'description': 'Take a photo celebrating something you love about yourself',
            'icon': '💖',
            'points': 125,
            'social_message': '1,203 sisters have shared their self-love today. Your turn to shine!',
            'urgency': 'Sunday special ends in 4 hours!'
        }
    ]
    
    # Select today's challenge based on date
    today = datetime.now().day
    challenge = challenges[today % len(challenges)]
    
    return jsonify({
        'success': True,
        'challenge': challenge,
        'participation_count': random.randint(500, 2000),  # Fake social proof
        'completion_rate': random.randint(65, 85)  # Fake completion rate
    })

# Scarcity-based rewards
@addiction_bp.route('/limited-offer', methods=['GET'])
def get_limited_offer():
    """Get current limited-time offers with scarcity messaging"""
    
    offers = [
        {
            'id': 'golden_hour',
            'title': 'Golden Hour Blessing',
            'description': 'Double points for the next 2 hours only',
            'icon': '⏰',
            'multiplier': 2,
            'expires_in_minutes': 120,
            'scarcity_message': 'Only 47 spots remaining for this divine blessing!',
            'urgency_message': 'This opportunity vanishes at sunset!'
        },
        {
            'id': 'sister_circle_bonus',
            'title': 'Sister Circle Exclusive',
            'description': 'Unlock exclusive content for 24 hours',
            'icon': '🔓',
            'content_type': 'exclusive_wisdom',
            'expires_in_minutes': 1440,
            'scarcity_message': 'Limited to first 100 awakened sisters only!',
            'urgency_message': 'Sacred knowledge disappears at midnight!'
        }
    ]
    
    # Select random offer
    offer = random.choice(offers)
    
    # Add fake countdown and scarcity numbers
    offer['spots_remaining'] = random.randint(15, 99)
    offer['claimed_by'] = random.randint(200, 800)
    
    return jsonify({
        'success': True,
        'offer': offer,
        'is_active': True
    })

# Emotional milestone tracking
@addiction_bp.route('/milestone-progress', methods=['GET'])
def get_milestone_progress():
    """Track emotional milestones with psychological reinforcement"""
    
    milestones = [
        {
            'id': 'awakening',
            'name': 'The Awakening',
            'description': 'You\'ve opened your eyes to your true potential',
            'progress_message': 'You\'re 73% through your awakening journey',
            'emotional_trigger': 'Feel the old you fading away as your true self emerges',
            'icon': '👁️',
            'progress_percent': 73
        },
        {
            'id': 'transformation',
            'name': 'The Transformation',
            'description': 'Your metamorphosis into your highest self',
            'progress_message': 'You\'re 45% transformed into your divine self',
            'emotional_trigger': 'Like a butterfly emerging from its cocoon, you\'re becoming magnificent',
            'icon': '🦋',
            'progress_percent': 45
        },
        {
            'id': 'empowerment',
            'name': 'The Empowerment',
            'description': 'Claiming your power and stepping into your throne',
            'progress_message': 'You\'re 89% ready to claim your crown',
            'emotional_trigger': 'The queen within you is almost ready to rule her kingdom',
            'icon': '👑',
            'progress_percent': 89
        }
    ]
    
    return jsonify({
        'success': True,
        'milestones': milestones,
        'overall_progress': 69,  # Fake overall progress
        'next_breakthrough': 'Your next major breakthrough is just 3 days away!'
    })

