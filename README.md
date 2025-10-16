# 📊 Trading Journal - Django Web Application

A comprehensive trading journal web application built with Django to help traders track their performance, analyze patterns, and improve their trading strategies.

## 🎯 Features

### Core Functionality
- **Trade Management**: Add, edit, delete, and view all your trades
- **Performance Analytics**: Comprehensive dashboard with charts and metrics
- **Weekly & Monthly Reviews**: Structured review system for continuous improvement
- **Screenshot Upload**: Visual documentation of your trades
- **Advanced Filtering**: Filter trades by symbol, type, date, and profitability

### Analytics & Insights
- **Win Rate Analysis**: Track your success rate over time
- **P&L Tracking**: Monitor profit and loss with detailed breakdowns
- **Setup Performance**: Analyze which trading setups work best for you
- **Risk-Reward Analysis**: Calculate and track risk-reward ratios
- **Confidence Level Tracking**: Correlate confidence with performance

### User Experience
- **Modern UI**: Clean, responsive design with Tailwind CSS
- **Interactive Charts**: Visual representation of your trading data
- **Mobile Friendly**: Works seamlessly on desktop and mobile devices
- **User Authentication**: Secure login and registration system

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project**
   ```bash
   cd trading_journey
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example environment file
   cp env_example.txt .env
   
   # Edit .env file with your settings
   # Generate a new SECRET_KEY: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

5. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Open your browser and go to `http://127.0.0.1:8000`
   - Register a new account or login with your superuser credentials

## 📁 Project Structure

```
trading_journey/
├── trading_journal/          # Django project settings
│   ├── settings.py          # Main configuration
│   ├── urls.py              # URL routing
│   └── wsgi.py              # WSGI configuration
├── journal/                 # Main application
│   ├── models.py            # Database models
│   ├── views.py             # View logic
│   ├── forms.py             # Django forms
│   ├── urls.py              # App URL patterns
│   └── admin.py             # Admin interface
├── templates/               # HTML templates
│   ├── base.html            # Base template
│   ├── registration/        # Auth templates
│   └── journal/             # App templates
├── static/                  # Static files
│   ├── css/                 # Custom styles
│   └── js/                  # JavaScript files
├── media/                   # User uploaded files
├── requirements.txt         # Python dependencies
└── manage.py               # Django management script
```

## 🗄️ Database Models

### Trade Model
- **Basic Info**: Date, symbol, trade type (LONG/SHORT), quantity
- **Price Data**: Entry price, exit price, stop loss, target price
- **Results**: Profit/loss, percentage gain/loss, exit reason
- **Analysis**: Setup type, confidence level (1-10)
- **Documentation**: Before/after screenshots
- **Psychology**: Emotion notes, learning notes

### Review Models
- **WeeklyReview**: Weekly performance analysis and goals
- **MonthlyReview**: Monthly summary and strategy improvements

## 🎨 Customization

### Adding New Setup Types
Edit `journal/models.py` and add to `SETUP_TYPE_CHOICES`:
```python
SETUP_TYPE_CHOICES = [
    # ... existing choices
    ('YOUR_SETUP', 'Your Setup Name'),
]
```

### Customizing Charts
The dashboard uses Chart.js. Modify the JavaScript in templates to customize:
- Chart types (line, bar, pie, etc.)
- Colors and styling
- Data sources and calculations

### Styling
- **CSS**: Edit `static/css/custom.css`
- **Tailwind**: Modify classes in templates
- **Colors**: Update the color scheme in `templates/base.html`

## 🔧 Configuration

### Production Deployment
1. Set `DEBUG = False` in settings.py
2. Configure a production database (PostgreSQL recommended)
3. Set up static file serving
4. Configure environment variables
5. Use a production WSGI server (Gunicorn, uWSGI)

### Email Configuration
For email functionality, add to your `.env` file:
```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## 📊 Usage Guide

### Adding Your First Trade
1. Click "Add Trade" in the sidebar
2. Fill in the basic information (date, symbol, type)
3. Enter price data (entry, exit, stop loss, target)
4. Add your results and analysis
5. Upload screenshots if available
6. Add emotion and learning notes
7. Save the trade

### Creating Reviews
1. **Weekly Reviews**: Analyze your week's performance
2. **Monthly Reviews**: Look at longer-term trends and goals
3. Use the structured questions to guide your analysis

### Using Analytics
1. **Dashboard**: Overview of key metrics
2. **Analytics Page**: Detailed performance breakdowns
3. **Filtering**: Use filters to analyze specific time periods or setups

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🆘 Support

If you encounter any issues:
1. Check the Django documentation
2. Review the error logs
3. Ensure all dependencies are installed
4. Verify your database migrations are up to date

## 🚀 Future Enhancements

- **API Integration**: Connect to real-time market data
- **AI Insights**: Machine learning for trade pattern recognition
- **Export Features**: PDF/Excel export of reports
- **Mobile App**: Native mobile application
- **Social Features**: Share insights with trading community
- **Backtesting**: Historical strategy testing
- **Risk Management**: Advanced position sizing calculations

---

**Happy Trading! 📈**

*Remember: This tool is for educational and personal use. Always do your own research and consider consulting with financial professionals before making trading decisions.*
