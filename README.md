# InsightPro 💠

**InsightPro** is a premium SaaS-ready inventory management and supply chain intelligence platform built with Streamlit, Machine Learning, and AI-powered insights.

## 🎯 Overview

InsightPro provides real-time inventory visibility, predictive analytics, and AI-driven procurement recommendations to optimize supply chain operations. Built for enterprise-grade performance with a modern, intuitive UI.

### Key Features

- 📊 **Real-time Inventory Tracking** - Live stock levels with instant ML-based burn rate calculations
- 🤖 **AI-Powered Insights** - Google Gemini integration for intelligent supply chain analysis
- 📈 **Predictive Analytics** - Machine learning models predict stockout timelines
- 💾 **Data Management** - Import custom inventory data via CSV/Excel
- 🎨 **Premium UI/UX** - Modern glassmorphism design with dark mode support
- 💰 **Financial Metrics** - Total inventory value and risk assessment
- 🔴 **Status Indicators** - Critical, Warning, and Healthy status tracking
- ⚡ **Real-time Updates** - Interactive data editor with instant ML recalculation

## 🏗️ Architecture

```
InsightPro/
├── app.py                    # Main Streamlit application
├── api_bridge.py            # Google Gemini AI integration
├── style.css                # Premium UI styling
├── settings_icon.svg        # Settings button icon
├── sample_inventory_large.csv # Sample data
├── engine/
│   ├── db_manager.py        # SQLite database operations
│   └── ml_logic.py          # Machine learning models
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (API keys)
├── .gitignore              # Git ignore patterns
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Google Gemini API Key (free tier available)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/InsightPro.git
   cd InsightPro
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API Key**
   - Get your free Google Gemini API key from [Google AI Studio](https://ai.google.dev)
   - Create a `.env` file in the project root:
     ```
     GEMINI_API_KEY=your_api_key_here
     ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Access the dashboard**
   - Open your browser to `http://localhost:8503`

## 💡 Features in Detail

### Real-Time Inventory Monitoring
- View all products with current stock levels
- Edit stock quantities directly in the data grid
- Automatic ML calculation of burn rates and stockout predictions
- Color-coded status indicators (🔴 Critical, 🟡 Warning, 🟢 Healthy)

### AI-Powered Supply Chain Brief
- Click "Generate AI Brief" to get actionable insights
- AI analyzes critical items and provides procurement recommendations
- Identifies capital allocation urgency
- Suggests strategic actions with timelines

### Burn Rate Analysis
- Predicts daily stock consumption based on historical data
- Calculates remaining runway (days until stockout)
- Visual charts showing top burning products
- ML-based predictions using Linear Regression

### Data Import
- Upload custom inventory data as CSV or Excel files
- Automatic column validation and normalization
- Support for custom pricing and categorization

## 🔧 Configuration

### Environment Variables
Create a `.env` file with the following variables:

```env
GEMINI_API_KEY=your_google_gemini_api_key
```

### Database
- SQLite database: `inventory_v2.db`
- Auto-generated mock data on first run
- 15 premium office equipment items included

## 📊 API Integration

### Google Gemini API
- Model: gemini-2.5-flash (free tier optimized)
- Rate limiting: Automatic retry logic with exponential backoff
- Fallback models for reliability
- Advanced prompting for comprehensive analysis

## 🎨 UI/UX Design

### Color Scheme
- Primary Navy: `#002D5B`
- Accent Cyan: `#00AEEF`
- Background: `#F5F7FA`
- Text Dark: `#1A1F2C`

### Typography
- Headers: Montserrat (bold, modern)
- Body: Inter (clean, readable)
- Responsive design for all screen sizes

### Components
- Glassmorphic cards with backdrop blur
- Gradient backgrounds
- Smooth animations and transitions
- Dark mode compatible styling

## 🔒 Security

- Environment variables for sensitive data (API keys)
- No hardcoded credentials
- SQLite for local data storage
- Input validation for file uploads

## 📈 Machine Learning

### Burn Rate Calculation
- Linear Regression model for trend analysis
- Analyzes last 30 days of sales data
- Handles missing data gracefully
- Predicts days to stockout

### Model Details
- Algorithm: sklearn.linear_model.LinearRegression
- Feature: Time series (days since first sale)
- Target: Daily sales quantity
- Fallback: Simple average if insufficient data

## 🐛 Troubleshooting

### API Key Issues
- Verify API key is set in `.env` file
- Check API key is active and has quota remaining
- Free tier limit: 15 requests per minute
- Upgrade to paid plan for higher limits

### Database Issues
- Delete `inventory_v2.db` to reset with fresh mock data
- Check write permissions in project directory

### Streamlit Issues
- Clear Streamlit cache: `streamlit cache clear`
- Restart the application
- Check Python version compatibility

## 📝 Development

### Adding New Features
1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make changes and commit: `git commit -m "Add feature"`
3. Push to GitHub: `git push origin feature/your-feature`
4. Create a Pull Request

### Code Style
- Follow PEP 8 guidelines
- Add docstrings to functions
- Use type hints where possible
- Test changes locally before pushing

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Ensure code quality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- AI powered by [Google Generative AI](https://ai.google.dev/)
- Data visualization with [Plotly](https://plotly.com/)
- Machine Learning with [scikit-learn](https://scikit-learn.org/)

## 📧 Support

For issues, feature requests, or questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Provide detailed error messages and screenshots

## 🎯 Roadmap

- [ ] Multi-user support with authentication
- [ ] Advanced forecasting with Prophet/ARIMA
- [ ] Supplier integration APIs
- [ ] Mobile app version
- [ ] Webhook integrations
- [ ] Custom reporting
- [ ] Role-based access control (RBAC)
- [ ] Automated alerts and notifications

---

**Version:** 2.1 SaaS Edition  
**Last Updated:** January 22, 2026  
**Status:** Production Ready ✅
