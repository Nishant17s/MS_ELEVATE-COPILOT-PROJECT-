# Setup & Installation Guide

## System Requirements

- **Python:** 3.8 or higher
- **OS:** Windows, macOS, or Linux
- **RAM:** 4GB minimum (8GB recommended)
- **Disk Space:** 500MB
- **Internet:** Required for Gemini API calls

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/InsightPro.git
cd InsightPro
```

### 2. Create Virtual Environment

**On macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**On Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Get API Key

1. Visit [Google AI Studio](https://ai.google.dev/aistudio)
2. Click "Create API Key"
3. Select "Create API key in new project"
4. Copy the API key

### 5. Configure Environment

Create a `.env` file in the project root:

```bash
# Linux/macOS
cat > .env << EOF
GEMINI_API_KEY=your_api_key_here
EOF

# Windows (PowerShell)
"GEMINI_API_KEY=your_api_key_here" | Out-File -Encoding UTF8 .env
```

**IMPORTANT:** Never commit `.env` to version control!

### 6. Verify Installation

```bash
# Check Python version
python --version

# Check virtual environment
pip list

# Verify Streamlit
streamlit --version
```

### 7. Run Application

```bash
streamlit run app.py
```

The app will open at `http://localhost:8503`

## Troubleshooting

### Common Issues

#### 1. "ModuleNotFoundError: No module named 'streamlit'"

**Solution:**
```bash
# Ensure virtual environment is activated
# Then reinstall dependencies
pip install -r requirements.txt
```

#### 2. "GEMINI_API_KEY not found"

**Solution:**
- Verify `.env` file exists in project root
- Check file is not in `.venv` or other subdirectories
- Reload Streamlit: `streamlit cache clear` then restart

#### 3. "Port 8503 already in use"

**Solution:**
```bash
# Use different port
streamlit run app.py --server.port=8504
```

#### 4. Database Error: "database is locked"

**Solution:**
```bash
# Delete database and restart (mock data will regenerate)
rm inventory_v2.db
streamlit run app.py
```

#### 5. Slow Performance

**Solutions:**
- Check API rate limits (free tier: 15 req/min)
- Upgrade Python version to 3.11+
- Increase RAM allocation
- Clear Streamlit cache: `streamlit cache clear`

## Development Setup

### Install Development Dependencies

```bash
pip install pytest pytest-cov flake8 black
```

### Code Quality Checks

```bash
# Format code
black *.py engine/*.py

# Lint code
flake8 *.py engine/*.py

# Run tests
pytest -v
```

## Docker Setup (Optional)

### Build Docker Image

```bash
docker build -t insightpro:latest .
```

### Run with Docker

```bash
docker run -p 8503:8503 \
  -e GEMINI_API_KEY=your_api_key \
  insightpro:latest
```

## Advanced Configuration

### Custom Streamlit Config

Create `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#002D5B"
backgroundColor = "#F5F7FA"
secondaryBackgroundColor = "#FFFFFF"
textColor = "#1A1F2C"
font = "sans serif"

[client]
showErrorDetails = true
toolbarMode = "developer"

[server]
maxUploadSize = 50
port = 8503
```

### Environment Variables

Available configuration options:

```bash
# API Configuration
GEMINI_API_KEY=your_key_here

# Database
DB_NAME=inventory_v2.db

# Streamlit
STREAMLIT_SERVER_PORT=8503
STREAMLIT_SERVER_HEADLESS=true
```

## Production Deployment

### Using Streamlit Cloud

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect GitHub repository
4. Add secrets (GEMINI_API_KEY) in app settings
5. Deploy!

### Using Docker & Cloud Run (GCP)

```bash
# Build image
docker build -t gcr.io/PROJECT_ID/insightpro:latest .

# Push to GCP
docker push gcr.io/PROJECT_ID/insightpro:latest

# Deploy
gcloud run deploy insightpro \
  --image gcr.io/PROJECT_ID/insightpro:latest \
  --platform managed \
  --region us-central1
```

### Using Heroku

```bash
# Create Heroku app
heroku create your-app-name

# Add buildpack
heroku buildpacks:add heroku/python

# Set environment variables
heroku config:set GEMINI_API_KEY=your_key

# Deploy
git push heroku main
```

## Performance Optimization

### Database Optimization
- Add indexes to frequently queried columns
- Archive old sales data (>1 year)
- Regular database cleanup

### API Optimization
- Implement caching for AI responses (24h TTL)
- Batch API calls where possible
- Use streaming for large responses

### UI Optimization
- Lazy load charts
- Cache Streamlit widgets
- Use `st.cache_data` for expensive operations

## Monitoring & Logging

### Enable Debug Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Monitor API Usage

```bash
# Check Gemini API quota
# Visit: https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com
```

### Application Logs

```bash
# View Streamlit logs
tail -f ~/.streamlit/logs/2024-01-*.log
```

## Security Best Practices

1. **Never commit sensitive data**
   - Use `.env` with `.gitignore`
   - Use environment variables in production

2. **API Key Rotation**
   - Rotate keys every 90 days
   - Use separate keys for dev/prod

3. **Database Security**
   - Restrict database file permissions
   - Use encrypted backups in production

4. **Input Validation**
   - Validate all file uploads
   - Sanitize user inputs

## Support & Help

- **Documentation:** See [README.md](README.md)
- **Issues:** Open on GitHub
- **Questions:** Start a discussion

---

**Last Updated:** January 22, 2026
**Status:** Production Ready ✅
