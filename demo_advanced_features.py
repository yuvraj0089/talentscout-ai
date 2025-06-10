#!/usr/bin/env python3
"""
TalentScout Advanced Features Demo
Interactive demonstration of all advanced capabilities
"""

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def demo_sentiment_analysis():
    """Demonstrate sentiment analysis capabilities."""
    print("🧠 SENTIMENT ANALYSIS DEMO")
    print("=" * 50)
    
    from sentiment_analyzer import sentiment_analyzer
    
    test_inputs = [
        ("I'm really excited about this Python developer role!", "Positive/Excited"),
        ("I'm not sure if I have enough experience for this position.", "Nervous/Uncertain"),
        ("I have 5 years of experience in software development.", "Neutral/Professional"),
        ("This is challenging, but I think I can handle it.", "Confident/Determined"),
        ("I'm frustrated with my current job situation.", "Negative/Frustrated")
    ]
    
    for text, expected in test_inputs:
        result = sentiment_analyzer.analyze_sentiment(text)
        emoji = sentiment_analyzer.get_emotion_emoji(result.emotion)
        encouragement = sentiment_analyzer.get_encouragement_message(result)
        
        print(f"\n📝 Input: \"{text}\"")
        print(f"🎯 Expected: {expected}")
        print(f"{emoji} Detected: {result.emotion.title()} (polarity: {result.polarity:.2f})")
        print(f"💬 Response: {encouragement}")
        time.sleep(1)

def demo_multilingual_support():
    """Demonstrate multilingual capabilities."""
    print("\n\n🌍 MULTILINGUAL SUPPORT DEMO")
    print("=" * 50)
    
    from multilingual_support import multilingual_manager
    
    test_phrases = [
        ("Hello, I'm interested in the software developer position.", "en"),
        ("Hola, estoy interesado en el puesto de desarrollador.", "es"),
        ("Bonjour, je suis intéressé par le poste de développeur.", "fr"),
        ("Hallo, ich interessiere mich für die Entwicklerposition.", "de"),
        ("مرحبا، أنا مهتم بمنصب المطور.", "ar")
    ]
    
    for phrase, expected_lang in test_phrases:
        detected = multilingual_manager.detect_language(phrase)
        flag = multilingual_manager.supported_languages.get(detected, {}).flag if detected in multilingual_manager.supported_languages else "🏳️"
        
        print(f"\n📝 Input: \"{phrase}\"")
        print(f"🎯 Expected: {expected_lang}")
        print(f"{flag} Detected: {detected}")
        
        # Show translation of welcome message
        welcome = multilingual_manager.get_translation('welcome_message', detected)
        print(f"💬 Welcome: {welcome[:60]}...")
        time.sleep(1)

def demo_personalization():
    """Demonstrate personalization features."""
    print("\n\n🎯 PERSONALIZATION DEMO")
    print("=" * 50)
    
    from personalization import personalization_manager, UserPreferences
    
    # Demo different communication styles
    styles = ['casual', 'professional', 'formal']
    
    for style in styles:
        preferences = UserPreferences(communication_style=style)
        greeting = personalization_manager.get_personalized_greeting(preferences, "Alex")
        encouragement = personalization_manager.get_personalized_encouragement(preferences, 0.3)
        
        print(f"\n🎨 Style: {style.title()}")
        print(f"👋 Greeting: {greeting}")
        print(f"💪 Encouragement: {encouragement}")
        time.sleep(1)
    
    # Demo difficulty adaptation
    print(f"\n🎓 DIFFICULTY ADAPTATION")
    experience_levels = [1, 3, 7]
    
    for years in experience_levels:
        preferences = UserPreferences(question_difficulty='adaptive')
        difficulty_prompt = personalization_manager.adapt_question_difficulty(preferences, years)
        
        print(f"\n📊 Experience: {years} years")
        print(f"🎯 Adaptation: {difficulty_prompt}")
        time.sleep(1)

def demo_performance_optimization():
    """Demonstrate performance optimization."""
    print("\n\n⚡ PERFORMANCE OPTIMIZATION DEMO")
    print("=" * 50)
    
    from performance_optimizer import performance_optimizer
    
    # Demo caching
    @performance_optimizer.timed_cache(ttl_seconds=60)
    def expensive_operation(x):
        time.sleep(0.1)  # Simulate expensive operation
        return x ** 2
    
    print("🔄 Testing caching performance...")
    
    # First call (not cached)
    start_time = time.time()
    result1 = expensive_operation(10)
    time1 = time.time() - start_time
    
    # Second call (cached)
    start_time = time.time()
    result2 = expensive_operation(10)
    time2 = time.time() - start_time
    
    print(f"📊 First call: {time1:.3f}s (not cached)")
    print(f"📊 Second call: {time2:.3f}s (cached)")
    print(f"🚀 Speed improvement: {time1/time2:.1f}x faster")
    
    # Show performance report
    report = performance_optimizer.get_performance_report()
    print(f"\n📈 Performance Report:")
    print(f"   Cache size: {report['cache_size']} entries")
    print(f"   Cache hit ratio: {report['cache_hit_ratio']:.2%}")
    print(f"   Memory usage: {report['memory_usage']['total_bytes']/1024:.1f} KB")

def demo_integration():
    """Demonstrate feature integration."""
    print("\n\n🔗 FEATURE INTEGRATION DEMO")
    print("=" * 50)
    
    from sentiment_analyzer import sentiment_analyzer
    from multilingual_support import multilingual_manager
    from personalization import personalization_manager, UserPreferences
    
    # Simulate a complete interaction
    scenarios = [
        {
            "input": "¡Estoy muy emocionado por esta oportunidad de trabajo en Python!",
            "name": "Carlos",
            "style": "casual"
        },
        {
            "input": "I'm a bit nervous about the technical questions.",
            "name": "Sarah", 
            "style": "professional"
        },
        {
            "input": "Je suis confiant dans mes compétences en développement.",
            "name": "Pierre",
            "style": "formal"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n🎬 Scenario {i}: {scenario['name']}")
        print(f"📝 Input: \"{scenario['input']}\"")
        
        # Step 1: Detect language
        language = multilingual_manager.detect_language(scenario['input'])
        flag = multilingual_manager.supported_languages.get(language, {}).flag if language in multilingual_manager.supported_languages else "🏳️"
        print(f"🌍 Language: {flag} {language}")
        
        # Step 2: Analyze sentiment
        sentiment = sentiment_analyzer.analyze_sentiment(scenario['input'])
        emoji = sentiment_analyzer.get_emotion_emoji(sentiment.emotion)
        print(f"🧠 Sentiment: {emoji} {sentiment.emotion} ({sentiment.polarity:.2f})")
        
        # Step 3: Generate personalized response
        preferences = UserPreferences(communication_style=scenario['style'])
        greeting = personalization_manager.get_personalized_greeting(preferences, scenario['name'])
        encouragement = personalization_manager.get_personalized_encouragement(preferences, sentiment.polarity)
        
        print(f"🎯 Style: {scenario['style']}")
        print(f"👋 Response: {greeting}")
        print(f"💬 Encouragement: {encouragement}")
        
        time.sleep(2)

def main():
    """Run the complete advanced features demo."""
    print("🚀 TALENTSCOUT ADVANCED FEATURES DEMO")
    print("=" * 60)
    print("Welcome to the interactive demonstration of TalentScout's")
    print("cutting-edge AI-powered recruitment features!")
    print("=" * 60)
    
    try:
        # Run all demos
        demo_sentiment_analysis()
        demo_multilingual_support()
        demo_personalization()
        demo_performance_optimization()
        demo_integration()
        
        print("\n\n🎉 DEMO COMPLETE!")
        print("=" * 60)
        print("✅ All advanced features demonstrated successfully!")
        print("\n🚀 Ready to revolutionize your hiring process?")
        print("   Run: streamlit run app.py")
        print("\n📚 Learn more:")
        print("   • Read ADVANCED_FEATURES.md for detailed documentation")
        print("   • Run test_advanced_features.py for comprehensive testing")
        print("   • Check README.md for setup instructions")
        
    except ImportError as e:
        print(f"\n❌ Demo failed: Missing dependencies")
        print(f"Error: {e}")
        print("\n💡 To fix this:")
        print("   pip install textblob langdetect plotly")
        print("   python test_advanced_features.py")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        print("\n💡 Please check your installation and try again")

if __name__ == "__main__":
    main()
