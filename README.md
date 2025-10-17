# Trading Journal - Supabase + Netlify

A modern trading journal built with Supabase backend and static frontend for Netlify hosting.

## Features

✅ **Complete Trading Journal**
- Add, edit, delete trades
- Track win/loss streaks
- Daily and weekly performance summaries
- Monthly performance charts
- Best/worst performing symbols
- Trade status tracking (Open, Closed, Partial)

✅ **Advanced Analytics**
- Psychology tracking
- Goal setting and tracking
- Market condition analysis
- Tax reporting
- Export capabilities

✅ **Modern UI/UX**
- Responsive design with Tailwind CSS
- Interactive charts with Chart.js
- Smooth animations with GSAP
- Real-time updates

## Setup Instructions

### 1. Supabase Database Setup

1. Go to your Supabase project dashboard
2. Navigate to SQL Editor
3. Run the complete SQL script provided earlier to create:
   - All 7 tables with proper relationships
   - Row Level Security (RLS) policies
   - Performance indexes
   - Automatic timestamp updates

### 2. Configure Supabase Credentials

1. Get your Supabase URL and anon key from your project settings
2. Update `supabase-config.js`:
   ```javascript
   const SUPABASE_URL = 'your-actual-supabase-url';
   const SUPABASE_ANON_KEY = 'your-actual-anon-key';
   ```

### 3. Deploy to Netlify

1. **Option A: Drag & Drop**
   - Zip all files (index.html, js/, netlify.toml, etc.)
   - Drag to Netlify dashboard

2. **Option B: Git Integration**
   - Push to GitHub repository
   - Connect Netlify to your repository
   - Deploy automatically

3. **Set Environment Variables in Netlify**
   - Go to Site Settings > Environment Variables
   - Add:
     - `SUPABASE_URL`: Your Supabase URL
     - `SUPABASE_ANON_KEY`: Your Supabase anon key

### 4. Test Your Deployment

1. Visit your Netlify URL
2. Register a new account
3. Add some sample trades
4. Check if dashboard loads correctly

## File Structure

```
trading_journey/
├── index.html              # Main HTML file
├── netlify.toml           # Netlify configuration
├── supabase-config.js     # Supabase client setup
├── js/
│   ├── auth.js            # Authentication management
│   ├── api.js             # Supabase API calls
│   ├── dashboard.js       # Dashboard functionality
│   └── app.js             # App initialization
└── README.md              # This file
```

## Key Features Implemented

### Authentication
- User registration and login
- Session management
- Automatic logout handling

### Dashboard
- Real-time statistics
- Interactive charts
- Quick actions
- Recent trades display

### Data Management
- CRUD operations for trades
- Psychology tracking
- Goal management
- Performance analytics

## Next Steps

The basic structure is ready! You can now:

1. **Add more pages**: Create additional HTML files for different sections
2. **Implement forms**: Add trade entry, psychology, and goal forms
3. **Add more charts**: Implement additional analytics and reports
4. **Enhance UI**: Add more animations and interactions
5. **Add export features**: PDF and Excel export functionality

## Support

If you encounter any issues:
1. Check browser console for errors
2. Verify Supabase credentials
3. Ensure RLS policies are properly set up
4. Check Netlify deployment logs

Your trading journal is now ready for deployment! 🚀