# Trading Journal Deployment Guide

## Prerequisites
- Git installed
- GitHub account
- Supabase database already configured (✓ Done)

---

## Option 1: Render.com Deployment (Recommended - Free)

### Step 1: Push Code to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

### Step 2: Create Render Account
1. Go to https://render.com/
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Connect your GitHub repository

### Step 3: Configure Web Service
**Basic Settings:**
- Name: `trading-journal` (ya apna naam)
- Region: Oregon (US West)
- Branch: `main`
- Runtime: `Python 3`
- Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
- Start Command: `gunicorn trading_journal.wsgi`

### Step 4: Add Environment Variables
Render Dashboard → Environment → Add Environment Variable

```
SECRET_KEY = django-insecure-generate-a-new-secret-key-here-use-random-string
DEBUG = False
ALLOWED_HOSTS = your-app-name.onrender.com
DB_NAME = postgres
DB_USER = postgres
DB_PASSWORD = Bhaskar@24275270
DB_HOST = db.nqjvhriwceldhkkkinba.supabase.co
DB_PORT = 5432
```

**Important:**
- Replace `your-app-name.onrender.com` with actual Render URL
- Generate new SECRET_KEY: https://djecrety.ir/

### Step 5: Deploy
1. Click "Create Web Service"
2. Wait 5-10 minutes for deployment
3. Visit your app at: `https://your-app-name.onrender.com`

---

## Option 2: Railway.app Deployment

### Step 1: Push to GitHub (same as above)

### Step 2: Deploy on Railway
1. Go to https://railway.app/
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository

### Step 3: Add Environment Variables
```
SECRET_KEY = your-new-secret-key
DEBUG = False
ALLOWED_HOSTS = ${{RAILWAY_PUBLIC_DOMAIN}}
DB_NAME = postgres
DB_USER = postgres
DB_PASSWORD = Bhaskar@24275270
DB_HOST = db.nqjvhriwceldhkkkinba.supabase.co
DB_PORT = 5432
```

### Step 4: Configure Settings
- Railway will auto-detect Django
- Add custom start command if needed: `gunicorn trading_journal.wsgi`

---

## Post-Deployment Steps

### 1. Create Superuser
Render Dashboard → Shell tab:
```bash
python manage.py createsuperuser
```

Railway:
```bash
railway run python manage.py createsuperuser
```

### 2. Update CSRF Settings
After deployment, add your domain to `settings.py`:
```python
CSRF_TRUSTED_ORIGINS = [
    'https://your-app.onrender.com',
    # or
    'https://your-app.up.railway.app',
]
```

### 3. Test Your App
- Visit homepage
- Try login/register
- Create a test trade
- Check admin panel: `https://your-app.onrender.com/admin`

---

## Troubleshooting

### Database Connection Error
- Verify Supabase credentials
- Check if DB_HOST is correct
- Ensure SSL mode is enabled

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
```

### 500 Internal Server Error
- Check logs in Render/Railway dashboard
- Verify DEBUG=False
- Check ALLOWED_HOSTS includes your domain

### CSRF Verification Failed
- Add your domain to CSRF_TRUSTED_ORIGINS
- Redeploy

---

## Monitoring & Maintenance

### View Logs
- **Render:** Dashboard → Logs tab
- **Railway:** Dashboard → Deployments → View Logs

### Update Application
```bash
git add .
git commit -m "Update message"
git push
```
Render/Railway will auto-deploy!

---

## Free Tier Limitations

### Render Free Tier
- App sleeps after 15 min inactivity
- 750 hours/month (enough for 24/7 if single app)
- First request after sleep takes ~30 seconds

### Railway Free Tier
- $5 credit/month
- After credit, app pauses
- Good for testing

---

## Security Checklist
- ✓ DEBUG = False in production
- ✓ Strong SECRET_KEY
- ✓ ALLOWED_HOSTS configured
- ✓ SSL enabled on database
- ✓ Environment variables not in code
- ✓ .env files in .gitignore

---

## Need Help?
- Render Docs: https://render.com/docs
- Railway Docs: https://docs.railway.app/
- Django Deployment: https://docs.djangoproject.com/en/stable/howto/deployment/

---

## Quick Deploy Commands Summary

```bash
# 1. Prepare for deployment
git init
git add .
git commit -m "Ready for deployment"

# 2. Push to GitHub
git remote add origin YOUR_REPO_URL
git push -u origin main

# 3. Go to Render.com or Railway.app
# 4. Connect GitHub repo
# 5. Add environment variables
# 6. Deploy!
```

Your database is already configured and ready to use! 🚀
