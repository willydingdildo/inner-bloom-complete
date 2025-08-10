from flask import Blueprint, jsonify, request
import os
import sqlite3
import logging
import requests
import json

logger = logging.getLogger(__name__)

initiation_bp = Blueprint("initiation", __name__)

# Get OpenAI API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

def save_bloom_name(user_id, bloom_name, backstory):
    """Store Bloom Name and backstory in the user's record"""
    conn = sqlite3.connect("inner_bloom.db")
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE users SET bloom_name = ?, bloom_backstory = ? WHERE id = ?",
                       (bloom_name, backstory, user_id))
        conn.commit()
        logger.info(f"Bloom name saved for user_id {user_id}")
        return True
    except Exception as e:
        logger.error(f"Error saving bloom name for user_id {user_id}: {e}")
        return False
    finally:
        conn.close()

@initiation_bp.route("/initiation", methods=["POST"])
def handle_initiation():
    """Handle initiation quiz answers, generate Bloom Name and backstory via OpenAI."""
    try:
        data = request.get_json()
        answers = data.get("answers")
        user_id = data.get("user_id") # Assuming user_id is passed from frontend after initial login/signup

        if not answers or not user_id:
            return jsonify({"error": "Answers and user_id are required"}), 400

        prompt = f"""
The user answered these initiation scenarios: {", ".join(answers)}.
Generate a single powerful and symbolic Bloom Name (3-5 words) that feels divinely appointed for a woman’s spiritual and financial awakening journey.
Also create a 2-3 sentence prophetic backstory that makes her feel chosen, using biblical undertones and emotional language. Do not mention this is an initiation.
Return as JSON: {{ "name": "...", "backstory": "..." }}
"""

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }
        payload = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.9,
            "response_format": { "type": "json_object" }
        }

        response = requests.post(OPENAI_API_URL, headers=headers, json=payload)
        response.raise_for_status() # Raise an exception for HTTP errors

        ai_result = response.json()
        bloom_name = ai_result["choices"][0]["message"]["content"]
        bloom_name = json.loads(bloom_name).get("name", "The Anointed Dawn")
        backstory = ai_result["choices"][0]["message"]["content"]
        backstory = json.loads(backstory).get("backstory", "You were called...")

        # Store the generated name and backstory in the user's record
        save_bloom_name(user_id, bloom_name, backstory)

        return jsonify({"name": bloom_name, "backstory": backstory})

    except requests.exceptions.RequestException as e:
        logger.error(f"OpenAI API request error during initiation: {e}")
        return jsonify({"error": "Failed to generate Bloom Name. Please try again later.", "details": str(e)}), 500
    except Exception as e:
        logger.error(f"Error in initiation sequence: {e}")
        return jsonify({"error": "An unexpected error occurred.", "details": str(e)}), 500


