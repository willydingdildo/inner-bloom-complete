"""
Inner Bloom Marketplace API Routes
"""

from flask import Blueprint, request, jsonify
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.models.marketplace import marketplace_db

marketplace_bp = Blueprint("marketplace", __name__)

@marketplace_bp.route("/products", methods=["GET"])
def get_products():
    """Get all products or filter by category"""
    try:
        category = request.args.get("category")
        limit = request.args.get("limit", 20, type=int)
        offset = request.args.get("offset", 0, type=int)
        
        products = marketplace_db.get_products(category, limit, offset)
        
        return jsonify({
            "success": True,
            "products": products,
            "total": len(products)
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@marketplace_bp.route("/products", methods=["POST"])
def create_product():
    """Create a new product listing"""
    try:
        data = request.get_json()
        
        required_fields = ["seller_id", "title", "description", "price", "category"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        product_id = marketplace_db.create_product(
            seller_id=data["seller_id"],
            title=data["title"],
            description=data["description"],
            price=float(data["price"]),
            category=data["category"],
            image_url=data.get("image_url")
        )
        
        return jsonify({
            "success": True,
            "product_id": product_id,
            "message": "Product created successfully"
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@marketplace_bp.route("/user/<user_id>/products", methods=["GET"])
def get_user_products(user_id):
    """Get all products for a specific user"""
    try:
        products = marketplace_db.get_user_products(user_id)
        
        return jsonify({
            "success": True,
            "products": products,
            "total": len(products)
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@marketplace_bp.route("/purchase", methods=["POST"])
def purchase_product():
    """Purchase a product"""
    try:
        data = request.get_json()
        
        if "product_id" not in data or "buyer_id" not in data:
            return jsonify({"error": "Missing product_id or buyer_id"}), 400
        
        result = marketplace_db.purchase_product(
            product_id=data["product_id"],
            buyer_id=data["buyer_id"]
        )
        
        if result:
            return jsonify({
                "success": True,
                "sale": result,
                "message": "Purchase completed successfully"
            })
        else:
            return jsonify({"error": "Product not available"}), 404
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@marketplace_bp.route("/stats", methods=["GET"])
def get_marketplace_stats():
    """Get marketplace statistics"""
    try:
        stats = marketplace_db.get_sales_stats()
        
        return jsonify({
            "success": True,
            "stats": stats
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@marketplace_bp.route("/user/<user_id>/stats", methods=["GET"])
def get_user_sales_stats(user_id):
    """Get sales statistics for a specific user"""
    try:
        stats = marketplace_db.get_sales_stats(user_id)
        
        return jsonify({
            "success": True,
            "stats": stats
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@marketplace_bp.route("/categories", methods=["GET"])
def get_categories():
    """Get available product categories"""
    categories = [
        "Digital Products",
        "Planners",
        "Business Tools",
        "Courses",
        "Templates",
        "Coaching",
        "Ebooks",
        "Printables",
        "Software",
        "Services"
    ]
    
    return jsonify({
        "success": True,
        "categories": categories
    })

