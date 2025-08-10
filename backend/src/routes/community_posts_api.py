"""
Inner Bloom Community Posts API Routes
"""

from flask import Blueprint, request, jsonify
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.models.community_posts import community_db

community_posts_bp = Blueprint("community_posts", __name__)

@community_posts_bp.route("/posts", methods=["GET"])
def get_posts():
    """Get community posts"""
    try:
        limit = request.args.get("limit", 20, type=int)
        offset = request.args.get("offset", 0, type=int)
        
        posts = community_db.get_posts(limit, offset)
        
        return jsonify({
            "success": True,
            "posts": posts,
            "total": len(posts)
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@community_posts_bp.route("/posts", methods=["POST"])
def create_post():
    """Create a new community post"""
    try:
        data = request.get_json()
        
        if "user_id" not in data or "content" not in data:
            return jsonify({"error": "Missing user_id or content"}), 400
        
        post_id = community_db.create_post(
            user_id=data["user_id"],
            content=data["content"],
            image_url=data.get("image_url")
        )
        
        return jsonify({
            "success": True,
            "post_id": post_id,
            "message": "Post created successfully"
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@community_posts_bp.route("/posts/<post_id>/like", methods=["POST"])
def like_post(post_id):
    """Like or unlike a post"""
    try:
        data = request.get_json()
        
        if "user_id" not in data:
            return jsonify({"error": "Missing user_id"}), 400
        
        result = community_db.like_post(post_id, data["user_id"])
        
        return jsonify({
            "success": True,
            "liked": result["liked"],
            "like_count": result["like_count"]
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@community_posts_bp.route("/posts/<post_id>/comments", methods=["GET"])
def get_post_comments(post_id):
    """Get comments for a specific post"""
    try:
        comments = community_db.get_post_comments(post_id)
        
        return jsonify({
            "success": True,
            "comments": comments,
            "total": len(comments)
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@community_posts_bp.route("/posts/<post_id>/comments", methods=["POST"])
def add_comment(post_id):
    """Add a comment to a post"""
    try:
        data = request.get_json()
        
        if "user_id" not in data or "content" not in data:
            return jsonify({"error": "Missing user_id or content"}), 400
        
        comment_id = community_db.add_comment(
            post_id=post_id,
            user_id=data["user_id"],
            content=data["content"]
        )
        
        return jsonify({
            "success": True,
            "comment_id": comment_id,
            "message": "Comment added successfully"
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@community_posts_bp.route("/stats", methods=["GET"])
def get_community_stats():
    """Get community statistics"""
    try:
        stats = community_db.get_community_stats()
        
        return jsonify({
            "success": True,
            "stats": stats
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

