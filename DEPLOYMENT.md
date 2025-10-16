# Trading Journal - Deployment Guide

## 🚀 Quick Deployment to Render

### Prerequisites
1. GitHub account
2. Render account (free tier available)
3. Supabase account (for database and authentication)

### Step 1: Upload to GitHub

1. **Initialize Git Repository** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Trading Journal App"
   ```

2. **Create GitHub Repository**:
   - Go to [GitHub](https://github.com) and create a new repository
   - Name it `trading-journal` or any name you prefer
   - Don't initialize with README (since we already have files)

3. **Push to GitHub**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/trading-journal.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy on Render

1. **Sign up/Login to Render**:
   - Go to [render.com](https://render.com)
   - Sign up with your GitHub account

2. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select your `trading-journal` repository

3. **Configure Build Settings**:
   - **Name**: `trading-journal` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `chmod +x build.sh && ./build.sh`
   - **Start Command**: `gunicorn trading_journal.wsgi --log-file -`

4. **Add Environment Variables**:
   ```
   SECRET_KEY=your-super-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=your-app-name.onrender.com
   SUPABASE_URL=https://nqjvhriwceldhkkkinba.supabase.co
   SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5xanZocml3Y2VsZGhra2tpbmJhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA1ODYxODUsImV4cCI6MjA3NjE2MjE4NX0.3ztzriqhj4iJ6lUMwx4CP-ZUEW6iYSG8B76cqz70jeY
   SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5xanZocml3Y2VsZGhra2tpbmJhIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MDU4NjE4NSwiZXhwIjoyMDc2MTYyMTg1fQ.kD0A-RyhKj9v10dRmwPzau18DsLkv7vDMsjAWqSJvig
   ```

5. **Deploy**:
   - Click "Create Web Service"
   - Render will automatically build and deploy your app
   - Wait for deployment to complete (usually 5-10 minutes)

### Step 3: Database Setup

Your app uses Supabase for database and authentication, so no additional database setup is needed on Render.

### Step 4: Access Your App

Once deployment is complete, you'll get a URL like:
`https://your-app-name.onrender.com`

## 🔧 Environment Variables

### Required Variables:
- `SECRET_KEY`: Django secret key (generate a new one for production)
- `DEBUG`: Set to `False` for production
- `ALLOWED_HOSTS`: Your Render app URL
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_ANON_KEY`: Your Supabase anonymous key
- `SUPABASE_SERVICE_ROLE_KEY`: Your Supabase service role key

### Optional Variables:
- `EMAIL_HOST_USER`: For email notifications
- `EMAIL_HOST_PASSWORD`: For email notifications
- `TWILIO_ACCOUNT_SID`: For SMS notifications
- `TWILIO_AUTH_TOKEN`: For SMS notifications

## 🛠️ Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/trading-journal.git
   cd trading-journal
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp env_example.txt .env
   # Edit .env with your actual values
   ```

5. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**:
   ```bash
   python manage.py runserver
   ```

## 📱 Features

- **User Authentication**: Supabase-powered authentication
- **Trading Journal**: Track your trades with detailed analytics
- **Goal Setting**: Set and track trading goals
- **Habit Tracking**: Monitor trading habits and psychology
- **Market Analysis**: Record market conditions and insights
- **Reports**: Generate PDF and Excel reports
- **Responsive Design**: Works on desktop and mobile

## 🔒 Security

- HTTPS enabled by default on Render
- Secure session cookies
- CSRF protection
- XSS protection
- Content Security Policy headers

## 📞 Support

If you encounter any issues during deployment, check:
1. Render build logs for errors
2. Environment variables are set correctly
3. Supabase configuration is correct
4. All dependencies are in requirements.txt

## 🎯 Next Steps

After successful deployment:
1. Test all features on the live site
2. Set up custom domain (optional)
3. Configure email notifications
4. Set up monitoring and backups
