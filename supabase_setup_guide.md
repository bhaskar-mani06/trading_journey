# Supabase Integration Guide for Trading Journal

## Step 1: Create Supabase Project

1. Go to [supabase.com](https://supabase.com) and create an account
2. Click "New Project"
3. Choose your organization and fill in project details:
   - Name: `trading-journal`
   - Database Password: Create a strong password
   - Region: Choose closest to your users
4. Wait for project to be created (2-3 minutes)

## Step 2: Get Project Credentials

1. Go to Settings → API
2. Copy the following values:
   - Project URL (e.g., `https://abcdefgh.supabase.co`)
   - Anon/Public Key
   - Service Role Key (keep this secret!)

3. Go to Settings → Database
4. Copy the connection details:
   - Host: `db.abcdefgh.supabase.co`
   - Database name: `postgres`
   - Port: `5432`
   - User: `postgres`
   - Password: (the one you set during project creation)

## Step 3: Configure Environment Variables

Create a `.env` file in your project root with:

```env
# Django Settings
SECRET_KEY=your-very-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,localhost,127.0.0.1

# Supabase Database
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your-supabase-db-password
DB_HOST=db.your-project-ref.supabase.co
DB_PORT=5432

# Supabase Project Settings
SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key

# Email Settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@tradingjournal.com
```

## Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 5: Run Database Migrations

```bash
python manage.py migrate
```

## Step 6: Set Up Supabase Storage

```bash
python manage.py setup_supabase
```

## Step 7: Create Superuser

```bash
python manage.py createsuperuser
```

## Step 8: Test the Application

```bash
python manage.py runserver
```

Visit `http://localhost:8000` and test:
- User registration
- Trade creation with screenshots
- Dashboard functionality

## Step 9: Deploy to Production

### For Heroku:

1. Install Heroku CLI
2. Create Heroku app:
   ```bash
   heroku create your-trading-journal
   ```
3. Set environment variables:
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS=your-trading-journal.herokuapp.com
   heroku config:set DB_NAME=postgres
   heroku config:set DB_USER=postgres
   heroku config:set DB_PASSWORD=your-supabase-password
   heroku config:set DB_HOST=db.your-project-ref.supabase.co
   heroku config:set DB_PORT=5432
   heroku config:set SUPABASE_URL=https://your-project-ref.supabase.co
   heroku config:set SUPABASE_ANON_KEY=your-anon-key
   heroku config:set SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
   ```
4. Deploy:
   ```bash
   git add .
   git commit -m "Add Supabase integration"
   git push heroku main
   ```
5. Run migrations on Heroku:
   ```bash
   heroku run python manage.py migrate
   heroku run python manage.py setup_supabase
   ```

## Step 10: Set Up Supabase Storage Bucket

1. Go to your Supabase project dashboard
2. Navigate to Storage
3. Create a new bucket named `trade-screenshots`
4. Make it public for easy access
5. Set up RLS policies if needed

## Features Enabled with Supabase:

✅ **Cloud Database**: PostgreSQL database hosted on Supabase
✅ **File Storage**: Trade screenshots stored in Supabase Storage
✅ **Real-time Updates**: Ready for real-time features
✅ **Scalability**: Automatic scaling with Supabase
✅ **Security**: Built-in authentication and security features
✅ **Backup**: Automatic database backups

## Troubleshooting:

### Database Connection Issues:
- Check your environment variables
- Ensure Supabase project is active
- Verify database password is correct

### File Upload Issues:
- Check Supabase Storage bucket exists
- Verify storage policies are set correctly
- Check file size limits

### Authentication Issues:
- Ensure Supabase keys are correct
- Check CORS settings in Supabase dashboard

## Next Steps:

1. **Real-time Features**: Add real-time trade updates
2. **Advanced Analytics**: Use Supabase Edge Functions for complex calculations
3. **Mobile App**: Use Supabase client libraries for mobile development
4. **API Integration**: Add market data APIs
5. **Notifications**: Set up email/SMS notifications for trade alerts

## Support:

- Supabase Documentation: https://supabase.com/docs
- Django Documentation: https://docs.djangoproject.com
- Project Issues: Create an issue in your repository
