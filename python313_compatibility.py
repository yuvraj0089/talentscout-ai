"""
Python 3.13 Compatibility Module
Provides compatibility fixes for modules that were removed in Python 3.13
"""

import sys
import warnings

def setup_compatibility():
    """Set up compatibility for Python 3.13."""
    
    # Check Python version
    if sys.version_info >= (3, 13):
        print("🔧 Setting up Python 3.13 compatibility...")
        
        # Create a mock cgi module for backward compatibility
        try:
            import cgi
        except ImportError:
            # Create a minimal cgi module replacement
            class MockCGI:
                def escape(self, s, quote=False):
                    """Escape HTML characters."""
                    s = s.replace("&", "&amp;")
                    s = s.replace("<", "&lt;")
                    s = s.replace(">", "&gt;")
                    if quote:
                        s = s.replace('"', "&quot;")
                        s = s.replace("'", "&#x27;")
                    return s
                
                def parse_qs(self, qs, keep_blank_values=False, strict_parsing=False):
                    """Parse query string (basic implementation)."""
                    from urllib.parse import parse_qs as urllib_parse_qs
                    return urllib_parse_qs(qs, keep_blank_values, strict_parsing)
            
            # Add mock cgi to sys.modules
            sys.modules['cgi'] = MockCGI()
            print("✅ Created cgi module compatibility layer")
        
        # Suppress specific warnings for Python 3.13
        warnings.filterwarnings("ignore", category=DeprecationWarning, module=".*cgi.*")
        warnings.filterwarnings("ignore", category=DeprecationWarning, module=".*imp.*")
        
        print("✅ Python 3.13 compatibility setup complete")
    
    return True

def check_dependencies():
    """Check and fix dependency issues."""
    
    # Check for problematic packages
    problematic_packages = []
    
    try:
        import googletrans
    except ImportError:
        problematic_packages.append("googletrans")
    except Exception as e:
        if "cgi" in str(e):
            problematic_packages.append("googletrans (cgi compatibility issue)")
    
    if problematic_packages:
        print(f"⚠️  Problematic packages detected: {', '.join(problematic_packages)}")
        print("💡 Using fallback implementations for compatibility")
        return False
    
    return True

def install_compatible_packages():
    """Install Python 3.13 compatible packages."""
    import subprocess
    import sys
    
    compatible_packages = [
        "streamlit>=1.32.0",
        "openai>=1.0.0", 
        "textblob>=0.17.1",
        "langdetect>=1.0.9",
        "plotly>=5.19.0",
        "pandas>=2.2.1",
        "numpy>=1.26.4"
    ]
    
    print("📦 Installing Python 3.13 compatible packages...")
    
    for package in compatible_packages:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", package], 
                         check=True, capture_output=True)
            print(f"✅ Installed: {package}")
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Warning: Could not install {package}")
    
    print("✅ Package installation complete")

def get_fallback_translation(text: str, target_lang: str) -> str:
    """Provide fallback translation without external dependencies."""
    
    # Basic translation dictionary for common phrases
    translations = {
        'es': {
            'welcome': 'bienvenido',
            'hello': 'hola',
            'thank you': 'gracias',
            'goodbye': 'adiós',
            'name': 'nombre',
            'email': 'correo electrónico',
            'phone': 'teléfono',
            'experience': 'experiencia',
            'position': 'posición',
            'location': 'ubicación'
        },
        'fr': {
            'welcome': 'bienvenue',
            'hello': 'bonjour',
            'thank you': 'merci',
            'goodbye': 'au revoir',
            'name': 'nom',
            'email': 'e-mail',
            'phone': 'téléphone',
            'experience': 'expérience',
            'position': 'position',
            'location': 'emplacement'
        },
        'de': {
            'welcome': 'willkommen',
            'hello': 'hallo',
            'thank you': 'danke',
            'goodbye': 'auf wiedersehen',
            'name': 'name',
            'email': 'e-mail',
            'phone': 'telefon',
            'experience': 'erfahrung',
            'position': 'position',
            'location': 'standort'
        }
    }
    
    if target_lang in translations:
        text_lower = text.lower()
        for english, translated in translations[target_lang].items():
            text = text.replace(english, translated)
            text = text.replace(english.title(), translated.title())
    
    return text

def safe_import(module_name: str, fallback=None):
    """Safely import a module with fallback."""
    try:
        return __import__(module_name)
    except ImportError as e:
        if "cgi" in str(e) or "imp" in str(e):
            print(f"⚠️  {module_name} has Python 3.13 compatibility issues, using fallback")
            return fallback
        else:
            raise e

# Auto-setup compatibility when module is imported
if __name__ != "__main__":
    setup_compatibility()
