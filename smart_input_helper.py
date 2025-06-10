"""
Smart Input Helper for TalentScout
Provides intelligent suggestions and validation for user inputs
"""

import streamlit as st
from typing import List, Dict, Optional

class SmartInputHelper:
    """Provides smart input suggestions and validation."""
    
    def __init__(self):
        self.tech_suggestions = {
            'programming_languages': [
                'Python', 'JavaScript', 'Java', 'C++', 'C#', 'TypeScript', 'Go', 'Rust',
                'PHP', 'Ruby', 'Swift', 'Kotlin', 'Scala', 'R', 'MATLAB', 'Perl'
            ],
            'frameworks': [
                'React', 'Angular', 'Vue.js', 'Django', 'Flask', 'Spring', 'Express.js',
                'Laravel', 'Ruby on Rails', 'ASP.NET', 'Flutter', 'React Native'
            ],
            'databases': [
                'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'SQLite', 'Oracle',
                'SQL Server', 'Cassandra', 'DynamoDB', 'Firebase'
            ],
            'cloud_platforms': [
                'AWS', 'Azure', 'Google Cloud', 'Heroku', 'DigitalOcean', 'Vercel'
            ],
            'tools': [
                'Git', 'Docker', 'Kubernetes', 'Jenkins', 'Terraform', 'Ansible',
                'VS Code', 'IntelliJ', 'Postman', 'Jira', 'Slack'
            ]
        }
        
        self.position_suggestions = [
            'Software Engineer', 'Frontend Developer', 'Backend Developer', 'Full Stack Developer',
            'Data Scientist', 'Data Analyst', 'Machine Learning Engineer', 'DevOps Engineer',
            'Product Manager', 'UI/UX Designer', 'QA Engineer', 'Mobile Developer',
            'Cloud Architect', 'Security Engineer', 'Technical Lead', 'Engineering Manager'
        ]
        
        self.location_suggestions = [
            'Remote', 'New York, NY', 'San Francisco, CA', 'Seattle, WA', 'Austin, TX',
            'Boston, MA', 'Chicago, IL', 'Los Angeles, CA', 'Denver, CO', 'Atlanta, GA',
            'London, UK', 'Berlin, Germany', 'Toronto, Canada', 'Sydney, Australia'
        ]
    
    def create_smart_input(self, label: str, input_type: str, placeholder: str = "", help_text: str = ""):
        """Create a smart input field with suggestions."""
        
        # Create the input field
        user_input = st.text_input(
            label,
            placeholder=placeholder,
            help=help_text,
            key=f"smart_input_{input_type}"
        )
        
        # Show suggestions based on input type
        if input_type == "tech_stack" and user_input:
            self._show_tech_suggestions(user_input)
        elif input_type == "position" and user_input:
            self._show_position_suggestions(user_input)
        elif input_type == "location" and user_input:
            self._show_location_suggestions(user_input)
        
        return user_input
    
    def _show_tech_suggestions(self, current_input: str):
        """Show technology suggestions."""
        current_techs = [tech.strip() for tech in current_input.split(',')]
        last_tech = current_techs[-1].lower() if current_techs else ""
        
        if len(last_tech) >= 2:
            suggestions = []
            
            # Find matching suggestions from all categories
            for category, techs in self.tech_suggestions.items():
                for tech in techs:
                    if last_tech in tech.lower() and tech not in current_techs:
                        suggestions.append(tech)
            
            if suggestions:
                st.markdown("💡 **Suggestions:**")
                cols = st.columns(min(len(suggestions), 4))
                for i, suggestion in enumerate(suggestions[:4]):
                    with cols[i]:
                        if st.button(suggestion, key=f"tech_suggestion_{i}"):
                            # Add suggestion to input
                            new_input = current_input.rstrip(current_techs[-1]) + suggestion
                            st.session_state[f"smart_input_tech_stack"] = new_input
                            st.rerun()
    
    def _show_position_suggestions(self, current_input: str):
        """Show position suggestions."""
        if len(current_input) >= 2:
            suggestions = [
                pos for pos in self.position_suggestions 
                if current_input.lower() in pos.lower()
            ]
            
            if suggestions:
                st.markdown("💡 **Popular Positions:**")
                cols = st.columns(min(len(suggestions), 3))
                for i, suggestion in enumerate(suggestions[:3]):
                    with cols[i]:
                        if st.button(suggestion, key=f"pos_suggestion_{i}"):
                            st.session_state[f"smart_input_position"] = suggestion
                            st.rerun()
    
    def _show_location_suggestions(self, current_input: str):
        """Show location suggestions."""
        if len(current_input) >= 2:
            suggestions = [
                loc for loc in self.location_suggestions 
                if current_input.lower() in loc.lower()
            ]
            
            if suggestions:
                st.markdown("💡 **Popular Locations:**")
                cols = st.columns(min(len(suggestions), 3))
                for i, suggestion in enumerate(suggestions[:3]):
                    with cols[i]:
                        if st.button(suggestion, key=f"loc_suggestion_{i}"):
                            st.session_state[f"smart_input_location"] = suggestion
                            st.rerun()
    
    def create_tech_stack_builder(self):
        """Create an interactive tech stack builder."""
        st.markdown("### 🛠️ Build Your Tech Stack")
        
        selected_techs = st.session_state.get('selected_techs', [])
        
        # Category tabs
        tabs = st.tabs(["💻 Languages", "🚀 Frameworks", "🗄️ Databases", "☁️ Cloud", "🔧 Tools"])
        
        with tabs[0]:
            self._create_tech_category_selector("programming_languages", "Languages", selected_techs)
        
        with tabs[1]:
            self._create_tech_category_selector("frameworks", "Frameworks", selected_techs)
        
        with tabs[2]:
            self._create_tech_category_selector("databases", "Databases", selected_techs)
        
        with tabs[3]:
            self._create_tech_category_selector("cloud_platforms", "Cloud Platforms", selected_techs)
        
        with tabs[4]:
            self._create_tech_category_selector("tools", "Tools", selected_techs)
        
        # Show selected technologies
        if selected_techs:
            st.markdown("### ✅ Your Selected Technologies:")
            
            # Display as badges
            cols = st.columns(4)
            for i, tech in enumerate(selected_techs):
                with cols[i % 4]:
                    if st.button(f"❌ {tech}", key=f"remove_tech_{i}"):
                        selected_techs.remove(tech)
                        st.session_state['selected_techs'] = selected_techs
                        st.rerun()
            
            # Convert to comma-separated string
            tech_string = ", ".join(selected_techs)
            st.text_area("Tech Stack (copy this):", value=tech_string, height=100)
        
        return selected_techs
    
    def _create_tech_category_selector(self, category: str, category_name: str, selected_techs: List[str]):
        """Create a technology category selector."""
        st.markdown(f"**{category_name}:**")
        
        techs = self.tech_suggestions.get(category, [])
        cols = st.columns(3)
        
        for i, tech in enumerate(techs):
            with cols[i % 3]:
                if tech not in selected_techs:
                    if st.button(f"➕ {tech}", key=f"add_{category}_{i}"):
                        if 'selected_techs' not in st.session_state:
                            st.session_state['selected_techs'] = []
                        st.session_state['selected_techs'].append(tech)
                        st.rerun()
                else:
                    st.success(f"✅ {tech}")
    
    def create_experience_helper(self):
        """Create an experience level helper."""
        st.markdown("### 💼 Experience Level Guide")
        
        experience_levels = {
            "0-1 years": {
                "description": "Entry Level / Recent Graduate",
                "icon": "🌱",
                "details": "New to the field, fresh graduate, or career changer"
            },
            "1-3 years": {
                "description": "Junior Developer",
                "icon": "🚀", 
                "details": "Some professional experience, learning and growing"
            },
            "3-5 years": {
                "description": "Mid-Level Developer",
                "icon": "💪",
                "details": "Solid experience, can work independently"
            },
            "5-8 years": {
                "description": "Senior Developer",
                "icon": "⭐",
                "details": "Experienced, mentors others, technical leadership"
            },
            "8+ years": {
                "description": "Expert / Lead",
                "icon": "👑",
                "details": "Highly experienced, architectural decisions, team leadership"
            }
        }
        
        cols = st.columns(len(experience_levels))
        
        for i, (years, info) in enumerate(experience_levels.items()):
            with cols[i]:
                if st.button(
                    f"{info['icon']}\n{years}\n{info['description']}", 
                    key=f"exp_level_{i}",
                    help=info['details']
                ):
                    # Extract number from years string
                    if "0-1" in years:
                        return 0.5
                    elif "1-3" in years:
                        return 2
                    elif "3-5" in years:
                        return 4
                    elif "5-8" in years:
                        return 6.5
                    else:
                        return 10
        
        return None

# Global instance
smart_input_helper = SmartInputHelper()
