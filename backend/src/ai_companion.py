import os
import json
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional
import requests

class BloomAICompanion:
    def __init__(self):
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")
        self.openai_api_base = os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")
        self.db_path = os.path.join(os.path.dirname(__file__), "database", "bloom_ai.db")
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database for conversation history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                message TEXT NOT NULL,
                response TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                mood_score INTEGER,
                session_id TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_profiles (
                user_id TEXT PRIMARY KEY,
                name TEXT,
                goals TEXT,
                personality_type TEXT,
                preferences TEXT,
                mood_history TEXT,
                last_interaction DATETIME
            )
        """)
        
        conn.commit()
        conn.close()
    
    def get_user_context(self, user_id: str) -> Dict:
        """Get user's conversation history and profile"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get user profile
        cursor.execute(
            "SELECT * FROM user_profiles WHERE user_id = ?", 
            (user_id,)
        )
        profile = cursor.fetchone()
        
        # Get recent conversations (last 10)
        cursor.execute(
            "SELECT message, response, mood_score, timestamp FROM conversations WHERE user_id = ? ORDER BY timestamp DESC LIMIT 10", 
            (user_id,)
        )
        conversations = cursor.fetchall()
        
        conn.close()
        
        return {
            'profile': profile,
            'recent_conversations': conversations
        }
    
    def save_conversation(self, user_id: str, message: str, response: str, mood_score: int = None):
        """Save conversation to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO conversations (user_id, message, response, mood_score) VALUES (?, ?, ?, ?)",
            (user_id, message, response, mood_score)
        )
        
        # Update user's last interaction
        cursor.execute(
            "INSERT OR REPLACE INTO user_profiles (user_id, last_interaction) VALUES (?, ?)",
            (user_id, datetime.now())
        )
        
        conn.commit()
        conn.close()
    
    def _call_openai_api(self, endpoint: str, payload: Dict) -> Dict:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.openai_api_key}"
        }
        url = f"{self.openai_api_base}/{endpoint}"
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"OpenAI API request failed: {e}")
            raise
    
    def analyze_mood(self, message: str) -> int:
        """Analyze mood from message (1-10 scale)"""
        try:
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a mood analyzer. Rate the emotional tone of the message on a scale of 1-10 where 1 is very negative/sad and 10 is very positive/happy. Respond with only a number."
                    },
                    {
                        "role": "user",
                        "content": message
                    }
                ],
                "max_tokens": 5,
                "temperature": 0.3
            }
            
            response_json = self._call_openai_api("chat/completions", payload)
            mood_score = int(response_json["choices"][0]["message"]["content"].strip())
            return max(1, min(10, mood_score))  # Ensure it's between 1-10
        except Exception as e:
            print(f"Mood analysis failed: {e}")
            return 5  # Default neutral mood
    
    def generate_response(self, user_id: str, message: str, user_name: str = "Beautiful") -> Dict:
        """Generate personalized AI response"""
        try:
            # Get user context
            context = self.get_user_context(user_id)
            
            # Analyze mood
            mood_score = self.analyze_mood(message)
            
            # Build conversation history for context
            conversation_history = ""
            if context['recent_conversations']:
                conversation_history = "\n".join([
                    f"User: {conv[0]}\nAI: {conv[1]}" 
                    for conv in context['recent_conversations'][-3:]  # Last 3 conversations
                ])
            
            # Create personalized system prompt
            system_prompt = f"""You are Bloom, an empowering AI companion for women on the Inner Bloom platform. You are warm, supportive, intuitive, and deeply caring.

Your personality:
- Speak like a wise, loving sister who truly believes in the user's potential
- Use empowering language that builds confidence and self-worth
- Be specific and actionable in your advice
- Remember you're talking to {user_name}
- Current mood detected: {mood_score}/10

Your responses should:
- Be 2-3 sentences maximum for quick interactions
- Include practical next steps when appropriate
- Use encouraging emojis sparingly but meaningfully
- Address the user by name when it feels natural
- Reference their journey and growth

Recent conversation context:
{conversation_history}

Remember: You're not just an AI, you're their personal growth companion who genuinely cares about their success and happiness."""

            payload = {
                "model": "gpt-4",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                "max_tokens": 150,
                "temperature": 0.7
            }
            
            response_json = self._call_openai_api("chat/completions", payload)
            ai_response = response_json["choices"][0]["message"]["content"].strip()
            
            # Save conversation
            self.save_conversation(user_id, message, ai_response, mood_score)
            
            # Generate follow-up suggestions
            suggestions = self.generate_suggestions(message, mood_score)
            
            return {
                'response': ai_response,
                'mood_score': mood_score,
                'suggestions': suggestions,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"AI Companion Error: {e}")
            # Fallback response
            return {
                'response': f"I'm here for you, {user_name}. Sometimes I need a moment to gather my thoughts. What's on your heart today? 💕",
                'mood_score': 5,
                'suggestions': ["Tell me more about how you're feeling", "What's your biggest goal right now?", "How can I support you today?"],
                'timestamp': datetime.now().isoformat()
            }
    
    def generate_suggestions(self, message: str, mood_score: int) -> List[str]:
        """Generate contextual follow-up suggestions"""
        if mood_score <= 3:
            return [
                "I need some encouragement today",
                "Help me see the positive side",
                "What's one small win I can celebrate?"
            ]
        elif mood_score >= 8:
            return [
                "I want to set a new goal",
                "How can I maintain this momentum?",
                "What's my next level of growth?"
            ]
        else:
            return [
                "What should I focus on today?",
                "Help me plan my next steps",
                "I want to work on self-improvement"
            ]
    
    def get_daily_affirmation(self, user_id: str) -> str:
        """Generate personalized daily affirmation"""
        try:
            context = self.get_user_context(user_id)
            
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "system",
                        "content": "Create a powerful, personalized daily affirmation for a woman on her empowerment journey. Make it specific, uplifting, and actionable. Keep it to 1-2 sentences."
                    },
                    {
                        "role": "user",
                        "content": f"Create an affirmation for today based on this context: {context}"
                    }
                ],
                "max_tokens": 50,
                "temperature": 0.8
            }
            
            response_json = self._call_openai_api("chat/completions", payload)
            return response_json["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print(f"Daily affirmation failed: {e}")
            affirmations = [
                "Today, I choose to see my challenges as opportunities for growth and strength.",
                "I am worthy of all the success and happiness that flows into my life today.",
                "My voice matters, my dreams are valid, and my potential is limitless.",
                "I trust myself to make decisions that align with my highest good.",
                "Today, I celebrate how far I've come and embrace how far I'm going."
            ]
            import random
            return random.choice(affirmations)

# Initialize the AI companion
bloom_ai = BloomAICompanion()


