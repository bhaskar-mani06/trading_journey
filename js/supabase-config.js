// Supabase Configuration
const SUPABASE_URL = 'https://nqjvhriwceldhkkkinba.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5xanZocml3Y2VsZGhra2tpbmJhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA1ODYxODUsImV4cCI6MjA3NjE2MjE4NX0.3ztzriqhj4iJ6lUMwx4CP-ZUEW6iYSG8B76cqz70jeY';

// Initialize Supabase client
const { createClient } = supabase;
const supabaseClient = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// Export for use in other files
window.supabase = supabaseClient;

// Database Tables (equivalent to Django models)
const tables = {
  trades: `
    CREATE TABLE trades (
      id SERIAL PRIMARY KEY,
      user_id UUID REFERENCES auth.users(id),
      date DATE NOT NULL,
      symbol VARCHAR(20) NOT NULL,
      trade_type VARCHAR(5) CHECK (trade_type IN ('LONG', 'SHORT')),
      trade_status VARCHAR(10) DEFAULT 'CLOSED' CHECK (trade_status IN ('OPEN', 'CLOSED', 'PARTIAL')),
      entry_price DECIMAL(10,2) NOT NULL,
      exit_price DECIMAL(10,2) NOT NULL,
      quantity INTEGER NOT NULL,
      stop_loss DECIMAL(10,2),
      target_price DECIMAL(10,2),
      exit_reason TEXT,
      profit_loss DECIMAL(10,2),
      percentage_gain_loss DECIMAL(5,2),
      setup_type VARCHAR(20),
      confidence_level INTEGER CHECK (confidence_level BETWEEN 1 AND 10),
      emotion_notes TEXT,
      learning_notes TEXT,
      created_at TIMESTAMP DEFAULT NOW(),
      updated_at TIMESTAMP DEFAULT NOW()
    );
  `,
  
  weekly_reviews: `
    CREATE TABLE weekly_reviews (
      id SERIAL PRIMARY KEY,
      user_id UUID REFERENCES auth.users(id),
      week_start_date DATE NOT NULL,
      week_end_date DATE NOT NULL,
      what_went_well TEXT,
      mistakes_repeated TEXT,
      best_setup TEXT,
      improvements_next_week TEXT,
      total_trades INTEGER DEFAULT 0,
      winning_trades INTEGER DEFAULT 0,
      losing_trades INTEGER DEFAULT 0,
      total_pnl DECIMAL(10,2) DEFAULT 0,
      created_at TIMESTAMP DEFAULT NOW(),
      updated_at TIMESTAMP DEFAULT NOW(),
      UNIQUE(user_id, week_start_date)
    );
  `,
  
  monthly_reviews: `
    CREATE TABLE monthly_reviews (
      id SERIAL PRIMARY KEY,
      user_id UUID REFERENCES auth.users(id),
      month DATE NOT NULL,
      monthly_summary TEXT,
      key_achievements TEXT,
      major_mistakes TEXT,
      strategy_improvements TEXT,
      goals_next_month TEXT,
      total_trades INTEGER DEFAULT 0,
      winning_trades INTEGER DEFAULT 0,
      losing_trades INTEGER DEFAULT 0,
      total_pnl DECIMAL(10,2) DEFAULT 0,
      max_drawdown DECIMAL(10,2) DEFAULT 0,
      created_at TIMESTAMP DEFAULT NOW(),
      updated_at TIMESTAMP DEFAULT NOW(),
      UNIQUE(user_id, month)
    );
  `,
  
  trading_psychology: `
    CREATE TABLE trading_psychology (
      id SERIAL PRIMARY KEY,
      user_id UUID REFERENCES auth.users(id),
      date DATE NOT NULL,
      pre_trade_emotion VARCHAR(20),
      pre_trade_confidence INTEGER CHECK (pre_trade_confidence BETWEEN 1 AND 10),
      pre_trade_stress_level INTEGER CHECK (pre_trade_stress_level BETWEEN 1 AND 10),
      during_trade_emotion VARCHAR(20),
      during_trade_confidence INTEGER CHECK (during_trade_confidence BETWEEN 1 AND 10),
      post_trade_emotion VARCHAR(20),
      post_trade_confidence INTEGER CHECK (post_trade_confidence BETWEEN 1 AND 10),
      post_trade_satisfaction INTEGER CHECK (post_trade_satisfaction BETWEEN 1 AND 10),
      sleep_quality INTEGER CHECK (sleep_quality BETWEEN 1 AND 10),
      stress_level INTEGER CHECK (stress_level BETWEEN 1 AND 10),
      focus_level INTEGER CHECK (focus_level BETWEEN 1 AND 10),
      mental_notes TEXT,
      improvement_notes TEXT,
      created_at TIMESTAMP DEFAULT NOW(),
      UNIQUE(user_id, date)
    );
  `,
  
  trading_goals: `
    CREATE TABLE trading_goals (
      id SERIAL PRIMARY KEY,
      user_id UUID REFERENCES auth.users(id),
      goal_type VARCHAR(20),
      period VARCHAR(20),
      title VARCHAR(200) NOT NULL,
      description TEXT,
      target_value DECIMAL(10,2),
      current_value DECIMAL(10,2) DEFAULT 0,
      start_date DATE NOT NULL,
      end_date DATE NOT NULL,
      is_achieved BOOLEAN DEFAULT FALSE,
      is_active BOOLEAN DEFAULT TRUE,
      created_at TIMESTAMP DEFAULT NOW(),
      updated_at TIMESTAMP DEFAULT NOW()
    );
  `,
  
  market_conditions: `
    CREATE TABLE market_conditions (
      id SERIAL PRIMARY KEY,
      user_id UUID REFERENCES auth.users(id),
      date DATE NOT NULL,
      market_condition VARCHAR(20),
      volatility_level INTEGER CHECK (volatility_level BETWEEN 1 AND 10),
      sentiment VARCHAR(20),
      market_index VARCHAR(50),
      index_value DECIMAL(10,2),
      volume BIGINT,
      major_news TEXT,
      news_impact INTEGER CHECK (news_impact BETWEEN 1 AND 10),
      notes TEXT,
      created_at TIMESTAMP DEFAULT NOW(),
      UNIQUE(user_id, date)
    );
  `,
  
  trading_habits: `
    CREATE TABLE trading_habits (
      id SERIAL PRIMARY KEY,
      user_id UUID REFERENCES auth.users(id),
      habit_type VARCHAR(10) CHECK (habit_type IN ('GOOD', 'BAD')),
      name VARCHAR(200) NOT NULL,
      description TEXT,
      frequency VARCHAR(50),
      target_count INTEGER DEFAULT 1,
      current_count INTEGER DEFAULT 0,
      start_date DATE NOT NULL,
      end_date DATE,
      is_active BOOLEAN DEFAULT TRUE,
      is_achieved BOOLEAN DEFAULT FALSE,
      created_at TIMESTAMP DEFAULT NOW(),
      updated_at TIMESTAMP DEFAULT NOW()
    );
  `
}

// Row Level Security (RLS) policies
const rlsPolicies = `
  -- Enable RLS on all tables
  ALTER TABLE trades ENABLE ROW LEVEL SECURITY;
  ALTER TABLE weekly_reviews ENABLE ROW LEVEL SECURITY;
  ALTER TABLE monthly_reviews ENABLE ROW LEVEL SECURITY;
  ALTER TABLE trading_psychology ENABLE ROW LEVEL SECURITY;
  ALTER TABLE trading_goals ENABLE ROW LEVEL SECURITY;
  ALTER TABLE market_conditions ENABLE ROW LEVEL SECURITY;
  ALTER TABLE trading_habits ENABLE ROW LEVEL SECURITY;

  -- Create policies for each table
  CREATE POLICY "Users can view own trades" ON trades FOR SELECT USING (auth.uid() = user_id);
  CREATE POLICY "Users can insert own trades" ON trades FOR INSERT WITH CHECK (auth.uid() = user_id);
  CREATE POLICY "Users can update own trades" ON trades FOR UPDATE USING (auth.uid() = user_id);
  CREATE POLICY "Users can delete own trades" ON trades FOR DELETE USING (auth.uid() = user_id);

  -- Similar policies for other tables...
`

export { supabase, tables, rlsPolicies }
