"""
Personalization Module for TalentScout
Manages user preferences, history, and personalized responses
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import hashlib
import streamlit as st

@dataclass
class UserPreferences:
    """User preferences data structure."""
    language: str = 'en'
    communication_style: str = 'professional'  # casual, professional, formal
    question_difficulty: str = 'adaptive'  # easy, medium, hard, adaptive
    response_length: str = 'medium'  # short, medium, detailed
    preferred_topics: List[str] = None
    accessibility_needs: List[str] = None
    timezone: str = 'UTC'
    
    def __post_init__(self):
        if self.preferred_topics is None:
            self.preferred_topics = []
        if self.accessibility_needs is None:
            self.accessibility_needs = []

@dataclass
class ConversationHistory:
    """Conversation history data structure."""
    session_id: str
    user_id: str
    timestamp: datetime
    messages: List[Dict[str, Any]]
    sentiment_scores: List[float]
    completion_rate: float
    tech_stack: List[str]
    performance_metrics: Dict[str, Any]

class PersonalizationManager:
    """Manages user personalization and history."""
    
    def __init__(self):
        self.data_dir = "user_data"
        self.preferences_file = "user_preferences.json"
        self.history_file = "conversation_history.json"
        self.ensure_data_directory()
        
        # Communication styles
        self.communication_styles = {
            'casual': {
                'greeting': "Hey there! 👋",
                'encouragement': "You're doing great!",
                'transition': "Alright, let's move on to",
                'closing': "Thanks a bunch! Talk soon! 😊"
            },
            'professional': {
                'greeting': "Good day! 👋",
                'encouragement': "Excellent response!",
                'transition': "Now, let's proceed to",
                'closing': "Thank you for your time. We'll be in touch soon."
            },
            'formal': {
                'greeting': "Good day, and welcome to TalentScout.",
                'encouragement': "Your response demonstrates strong competency.",
                'transition': "We shall now proceed to",
                'closing': "We appreciate your participation in this assessment."
            }
        }
        
        # Question difficulty mappings
        self.difficulty_modifiers = {
            'easy': {
                'prompt_addition': "Please provide beginner-friendly questions that focus on basic concepts.",
                'complexity_level': 1
            },
            'medium': {
                'prompt_addition': "Please provide intermediate-level questions that test practical knowledge.",
                'complexity_level': 2
            },
            'hard': {
                'prompt_addition': "Please provide advanced questions that test deep understanding and complex scenarios.",
                'complexity_level': 3
            },
            'adaptive': {
                'prompt_addition': "Please provide questions that adapt to the candidate's experience level.",
                'complexity_level': 2
            }
        }
    
    def ensure_data_directory(self):
        """Create data directory if it doesn't exist."""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def generate_user_id(self, email: str) -> str:
        """Generate anonymous user ID from email."""
        return hashlib.sha256(email.encode()).hexdigest()[:16]
    
    def save_user_preferences(self, user_id: str, preferences: UserPreferences):
        """Save user preferences to file."""
        try:
            prefs_path = os.path.join(self.data_dir, f"{user_id}_preferences.json")
            with open(prefs_path, 'w') as f:
                json.dump(asdict(preferences), f, indent=2)
        except Exception as e:
            st.error(f"Error saving preferences: {e}")
    
    def load_user_preferences(self, user_id: str) -> UserPreferences:
        """Load user preferences from file."""
        try:
            prefs_path = os.path.join(self.data_dir, f"{user_id}_preferences.json")
            if os.path.exists(prefs_path):
                with open(prefs_path, 'r') as f:
                    data = json.load(f)
                return UserPreferences(**data)
        except Exception as e:
            st.warning(f"Could not load preferences: {e}")
        
        return UserPreferences()  # Return default preferences
    
    def save_conversation_history(self, history: ConversationHistory):
        """Save conversation history."""
        try:
            history_path = os.path.join(self.data_dir, f"{history.user_id}_history.json")
            
            # Load existing history
            existing_history = []
            if os.path.exists(history_path):
                with open(history_path, 'r') as f:
                    existing_history = json.load(f)
            
            # Add new conversation
            history_dict = asdict(history)
            history_dict['timestamp'] = history.timestamp.isoformat()
            existing_history.append(history_dict)
            
            # Keep only last 10 conversations
            existing_history = existing_history[-10:]
            
            with open(history_path, 'w') as f:
                json.dump(existing_history, f, indent=2, default=str)
                
        except Exception as e:
            st.error(f"Error saving conversation history: {e}")
    
    def load_conversation_history(self, user_id: str) -> List[ConversationHistory]:
        """Load conversation history for user."""
        try:
            history_path = os.path.join(self.data_dir, f"{user_id}_history.json")
            if os.path.exists(history_path):
                with open(history_path, 'r') as f:
                    data = json.load(f)
                
                histories = []
                for item in data:
                    item['timestamp'] = datetime.fromisoformat(item['timestamp'])
                    histories.append(ConversationHistory(**item))
                
                return histories
        except Exception as e:
            st.warning(f"Could not load conversation history: {e}")
        
        return []
    
    def get_personalized_greeting(self, preferences: UserPreferences, user_name: str = "") -> str:
        """Generate personalized greeting based on preferences."""
        style = self.communication_styles.get(preferences.communication_style, self.communication_styles['professional'])
        base_greeting = style['greeting']
        
        if user_name:
            if preferences.communication_style == 'casual':
                return f"{base_greeting} {user_name}! Ready to dive in?"
            elif preferences.communication_style == 'formal':
                return f"{base_greeting} {user_name}. We are pleased to begin this assessment."
            else:
                return f"{base_greeting} {user_name}! Let's get started with your application."
        
        return base_greeting
    
    def get_personalized_encouragement(self, preferences: UserPreferences, sentiment_score: float = 0.0) -> str:
        """Generate personalized encouragement based on preferences and sentiment."""
        style = self.communication_styles.get(preferences.communication_style, self.communication_styles['professional'])
        base_encouragement = style['encouragement']
        
        # Adjust based on sentiment
        if sentiment_score < -0.3:  # Negative sentiment
            if preferences.communication_style == 'casual':
                return "No worries at all! You're doing fine. 😊"
            elif preferences.communication_style == 'formal':
                return "Please proceed with confidence. Your responses are valued."
            else:
                return "That's perfectly fine. Take your time with your response."
        elif sentiment_score > 0.3:  # Positive sentiment
            return base_encouragement
        else:
            return "Thank you for your response."
    
    def adapt_question_difficulty(self, preferences: UserPreferences, experience_years: float, previous_performance: float = 0.5) -> str:
        """Adapt question difficulty based on user profile."""
        if preferences.question_difficulty == 'adaptive':
            if experience_years < 2:
                difficulty = 'easy'
            elif experience_years < 5:
                difficulty = 'medium'
            else:
                difficulty = 'hard'
            
            # Adjust based on previous performance
            if previous_performance < 0.3:
                difficulty = 'easy'
            elif previous_performance > 0.8:
                difficulty = 'hard'
        else:
            difficulty = preferences.question_difficulty
        
        return self.difficulty_modifiers.get(difficulty, self.difficulty_modifiers['medium'])['prompt_addition']
    
    def get_response_length_modifier(self, preferences: UserPreferences) -> str:
        """Get response length modifier for prompts."""
        length_modifiers = {
            'short': "Keep responses concise and to the point.",
            'medium': "Provide clear and comprehensive responses.",
            'detailed': "Provide detailed explanations and examples where helpful."
        }
        return length_modifiers.get(preferences.response_length, length_modifiers['medium'])
    
    def analyze_user_patterns(self, user_id: str) -> Dict[str, Any]:
        """Analyze user patterns from conversation history."""
        history = self.load_conversation_history(user_id)
        
        if not history:
            return {'pattern': 'new_user', 'recommendations': []}
        
        # Analyze patterns
        avg_completion_rate = sum(h.completion_rate for h in history) / len(history)
        common_tech_stacks = []
        avg_sentiment = 0.0
        
        for h in history:
            common_tech_stacks.extend(h.tech_stack)
            if h.sentiment_scores:
                avg_sentiment += sum(h.sentiment_scores) / len(h.sentiment_scores)
        
        avg_sentiment = avg_sentiment / len(history) if history else 0.0
        
        # Generate recommendations
        recommendations = []
        if avg_completion_rate < 0.5:
            recommendations.append("Consider shorter sessions or easier questions")
        if avg_sentiment < -0.2:
            recommendations.append("Provide more encouragement and support")
        if len(set(common_tech_stacks)) > 10:
            recommendations.append("User has diverse technical background")
        
        return {
            'pattern': 'returning_user',
            'avg_completion_rate': avg_completion_rate,
            'avg_sentiment': avg_sentiment,
            'common_technologies': list(set(common_tech_stacks)),
            'recommendations': recommendations,
            'total_sessions': len(history)
        }
    
    def create_preferences_ui(self) -> UserPreferences:
        """Create UI for setting user preferences."""
        st.sidebar.subheader("🎯 Personalization Settings")
        
        # Communication style
        comm_style = st.sidebar.selectbox(
            "Communication Style",
            options=['casual', 'professional', 'formal'],
            index=1,
            help="Choose how you'd like me to communicate with you"
        )
        
        # Question difficulty
        difficulty = st.sidebar.selectbox(
            "Question Difficulty",
            options=['easy', 'medium', 'hard', 'adaptive'],
            index=3,
            help="Adaptive adjusts based on your experience"
        )
        
        # Response length
        response_length = st.sidebar.selectbox(
            "Response Detail Level",
            options=['short', 'medium', 'detailed'],
            index=1,
            help="How detailed should my responses be?"
        )
        
        # Accessibility options
        accessibility = st.sidebar.multiselect(
            "Accessibility Needs",
            options=['large_text', 'high_contrast', 'screen_reader', 'simple_language'],
            help="Select any accessibility features you need"
        )
        
        return UserPreferences(
            communication_style=comm_style,
            question_difficulty=difficulty,
            response_length=response_length,
            accessibility_needs=accessibility
        )

# Global instance
personalization_manager = PersonalizationManager()
