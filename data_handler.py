"""
Data handling and security module for TalentScout hiring assistant.
Handles secure data storage, validation, and export functionality.
"""

import json
import csv
import hashlib
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
import streamlit as st


class SecureDataHandler:
    """Handles secure data operations for candidate information."""
    
    def __init__(self):
        self.data_dir = "candidate_data"
        self.ensure_data_directory()
    
    def ensure_data_directory(self):
        """Create data directory if it doesn't exist."""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def hash_sensitive_data(self, data: str) -> str:
        """Hash sensitive data for privacy."""
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def sanitize_candidate_data(self, candidate_info: Dict) -> Dict:
        """Sanitize candidate data for storage/export."""
        sanitized = candidate_info.copy()
        
        # Add timestamp
        sanitized['submission_time'] = datetime.now().isoformat()
        
        # Hash email for privacy (optional)
        if 'email' in sanitized:
            sanitized['email_hash'] = self.hash_sensitive_data(sanitized['email'])
        
        # Ensure tech stack is properly formatted
        if 'tech_stack' in sanitized and isinstance(sanitized['tech_stack'], list):
            sanitized['tech_stack'] = [tech.strip() for tech in sanitized['tech_stack']]
        
        return sanitized
    
    def export_to_json(self, candidate_info: Dict, filename: Optional[str] = None) -> str:
        """Export candidate data to JSON format."""
        try:
            sanitized_data = self.sanitize_candidate_data(candidate_info)
            
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                candidate_name = candidate_info.get('name', 'candidate').replace(' ', '_')
                filename = f"candidate_{candidate_name}_{timestamp}.json"
            
            filepath = os.path.join(self.data_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(sanitized_data, f, indent=2, ensure_ascii=False)
            
            return filepath
            
        except Exception as e:
            st.error(f"Error exporting to JSON: {e}")
            return ""
    
    def export_to_csv(self, candidate_info: Dict, filename: Optional[str] = None) -> str:
        """Export candidate data to CSV format."""
        try:
            sanitized_data = self.sanitize_candidate_data(candidate_info)
            
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                candidate_name = candidate_info.get('name', 'candidate').replace(' ', '_')
                filename = f"candidate_{candidate_name}_{timestamp}.csv"
            
            filepath = os.path.join(self.data_dir, filename)
            
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Field', 'Value'])
                
                for key, value in sanitized_data.items():
                    if isinstance(value, list):
                        value = ', '.join(map(str, value))
                    elif isinstance(value, dict):
                        value = json.dumps(value)
                    writer.writerow([key, value])
            
            return filepath
            
        except Exception as e:
            st.error(f"Error exporting to CSV: {e}")
            return ""
    
    def validate_data_completeness(self, candidate_info: Dict) -> tuple[bool, List[str]]:
        """Validate that all required fields are present."""
        required_fields = ['name', 'email', 'phone', 'experience', 'position', 'location', 'tech_stack']
        missing_fields = []
        
        for field in required_fields:
            if field not in candidate_info or not candidate_info[field]:
                missing_fields.append(field)
        
        return len(missing_fields) == 0, missing_fields
    
    def generate_candidate_report(self, candidate_info: Dict) -> str:
        """Generate a comprehensive candidate report."""
        is_complete, missing_fields = self.validate_data_completeness(candidate_info)
        
        report = f"""
# Candidate Assessment Report
Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Personal Information
- **Name**: {candidate_info.get('name', 'N/A')}
- **Email**: {candidate_info.get('email', 'N/A')}
- **Phone**: {candidate_info.get('phone', 'N/A')}
- **Location**: {candidate_info.get('location', 'N/A')}

## Professional Information
- **Experience**: {candidate_info.get('experience', 'N/A')} years
- **Desired Position**: {candidate_info.get('position', 'N/A')}
- **Technical Skills**: {', '.join(candidate_info.get('tech_stack', []))}

## Technical Assessment
### Questions Asked:
"""
        
        questions = candidate_info.get('technical_questions', [])
        for i, question in enumerate(questions, 1):
            report += f"{i}. {question}\n"
        
        report += f"\n### Candidate Responses:\n{candidate_info.get('technical_answers', 'No responses provided')}\n"
        
        if not is_complete:
            report += f"\n## ⚠️ Missing Information\nThe following fields are incomplete: {', '.join(missing_fields)}\n"
        
        report += "\n## Next Steps\n- Review technical responses\n- Schedule follow-up interview if qualified\n- Contact candidate with decision\n"
        
        return report
    
    def save_candidate_session(self, candidate_info: Dict) -> bool:
        """Save candidate session data securely."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            session_id = self.hash_sensitive_data(f"{candidate_info.get('email', 'unknown')}_{timestamp}")
            
            session_data = {
                'session_id': session_id,
                'candidate_data': self.sanitize_candidate_data(candidate_info),
                'report': self.generate_candidate_report(candidate_info)
            }
            
            filename = f"session_{session_id}.json"
            filepath = os.path.join(self.data_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            st.error(f"Error saving session: {e}")
            return False
    
    def get_data_privacy_notice(self) -> str:
        """Return data privacy notice."""
        return """
## 🔒 Data Privacy Notice

Your privacy is important to us. Here's how we handle your data:

- **Local Storage**: All data is stored locally on this system
- **No Cloud Upload**: Your information is not automatically uploaded to external servers
- **Secure Handling**: Sensitive data is processed securely
- **Data Control**: You can export or delete your data at any time
- **Compliance**: We follow data privacy best practices

By continuing, you consent to the collection and processing of your information for recruitment purposes.
        """


# Global instance for easy access
data_handler = SecureDataHandler()
