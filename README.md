# 🚀 TalentScout - AI Hiring Assistant

An intelligent, AI-powered chatbot designed to streamline the initial screening process for technology candidates. TalentScout collects essential candidate information and conducts personalized technical assessments based on declared tech stacks.

![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

### Core Functionality
- 🤖 **Interactive AI Chat Interface** - Natural conversation flow using Streamlit
- 📋 **Comprehensive Data Collection** - Gathers name, contact details, experience, and more
- 💻 **Tech Stack Assessment** - Customized technical questions based on candidate's skills
- 🧠 **Context-Aware Conversations** - Maintains conversation flow and handles edge cases
- 🔒 **Secure Data Handling** - Privacy-compliant data processing and storage

### Enhanced Features
- 📊 **Live Analytics** - Real-time conversation metrics with interactive animations
- 🌍 **Multilingual Support** - 12+ languages with auto-detection
- 😊 **Sentiment Analysis** - Real-time emotion detection and response adaptation
- 🎨 **Enhanced UI** - Clean white interface with smooth animations
- 🔄 **Smart Progress Tracking** - Visual progress with completion indicators
- 📥 **Advanced Export** - JSON, CSV, and PDF export capabilities
- 🛡️ **Python 3.13 Compatibility** - Future-proof with compatibility layer
- 📱 **Mobile Optimized** - Responsive design for all devices
- 🤖 **Personalization Engine** - Adaptive responses based on user preferences
- ⚡ **Performance Monitoring** - Real-time system performance tracking

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenAI API key

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/talent-scout.git
cd talent-scout
```

2. **Create and activate virtual environment:**
```bash
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
OPENAI_API_KEY=your_openai_api_key_here
```

5. **Run the application:**
```bash
streamlit run app.py
```

6. **Open your browser** and navigate to `http://localhost:8501`

## 📁 Project Structure

```
talent-scout/
├── 📄 app.py                 # Main Streamlit application
├── ⚙️ config.py              # Configuration settings and prompts
├── 🛠️ utils.py               # Helper functions and utilities
├── 🔐 data_handler.py        # Secure data handling and export
├── 📋 requirements.txt       # Project dependencies
├── 🌍 .env.example          # Environment variables template
├── 📁 candidate_data/       # Exported candidate data (created automatically)
├── 📁 venv/                 # Virtual environment
└── 📖 README.md             # Project documentation
```

## 🔧 Technical Architecture

### Core Components

- **Frontend**: Streamlit with custom CSS styling
- **AI Engine**: OpenAI GPT-4 for natural language processing
- **Data Layer**: Secure local storage with export capabilities
- **Validation**: Comprehensive input validation and error handling

### Key Technologies

| Component | Technology | Purpose |
|-----------|------------|---------|
| UI Framework | Streamlit | Interactive web interface |
| AI Model | OpenAI GPT-4 | Natural language understanding |
| Data Processing | Python | Core application logic |
| Validation | Regex + Custom | Input validation and sanitization |
| Export | JSON/CSV | Data export functionality |

## 🎯 Usage Guide

### For Candidates

1. **Start the Application** - Open the provided URL
2. **Follow the Prompts** - Provide information step by step
3. **Answer Technical Questions** - Based on your declared tech stack
4. **Complete the Process** - Review your information summary

### For Recruiters

1. **Monitor Progress** - Use the sidebar to track application completion
2. **Export Data** - Download candidate information in preferred format
3. **Review Responses** - Analyze technical question responses
4. **Reset for New Candidates** - Use the reset button between sessions

## 🔒 Security & Privacy

### Data Protection
- ✅ **Local Storage Only** - No automatic cloud uploads
- ✅ **Data Encryption** - Sensitive data hashing capabilities
- ✅ **Privacy Compliance** - GDPR-ready data handling
- ✅ **Secure Export** - Controlled data export functionality
- ✅ **Session Management** - Secure session handling

### Privacy Notice
All candidate data is processed locally and securely. No information is shared with third parties without explicit consent.

## 🛠️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for GPT access | Yes |
| `DEBUG_MODE` | Enable debug logging | No |
| `DATA_DIRECTORY` | Custom data storage location | No |

### Customization Options

- **Tech Stack Questions** - Modify `FALLBACK_QUESTIONS` in `config.py`
- **UI Styling** - Update CSS in `app.py`
- **Conversation Flow** - Adjust stages in `config.py`
- **Validation Rules** - Modify patterns in `config.py`

## 🧪 Testing

### Running the Application

```bash
# Start the application
streamlit run app.py

# Test with sample data
# Navigate to http://localhost:8501
# Follow the conversation flow
```

### Test Scenarios

1. **Complete Application Flow**
   - Provide all required information
   - Test technical question generation
   - Verify data export functionality

2. **Error Handling**
   - Test invalid email formats
   - Test invalid phone numbers
   - Test empty responses

3. **Edge Cases**
   - Test conversation reset
   - Test exit commands
   - Test off-topic responses

## 🚀 Deployment

### Local Deployment
The application runs locally by default. Perfect for internal recruitment processes.

### Cloud Deployment (Optional)

#### Streamlit Cloud
1. Push code to GitHub
2. Connect to Streamlit Cloud
3. Add environment variables
4. Deploy

#### Docker Deployment
```bash
# Build Docker image
docker build -t talentscout .

# Run container
docker run -p 8501:8501 -e OPENAI_API_KEY=your_key talentscout
```

## 🎨 Prompt Engineering

### System Prompts
The application uses carefully crafted prompts to:
- Generate relevant technical questions
- Maintain professional conversation tone
- Handle diverse technology stacks
- Provide appropriate difficulty levels

### Key Prompt Strategies
1. **Context Awareness** - Prompts include candidate's tech stack
2. **Difficulty Scaling** - Questions adapt to experience level
3. **Comprehensive Coverage** - Multiple aspects of each technology
4. **Practical Focus** - Real-world application scenarios

## 🔧 Troubleshooting

### Common Issues

#### OpenAI API Errors
```bash
Error: Invalid API key
Solution: Check your .env file and API key validity
```

#### Import Errors
```bash
Error: Module not found
Solution: Ensure virtual environment is activated and dependencies installed
```

#### Streamlit Issues
```bash
Error: Port already in use
Solution: Use different port: streamlit run app.py --server.port 8502
```

### Debug Mode
Enable debug mode in `.env`:
```
DEBUG_MODE=True
```

## 📈 Performance Optimization

### Response Time
- Fallback questions for API failures
- Efficient prompt engineering
- Local data processing

### Scalability
- Session-based architecture
- Stateless design principles
- Efficient memory usage

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Code Style
- Follow PEP 8 guidelines
- Add docstrings to functions
- Use type hints where appropriate
- Keep functions focused and small

### Areas for Contribution
- 🌐 **Multilingual Support** - Add language options
- 📊 **Analytics Dashboard** - Candidate statistics
- 🔌 **API Integration** - Connect with ATS systems
- 🎨 **UI Enhancements** - Improve user experience
- 🧪 **Testing** - Add comprehensive test suite

## 📋 Challenges & Solutions

### Challenge 1: Dynamic Question Generation
**Problem**: Generating relevant questions for diverse tech stacks
**Solution**: Comprehensive fallback system + AI-powered generation

### Challenge 2: Conversation Context
**Problem**: Maintaining context throughout the conversation
**Solution**: State management with validation and error recovery

### Challenge 3: Data Privacy
**Problem**: Handling sensitive candidate information
**Solution**: Local storage, encryption options, and privacy controls

### Challenge 4: User Experience
**Problem**: Making the interface intuitive and professional
**Solution**: Progressive disclosure, clear feedback, and modern UI design

## 🔮 Future Enhancements

### Planned Features
- [ ] **Sentiment Analysis** - Gauge candidate emotions
- [ ] **Video Integration** - Record video responses
- [ ] **ATS Integration** - Connect with popular ATS platforms
- [ ] **Advanced Analytics** - Detailed candidate insights
- [ ] **Mobile App** - Native mobile application
- [ ] **Multi-language Support** - International candidate support

### Technical Improvements
- [ ] **Database Integration** - Persistent data storage
- [ ] **API Development** - RESTful API for integrations
- [ ] **Real-time Collaboration** - Multiple recruiter access
- [ ] **Advanced Security** - Enhanced encryption and auth

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for providing the GPT API
- Streamlit team for the excellent framework
- The open-source community for inspiration and tools

## 📞 Support

For support, questions, or feedback:
- 📧 Email: support@talentscout.ai
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/talent-scout/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/yourusername/talent-scout/discussions)

---

**Made with ❤️ for better hiring experiences**