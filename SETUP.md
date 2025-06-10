# 🚀 TalentScout Setup Guide

## Quick Start (5 minutes)

### 1. Environment Setup
```bash
# Activate virtual environment
source venv/bin/activate

# Install/upgrade dependencies
pip install --upgrade openai
pip install -r requirements.txt
```

### 2. Configure API Key
```bash
# Copy environment template
cp .env.example .env

# Edit .env file and add your OpenAI API key
# Replace 'your_openai_api_key_here' with your actual API key
```

### 3. Test the Application
```bash
# Run tests to verify everything works
python test_app.py

# Should show: "🎉 All tests passed! The application is ready to run."
```

### 4. Launch the App
```bash
# Start the Streamlit application
streamlit run app.py

# Or use the automated startup script
python run_app.py
```

### 5. Access the Application
- Open your browser to: `http://localhost:8501`
- The app should load with the TalentScout interface

## Troubleshooting

### Common Issues

#### 1. OpenAI API Error
```
Error: Failed to initialize OpenAI client
```
**Solution**: 
- Check your `.env` file has the correct API key
- Ensure the API key is valid and has credits
- The app will work with fallback questions if API fails

#### 2. Streamlit Page Config Error
```
StreamlitAPIException: set_page_config() can only be called once
```
**Solution**: 
- This has been fixed in the latest version
- Restart the app if you see this error

#### 3. Import Errors
```
ModuleNotFoundError: No module named 'openai'
```
**Solution**:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

#### 4. Port Already in Use
```
Error: Port 8501 is already in use
```
**Solution**:
```bash
streamlit run app.py --server.port 8502
```

### Testing Without OpenAI API

The application works without an OpenAI API key using fallback questions:

1. Leave the API key empty in `.env`
2. The app will automatically use predefined technical questions
3. All other features work normally

### Features Available

✅ **Working Features**:
- Interactive chat interface
- Candidate information collection
- Technical question generation (AI + fallback)
- Data validation and error handling
- Progress tracking
- Data export (JSON/CSV)
- Conversation reset
- Professional UI

### Performance Notes

- **Response Time**: 1-3 seconds with OpenAI API
- **Fallback Mode**: Instant responses
- **Memory Usage**: ~50MB typical
- **Browser Compatibility**: All modern browsers

### Development Mode

For development and testing:

```bash
# Enable debug mode
echo "DEBUG_MODE=True" >> .env

# Run with auto-reload
streamlit run app.py --server.runOnSave true
```

### Production Deployment

For production use:

1. **Environment Variables**:
   - Set `OPENAI_API_KEY` securely
   - Configure `DATA_DIRECTORY` for data storage
   - Set `DEBUG_MODE=False`

2. **Security**:
   - Use HTTPS in production
   - Implement proper authentication if needed
   - Regular backup of candidate data

3. **Scaling**:
   - Consider using Streamlit Cloud or Docker
   - Monitor API usage and costs
   - Implement rate limiting if needed

## Support

If you encounter issues:

1. **Check the test suite**: `python test_app.py`
2. **Review logs**: Check terminal output for errors
3. **Verify environment**: Ensure virtual environment is activated
4. **Update dependencies**: `pip install --upgrade -r requirements.txt`

## Next Steps

Once the app is running:

1. **Test the full flow**: Complete a candidate application
2. **Try different tech stacks**: Test question generation
3. **Export data**: Test JSON/CSV export functionality
4. **Customize**: Modify questions in `config.py` as needed

---

**Ready to hire better? Let's go! 🚀**
