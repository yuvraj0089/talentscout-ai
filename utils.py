import re
from typing import Dict, List, Tuple, Optional
import openai
import streamlit as st
from config import (
    OPENAI_API_KEY,
    MODEL_NAME,
    EMAIL_PATTERN,
    PHONE_PATTERN,
    TECH_ASSESSMENT_PROMPT,
    EXIT_KEYWORDS,
    SYSTEM_PROMPT,
    TEMPERATURE,
    MAX_TOKENS,
    FALLBACK_QUESTIONS
)

# Initialize OpenAI client with Python 3.13 compatibility
try:
    # Setup compatibility first
    try:
        from python313_compatibility import setup_compatibility
        setup_compatibility()
    except ImportError:
        pass

    if OPENAI_API_KEY and OPENAI_API_KEY != "your_openai_api_key_here":
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
    else:
        client = None
        print("Warning: OpenAI API key not configured. Using fallback questions only.")
except Exception as e:
    print(f"Failed to initialize OpenAI client: {e}")
    print("Using fallback questions only.")
    client = None

def validate_email(email: str) -> bool:
    """Validate email format."""
    return bool(re.match(EMAIL_PATTERN, email))

def validate_phone(phone: str) -> bool:
    """Validate phone number format."""
    return bool(re.match(PHONE_PATTERN, phone))

def is_exit_command(text: str) -> bool:
    """Check if the user wants to exit the conversation."""
    return text.lower().strip() in EXIT_KEYWORDS

def validate_experience(experience: str) -> Tuple[bool, Optional[float]]:
    """Validate years of experience."""
    try:
        years = float(experience.replace('years', '').replace('year', '').strip())
        return True, years
    except ValueError:
        return False, None

def generate_technical_questions(tech_stack: List[str]) -> List[str]:
    """Generate technical questions based on the candidate's tech stack with error handling."""
    if not client:
        return get_fallback_questions(tech_stack)

    try:
        prompt = TECH_ASSESSMENT_PROMPT.format(tech_stack=", ".join(tech_stack))

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS
        )

        content = response.choices[0].message.content
        questions = [q.strip() for q in content.split('\n') if q.strip() and any(char.isalpha() for char in q)]

        # Filter out empty or invalid questions
        valid_questions = []
        for q in questions:
            if len(q) > 10 and '?' in q:  # Basic validation
                valid_questions.append(q)

        return valid_questions if valid_questions else get_fallback_questions(tech_stack)

    except Exception as e:
        st.error(f"Error generating technical questions: {e}")
        return get_fallback_questions(tech_stack)

def get_fallback_questions(tech_stack: List[str]) -> List[str]:
    """Provide fallback questions when AI generation fails."""
    fallback_questions = []

    for tech in tech_stack[:3]:  # Limit to first 3 technologies
        tech_lower = tech.lower()
        if tech_lower in FALLBACK_QUESTIONS:
            fallback_questions.extend(FALLBACK_QUESTIONS[tech_lower][:2])  # 2 questions per tech

    # Add generic questions if no specific ones found
    if not fallback_questions:
        fallback_questions = [
            f"Can you explain your experience with {tech_stack[0]}?",
            f"What projects have you worked on using {tech_stack[0]}?",
            "Describe a challenging technical problem you've solved recently.",
            "How do you stay updated with new technologies in your field?"
        ]

    return fallback_questions[:5]  # Limit to 5 questions

def format_candidate_summary(candidate_info: Dict) -> str:
    """Format candidate information for final summary."""
    summary = """
📋 Candidate Summary:
------------------------
Full Name: {name}
Email: {email}
Phone: {phone}
Experience: {experience} years
Desired Position: {position}
Location: {location}
Tech Stack: {tech_stack}

🔍 Technical Assessment:
------------------------
{technical_questions}

Thank you for completing the initial screening! Our team will review your information and get back to you soon.
    """.format(
        name=candidate_info.get('name', 'N/A'),
        email=candidate_info.get('email', 'N/A'),
        phone=candidate_info.get('phone', 'N/A'),
        experience=candidate_info.get('experience', 'N/A'),
        position=candidate_info.get('position', 'N/A'),
        location=candidate_info.get('location', 'N/A'),
        tech_stack=", ".join(candidate_info.get('tech_stack', [])),
        technical_questions="\n".join(candidate_info.get('technical_questions', []))
    )
    return summary

def parse_tech_stack(tech_input: str) -> List[str]:
    """Parse and clean the tech stack input with enhanced validation."""
    if not tech_input or not tech_input.strip():
        return []

    # Handle multiple separators
    separators = [',', ';', '|', '\n']
    for sep in separators:
        if sep in tech_input:
            tech_input = tech_input.replace(sep, ',')

    # Split and clean
    techs = [t.strip().title() for t in tech_input.split(',')]

    # Filter out empty strings and very short entries
    valid_techs = [t for t in techs if t and len(t) > 1]

    # Remove duplicates while preserving order
    seen = set()
    unique_techs = []
    for tech in valid_techs:
        tech_lower = tech.lower()
        if tech_lower not in seen:
            seen.add(tech_lower)
            unique_techs.append(tech)

    return unique_techs[:10]  # Limit to 10 technologies

def export_candidate_data(candidate_info: Dict, format_type: str = "json") -> str:
    """Export candidate data to specified format using secure data handler."""
    try:
        from data_handler import data_handler

        if format_type.lower() == "json":
            return data_handler.export_to_json(candidate_info)
        elif format_type.lower() == "csv":
            return data_handler.export_to_csv(candidate_info)
        else:
            st.error(f"Unsupported export format: {format_type}")
            return ""

    except Exception as e:
        st.error(f"Error exporting data: {e}")
        return ""

def validate_conversation_context(user_input: str, current_stage: int) -> Tuple[bool, str]:
    """Validate if user input is appropriate for current conversation stage."""
    user_input_lower = user_input.lower().strip()

    # Check for off-topic inputs
    off_topic_keywords = [
        'weather', 'sports', 'politics', 'food', 'movie', 'music',
        'game', 'celebrity', 'news', 'joke', 'story'
    ]

    if any(keyword in user_input_lower for keyword in off_topic_keywords):
        return False, "I'm here to help with your job application. Let's focus on gathering your professional information."

    # Check for inappropriate content
    inappropriate_keywords = ['hate', 'violence', 'illegal', 'drugs']
    if any(keyword in user_input_lower for keyword in inappropriate_keywords):
        return False, "Please keep our conversation professional and appropriate."

    # Stage-specific validation
    if current_stage == 1 and '@' not in user_input and len(user_input) > 5:  # Email stage
        return False, "Please provide a valid email address with @ symbol."

    return True, ""

def handle_unexpected_input(user_input: str, current_stage: int) -> str:
    """Handle unexpected or unclear user inputs with helpful responses."""
    stage_names = {
        0: "your name",
        1: "your email address",
        2: "your phone number",
        3: "your years of experience",
        4: "your desired position",
        5: "your location",
        6: "your technical skills"
    }

    # Log the unexpected input for debugging
    if len(user_input.strip()) == 0:
        return "Please provide a response. I'm waiting for your input."

    if current_stage in stage_names:
        return f"I didn't quite understand '{user_input[:50]}...'. Could you please provide {stage_names[current_stage]}?"

    return f"I'm not sure I understand '{user_input[:50]}...'. Could you please rephrase your response?"