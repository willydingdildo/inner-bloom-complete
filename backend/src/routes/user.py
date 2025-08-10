from flask import Blueprint, jsonify, request
from src.models.user import User, db
from src.models.affiliate_tracking import ReferralTracking, calculate_referral_bonus

user_bp = Blueprint("user", __name__)

@user_bp.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@user_bp.route("/users", methods=["POST"])
def create_user():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    referral_code = data.get("referral_code")
    subscription_type = data.get("subscription_type", "free") # Default to free if not provided

    if not username or not email:
        return jsonify({"error": "Username and email are required"}), 400

    # Check if user already exists
    if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
        return jsonify({"error": "User with this email or username already exists"}), 409

    referred_by_id = None
    if referral_code:
        # Find the referrer based on the referral code
        # Assuming referral codes are generated from the referrer's ID or a unique link
        # For simplicity, let's assume the referral_code directly corresponds to a referrer's user ID for now
        # In a real system, this would involve looking up the ReferralTracking table or a dedicated referral code table
        referrer_user = User.query.filter_by(referral_code_used=referral_code).first() # This needs to be refined
        if referrer_user:
            referred_by_id = referrer_user.id
        else:
            # If the referral code doesn't directly map to a user's referral_code_used, 
            # we need to search the ReferralTracking table for the referrer_id
            # This is a placeholder for more complex referral code lookup logic
            referral_entry = ReferralTracking.query.filter_by(referral_code=referral_code, level=1).first()
            if referral_entry:
                referred_by_id = referral_entry.referrer_id

    user = User(
        username=username,
        email=email,
        referred_by_id=referred_by_id,
        referral_code_used=referral_code
    )
    db.session.add(user)
    db.session.commit()

    # If referred, initiate referral tracking and bonus calculation
    if referred_by_id:
        # This is where the initial referral entry is created for the direct referrer (level 1)
        # Subsequent levels are handled within calculate_referral_bonus
        referral_entry = ReferralTracking(
            referrer_id=referred_by_id,
            referred_id=user.id,
            referral_code=referral_code, # Use the code provided by the new user
            level=1,
            subscription_type=subscription_type,
            payment_status='pending'  # Status is pending until payment is confirmed
        )
        db.session.add(referral_entry)
        db.session.commit()

        # If the referred user immediately pays for a subscription/product, trigger bonus calculation
        # This part would typically be called by a webhook from a payment gateway
        # For demo purposes, let's assume if subscription_type is not 'free', payment is confirmed
        if subscription_type != 'free':
            calculate_referral_bonus(referred_by_id, user.id, subscription_type)

    return jsonify(user.to_dict()), 201

@user_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@user_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json
    user.username = data.get("username", user.username)
    user.email = data.get("email", user.email)
    db.session.commit()
    return jsonify(user.to_dict())

@user_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return "", 204


