from decouple import config

# API Configuration
OPENAI_API_KEY = config('OPENAI_API_KEY')

# Model Configuration
MODEL_NAME = "gpt-4-turbo-preview"
TEMPERATURE = 0.7
MAX_TOKENS = 1000

# System Prompts
SYSTEM_PROMPT = """You are a technical interviewer for TalentScout, a technology recruitment agency. 
Your role is to generate relevant and challenging technical questions based on candidates' tech stacks.
Focus on fundamental understanding, practical application, and problem-solving abilities."""

# Chatbot Configuration
INITIAL_PROMPT = """You are an AI Hiring Assistant for TalentScout, a technology recruitment agency. 
Your role is to conduct initial candidate screenings professionally and effectively. 
Maintain a friendly yet professional tone throughout the conversation."""

# System Messages
WELCOME_MESSAGE = """Welcome to TalentScout! 👋 
I'm your AI Hiring Assistant, and I'll be helping you with the initial screening process. 
I'll collect some information about you and ask relevant technical questions based on your expertise.
Let's get started! Could you please tell me your full name?"""

# Interview Stages
STAGES = {
    'NAME': 0,
    'EMAIL': 1,
    'PHONE': 2,
    'EXPERIENCE': 3,
    'POSITION': 4,
    'LOCATION': 5,
    'TECH_STACK': 6,
    'TECHNICAL_QUESTIONS': 7,
    'CONCLUSION': 8
}

# Questions for each stage
STAGE_QUESTIONS = {
    'EMAIL': "Great! Could you please provide your email address?",
    'PHONE': "Thank you! What's the best phone number to reach you?",
    'EXPERIENCE': "How many years of professional experience do you have?",
    'POSITION': "What position(s) are you interested in?",
    'LOCATION': "What is your current location?",
    'TECH_STACK': "Please list the technologies you're proficient in (programming languages, frameworks, databases, tools, etc.):",
}

# Enhanced technical assessment prompt
TECH_ASSESSMENT_PROMPT = """Based on the candidate's tech stack: {tech_stack}

Generate exactly 4-5 relevant technical questions that:
1. Assess fundamental understanding of core concepts
2. Test practical application and real-world usage
3. Evaluate problem-solving and debugging abilities
4. Explore best practices and optimization techniques

Requirements:
- Each question should be specific to the mentioned technologies
- Questions should be appropriate for different experience levels
- Include both theoretical and practical aspects
- Format as a numbered list with clear, concise questions
- Each question should end with a question mark

Example format:
1. [Specific technical question about technology X]?
2. [Practical scenario question about technology Y]?
"""

# Exit keywords
EXIT_KEYWORDS = ['quit', 'exit', 'bye', 'goodbye', 'end', 'stop', 'finish', 'done']

# Validation patterns
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
PHONE_PATTERN = r'^\+?1?\d{9,15}$'

# Fallback technical questions for common technologies
FALLBACK_QUESTIONS = {
    'python': [
        "What are the key differences between lists and tuples in Python?",
        "How do you handle exceptions in Python and why is it important?",
        "Explain the concept of decorators in Python with an example.",
        "What is the difference between '==' and 'is' operators in Python?"
    ],
    'javascript': [
        "What is the difference between 'let', 'const', and 'var' in JavaScript?",
        "How do you handle asynchronous operations in JavaScript?",
        "Explain event bubbling and event capturing in JavaScript.",
        "What are closures in JavaScript and how are they useful?"
    ],
    'react': [
        "What is the difference between state and props in React?",
        "How do you optimize React component performance?",
        "Explain the React component lifecycle methods.",
        "What are React Hooks and why were they introduced?"
    ],
    'node.js': [
        "What is the event loop in Node.js and how does it work?",
        "How do you handle file operations in Node.js?",
        "What are the differences between Node.js and browser JavaScript?",
        "How do you manage dependencies in a Node.js project?"
    ],
    'sql': [
        "What is the difference between INNER JOIN and LEFT JOIN?",
        "How do you optimize a slow-performing SQL query?",
        "Explain the concept of database normalization.",
        "What are indexes and how do they improve query performance?"
    ],
    'java': [
        "What is the difference between abstract classes and interfaces in Java?",
        "How does garbage collection work in Java?",
        "Explain the concept of polymorphism in Java.",
        "What are the main principles of Object-Oriented Programming?"
    ],
    'aws': [
        "What are the main differences between EC2, ECS, and Lambda?",
        "How do you secure data in AWS S3 buckets?",
        "Explain the concept of Auto Scaling in AWS.",
        "What is the difference between RDS and DynamoDB?"
    ],
    'docker': [
        "What is the difference between a Docker image and a container?",
        "How do you optimize Docker image size?",
        "Explain the purpose of a Dockerfile.",
        "What are the benefits of using Docker in development?"
    ]
}