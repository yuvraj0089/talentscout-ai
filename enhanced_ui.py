"""
Enhanced UI Module for TalentScout
Provides advanced styling, animations, and interactive elements
"""

import streamlit as st
import plotly.graph_objects as go
from typing import Dict, List
from datetime import datetime

class EnhancedUI:
    """Enhanced UI components and styling for TalentScout."""
    
    def __init__(self):
        self.primary_color = "#4CAF50"
        self.secondary_color = "#2196F3"
        self.accent_color = "#FF9800"
        self.success_color = "#4CAF50"
        self.warning_color = "#FF9800"
        self.error_color = "#F44336"
        self.background_color = "#FAFAFA"
        
    def inject_custom_css(self):
        """Inject comprehensive custom CSS for enhanced styling."""
        css = f"""
        <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Global Styles */
        .stApp {{
            font-family: 'Inter', sans-serif;
            background: white;
            min-height: 100vh;
        }}
        
        /* Main Container */
        .main-container {{
            background: white;
            border-radius: 20px;
            padding: 2rem;
            margin: 1rem;
            box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        }}
        
        /* Header Styling */
        .app-header {{
            text-align: center;
            padding: 3rem 2rem;
            background: linear-gradient(135deg, {self.primary_color}, #45a049);
            border-radius: 20px;
            color: white;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(76, 175, 80, 0.3);
            position: relative;
            overflow: hidden;
        }}

        .app-header::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: shimmer 3s ease-in-out infinite;
        }}
        
        .app-title {{
            font-size: 2.5rem;
            font-weight: 700;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .app-subtitle {{
            font-size: 1.2rem;
            font-weight: 300;
            margin: 0.5rem 0 0 0;
            opacity: 0.9;
        }}
        
        /* Enhanced Chat Messages */
        .chat-message {{
            padding: 1.5rem;
            border-radius: 20px;
            margin: 1rem 0;
            animation: slideIn 0.4s ease-out;
            box-shadow: 0 8px 25px rgba(0,0,0,0.08);
            position: relative;
            transition: all 0.3s ease;
        }}

        .chat-message:hover {{
            transform: translateY(-2px);
            box-shadow: 0 12px 35px rgba(0,0,0,0.12);
        }}

        .user-message {{
            background: linear-gradient(135deg, {self.secondary_color}, #1976D2);
            color: white;
            margin-left: 3rem;
            border-bottom-right-radius: 8px;
            position: relative;
        }}

        .user-message::before {{
            content: '👤';
            position: absolute;
            left: -2.5rem;
            top: 50%;
            transform: translateY(-50%);
            background: white;
            border-radius: 50%;
            width: 2rem;
            height: 2rem;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}

        .assistant-message {{
            background: linear-gradient(135deg, #ffffff, #f8f9fa);
            color: #333;
            margin-right: 3rem;
            border-bottom-left-radius: 8px;
            border-left: 4px solid {self.primary_color};
            position: relative;
        }}

        .assistant-message::before {{
            content: '🤖';
            position: absolute;
            right: -2.5rem;
            top: 50%;
            transform: translateY(-50%);
            background: {self.primary_color};
            border-radius: 50%;
            width: 2rem;
            height: 2rem;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1rem;
            box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
        }}
        
        /* Progress Bar */
        .progress-container {{
            background: #f0f0f0;
            border-radius: 25px;
            padding: 5px;
            margin: 1rem 0;
            box-shadow: inset 0 2px 5px rgba(0,0,0,0.1);
        }}
        
        .progress-bar {{
            background: linear-gradient(90deg, {self.primary_color}, {self.secondary_color});
            height: 20px;
            border-radius: 20px;
            transition: width 0.5s ease;
            box-shadow: 0 2px 10px rgba(76, 175, 80, 0.3);
        }}
        
        .progress-text {{
            text-align: center;
            font-weight: 600;
            color: #555;
            margin-top: 0.5rem;
        }}
        
        /* Stage Indicator */
        .stage-indicator {{
            background: linear-gradient(135deg, #fff, #f8f9fa);
            padding: 1.5rem;
            border-radius: 15px;
            border-left: 5px solid {self.primary_color};
            margin: 1rem 0;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.2s ease;
        }}
        
        .stage-indicator:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }}
        
        .stage-title {{
            font-weight: 600;
            color: {self.primary_color};
            font-size: 1.1rem;
            margin-bottom: 0.5rem;
        }}
        
        /* Buttons */
        .stButton > button {{
            background: linear-gradient(135deg, {self.primary_color}, #45a049);
            color: white;
            border: none;
            border-radius: 25px;
            padding: 0.75rem 2rem;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(76, 175, 80, 0.3);
        }}
        
        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(76, 175, 80, 0.4);
            background: linear-gradient(135deg, #45a049, {self.primary_color});
        }}
        
        /* Input Fields */
        .stTextInput > div > div > input {{
            border: 2px solid #e0e0e0;
            border-radius: 15px;
            padding: 1rem;
            font-size: 1rem;
            transition: all 0.3s ease;
            background: white;
        }}
        
        .stTextInput > div > div > input:focus {{
            border-color: {self.primary_color};
            box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
            outline: none;
        }}
        
        /* Selectbox */
        .stSelectbox > div > div > select {{
            border: 2px solid #e0e0e0;
            border-radius: 15px;
            padding: 0.75rem;
            background: white;
        }}
        
        /* Sidebar */
        .css-1d391kg {{
            background: #f8f9fa;
            border-right: 1px solid #e9ecef;
        }}
        
        /* Enhanced Animations */
        @keyframes slideIn {{
            from {{
                opacity: 0;
                transform: translateY(20px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        @keyframes slideInLeft {{
            from {{
                opacity: 0;
                transform: translateX(-30px);
            }}
            to {{
                opacity: 1;
                transform: translateX(0);
            }}
        }}

        @keyframes slideInRight {{
            from {{
                opacity: 0;
                transform: translateX(30px);
            }}
            to {{
                opacity: 1;
                transform: translateX(0);
            }}
        }}

        @keyframes pulse {{
            0% {{ transform: scale(1); }}
            50% {{ transform: scale(1.05); }}
            100% {{ transform: scale(1); }}
        }}

        @keyframes shimmer {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}

        @keyframes bounce {{
            0%, 20%, 50%, 80%, 100% {{ transform: translateY(0); }}
            40% {{ transform: translateY(-10px); }}
            60% {{ transform: translateY(-5px); }}
        }}

        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        .pulse-animation {{
            animation: pulse 2s infinite;
        }}

        .bounce-animation {{
            animation: bounce 2s infinite;
        }}

        .fade-in-up {{
            animation: fadeInUp 0.6s ease-out;
        }}

        .slide-in-left {{
            animation: slideInLeft 0.5s ease-out;
        }}

        .slide-in-right {{
            animation: slideInRight 0.5s ease-out;
        }}
        
        /* Sentiment Indicators */
        .sentiment-positive {{
            color: {self.success_color};
            font-weight: 600;
        }}
        
        .sentiment-negative {{
            color: {self.error_color};
            font-weight: 600;
        }}
        
        .sentiment-neutral {{
            color: #666;
            font-weight: 500;
        }}
        
        /* Cards */
        .info-card {{
            background: white;
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            border-left: 4px solid {self.accent_color};
            transition: transform 0.2s ease;
        }}
        
        .info-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        }}
        
        /* Loading Spinner */
        .loading-spinner {{
            border: 4px solid #f3f3f3;
            border-top: 4px solid {self.primary_color};
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }}
        
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        
        /* Responsive Design */
        @media (max-width: 768px) {{
            .app-title {{
                font-size: 2rem;
            }}
            
            .chat-message {{
                margin-left: 0.5rem;
                margin-right: 0.5rem;
            }}
            
            .main-container {{
                margin: 0.5rem;
                padding: 1rem;
            }}
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
    
    def create_animated_header(self, title: str, subtitle: str):
        """Create enhanced animated header with interactive elements."""
        header_html = f"""
        <div class="app-header fade-in-up">
            <div class="header-content">
                <div class="logo-container bounce-animation">
                    <div class="logo">🚀</div>
                </div>
                <h1 class="app-title">{title}</h1>
                <p class="app-subtitle">{subtitle}</p>
                <div class="header-features">
                    <div class="feature-badge slide-in-left">
                        <span class="feature-icon">🧠</span>
                        <span>AI-Powered</span>
                    </div>
                    <div class="feature-badge slide-in-right">
                        <span class="feature-icon">🌍</span>
                        <span>Multilingual</span>
                    </div>
                    <div class="feature-badge fade-in-up">
                        <span class="feature-icon">⚡</span>
                        <span>Real-time</span>
                    </div>
                </div>
            </div>
        </div>

        <style>
        .header-content {{
            position: relative;
            z-index: 2;
        }}

        .logo-container {{
            margin-bottom: 1rem;
        }}

        .logo {{
            font-size: 3rem;
            display: inline-block;
            filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));
        }}

        .header-features {{
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin-top: 1.5rem;
            flex-wrap: wrap;
        }}

        .feature-badge {{
            background: rgba(255,255,255,0.2);
            padding: 0.5rem 1rem;
            border-radius: 25px;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.9rem;
            font-weight: 500;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.3);
            transition: all 0.3s ease;
        }}

        .feature-badge:hover {{
            background: rgba(255,255,255,0.3);
            transform: translateY(-2px);
        }}

        .feature-icon {{
            font-size: 1.1rem;
        }}
        </style>
        """
        st.markdown(header_html, unsafe_allow_html=True)
    
    def create_progress_bar(self, progress: float, stage_name: str):
        """Create clean animated progress bar without step indicators."""

        progress_html = f"""
        <div class="clean-progress-container fade-in-up">
            <div class="progress-header">
                <h3 style="margin: 0; color: {self.primary_color};">Progress</h3>
                <span class="progress-percentage">{progress * 100:.0f}%</span>
            </div>
            <div class="progress-container">
                <div class="progress-bar" style="width: {progress * 100}%">
                    <div class="progress-shine"></div>
                </div>
            </div>
            <div class="progress-text">
                <strong>{stage_name}</strong>
            </div>
        </div>

        <style>
        .clean-progress-container {{
            background: white;
            padding: 1.5rem;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.08);
            margin: 1rem 0;
        }}

        .progress-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }}

        .progress-percentage {{
            font-size: 1.5rem;
            font-weight: bold;
            color: {self.primary_color};
        }}

        .progress-container {{
            background-color: #f0f0f0;
            border-radius: 25px;
            padding: 5px;
            margin: 1rem 0;
            box-shadow: inset 0 2px 5px rgba(0,0,0,0.1);
            position: relative;
            overflow: hidden;
        }}

        .progress-bar {{
            background: linear-gradient(90deg, {self.primary_color}, {self.secondary_color});
            height: 20px;
            border-radius: 20px;
            transition: width 0.5s ease;
            box-shadow: 0 2px 10px rgba(76, 175, 80, 0.3);
            position: relative;
            overflow: hidden;
        }}

        .progress-shine {{
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
            animation: shine 2s infinite;
        }}

        @keyframes shine {{
            0% {{ left: -100%; }}
            100% {{ left: 100%; }}
        }}

        .progress-text {{
            text-align: center;
            font-weight: 600;
            color: #555;
            margin-top: 0.5rem;
            font-size: 1rem;
        }}
        </style>
        """
        st.markdown(progress_html, unsafe_allow_html=True)
    
    def create_stage_indicator(self, stage_name: str, description: str, is_current: bool = False):
        """Create stage indicator card."""
        pulse_class = "pulse-animation" if is_current else ""
        indicator_html = f"""
        <div class="stage-indicator {pulse_class}">
            <div class="stage-title">{'🔄 ' if is_current else '✅ '}{stage_name}</div>
            <div>{description}</div>
        </div>
        """
        st.markdown(indicator_html, unsafe_allow_html=True)
    
    def create_sentiment_display(self, sentiment_score: float, emotion: str):
        """Create sentiment visualization."""
        if sentiment_score > 0.2:
            sentiment_class = "sentiment-positive"
            emoji = "😊"
        elif sentiment_score < -0.2:
            sentiment_class = "sentiment-negative"
            emoji = "😔"
        else:
            sentiment_class = "sentiment-neutral"
            emoji = "😐"
        
        sentiment_html = f"""
        <div class="info-card">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 1.5rem;">{emoji}</span>
                <div>
                    <div class="{sentiment_class}">Sentiment: {emotion.title()}</div>
                    <div style="font-size: 0.9rem; color: #666;">
                        Score: {sentiment_score:.2f}
                    </div>
                </div>
            </div>
        </div>
        """
        st.markdown(sentiment_html, unsafe_allow_html=True)
    
    def create_tech_stack_visualization(self, tech_stack: List[str]):
        """Create interactive tech stack visualization."""
        if not tech_stack:
            return
        
        # Create a simple bar chart
        fig = go.Figure(data=[
            go.Bar(
                x=tech_stack,
                y=[1] * len(tech_stack),
                marker_color=self.primary_color,
                text=tech_stack,
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title="Your Technical Skills",
            xaxis_title="Technologies",
            yaxis_title="Proficiency",
            showlegend=False,
            height=300,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def create_enhanced_conversation_metrics(self, metrics: Dict):
        """Create enhanced interactive conversation metrics with all animations and features."""

        # Get metrics values
        message_count = metrics.get('message_count', 0)
        avg_sentiment = metrics.get('avg_sentiment', 0.0)
        completion_rate = metrics.get('completion_rate', 0.0)

        # Determine sentiment emoji, color, and detailed analysis
        if avg_sentiment > 0.4:
            sentiment_emoji = "🤩"
            sentiment_color = "#4CAF50"
            sentiment_text = "Excellent"
            sentiment_bg = "linear-gradient(135deg, #4CAF50, #8BC34A)"
        elif avg_sentiment > 0.2:
            sentiment_emoji = "😄"
            sentiment_color = "#4CAF50"
            sentiment_text = "Very Positive"
            sentiment_bg = "#4CAF50"
        elif avg_sentiment > 0.1:
            sentiment_emoji = "😊"
            sentiment_color = "#8BC34A"
            sentiment_text = "Positive"
            sentiment_bg = "#8BC34A"
        elif avg_sentiment > -0.1:
            sentiment_emoji = "😐"
            sentiment_color = "#FFC107"
            sentiment_text = "Neutral"
            sentiment_bg = "#FFC107"
        elif avg_sentiment > -0.2:
            sentiment_emoji = "😕"
            sentiment_color = "#FF9800"
            sentiment_text = "Concerned"
            sentiment_bg = "#FF9800"
        else:
            sentiment_emoji = "😟"
            sentiment_color = "#F44336"
            sentiment_text = "Needs Support"
            sentiment_bg = "#F44336"

        # Create enhanced interactive metrics with all features
        metrics_html = f"""
        <div class="enhanced-interactive-metrics">
            <div class="metrics-header">
                <h3>📊 Live Conversation Analytics</h3>
                <div class="metrics-status">
                    {"🔥 Active Session" if message_count > 3 else "📝 Getting Started" if message_count > 0 else "👋 Ready to Begin"}
                </div>
            </div>

            <div class="metrics-cards-container">
                <!-- Messages Metric with Pulsing Animation -->
                <div class="enhanced-metric-card messages-card">
                    <div class="metric-header">
                        <div class="metric-icon-wrapper">
                            <div class="metric-icon pulse-animation">💬</div>
                            <div class="metric-pulse-ring"></div>
                        </div>
                        <div class="metric-badge animated-badge">{message_count}</div>
                    </div>
                    <div class="metric-body">
                        <div class="metric-value">{message_count}</div>
                        <div class="metric-label">Messages</div>
                        <div class="metric-trend">
                            {"🔥 Very Active!" if message_count > 8 else "⚡ Active Chat" if message_count > 5 else "📝 Getting Started" if message_count > 0 else "👋 Ready to Chat"}
                        </div>
                        <div class="metric-detail">
                            {"Excellent engagement" if message_count > 8 else "Good conversation flow" if message_count > 5 else "Building momentum" if message_count > 0 else "Waiting for first message"}
                        </div>
                    </div>
                </div>

                <!-- Sentiment Metric with Bouncing Animation and Color Coding -->
                <div class="enhanced-metric-card sentiment-card" style="border-left: 4px solid {sentiment_color};">
                    <div class="metric-header">
                        <div class="metric-icon-wrapper">
                            <div class="metric-icon bounce-animation">{sentiment_emoji}</div>
                            <div class="sentiment-aura" style="background: {sentiment_color}20;"></div>
                        </div>
                        <div class="metric-badge sentiment-badge" style="background: {sentiment_bg};">
                            {avg_sentiment:+.2f}
                        </div>
                    </div>
                    <div class="metric-body">
                        <div class="metric-value" style="color: {sentiment_color};">{sentiment_text}</div>
                        <div class="metric-label">Sentiment Analysis</div>
                        <div class="metric-trend sentiment-trend" style="background: {sentiment_color}20; color: {sentiment_color};">
                            {"🎉 Amazing vibes!" if avg_sentiment > 0.3 else "👍 Great energy!" if avg_sentiment > 0.1 else "😊 Positive flow" if avg_sentiment > 0 else "😐 Neutral tone" if avg_sentiment > -0.1 else "💪 Stay encouraged!"}
                        </div>
                        <div class="sentiment-bar">
                            <div class="sentiment-fill" style="width: {min(abs(avg_sentiment) * 100, 100)}%; background: {sentiment_color};"></div>
                        </div>
                        <div class="metric-detail">
                            {"Candidate is very enthusiastic" if avg_sentiment > 0.3 else "Positive candidate experience" if avg_sentiment > 0.1 else "Candidate seems comfortable" if avg_sentiment > 0 else "Neutral conversation tone" if avg_sentiment > -0.1 else "Consider providing encouragement"}
                        </div>
                    </div>
                </div>

                <!-- Completion Metric with Complex Progress Indicators -->
                <div class="enhanced-metric-card completion-card">
                    <div class="metric-header">
                        <div class="metric-icon-wrapper">
                            <div class="metric-icon rotate-animation">
                                {"🎯" if completion_rate > 0.8 else "⚡" if completion_rate > 0.6 else "🚀" if completion_rate > 0.3 else "✨"}
                            </div>
                            <div class="completion-ring">
                                <svg class="progress-ring" width="40" height="40">
                                    <circle class="progress-ring-circle" cx="20" cy="20" r="15"
                                            style="stroke-dasharray: {2 * 3.14159 * 15};
                                                   stroke-dashoffset: {2 * 3.14159 * 15 * (1 - completion_rate)};">
                                    </circle>
                                </svg>
                            </div>
                        </div>
                        <div class="metric-badge completion-badge" style="background: linear-gradient(45deg, {self.primary_color}, #45a049);">
                            {completion_rate:.0%}
                        </div>
                    </div>
                    <div class="metric-body">
                        <div class="metric-value">{completion_rate:.0%}</div>
                        <div class="metric-label">Application Progress</div>
                        <div class="metric-trend completion-trend">
                            {"🏁 Almost finished!" if completion_rate > 0.8 else "🎯 Great progress!" if completion_rate > 0.6 else "⚡ Moving forward!" if completion_rate > 0.3 else "🚀 Just getting started!" if completion_rate > 0 else "🌟 Ready to begin!"}
                        </div>
                        <div class="complex-progress-bar">
                            <div class="progress-track">
                                <div class="progress-fill" style="width: {completion_rate * 100}%;">
                                    <div class="progress-shine"></div>
                                </div>
                            </div>
                            <div class="progress-markers">
                                {"".join([f'<div class="progress-marker {"active" if i/8 <= completion_rate else ""}" style="left: {i/8*100}%;"></div>' for i in range(9)])}
                            </div>
                        </div>
                        <div class="metric-detail">
                            {"Final questions coming up!" if completion_rate > 0.8 else "Halfway through the process" if completion_rate > 0.5 else "Building candidate profile" if completion_rate > 0.2 else "Starting the journey"}
                        </div>
                    </div>
                </div>
            </div>

            <!-- Interactive Tips and Trend Messages -->
            <div class="interactive-tips-section">
                <div class="tips-header">
                    <span class="tips-icon pulse-animation">💡</span>
                    <span class="tips-title">Smart Insights</span>
                </div>
                <div class="tips-content">
                    <div class="tip-item primary-tip">
                        <span class="tip-icon">{"🎉" if avg_sentiment > 0.2 else "💪" if avg_sentiment < -0.1 else "👍"}</span>
                        <span class="tip-text">
                            {"Keep up the fantastic energy! The candidate is very engaged." if avg_sentiment > 0.2 else "Consider providing more encouragement to boost candidate confidence." if avg_sentiment < -0.1 else "Conversation is flowing well. Keep the momentum going!"}
                        </span>
                    </div>
                    <div class="tip-item secondary-tip">
                        <span class="tip-icon">{"🏁" if completion_rate > 0.8 else "🎯" if completion_rate > 0.5 else "🚀"}</span>
                        <span class="tip-text">
                            {"Almost done! Prepare for final technical questions." if completion_rate > 0.8 else "Great progress! Continue with the structured flow." if completion_rate > 0.5 else "Building rapport. Take time to understand the candidate."}
                        </span>
                    </div>
                    {"<div class='tip-item bonus-tip'><span class='tip-icon'>⭐</span><span class='tip-text'>High-quality conversation detected! This candidate shows strong communication skills.</span></div>" if message_count > 6 and avg_sentiment > 0.1 else ""}
                </div>
            </div>
        </div>

        <style>
        .enhanced-interactive-metrics {{
            background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
            border-radius: 20px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            border: 1px solid #e9ecef;
            position: relative;
            overflow: hidden;
        }}

        .enhanced-interactive-metrics::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(76,175,80,0.05) 0%, transparent 70%);
            animation: shimmer 4s ease-in-out infinite;
        }}

        .metrics-header {{
            text-align: center;
            margin-bottom: 1.5rem;
            position: relative;
            z-index: 2;
        }}

        .metrics-header h3 {{
            color: {self.primary_color};
            margin: 0 0 0.5rem 0;
            font-size: 1.2rem;
            font-weight: 600;
        }}

        .metrics-status {{
            background: linear-gradient(135deg, {self.primary_color}20, {self.secondary_color}20);
            color: {self.primary_color};
            padding: 0.3rem 1rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 500;
            display: inline-block;
        }}

        .metrics-cards-container {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 1rem;
            margin-bottom: 1.5rem;
            position: relative;
            z-index: 2;
        }}

        .enhanced-metric-card {{
            background: white;
            border-radius: 15px;
            padding: 1.2rem;
            box-shadow: 0 5px 20px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }}

        .enhanced-metric-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        }}

        .metric-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }}

        .metric-icon-wrapper {{
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .metric-icon {{
            font-size: 1.8rem;
            position: relative;
            z-index: 3;
        }}

        .metric-pulse-ring {{
            position: absolute;
            width: 3rem;
            height: 3rem;
            border: 2px solid {self.primary_color}40;
            border-radius: 50%;
            animation: pulse-ring 2s infinite;
        }}

        .sentiment-aura {{
            position: absolute;
            width: 3rem;
            height: 3rem;
            border-radius: 50%;
            animation: aura-glow 3s infinite;
        }}

        .completion-ring {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
        }}

        .progress-ring-circle {{
            fill: none;
            stroke: {self.primary_color};
            stroke-width: 3;
            stroke-linecap: round;
            transform: rotate(-90deg);
            transform-origin: 50% 50%;
            transition: stroke-dashoffset 0.5s ease;
        }}

        .metric-badge {{
            background: {self.primary_color};
            color: white;
            border-radius: 25px;
            padding: 0.3rem 0.8rem;
            font-size: 0.8rem;
            font-weight: bold;
            box-shadow: 0 3px 10px rgba(76,175,80,0.3);
        }}

        .animated-badge {{
            animation: badge-bounce 2s infinite;
        }}

        .metric-body {{
            text-align: center;
        }}

        .metric-value {{
            font-size: 1.4rem;
            font-weight: bold;
            color: {self.primary_color};
            margin-bottom: 0.3rem;
        }}

        .metric-label {{
            font-size: 0.9rem;
            color: #6c757d;
            font-weight: 500;
            margin-bottom: 0.5rem;
        }}

        .metric-trend {{
            font-size: 0.8rem;
            color: #28a745;
            font-weight: 500;
            background: rgba(40, 167, 69, 0.1);
            padding: 0.3rem 0.8rem;
            border-radius: 15px;
            display: inline-block;
            margin-bottom: 0.5rem;
        }}

        .sentiment-bar {{
            height: 6px;
            background: #e9ecef;
            border-radius: 3px;
            margin: 0.5rem 0;
            overflow: hidden;
        }}

        .sentiment-fill {{
            height: 100%;
            border-radius: 3px;
            transition: width 0.5s ease;
        }}

        .complex-progress-bar {{
            margin: 0.8rem 0;
            position: relative;
        }}

        .progress-track {{
            height: 8px;
            background: #e9ecef;
            border-radius: 4px;
            overflow: hidden;
            position: relative;
        }}

        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, {self.primary_color}, {self.secondary_color});
            border-radius: 4px;
            transition: width 0.5s ease;
            position: relative;
            overflow: hidden;
        }}

        .progress-shine {{
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.6), transparent);
            animation: shine 2s infinite;
        }}

        .progress-markers {{
            position: absolute;
            top: -2px;
            left: 0;
            right: 0;
            height: 12px;
        }}

        .progress-marker {{
            position: absolute;
            width: 3px;
            height: 12px;
            background: #ccc;
            border-radius: 2px;
            transition: background 0.3s ease;
        }}

        .progress-marker.active {{
            background: {self.primary_color};
            box-shadow: 0 0 5px {self.primary_color}50;
        }}

        .metric-detail {{
            font-size: 0.75rem;
            color: #8a8a8a;
            font-style: italic;
            margin-top: 0.3rem;
        }}

        .interactive-tips-section {{
            background: linear-gradient(135deg, rgba(76,175,80,0.1), rgba(33,150,243,0.1));
            border-radius: 15px;
            padding: 1rem;
            border-left: 4px solid {self.primary_color};
            position: relative;
            z-index: 2;
        }}

        .tips-header {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 0.8rem;
        }}

        .tips-title {{
            font-weight: 600;
            color: {self.primary_color};
            font-size: 1rem;
        }}

        .tips-content {{
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }}

        .tip-item {{
            display: flex;
            align-items: flex-start;
            gap: 0.5rem;
            padding: 0.5rem;
            border-radius: 10px;
            transition: background 0.2s ease;
        }}

        .tip-item:hover {{
            background: rgba(255,255,255,0.5);
        }}

        .primary-tip {{
            background: rgba(76,175,80,0.1);
        }}

        .secondary-tip {{
            background: rgba(33,150,243,0.1);
        }}

        .bonus-tip {{
            background: linear-gradient(135deg, rgba(255,193,7,0.2), rgba(255,152,0,0.2));
            border: 1px solid rgba(255,193,7,0.3);
        }}

        .tip-icon {{
            font-size: 1rem;
            margin-top: 0.1rem;
        }}

        .tip-text {{
            font-size: 0.85rem;
            color: #2d5a2d;
            font-weight: 500;
            line-height: 1.4;
        }}

        /* Enhanced Animations */
        @keyframes pulse-animation {{
            0% {{ transform: scale(1); }}
            50% {{ transform: scale(1.1); }}
            100% {{ transform: scale(1); }}
        }}

        @keyframes bounce-animation {{
            0%, 20%, 50%, 80%, 100% {{ transform: translateY(0); }}
            40% {{ transform: translateY(-8px); }}
            60% {{ transform: translateY(-4px); }}
        }}

        @keyframes rotate-animation {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}

        @keyframes pulse-ring {{
            0% {{ transform: scale(0.8); opacity: 1; }}
            100% {{ transform: scale(1.4); opacity: 0; }}
        }}

        @keyframes aura-glow {{
            0%, 100% {{ transform: scale(1); opacity: 0.3; }}
            50% {{ transform: scale(1.2); opacity: 0.1; }}
        }}

        @keyframes badge-bounce {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.05); }}
        }}

        @keyframes shimmer {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}

        @keyframes shine {{
            0% {{ left: -100%; }}
            100% {{ left: 100%; }}
        }}

        .pulse-animation {{
            animation: pulse-animation 2s infinite;
        }}

        .bounce-animation {{
            animation: bounce-animation 2s infinite;
        }}

        .rotate-animation {{
            animation: rotate-animation 3s linear infinite;
        }}
        </style>
        """

        st.markdown(metrics_html, unsafe_allow_html=True)

    def _create_detailed_metrics(self, metrics: Dict):
        """Create detailed metrics breakdown."""
        message_count = metrics.get('message_count', 0)
        avg_sentiment = metrics.get('avg_sentiment', 0.0)
        completion_rate = metrics.get('completion_rate', 0.0)

        # Create metrics breakdown
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**💬 Conversation Stats**")
            st.metric("Total Messages", message_count, delta=None)

            if message_count > 0:
                avg_length = 50  # Estimated average message length
                st.metric("Est. Avg Length", f"{avg_length} chars", delta=None)

                conversation_quality = "Excellent" if message_count > 10 else "Good" if message_count > 5 else "Getting Started"
                st.info(f"Quality: {conversation_quality}")

        with col2:
            st.markdown("**😊 Sentiment Analysis**")
            st.metric("Average Sentiment", f"{avg_sentiment:.3f}", delta=f"{avg_sentiment:+.3f}")

            # Sentiment breakdown
            if avg_sentiment > 0.2:
                st.success("😄 Very Positive - Great engagement!")
            elif avg_sentiment > 0:
                st.info("😊 Positive - Good conversation flow")
            elif avg_sentiment > -0.2:
                st.warning("😐 Neutral - Consider more encouragement")
            else:
                st.error("😟 Negative - Candidate may need support")

        # Progress breakdown
        st.markdown("**🎯 Progress Breakdown**")
        progress_col1, progress_col2, progress_col3 = st.columns(3)

        with progress_col1:
            st.metric("Completion", f"{completion_rate:.1%}", delta=None)

        with progress_col2:
            remaining = 1 - completion_rate
            st.metric("Remaining", f"{remaining:.1%}", delta=None)

        with progress_col3:
            if completion_rate > 0:
                eta = "2-3 min" if completion_rate > 0.7 else "5-7 min" if completion_rate > 0.3 else "8-10 min"
                st.metric("Est. Time Left", eta, delta=None)

        # Interactive recommendations
        st.markdown("**💡 AI Recommendations**")

        recommendations = []
        if avg_sentiment < -0.1:
            recommendations.append("🤗 Provide more encouragement and support")
        if message_count < 3:
            recommendations.append("💬 Encourage more detailed responses")
        if completion_rate < 0.3:
            recommendations.append("🚀 Guide candidate through next steps")
        if completion_rate > 0.8:
            recommendations.append("🎉 Almost done! Prepare for final questions")

        if not recommendations:
            recommendations.append("✅ Conversation is flowing well!")

        for rec in recommendations:
            st.write(f"• {rec}")

        # Quick actions
        st.markdown("**⚡ Quick Actions**")
        action_col1, action_col2, action_col3 = st.columns(3)

        with action_col1:
            if st.button("🔄 Reset Metrics", help="Reset conversation metrics"):
                st.session_state.conversation_metrics = {
                    'message_count': 0,
                    'avg_sentiment': 0.0,
                    'completion_rate': 0.0
                }
                st.success("Metrics reset!")
                st.rerun()

        with action_col2:
            if st.button("📊 Export Stats", help="Export conversation statistics"):
                stats_data = {
                    'timestamp': str(datetime.now()),
                    'metrics': metrics,
                    'recommendations': recommendations
                }
                st.download_button(
                    label="📥 Download JSON",
                    data=str(stats_data),
                    file_name=f"conversation_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )

        with action_col3:
            if st.button("🎯 Optimize", help="Get optimization suggestions"):
                st.info("💡 Optimization suggestions based on current metrics will appear here!")

    def create_live_sentiment_chart(self, sentiment_history):
        """Create a live sentiment chart."""
        if not sentiment_history:
            return

        import plotly.graph_objects as go

        # Extract sentiment scores
        scores = [s.polarity for s in sentiment_history[-10:]]  # Last 10 messages
        messages = list(range(1, len(scores) + 1))

        fig = go.Figure()

        # Add sentiment line
        fig.add_trace(go.Scatter(
            x=messages,
            y=scores,
            mode='lines+markers',
            name='Sentiment',
            line=dict(color=self.primary_color, width=3),
            marker=dict(size=8, color=self.primary_color)
        ))

        # Add zero line
        fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)

        # Add positive/negative zones
        fig.add_hrect(y0=0, y1=1, fillcolor="green", opacity=0.1, line_width=0)
        fig.add_hrect(y0=-1, y1=0, fillcolor="red", opacity=0.1, line_width=0)

        fig.update_layout(
            title="Live Sentiment Tracking",
            xaxis_title="Message #",
            yaxis_title="Sentiment Score",
            height=300,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )

        st.plotly_chart(fig, use_container_width=True)
    
    def create_metric_card(self, title: str, value: str, icon: str):
        """Create a metric display card."""
        card_html = f"""
        <div class="info-card" style="text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
            <div style="font-size: 1.5rem; font-weight: 600; color: {self.primary_color};">{value}</div>
            <div style="font-size: 0.9rem; color: #666;">{title}</div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
    
    def show_loading_spinner(self, message: str = "Processing..."):
        """Show loading spinner with message."""
        spinner_html = f"""
        <div style="text-align: center; padding: 2rem;">
            <div class="loading-spinner"></div>
            <div style="margin-top: 1rem; color: #666;">{message}</div>
        </div>
        """
        return st.markdown(spinner_html, unsafe_allow_html=True)
    
    def create_language_selector_ui(self, languages: Dict[str, str]):
        """Create enhanced language selector."""
        st.markdown("### 🌍 Language Selection")
        
        # Create columns for language flags
        cols = st.columns(min(len(languages), 4))
        
        selected_lang = None
        for i, (display_name, code) in enumerate(languages.items()):
            with cols[i % 4]:
                if st.button(display_name, key=f"lang_{code}"):
                    selected_lang = code
        
        return selected_lang
    
    def create_accessibility_toolbar(self):
        """Create enhanced accessibility toolbar."""
        with st.expander("♿ Accessibility & Help", expanded=False):
            # Accessibility options
            st.subheader("🎨 Accessibility Options")
            col1, col2 = st.columns(2)

            with col1:
                font_size = st.selectbox("Font Size", ["Normal", "Large", "Extra Large"])
                high_contrast = st.checkbox("High Contrast Mode")

            with col2:
                screen_reader = st.checkbox("Screen Reader Optimized")
                simple_language = st.checkbox("Simple Language Mode")

            # Help section
            st.subheader("❓ Quick Help")

            help_tabs = st.tabs(["🚀 Getting Started", "💬 Chat Tips", "🔧 Troubleshooting"])

            with help_tabs[0]:
                st.markdown("""
                **Welcome to TalentScout!** Here's how to get started:

                1. **Start the conversation** by typing your name
                2. **Follow the prompts** for each step
                3. **Be honest and detailed** in your responses
                4. **Use any language** - we support 12+ languages
                5. **Watch the progress bar** to track your application
                """)

            with help_tabs[1]:
                st.markdown("""
                **Chat Tips for Best Experience:**

                • 💬 **Be conversational** - talk naturally
                • 🌍 **Switch languages** anytime (Spanish, French, German, etc.)
                • 😊 **Express emotions** - our AI detects sentiment
                • 📝 **Be specific** about your technical skills
                • ❓ **Ask questions** if you need clarification
                """)

            with help_tabs[2]:
                st.markdown("""
                **Common Issues & Solutions:**

                • **Slow responses?** Check your internet connection
                • **Language not detected?** Type a longer message
                • **Technical questions too hard?** Adjust difficulty in settings
                • **Need to restart?** Use the reset button in sidebar
                • **Export not working?** Complete all steps first
                """)

            return {
                'font_size': font_size,
                'high_contrast': high_contrast,
                'screen_reader': screen_reader,
                'simple_language': simple_language
            }

    def create_simple_welcome_message(self):
        """Create a simple, clean welcome message."""
        welcome_html = f"""
        <div class="simple-welcome fade-in-up">
            <div class="welcome-content">
                <h3>👋 Welcome to TalentScout!</h3>
                <p>I'm your AI hiring assistant. Let's get started with your application.</p>
            </div>
        </div>

        <style>
        .simple-welcome {{
            background: white;
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            border-left: 4px solid {self.primary_color};
        }}

        .welcome-content {{
            text-align: center;
        }}

        .welcome-content h3 {{
            color: {self.primary_color};
            margin: 0 0 0.5rem 0;
            font-size: 1.3rem;
        }}

        .welcome-content p {{
            color: #6c757d;
            margin: 0;
            font-size: 1rem;
        }}
        </style>
        """
        st.markdown(welcome_html, unsafe_allow_html=True)

    def create_floating_help_button(self):
        """Create a floating help button."""
        help_html = f"""
        <div class="floating-help-container">
            <div class="floating-help-button" onclick="toggleHelp()">
                <span class="help-icon">❓</span>
                <span class="help-text">Help</span>
            </div>

            <div class="floating-help-menu" id="helpMenu">
                <div class="help-item">
                    <span class="help-item-icon">🚀</span>
                    <span class="help-item-text">Getting Started</span>
                </div>
                <div class="help-item">
                    <span class="help-item-icon">💬</span>
                    <span class="help-item-text">Chat Tips</span>
                </div>
                <div class="help-item">
                    <span class="help-item-icon">🌍</span>
                    <span class="help-item-text">Languages</span>
                </div>
                <div class="help-item">
                    <span class="help-item-icon">🔧</span>
                    <span class="help-item-text">Settings</span>
                </div>
            </div>
        </div>

        <style>
        .floating-help-container {{
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            z-index: 1000;
        }}

        .floating-help-button {{
            background: linear-gradient(135deg, {self.primary_color}, #45a049);
            color: white;
            border-radius: 50px;
            padding: 1rem 1.5rem;
            box-shadow: 0 8px 25px rgba(76, 175, 80, 0.3);
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            transition: all 0.3s ease;
            font-weight: 600;
        }}

        .floating-help-button:hover {{
            transform: translateY(-3px);
            box-shadow: 0 12px 35px rgba(76, 175, 80, 0.4);
        }}

        .help-icon {{
            font-size: 1.2rem;
        }}

        .floating-help-menu {{
            position: absolute;
            bottom: 100%;
            right: 0;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            padding: 1rem;
            margin-bottom: 1rem;
            min-width: 200px;
            opacity: 0;
            visibility: hidden;
            transform: translateY(10px);
            transition: all 0.3s ease;
        }}

        .floating-help-menu.show {{
            opacity: 1;
            visibility: visible;
            transform: translateY(0);
        }}

        .help-item {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.75rem;
            border-radius: 10px;
            cursor: pointer;
            transition: background 0.2s ease;
        }}

        .help-item:hover {{
            background: #f8f9fa;
        }}

        .help-item-icon {{
            font-size: 1.1rem;
        }}

        .help-item-text {{
            font-weight: 500;
            color: #333;
        }}
        </style>

        <script>
        function toggleHelp() {{
            const menu = document.getElementById('helpMenu');
            menu.classList.toggle('show');
        }}

        // Close menu when clicking outside
        document.addEventListener('click', function(event) {{
            const container = document.querySelector('.floating-help-container');
            if (!container.contains(event.target)) {{
                document.getElementById('helpMenu').classList.remove('show');
            }}
        }});
        </script>
        """
        st.markdown(help_html, unsafe_allow_html=True)

    def create_quick_actions_panel(self):
        """Create a quick actions panel."""
        st.markdown("### ⚡ Quick Actions")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("🔄 Reset Chat", help="Start a new conversation"):
                return "reset"

        with col2:
            if st.button("📥 Export Data", help="Download your information"):
                return "export"

        with col3:
            if st.button("🌍 Change Language", help="Switch to another language"):
                return "language"

        with col4:
            if st.button("❓ Get Help", help="Show help and tips"):
                return "help"

        return None

# Global instance
enhanced_ui = EnhancedUI()
