from flask import Blueprint, request, jsonify, send_file
import os
import sys
import json
from datetime import datetime
import io

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import our real functionality
from src.ai_companion import bloom_ai
from src.real_database import real_db
# from src.pdf_generator import PDFGenerator # Temporarily commented out

real_api_bp = Blueprint("real_api", __name__)

# pdf_generator = PDFGenerator() # Temporarily commented out

# Health check endpoint
@real_api_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "message": "Inner Bloom Real API is running"
    })

# Real AI Companion endpoint
@real_api_bp.route("/ai/chat", methods=["POST"])
def ai_chat():
    try:
        data = request.get_json()
        user_id = data.get("user_id", "demo_user")
        message = data.get("message", "")
        user_name = data.get("user_name", "Beautiful")
        
        if not message:
            return jsonify({"error": "Message is required"}), 400
        
        # Generate real AI response
        response = bloom_ai.generate_response(user_id, message, user_name)
        
        # Add points for AI interaction
        real_db.add_points(user_id, 5, "ai_chat", "Chatted with Bloom AI")
        
        return jsonify(response)
    
    except Exception as e:
        print(f"AI Chat Error: {e}")
        return jsonify({"error": str(e)}), 500

# Daily affirmation endpoint
@real_api_bp.route("/ai/affirmation", methods=["GET"])
def daily_affirmation():
    try:
        user_id = request.args.get("user_id", "demo_user")
        affirmation = bloom_ai.get_daily_affirmation(user_id)
        
        return jsonify({
            "affirmation": affirmation,
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        print(f"Affirmation Error: {e}")
        return jsonify({"error": str(e)}), 500

# Real user data endpoint
@real_api_bp.route("/user/<user_id>", methods=["GET"])
def get_user(user_id):
    try:
        user = real_db.get_user(user_id)
        if not user:
            # Create demo user if doesn't exist
            user_id = real_db.create_user("demo@innerbloom.com", "Demo User")
            user = real_db.get_user(user_id)
        
        return jsonify(user)
    
    except Exception as e:
        print(f"Get User Error: {e}")
        return jsonify({"error": str(e)}), 500

# Real platform statistics
@real_api_bp.route("/stats", methods=["GET"])
def platform_stats():
    try:
        stats = real_db.get_platform_stats()
        return jsonify(stats)
    
    except Exception as e:
        print(f"Stats Error: {e}")
        return jsonify({"error": str(e)}), 500

# Add points endpoint
@real_api_bp.route("/user/<user_id>/points", methods=["POST"])
def add_points(user_id):
    try:
        data = request.get_json()
        points = data.get("points", 0)
        activity = data.get("activity", "unknown")
        description = data.get("description", "Points earned")
        
        real_db.add_points(user_id, points, activity, description)
        
        return jsonify({"success": True, "points_added": points})
    
    except Exception as e:
        print(f"Add Points Error: {e}")
        return jsonify({"error": str(e)}), 500

# Leaderboard endpoint
@real_api_bp.route("/leaderboard", methods=["GET"])
def leaderboard():
    try:
        limit = request.args.get("limit", 10, type=int)
        leaders = real_db.get_leaderboard(limit)
        return jsonify(leaders)
    
    except Exception as e:
        print(f"Leaderboard Error: {e}")
        return jsonify({"error": str(e)}), 500

# PDF Download endpoints (Temporarily commented out)
# @real_api_bp.route("/download/parenting-guide", methods=["POST"])
# def download_parenting_guide():
#     try:
#         data = request.get_json()
#         user_email = data.get("user_email", "demo@innerbloom.com")
#         user_name = data.get("user_name", "Demo User")
#         user_id = data.get("user_id", "demo_user")
        
#         # Generate PDF
#         pdf_bytes = pdf_generator.generate_parenting_guide(user_email, user_name)
        
#         # Log download
#         real_db.add_points(user_id, 20, "pdf_download", "Downloaded Divine Motherhood Blueprint")
        
#         # Return PDF
#         return send_file(
#             io.BytesIO(pdf_bytes),
#             mimetype="application/pdf",
#             as_attachment=True,
#             download_name=f"Divine_Motherhood_Blueprint_{user_name.replace(" ", "_")}.pdf"
#         )
    
#     except Exception as e:
#         print(f"PDF Download Error: {e}")
#         return jsonify({"error": str(e)}), 500

# @real_api_bp.route("/download/empowerment-guide", methods=["POST"])
# def download_empowerment_guide():
#     try:
#         data = request.get_json()
#         user_email = data.get("user_email", "demo@innerbloom.com")
#         user_name = data.get("user_name", "Demo User")
#         user_id = data.get("user_id", "demo_user")
        
#         # Generate PDF
#         pdf_bytes = pdf_generator.generate_empowerment_guide(user_email, user_name)
        
#         # Log download
#         real_db.add_points(user_id, 15, "pdf_download", "Downloaded Empowerment Guide")
        
#         return send_file(
#             io.BytesIO(pdf_bytes),
#             mimetype="application/pdf",
#             as_attachment=True,
#             download_name=f"Inner_Bloom_Empowerment_Guide_{user_name.replace(" ", "_")}.pdf"
#         )
    
#     except Exception as e:
#         print(f"PDF Download Error: {e}")
#         return jsonify({"error": str(e)}), 500

# @real_api_bp.route("/download/business-guide", methods=["POST"])
# def download_business_guide():
#     try:
#         data = request.get_json()
#         user_email = data.get("user_email", "demo@innerbloom.com")
#         user_name = data.get("user_name", "Demo User")
#         user_id = data.get("user_id", "demo_user")
        
#         # Generate PDF
#         pdf_bytes = pdf_generator.generate_business_guide(user_email, user_name)
        
#         # Log download
#         real_db.add_points(user_id, 25, "pdf_download", "Downloaded She-EO Success Blueprint")
        
#         return send_file(
#             io.BytesIO(pdf_bytes),
#             mimetype="application/pdf",
#             as_attachment=True,
#             download_name=f"She_EO_Success_Blueprint_{user_name.replace(" ", "_")}.pdf"
#         )
    
#     except Exception as e:
#         print(f"PDF Download Error: {e}")
#         return jsonify({"error": str(e)}), 500

# Community post endpoint
@real_api_bp.route("/community/post", methods=["POST"])
def create_community_post():
    try:
        data = request.get_json()
        user_id = data.get("user_id", "demo_user")
        content = data.get("content", "")
        
        if not content:
            return jsonify({"error": "Content is required"}), 400
        
        # Add to database (simplified for demo)
        real_db.add_points(user_id, 15, "community_post", "Posted in community")
        
        return jsonify({
            "success": True,
            "message": "Post created successfully",
            "points_earned": 15
        })
    
    except Exception as e:
        print(f"Community Post Error: {e}")
        return jsonify({"error": str(e)}), 500


