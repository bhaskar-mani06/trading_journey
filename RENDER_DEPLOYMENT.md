# Render Deployment Guide 🚀

## Step 1: Create Render Account
1. Go to https://render.com
2. Sign up with GitHub
3. Connect your repository

## Step 2: Create Web Service
1. Click "New" → "Web Service"
2. Connect your GitHub repository: `bhaskar-mani06/trading_journey`
3. Select branch: `main`

## Step 3: Configure Build Settings
```
Name: trading-journal
Environment: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn trading_journal.wsgi:application
```

## Step 4: Environment Variables
Add these in Render Dashboard → Environment:

### Required Variables:
```
SECRET_KEY=your-secret-key-here-change-this
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=Bhaskar@24275270
DB_HOST=db.nqjvhriwceldhkkkinba.supabase.co
DB_PORT=5432
```

### Optional Variables:
```
DJANGO_SETTINGS_MODULE=trading_journal.settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@tradingjournal.com
```

**Important:** Replace `your-secret-key-here-change-this` with a strong secret key!

## Step 5: Deploy
1. Click "Create Web Service"
2. Wait for build to complete
3. Your app will be available at: `https://your-app-name.onrender.com`

## Step 6: Database Setup
After deployment, run migrations:
1. Go to Render Dashboard
2. Click on your service
3. Go to "Shell" tab
4. Run: `python manage.py migrate`
5. Create superuser: `python manage.py createsuperuser`

## Troubleshooting:
- Check build logs for errors
- Ensure all environment variables are set
- Verify database connection
- Check static files are collected

## Your App URL:
After successful deployment, your app will be live at:
`https://your-app-name.onrender.com`
