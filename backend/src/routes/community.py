from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from src.models.community import (
    SisterhoodCircle, CircleMembership, CommunityPost, PostComment, 
    VirtualHug, UserAchievement, UserEngagement, ShareableContent, db
)
import json
from datetime import datetime

community_bp = Blueprint('community', __name__)

@community_bp.route('/circles', methods=['GET'])
@cross_origin()
def get_circles():
    """Get all public circles or user's circles"""
    user_id = request.args.get('user_id', type=int)
    
    if user_id:
        # Get circles the user is a member of
        memberships = CircleMembership.query.filter_by(user_id=user_id).all()
        circle_ids = [m.circle_id for m in memberships]
        circles = SisterhoodCircle.query.filter(SisterhoodCircle.id.in_(circle_ids)).all()
    else:
        # Get public circles
        circles = SisterhoodCircle.query.filter_by(is_private=False).all()
    
    return jsonify([circle.to_dict() for circle in circles])

@community_bp.route('/circles', methods=['POST'])
@cross_origin()
def create_circle():
    """Create a new sisterhood circle"""
    data = request.json
    circle = SisterhoodCircle(
        name=data['name'],
        description=data.get('description', ''),
        creator_id=data['creator_id'],
        max_members=data.get('max_members', 10),
        focus_area=data.get('focus_area', ''),
        is_private=data.get('is_private', True)
    )
    db.session.add(circle)
    db.session.flush()  # Get the circle ID
    
    # Add creator as a member
    membership = CircleMembership(
        circle_id=circle.id,
        user_id=data['creator_id'],
        role='creator'
    )
    db.session.add(membership)
    db.session.commit()
    
    return jsonify(circle.to_dict()), 201

@community_bp.route('/circles/<int:circle_id>/join', methods=['POST'])
@cross_origin()
def join_circle(circle_id):
    """Join a sisterhood circle"""
    data = request.json
    user_id = data['user_id']
    
    # Check if already a member
    existing = CircleMembership.query.filter_by(circle_id=circle_id, user_id=user_id).first()
    if existing:
        return jsonify({'error': 'Already a member'}), 400
    
    # Check circle capacity
    circle = SisterhoodCircle.query.get_or_404(circle_id)
    if circle.current_members >= circle.max_members:
        return jsonify({'error': 'Circle is full'}), 400
    
    membership = CircleMembership(
        circle_id=circle_id,
        user_id=user_id,
        role='member'
    )
    db.session.add(membership)
    
    # Update member count
    circle.current_members += 1
    db.session.commit()
    
    return jsonify(membership.to_dict()), 201

@community_bp.route('/posts', methods=['GET'])
@cross_origin()
def get_posts():
    """Get community posts"""
    circle_id = request.args.get('circle_id', type=int)
    limit = request.args.get('limit', 20, type=int)
    
    query = CommunityPost.query
    if circle_id:
        query = query.filter_by(circle_id=circle_id)
    else:
        # Public posts only
        query = query.filter_by(circle_id=None)
    
    posts = query.order_by(CommunityPost.created_at.desc()).limit(limit).all()
    return jsonify([post.to_dict() for post in posts])

@community_bp.route('/posts', methods=['POST'])
@cross_origin()
def create_post():
    """Create a new community post"""
    data = request.json
    post = CommunityPost(
        author_id=data['author_id'],
        circle_id=data.get('circle_id'),
        title=data.get('title', ''),
        content=data['content'],
        post_type=data.get('post_type', 'story'),
        tags=json.dumps(data.get('tags', [])),
        is_anonymous=data.get('is_anonymous', False)
    )
    db.session.add(post)
    db.session.commit()
    
    # Update user engagement
    engagement = UserEngagement.query.filter_by(user_id=data['author_id']).first()
    if engagement:
        engagement.posts_created += 1
        engagement.total_points += 10  # Points for creating a post
        db.session.commit()
    
    return jsonify(post.to_dict()), 201

@community_bp.route('/posts/<int:post_id>/comments', methods=['GET'])
@cross_origin()
def get_post_comments(post_id):
    """Get comments for a post"""
    comments = PostComment.query.filter_by(post_id=post_id)\
                               .order_by(PostComment.created_at.asc()).all()
    return jsonify([comment.to_dict() for comment in comments])

@community_bp.route('/posts/<int:post_id>/comments', methods=['POST'])
@cross_origin()
def create_comment(post_id):
    """Create a comment on a post"""
    data = request.json
    comment = PostComment(
        post_id=post_id,
        author_id=data['author_id'],
        content=data['content'],
        parent_comment_id=data.get('parent_comment_id'),
        is_anonymous=data.get('is_anonymous', False)
    )
    db.session.add(comment)
    
    # Update post comment count
    post = CommunityPost.query.get(post_id)
    if post:
        post.comments_count += 1
    
    # Update user engagement
    engagement = UserEngagement.query.filter_by(user_id=data['author_id']).first()
    if engagement:
        engagement.comments_made += 1
        engagement.total_points += 5  # Points for commenting
    
    db.session.commit()
    
    return jsonify(comment.to_dict()), 201

@community_bp.route('/virtual-hugs', methods=['POST'])
@cross_origin()
def send_virtual_hug():
    """Send a virtual hug"""
    data = request.json
    hug = VirtualHug(
        sender_id=data.get('sender_id'),
        recipient_id=data.get('recipient_id'),
        message=data.get('message', ''),
        hug_type=data.get('hug_type', 'general')
    )
    db.session.add(hug)
    
    # Update engagement metrics
    if data.get('sender_id'):
        sender_engagement = UserEngagement.query.filter_by(user_id=data['sender_id']).first()
        if sender_engagement:
            sender_engagement.total_hugs_sent += 1
            sender_engagement.total_points += 2
    
    if data.get('recipient_id'):
        recipient_engagement = UserEngagement.query.filter_by(user_id=data['recipient_id']).first()
        if recipient_engagement:
            recipient_engagement.total_hugs_received += 1
    
    db.session.commit()
    
    return jsonify(hug.to_dict()), 201

@community_bp.route('/virtual-hugs/count', methods=['GET'])
@cross_origin()
def get_hug_count():
    """Get total virtual hugs sent on the platform"""
    total_hugs = VirtualHug.query.count()
    return jsonify({'total_hugs': total_hugs})

@community_bp.route('/users/<int:user_id>/engagement', methods=['GET'])
@cross_origin()
def get_user_engagement(user_id):
    """Get user engagement metrics"""
    engagement = UserEngagement.query.filter_by(user_id=user_id).first()
    if not engagement:
        # Create default engagement record
        engagement = UserEngagement(user_id=user_id)
        db.session.add(engagement)
        db.session.commit()
    
    return jsonify(engagement.to_dict())

@community_bp.route('/users/<int:user_id>/achievements', methods=['GET'])
@cross_origin()
def get_user_achievements(user_id):
    """Get user achievements"""
    achievements = UserAchievement.query.filter_by(user_id=user_id)\
                                       .order_by(UserAchievement.earned_at.desc()).all()
    return jsonify([achievement.to_dict() for achievement in achievements])

@community_bp.route('/achievements', methods=['POST'])
@cross_origin()
def award_achievement():
    """Award an achievement to a user"""
    data = request.json
    achievement = UserAchievement(
        user_id=data['user_id'],
        achievement_type=data['achievement_type'],
        achievement_name=data['achievement_name'],
        description=data.get('description', ''),
        badge_icon=data.get('badge_icon', ''),
        points_earned=data.get('points_earned', 0)
    )
    db.session.add(achievement)
    
    # Update user's total points
    engagement = UserEngagement.query.filter_by(user_id=data['user_id']).first()
    if engagement:
        engagement.total_points += data.get('points_earned', 0)
        # Check for level up
        new_level = (engagement.total_points // 100) + 1
        if new_level > engagement.level:
            engagement.level = new_level
    
    db.session.commit()
    
    return jsonify(achievement.to_dict()), 201

@community_bp.route('/shareable-content', methods=['POST'])
@cross_origin()
def create_shareable_content():
    """Create shareable content for viral marketing"""
    data = request.json
    content = ShareableContent(
        creator_id=data['creator_id'],
        content_type=data['content_type'],
        title=data['title'],
        description=data.get('description', ''),
        content_data=json.dumps(data.get('content_data', {}))
    )
    db.session.add(content)
    db.session.commit()
    
    return jsonify(content.to_dict()), 201

@community_bp.route('/shareable-content/<int:content_id>/share', methods=['POST'])
@cross_origin()
def track_content_share(content_id):
    """Track when content is shared"""
    content = ShareableContent.query.get_or_404(content_id)
    content.share_count += 1
    db.session.commit()
    
    return jsonify({'message': 'Share tracked', 'share_count': content.share_count})

@community_bp.route('/shareable-content/<int:content_id>/view', methods=['POST'])
@cross_origin()
def track_content_view(content_id):
    """Track when shared content is viewed"""
    content = ShareableContent.query.get_or_404(content_id)
    content.view_count += 1
    
    # Check if viewer converted (signed up)
    data = request.json
    if data.get('converted', False):
        content.conversion_count += 1
    
    db.session.commit()
    
    return jsonify({'message': 'View tracked'})

@community_bp.route('/leaderboard', methods=['GET'])
@cross_origin()
def get_leaderboard():
    """Get community leaderboard"""
    leaderboard_type = request.args.get('type', 'points')
    limit = request.args.get('limit', 10, type=int)
    
    if leaderboard_type == 'points':
        top_users = UserEngagement.query.order_by(UserEngagement.total_points.desc()).limit(limit).all()
        return jsonify([{
            'user_id': user.user_id,
            'total_points': user.total_points,
            'level': user.level
        } for user in top_users])
    
    elif leaderboard_type == 'hugs':
        top_huggers = UserEngagement.query.order_by(UserEngagement.total_hugs_sent.desc()).limit(limit).all()
        return jsonify([{
            'user_id': user.user_id,
            'total_hugs_sent': user.total_hugs_sent
        } for user in top_huggers])
    
    return jsonify({'error': 'Invalid leaderboard type'}), 400

