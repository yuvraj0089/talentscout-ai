"""
Advanced Sentiment Analysis Module for TalentScout
Analyzes candidate emotions and provides insights during conversations
"""

import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
import streamlit as st

@dataclass
class SentimentResult:
    """Data class for sentiment analysis results."""
    polarity: float  # -1 (negative) to 1 (positive)
    subjectivity: float  # 0 (objective) to 1 (subjective)
    emotion: str  # Primary emotion detected
    confidence: float  # Confidence score
    keywords: List[str]  # Key emotional indicators
    timestamp: datetime

class AdvancedSentimentAnalyzer:
    """Advanced sentiment analyzer with multiple detection methods."""
    
    def __init__(self):
        self.emotion_keywords = {
            'excited': ['excited', 'thrilled', 'amazing', 'fantastic', 'love', 'passionate', 'enthusiastic'],
            'confident': ['confident', 'sure', 'certain', 'definitely', 'absolutely', 'skilled', 'experienced'],
            'nervous': ['nervous', 'worried', 'anxious', 'unsure', 'maybe', 'think so', 'hope'],
            'frustrated': ['frustrated', 'difficult', 'hard', 'struggle', 'challenging', 'annoying'],
            'positive': ['good', 'great', 'excellent', 'wonderful', 'perfect', 'happy', 'pleased'],
            'negative': ['bad', 'terrible', 'awful', 'hate', 'dislike', 'disappointed', 'sad'],
            'neutral': ['okay', 'fine', 'alright', 'normal', 'average', 'standard']
        }
        
        self.intensity_modifiers = {
            'very': 1.5, 'extremely': 2.0, 'really': 1.3, 'quite': 1.2,
            'somewhat': 0.8, 'slightly': 0.6, 'a bit': 0.7, 'not very': 0.4
        }
        
    def analyze_text_basic(self, text: str) -> SentimentResult:
        """Basic sentiment analysis using keyword matching."""
        if not text or len(text.strip()) < 3:
            return SentimentResult(0.0, 0.0, 'neutral', 0.5, [], datetime.now())
        
        text_lower = text.lower()
        detected_emotions = {}
        found_keywords = []
        
        # Analyze emotions based on keywords
        for emotion, keywords in self.emotion_keywords.items():
            score = 0
            emotion_keywords = []
            
            for keyword in keywords:
                if keyword in text_lower:
                    # Check for intensity modifiers
                    intensity = 1.0
                    for modifier, multiplier in self.intensity_modifiers.items():
                        if modifier in text_lower and keyword in text_lower:
                            intensity = multiplier
                            break
                    
                    score += intensity
                    emotion_keywords.append(keyword)
            
            if score > 0:
                detected_emotions[emotion] = score
                found_keywords.extend(emotion_keywords)
        
        # Determine primary emotion
        if detected_emotions:
            primary_emotion = max(detected_emotions, key=detected_emotions.get)
            confidence = min(detected_emotions[primary_emotion] / 3.0, 1.0)
        else:
            primary_emotion = 'neutral'
            confidence = 0.5
        
        # Calculate polarity (-1 to 1)
        positive_emotions = ['excited', 'confident', 'positive']
        negative_emotions = ['nervous', 'frustrated', 'negative']
        
        polarity = 0.0
        for emotion, score in detected_emotions.items():
            if emotion in positive_emotions:
                polarity += score * 0.3
            elif emotion in negative_emotions:
                polarity -= score * 0.3
        
        polarity = max(-1.0, min(1.0, polarity))
        
        # Calculate subjectivity (0 to 1)
        subjective_indicators = ['feel', 'think', 'believe', 'opinion', 'personally']
        subjectivity = sum(1 for indicator in subjective_indicators if indicator in text_lower) * 0.2
        subjectivity = min(1.0, subjectivity + 0.3)  # Base subjectivity
        
        return SentimentResult(
            polarity=polarity,
            subjectivity=subjectivity,
            emotion=primary_emotion,
            confidence=confidence,
            keywords=found_keywords,
            timestamp=datetime.now()
        )
    
    def analyze_with_textblob(self, text: str) -> Optional[SentimentResult]:
        """Enhanced sentiment analysis using TextBlob (if available)."""
        try:
            from textblob import TextBlob
            
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            # Map polarity to emotion
            if polarity > 0.3:
                emotion = 'positive'
            elif polarity < -0.3:
                emotion = 'negative'
            elif polarity > 0.1:
                emotion = 'confident'
            elif polarity < -0.1:
                emotion = 'nervous'
            else:
                emotion = 'neutral'
            
            confidence = abs(polarity) + 0.3
            
            return SentimentResult(
                polarity=polarity,
                subjectivity=subjectivity,
                emotion=emotion,
                confidence=min(confidence, 1.0),
                keywords=[],
                timestamp=datetime.now()
            )
            
        except ImportError:
            return None
    
    def analyze_sentiment(self, text: str) -> SentimentResult:
        """Main sentiment analysis method with fallback."""
        # Try advanced analysis first
        advanced_result = self.analyze_with_textblob(text)
        if advanced_result:
            return advanced_result
        
        # Fallback to basic analysis
        return self.analyze_text_basic(text)
    
    def get_emotion_emoji(self, emotion: str) -> str:
        """Get emoji representation of emotion."""
        emoji_map = {
            'excited': '🤩',
            'confident': '😊',
            'nervous': '😰',
            'frustrated': '😤',
            'positive': '😄',
            'negative': '😞',
            'neutral': '😐'
        }
        return emoji_map.get(emotion, '😐')
    
    def get_encouragement_message(self, sentiment: SentimentResult) -> str:
        """Generate encouraging response based on sentiment."""
        if sentiment.emotion == 'nervous':
            return "I can sense you might be a bit nervous - that's completely normal! Take your time, and remember there are no wrong answers here."
        elif sentiment.emotion == 'frustrated':
            return "I notice this might be challenging. Let's take it step by step, and feel free to ask if you need clarification on anything."
        elif sentiment.emotion == 'excited':
            return "I love your enthusiasm! Your excitement really comes through in your responses."
        elif sentiment.emotion == 'confident':
            return "Great confidence in your responses! It's clear you have strong knowledge in this area."
        elif sentiment.polarity > 0.2:
            return "Your positive attitude is wonderful to see!"
        else:
            return "Thank you for your thoughtful response."
    
    def analyze_conversation_trend(self, sentiments: List[SentimentResult]) -> Dict:
        """Analyze sentiment trends throughout the conversation."""
        if not sentiments:
            return {'trend': 'neutral', 'average_polarity': 0.0, 'stability': 1.0}
        
        polarities = [s.polarity for s in sentiments]
        emotions = [s.emotion for s in sentiments]
        
        # Calculate trend
        if len(polarities) > 1:
            trend_slope = (polarities[-1] - polarities[0]) / len(polarities)
            if trend_slope > 0.1:
                trend = 'improving'
            elif trend_slope < -0.1:
                trend = 'declining'
            else:
                trend = 'stable'
        else:
            trend = 'neutral'
        
        # Calculate stability (variance)
        avg_polarity = sum(polarities) / len(polarities)
        variance = sum((p - avg_polarity) ** 2 for p in polarities) / len(polarities)
        stability = max(0.0, 1.0 - variance)
        
        # Most common emotion
        emotion_counts = {}
        for emotion in emotions:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        dominant_emotion = max(emotion_counts, key=emotion_counts.get) if emotion_counts else 'neutral'
        
        return {
            'trend': trend,
            'average_polarity': avg_polarity,
            'stability': stability,
            'dominant_emotion': dominant_emotion,
            'emotion_distribution': emotion_counts
        }

# Global instance
sentiment_analyzer = AdvancedSentimentAnalyzer()
