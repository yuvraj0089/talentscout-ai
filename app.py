import streamlit as st
import utils
import time
from config import STAGES, STAGE_QUESTIONS, WELCOME_MESSAGE

# Configure Streamlit page - MUST be first Streamlit command
st.set_page_config(
    page_title="TalentScout - AI Hiring Assistant",
    page_icon="👨‍💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Setup Python 3.13 compatibility
try:
    from python313_compatibility import setup_compatibility, check_dependencies
    setup_compatibility()
    dependencies_ok = check_dependencies()
except ImportError:
    dependencies_ok = True

# Import advanced modules with compatibility handling
try:
    from sentiment_analyzer import sentiment_analyzer
    from multilingual_support import multilingual_manager
    from personalization import personalization_manager, UserPreferences
    from enhanced_ui import enhanced_ui
    from performance_optimizer import performance_optimizer
    ADVANCED_FEATURES_AVAILABLE = True
    if not dependencies_ok:
        st.sidebar.info("🔧 Running in compatibility mode for Python 3.13")
except ImportError as e:
    st.sidebar.warning(f"⚠️ Advanced features unavailable: {str(e)[:50]}...")
    st.sidebar.info("💡 Basic functionality still available")
    ADVANCED_FEATURES_AVAILABLE = False

def initialize_session_state():
    """Initialize session state variables with advanced features."""
    if 'stage' not in st.session_state:
        st.session_state.stage = STAGES['NAME']
    if 'candidate_info' not in st.session_state:
        st.session_state.candidate_info = {}
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({"role": "assistant", "content": WELCOME_MESSAGE})
    if 'conversation_started' not in st.session_state:
        st.session_state.conversation_started = False
    if 'error_count' not in st.session_state:
        st.session_state.error_count = 0

    # Advanced features initialization
    if ADVANCED_FEATURES_AVAILABLE:
        if 'sentiment_history' not in st.session_state:
            st.session_state.sentiment_history = []
        if 'user_language' not in st.session_state:
            st.session_state.user_language = 'en'
        if 'user_preferences' not in st.session_state:
            st.session_state.user_preferences = UserPreferences()
        if 'user_id' not in st.session_state:
            st.session_state.user_id = None
        if 'conversation_metrics' not in st.session_state:
            st.session_state.conversation_metrics = {
                'message_count': 0,
                'avg_sentiment': 0.0,
                'completion_rate': 0.0
            }

        # Initialize performance optimizer
        performance_optimizer.optimize_streamlit_performance()

def process_user_input(user_input: str) -> str:
    """Process user input with advanced features including sentiment analysis and multilingual support."""
    # Advanced features processing
    if ADVANCED_FEATURES_AVAILABLE:
        # Detect language if not set
        if st.session_state.user_language == 'en' and len(user_input) > 10:
            detected_lang = multilingual_manager.detect_language(user_input)
            if detected_lang != 'en':
                st.session_state.user_language = detected_lang
                st.sidebar.success(f"Language detected: {multilingual_manager.supported_languages[detected_lang].flag} {multilingual_manager.supported_languages[detected_lang].name}")

        # Analyze sentiment
        sentiment_result = sentiment_analyzer.analyze_sentiment(user_input)
        st.session_state.sentiment_history.append(sentiment_result)

        # Update conversation metrics
        st.session_state.conversation_metrics['message_count'] += 1
        avg_sentiment = sum(s.polarity for s in st.session_state.sentiment_history) / len(st.session_state.sentiment_history)
        st.session_state.conversation_metrics['avg_sentiment'] = avg_sentiment

    # Handle exit commands
    exit_message = "Thank you for your time! We appreciate you taking the time to speak with us. Our team will review your information and get back to you soon. Have a great day! 👋"
    if ADVANCED_FEATURES_AVAILABLE:
        exit_message = multilingual_manager.get_translation('goodbye', st.session_state.user_language)

    if utils.is_exit_command(user_input):
        return exit_message

    current_stage = st.session_state.stage

    # Validate conversation context
    is_valid, context_message = utils.validate_conversation_context(user_input, current_stage)
    if not is_valid:
        st.session_state.error_count += 1
        if st.session_state.error_count >= 3:
            return "I notice we're having some difficulty staying on topic. Let's focus on completing your application. " + context_message
        return context_message

    response = ""

    try:
        if current_stage == STAGES['NAME']:
            if len(user_input.strip()) < 2:
                return "Please provide your full name (at least 2 characters)."
            st.session_state.candidate_info['name'] = user_input.strip()
            st.session_state.conversation_started = True
            response = f"Nice to meet you, {user_input.strip()}! {STAGE_QUESTIONS['EMAIL']}"
            st.session_state.stage = STAGES['EMAIL']

        elif current_stage == STAGES['EMAIL']:
            if utils.validate_email(user_input):
                st.session_state.candidate_info['email'] = user_input.strip()
                response = STAGE_QUESTIONS['PHONE']
                st.session_state.stage = STAGES['PHONE']
                st.session_state.error_count = 0  # Reset error count on success
            else:
                st.session_state.error_count += 1
                if st.session_state.error_count >= 3:
                    response = "I'm having trouble with the email format. Please provide a valid email address like: example@company.com"
                else:
                    response = "Please provide a valid email address (e.g., john.doe@email.com)."

        elif current_stage == STAGES['PHONE']:
            if utils.validate_phone(user_input):
                st.session_state.candidate_info['phone'] = user_input.strip()
                response = STAGE_QUESTIONS['EXPERIENCE']
                st.session_state.stage = STAGES['EXPERIENCE']
                st.session_state.error_count = 0
            else:
                st.session_state.error_count += 1
                if st.session_state.error_count >= 3:
                    response = "Please provide a valid phone number with 10-15 digits. You can include country code if needed (e.g., +1234567890)."
                else:
                    response = "Please provide a valid phone number (e.g., +1234567890 or 1234567890)."

        elif current_stage == STAGES['EXPERIENCE']:
            is_valid, years = utils.validate_experience(user_input)
            if is_valid:
                st.session_state.candidate_info['experience'] = years
                response = STAGE_QUESTIONS['POSITION']
                st.session_state.stage = STAGES['POSITION']
                st.session_state.error_count = 0
            else:
                st.session_state.error_count += 1
                if st.session_state.error_count >= 3:
                    response = "Please provide your experience as a number (e.g., '3' for 3 years, '2.5' for 2.5 years, or '0' for entry level)."
                else:
                    response = "Please provide your experience in years as a number (e.g., 5, 2.5, or 0 for entry level)."

        elif current_stage == STAGES['POSITION']:
            if len(user_input.strip()) < 2:
                return "Please provide the position you're interested in (e.g., Software Developer, Data Scientist)."
            st.session_state.candidate_info['position'] = user_input.strip()
            response = STAGE_QUESTIONS['LOCATION']
            st.session_state.stage = STAGES['LOCATION']

        elif current_stage == STAGES['LOCATION']:
            if len(user_input.strip()) < 2:
                return "Please provide your current location (e.g., New York, NY or Remote)."
            st.session_state.candidate_info['location'] = user_input.strip()
            response = STAGE_QUESTIONS['TECH_STACK']
            st.session_state.stage = STAGES['TECH_STACK']

        elif current_stage == STAGES['TECH_STACK']:
            tech_stack = utils.parse_tech_stack(user_input)
            if tech_stack:
                st.session_state.candidate_info['tech_stack'] = tech_stack
                with st.spinner("Generating personalized technical questions..."):
                    technical_questions = utils.generate_technical_questions(tech_stack)
                st.session_state.candidate_info['technical_questions'] = technical_questions

                tech_list = ", ".join(tech_stack)
                response = f"Excellent! I see you're skilled in: {tech_list}\n\nHere are some technical questions based on your expertise:\n\n" + "\n".join(technical_questions) + "\n\nPlease provide your answers to these questions:"
                st.session_state.stage = STAGES['TECHNICAL_QUESTIONS']
            else:
                st.session_state.error_count += 1
                if st.session_state.error_count >= 3:
                    response = "Please list at least one technology you know. For example: 'Python, JavaScript' or 'React, Node.js, MongoDB'."
                else:
                    response = "Please provide at least one technology you're proficient in (e.g., Python, JavaScript, React)."

        elif current_stage == STAGES['TECHNICAL_QUESTIONS']:
            if len(user_input.strip()) < 10:
                return "Please provide more detailed answers to the technical questions."
            st.session_state.candidate_info['technical_answers'] = user_input.strip()
            response = utils.format_candidate_summary(st.session_state.candidate_info)
            st.session_state.stage = STAGES['CONCLUSION']

        elif current_stage == STAGES['CONCLUSION']:
            response = "Thank you! Your application has been completed. Is there anything else you'd like to add or any questions about the next steps?"

    except Exception as e:
        st.error(f"An error occurred: {e}")
        response = utils.handle_unexpected_input(user_input, current_stage)

    return response

def main():
    """Main application function with advanced features."""

    # Initialize session state first
    initialize_session_state()

    # Apply enhanced UI styling
    if ADVANCED_FEATURES_AVAILABLE:
        enhanced_ui.inject_custom_css()

        # Apply RTL CSS if needed
        rtl_css = multilingual_manager.get_rtl_css(st.session_state.user_language)
        if rtl_css:
            st.markdown(rtl_css, unsafe_allow_html=True)
    else:
        # Fallback basic styling with white background
        st.markdown("""
            <style>
            .stApp {
                max-width: 1200px;
                margin: 0 auto;
                background: white;
            }
            .stTextInput>div>div>input {
                border-radius: 10px;
                border: 2px solid #e0e0e0;
            }
            .stButton>button {
                border-radius: 10px;
                width: 100%;
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 0.5rem 1rem;
                font-weight: bold;
            }
            </style>
        """, unsafe_allow_html=True)

    # Enhanced Sidebar with advanced features
    with st.sidebar:
        # Language selector (if advanced features available)
        if ADVANCED_FEATURES_AVAILABLE:
            st.header("🌍 Language / Idioma")
            selected_lang = multilingual_manager.get_language_selector()
            if selected_lang != st.session_state.user_language:
                st.session_state.user_language = selected_lang
                st.rerun()

        st.header("🎯 Application Progress")

        # Progress indicator with enhanced UI
        current_stage = st.session_state.stage
        total_stages = len(STAGES) - 1  # Exclude conclusion stage
        progress = min(current_stage / total_stages, 1.0)

        if ADVANCED_FEATURES_AVAILABLE:
            stage_names = {
                0: "Personal Information",
                1: "Contact Details",
                2: "Phone Number",
                3: "Experience Level",
                4: "Desired Position",
                5: "Location",
                6: "Technical Skills",
                7: "Technical Assessment",
                8: "Complete"
            }
            current_stage_name = stage_names.get(current_stage, "Unknown")
            enhanced_ui.create_progress_bar(progress, current_stage_name)
        else:
            # Fallback progress bar
            st.markdown(f"""
            <div class="progress-bar">
                <div class="progress-fill" style="width: {progress * 100}%"></div>
            </div>
            <p style="text-align: center; margin: 0.5rem 0;">
                Step {min(current_stage + 1, total_stages)} of {total_stages}
            </p>
            """, unsafe_allow_html=True)

        # Advanced features in sidebar
        if ADVANCED_FEATURES_AVAILABLE:
            # Personalization settings
            st.session_state.user_preferences = personalization_manager.create_preferences_ui()

            # Sentiment analysis display
            if st.session_state.sentiment_history:
                latest_sentiment = st.session_state.sentiment_history[-1]
                enhanced_ui.create_sentiment_display(latest_sentiment.polarity, latest_sentiment.emotion)

            # Performance monitoring
            performance_optimizer.create_performance_dashboard()

            # Enhanced interactive conversation metrics with all animations
            enhanced_ui.create_enhanced_conversation_metrics(st.session_state.conversation_metrics)

            # Live sentiment chart if we have sentiment history
            if len(st.session_state.sentiment_history) > 2:
                st.markdown("### 📈 Sentiment Trend")
                enhanced_ui.create_live_sentiment_chart(st.session_state.sentiment_history)

            # Accessibility toolbar
            enhanced_ui.create_accessibility_toolbar()

        # Current stage indicator (fallback for non-advanced mode)
        if not ADVANCED_FEATURES_AVAILABLE:
            stage_names = {
                0: "👤 Personal Information",
                1: "📧 Contact Details",
                2: "📞 Phone Number",
                3: "💼 Experience Level",
                4: "🎯 Desired Position",
                5: "📍 Location",
                6: "💻 Technical Skills",
                7: "🔍 Technical Assessment",
                8: "✅ Complete"
            }

            current_stage_name = stage_names.get(current_stage, "Unknown")
            st.markdown(f"""
            <div class="stage-indicator">
                <strong>Current Step:</strong><br>
                {current_stage_name}
            </div>
            """, unsafe_allow_html=True)

        # Reset conversation button
        if st.button("🔄 Start New Application"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

        # Export data button (only show if conversation is complete)
        if current_stage >= STAGES['CONCLUSION'] and st.session_state.candidate_info:
            st.subheader("📥 Export Data")
            col1, col2 = st.columns(2)

            with col1:
                if st.button("Export JSON"):
                    filename = utils.export_candidate_data(st.session_state.candidate_info, "json")
                    if filename:
                        st.success(f"Exported: {filename}")

            with col2:
                if st.button("Export CSV"):
                    filename = utils.export_candidate_data(st.session_state.candidate_info, "csv")
                    if filename:
                        st.success(f"Exported: {filename}")

        # Help section
        st.subheader("❓ Need Help?")
        st.markdown("""
        **Tips:**
        - Answer questions clearly and completely
        - For technical skills, separate multiple items with commas
        - Type 'quit' or 'exit' to end the conversation
        - Use the reset button to start over
        """)

    # Enhanced main content area
    if ADVANCED_FEATURES_AVAILABLE:
        enhanced_ui.create_animated_header(
            "TalentScout - AI Hiring Assistant",
            "Intelligent recruitment powered by advanced AI technology"
        )

        # Show simple welcome message for new users
        if not st.session_state.conversation_started:
            enhanced_ui.create_simple_welcome_message()

        # Welcome message in user's language
        welcome_text = multilingual_manager.get_translation('welcome_message', st.session_state.user_language)

        # Personalized greeting if user info available
        if st.session_state.candidate_info.get('name'):
            welcome_text = personalization_manager.get_personalized_greeting(
                st.session_state.user_preferences,
                st.session_state.candidate_info['name']
            )

            # Show personalized dashboard for returning users
            st.markdown(f"""
            <div class="info-card fade-in-up">
                <h4 style="margin: 0; color: #4CAF50;">👋 Welcome back, {st.session_state.candidate_info['name']}!</h4>
                <p style="margin: 0.5rem 0 0 0; color: #5a6c7d;">
                    {welcome_text}
                </p>
            </div>
            """, unsafe_allow_html=True)

    else:
        # Enhanced fallback header
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #4CAF50, #45a049);
                    border-radius: 15px; color: white; margin-bottom: 2rem;">
            <h1 style="margin: 0; font-size: 2.5rem;">🚀 TalentScout</h1>
            <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">
                AI Hiring Assistant
            </p>
        </div>
        """, unsafe_allow_html=True)

        if not st.session_state.conversation_started:
            st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem;
                        box-shadow: 0 5px 15px rgba(0,0,0,0.08); border-left: 4px solid #4CAF50;">
                <div style="text-align: center;">
                    <h4 style="margin: 0 0 0.5rem 0; color: #4CAF50;">👋 Welcome to TalentScout!</h4>
                    <p style="margin: 0; color: #6c757d; font-size: 1rem;">
                        I'm your AI hiring assistant. Let's get started with your application.
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Enhanced Chat interface
    chat_container = st.container()
    with chat_container:
        for i, message in enumerate(st.session_state.messages):
            with st.chat_message(message["role"]):
                # Enhanced message display with sentiment if available
                if ADVANCED_FEATURES_AVAILABLE and message["role"] == "user" and i > 0:
                    # Show sentiment for user messages (skip first assistant message)
                    sentiment_idx = (i - 1) // 2  # Adjust for assistant/user alternation
                    if sentiment_idx < len(st.session_state.sentiment_history):
                        sentiment = st.session_state.sentiment_history[sentiment_idx]
                        emoji = sentiment_analyzer.get_emotion_emoji(sentiment.emotion)
                        st.write(f"{emoji} {message['content']}")
                    else:
                        st.write(message["content"])
                else:
                    # Format message with language if available
                    if ADVANCED_FEATURES_AVAILABLE and message["role"] == "assistant":
                        formatted_message = multilingual_manager.format_message_with_language(
                            message["content"],
                            st.session_state.user_language
                        )
                        st.write(formatted_message)
                    else:
                        st.write(message["content"])

    # Enhanced User input with smart features
    input_placeholder = "Type your message here..."
    if ADVANCED_FEATURES_AVAILABLE:
        if st.session_state.user_language == 'es':
            input_placeholder = "Escribe tu mensaje aquí..."
        elif st.session_state.user_language == 'fr':
            input_placeholder = "Tapez votre message ici..."
        elif st.session_state.user_language == 'de':
            input_placeholder = "Geben Sie hier Ihre Nachricht ein..."

    # Add contextual hints based on current stage
    current_stage = st.session_state.stage
    stage_hints = {
        0: "💡 Tip: Just type your full name to get started!",
        1: "💡 Tip: Use your professional email address",
        2: "💡 Tip: Include country code if international (e.g., +1234567890)",
        3: "💡 Tip: You can say '3 years' or just '3' - I understand both!",
        4: "💡 Tip: Be specific about the role you want (e.g., 'Senior Python Developer')",
        5: "💡 Tip: You can say 'Remote' or specify a city",
        6: "💡 Tip: List technologies separated by commas (e.g., 'Python, React, AWS')"
    }

    if current_stage in stage_hints:
        st.info(stage_hints[current_stage])

    # Show smart input helpers for specific stages
    if ADVANCED_FEATURES_AVAILABLE and current_stage == 6:  # Tech stack stage
        with st.expander("🛠️ Tech Stack Builder (Optional)", expanded=False):
            try:
                from smart_input_helper import smart_input_helper
                selected_techs = smart_input_helper.create_tech_stack_builder()
                if selected_techs and st.button("Use Selected Technologies"):
                    tech_string = ", ".join(selected_techs)
                    st.session_state.messages.append({"role": "user", "content": tech_string})
                    response = process_user_input(tech_string)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.rerun()
            except ImportError:
                pass

    if user_input := st.chat_input(input_placeholder):
        # Show loading spinner for advanced features
        if ADVANCED_FEATURES_AVAILABLE:
            with st.spinner("Processing your response..."):
                time.sleep(0.5)  # Brief pause for better UX

        with st.chat_message("user"):
            st.write(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Get assistant response with performance optimization
        if ADVANCED_FEATURES_AVAILABLE:
            # Use cached response if available
            @performance_optimizer.timed_cache(ttl_seconds=300)
            def get_cached_response(input_text, stage=None):
                # Stage parameter used for cache key differentiation in decorator
                _ = stage  # Acknowledge parameter usage
                return process_user_input(input_text)

            response = get_cached_response(user_input, st.session_state.stage)
        else:
            response = process_user_input(user_input)

        # Add personalized encouragement if advanced features available
        if ADVANCED_FEATURES_AVAILABLE and st.session_state.sentiment_history:
            latest_sentiment = st.session_state.sentiment_history[-1]
            encouragement = personalization_manager.get_personalized_encouragement(
                st.session_state.user_preferences,
                latest_sentiment.polarity
            )
            if encouragement and latest_sentiment.polarity < -0.2:
                response = f"{encouragement}\n\n{response}"

        with st.chat_message("assistant"):
            st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Update completion rate
        if ADVANCED_FEATURES_AVAILABLE:
            completion_rate = min(st.session_state.stage / (len(STAGES) - 1), 1.0)
            st.session_state.conversation_metrics['completion_rate'] = completion_rate

        # Auto-scroll to bottom
        st.rerun()

if __name__ == "__main__":
    main() 