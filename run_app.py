#!/usr/bin/env python3
"""
Startup script for TalentScout AI Hiring Assistant
Handles environment setup and launches the Streamlit app
"""

import os
import sys
import subprocess
from pathlib import Path

def check_environment():
    """Check if the environment is properly set up."""
    print("🔍 Checking environment setup...")
    
    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  .env file not found. Creating from template...")
        env_example = Path(".env.example")
        if env_example.exists():
            import shutil
            shutil.copy(".env.example", ".env")
            print("✅ Created .env file from template")
            print("📝 Please edit .env file and add your OpenAI API key")
            return False
        else:
            print("❌ .env.example file not found")
            return False
    
    # Check if OpenAI API key is set
    from decouple import config
    try:
        api_key = config('OPENAI_API_KEY', default='')
        if not api_key or api_key == 'your_openai_api_key_here':
            print("⚠️  OpenAI API key not configured in .env file")
            print("📝 Please edit .env file and add your OpenAI API key")
            print("💡 The app will work with fallback questions only")
        else:
            print("✅ OpenAI API key configured")
    except Exception as e:
        print(f"⚠️  Error reading .env file: {e}")
    
    return True

def install_dependencies():
    """Install required dependencies."""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def run_tests():
    """Run basic tests to verify setup."""
    print("🧪 Running basic tests...")
    try:
        result = subprocess.run([sys.executable, "test_app.py"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ All tests passed")
            return True
        else:
            print("⚠️  Some tests failed, but app may still work")
            print("📝 Check test output for details")
            return True  # Allow app to run even if tests fail
    except Exception as e:
        print(f"⚠️  Could not run tests: {e}")
        return True  # Allow app to run even if tests can't run

def launch_app():
    """Launch the Streamlit app."""
    print("🚀 Launching TalentScout AI Hiring Assistant...")
    print("📱 The app will open in your default browser")
    print("🔗 URL: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the app")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n👋 TalentScout app stopped. Thank you!")
    except Exception as e:
        print(f"❌ Failed to launch app: {e}")
        print("💡 Try running manually: streamlit run app.py")

def main():
    """Main function to set up and run the application."""
    print("🚀 TalentScout AI Hiring Assistant - Startup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("app.py").exists():
        print("❌ app.py not found. Please run this script from the project directory.")
        sys.exit(1)
    
    # Check environment setup
    if not check_environment():
        print("\n📝 Please configure your environment and run again.")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Failed to install dependencies. Please check your Python environment.")
        sys.exit(1)
    
    # Run tests
    run_tests()
    
    # Launch the app
    print("\n" + "=" * 50)
    launch_app()

if __name__ == "__main__":
    main()
