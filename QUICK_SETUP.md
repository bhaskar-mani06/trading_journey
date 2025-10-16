# 🚀 Quick Supabase Setup

## Step 1: Copy Keys from Supabase
1. Go to [supabase.com](https://supabase.com) → Your Project
2. Settings → API
3. Copy these 3 values:
   - **Project URL** (SUPABASE_URL)
   - **Anon Key** (SUPABASE_ANON_KEY) 
   - **Service Role Key** (SUPABASE_SERVICE_ROLE_KEY)

## Step 2: Update .env File
1. Copy `env_example.txt` to `.env`
2. Replace these 3 lines with your copied values:
   ```env
   SUPABASE_URL=https://your-project-ref.supabase.co
   SUPABASE_ANON_KEY=your-copied-anon-key
   SUPABASE_SERVICE_ROLE_KEY=your-copied-service-role-key
   ```

## Step 3: Run Setup
```bash
python setup_supabase.py
```

## Step 4: Start App
```bash
python manage.py runserver
```

## Done! 🎉
Your trading journal is now connected to Supabase!

---
**Need help?** Check the full guide in `supabase_setup_guide.md`
