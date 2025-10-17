from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse


class Trade(models.Model):
    TRADE_TYPE_CHOICES = [
        ('LONG', 'Long'),
        ('SHORT', 'Short'),
    ]
    
    SETUP_TYPE_CHOICES = [
        ('BREAKOUT', 'Breakout'),
        ('PULLBACK', 'Pullback'),
        ('NEWS_BASED', 'News-based'),
        ('TECHNICAL', 'Technical Analysis'),
        ('FUNDAMENTAL', 'Fundamental Analysis'),
        ('SCALPING', 'Scalping'),
        ('SWING', 'Swing Trading'),
        ('POSITION', 'Position Trading'),
        ('LIQUIDITY_SWEEP', 'Liquidity sweep setups'),
        ('ORDER_BLOCK', 'Order block trades'),
        ('FAIR_VALUE_GAP', 'Fair Value Gap trades'),
        ('BREAKER_BLOCK', 'Breaker block setups'),
        ('MITIGATION_BLOCK', 'Mitigation block trades'),
        ('MARKET_STRUCTURE', 'Market structure breaks'),
        ('BOS_CHOCH', 'Break of Structure / Change of Character'),
        ('REVERSAL', 'Reversal setups'),
        ('FIBONACCI', 'Fibonacci retracements/extensions'),
        ('SUPPORT_RESISTANCE', 'Support/Resistance levels'),
        ('OTHER', 'Other'),
    ]
    
    # Basic trade information
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trades')
    date = models.DateField(help_text="The day the trade was taken")
    symbol = models.CharField(max_length=20, help_text="Stock, forex pair, or asset name")
    trade_type = models.CharField(max_length=5, choices=TRADE_TYPE_CHOICES)
    
    # Price information
    entry_price = models.FloatField(validators=[MinValueValidator(0)], help_text="Entry price of the trade")
    exit_price = models.FloatField(validators=[MinValueValidator(0)], help_text="Exit price of the trade")
    quantity = models.PositiveIntegerField(help_text="Number of shares or lot size")
    
    # Risk management
    stop_loss = models.FloatField(validators=[MinValueValidator(0)], help_text="Defined stop loss")
    target_price = models.FloatField(validators=[MinValueValidator(0)], help_text="Take profit level")
    
    # Results
    exit_reason = models.TextField(help_text="Reason for exiting the trade")
    profit_loss = models.FloatField(help_text="Actual profit or loss amount")
    percentage_gain_loss = models.FloatField(help_text="Profit or loss in percentage")
    
    # Analysis
    setup_type = models.CharField(max_length=20, choices=SETUP_TYPE_CHOICES, help_text="Type of setup used")
    confidence_level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)], 
        help_text="Confidence rating (1-10)"
    )
    
    # Visual documentation
    screenshot_before = models.ImageField(
        upload_to='trade_screenshots/before/', 
        blank=True, 
        null=True,
        help_text="Chart before entering the trade"
    )
    screenshot_after = models.ImageField(
        upload_to='trade_screenshots/after/', 
        blank=True, 
        null=True,
        help_text="Chart after closing the trade"
    )
    
    # Local file storage URLs (for local development)
    screenshot_before_url = models.URLField(
        blank=True, 
        null=True,
        help_text="Local URL for before screenshot"
    )
    screenshot_after_url = models.URLField(
        blank=True, 
        null=True,
        help_text="Local URL for after screenshot"
    )
    
    # Psychological and learning
    emotion_notes = models.TextField(
        blank=True, 
        help_text="Emotions or psychological state during the trade"
    )
    learning_notes = models.TextField(
        blank=True, 
        help_text="Mistakes and lessons learned from this trade"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['user', 'date']),  # Most important for dashboard
            models.Index(fields=['user', 'profit_loss']),  # For win/loss calculations
            models.Index(fields=['user', 'symbol']),  # For symbol performance
            models.Index(fields=['user', 'setup_type']),  # For setup analysis
            models.Index(fields=['date']),
            models.Index(fields=['symbol']),
            models.Index(fields=['trade_type']),
            models.Index(fields=['setup_type']),
        ]
    
    def __str__(self):
        return f"{self.symbol} - {self.trade_type} - {self.date}"
    
    def get_absolute_url(self):
        return reverse('trade_detail', kwargs={'pk': self.pk})
    
    def is_profitable(self):
        """Check if the trade was profitable"""
        return self.profit_loss > 0
    
    def get_risk_reward_ratio(self):
        """Calculate risk-reward ratio"""
        if self.stop_loss and self.target_price and self.entry_price:
            if self.trade_type == 'LONG':
                risk = abs(self.entry_price - self.stop_loss)
                reward = abs(self.target_price - self.entry_price)
            else:  # SHORT
                risk = abs(self.stop_loss - self.entry_price)
                reward = abs(self.entry_price - self.target_price)
            
            if risk > 0:
                return round(reward / risk, 2)
        return None
    
    @classmethod
    def get_current_win_streak(cls, user):
        """Get current winning streak for a user - OPTIMIZED"""
        trades = cls.objects.filter(user=user).order_by('-date', '-created_at')
        
        streak = 0
        for trade in trades:
            if trade.profit_loss > 0:
                streak += 1
            else:
                break
        return streak
    
    @classmethod
    def get_current_loss_streak(cls, user):
        """Get current losing streak for a user - OPTIMIZED"""
        trades = cls.objects.filter(user=user).order_by('-date', '-created_at')
        
        streak = 0
        for trade in trades:
            if trade.profit_loss < 0:
                streak += 1
            else:
                break
        return streak
    
    @classmethod
    def get_max_win_streak(cls, user):
        """Get maximum winning streak for a user - OPTIMIZED"""
        trades = cls.objects.filter(user=user).order_by('date', 'created_at')
        
        max_streak = 0
        current_streak = 0
        
        for trade in trades:
            if trade.profit_loss > 0:
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 0
        
        return max_streak
    
    @classmethod
    def get_max_loss_streak(cls, user):
        """Get maximum losing streak for a user - OPTIMIZED"""
        trades = cls.objects.filter(user=user).order_by('date', 'created_at')
        
        max_streak = 0
        current_streak = 0
        
        for trade in trades:
            if trade.profit_loss < 0:
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 0
        
        return max_streak
    
    @classmethod
    def get_dashboard_stats(cls, user):
        """Get all dashboard statistics in optimized way"""
        from django.db.models import Count, Sum, Avg, Q
        from django.utils import timezone
        from datetime import timedelta
        
        user_trades = cls.objects.filter(user=user)
        
        # Single query for basic stats
        basic_stats = user_trades.aggregate(
            total_trades=Count('id'),
            winning_trades=Count('id', filter=Q(profit_loss__gt=0)),
            losing_trades=Count('id', filter=Q(profit_loss__lt=0)),
            total_pnl=Sum('profit_loss'),
            avg_profit=Avg('profit_loss', filter=Q(profit_loss__gt=0)),
            avg_loss=Avg('profit_loss', filter=Q(profit_loss__lt=0))
        )
        
        # Today's stats
        today = timezone.now().date()
        today_stats = user_trades.filter(date=today).aggregate(
            today_pnl=Sum('profit_loss'),
            today_trades_count=Count('id')
        )
        
        # This week's stats
        week_start = today - timedelta(days=today.weekday())
        week_stats = user_trades.filter(date__gte=week_start).aggregate(
            week_pnl=Sum('profit_loss'),
            week_trades_count=Count('id'),
            week_winning_trades=Count('id', filter=Q(profit_loss__gt=0))
        )
        
        # Calculate streaks efficiently
        trades_ordered = user_trades.order_by('-date', '-created_at')
        
        current_win_streak = 0
        current_loss_streak = 0
        
        for trade in trades_ordered:
            if trade.profit_loss > 0 and current_loss_streak == 0:
                current_win_streak += 1
            elif trade.profit_loss < 0 and current_win_streak == 0:
                current_loss_streak += 1
            else:
                break
        
        # Calculate max streaks
        trades_chronological = user_trades.order_by('date', 'created_at')
        max_win_streak = 0
        max_loss_streak = 0
        current_win = 0
        current_loss = 0
        
        for trade in trades_chronological:
            if trade.profit_loss > 0:
                current_win += 1
                current_loss = 0
                max_win_streak = max(max_win_streak, current_win)
            elif trade.profit_loss < 0:
                current_loss += 1
                current_win = 0
                max_loss_streak = max(max_loss_streak, current_loss)
            else:
                current_win = 0
                current_loss = 0
        
        return {
            'basic_stats': basic_stats,
            'today_stats': today_stats,
            'week_stats': week_stats,
            'current_win_streak': current_win_streak,
            'current_loss_streak': current_loss_streak,
            'max_win_streak': max_win_streak,
            'max_loss_streak': max_loss_streak,
        }


class WeeklyReview(models.Model):
    """Weekly review and analysis"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weekly_reviews')
    week_start_date = models.DateField(help_text="Start date of the week being reviewed")
    week_end_date = models.DateField(help_text="End date of the week being reviewed")
    
    # Review content
    what_went_well = models.TextField(help_text="What went well this week?")
    mistakes_repeated = models.TextField(help_text="What mistakes did I repeat?")
    best_setup = models.TextField(help_text="Which setup worked best?")
    improvements_next_week = models.TextField(help_text="What will I improve next week?")
    
    # Performance metrics for the week
    total_trades = models.PositiveIntegerField(default=0)
    winning_trades = models.PositiveIntegerField(default=0)
    losing_trades = models.PositiveIntegerField(default=0)
    total_pnl = models.FloatField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-week_start_date']
        unique_together = ['user', 'week_start_date']
    
    def __str__(self):
        return f"Weekly Review - {self.week_start_date} to {self.week_end_date}"
    
    def get_win_rate(self):
        """Calculate win rate for the week"""
        if self.total_trades > 0:
            return round((self.winning_trades / self.total_trades) * 100, 2)
        return 0


class MonthlyReview(models.Model):
    """Monthly review and analysis"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='monthly_reviews')
    month = models.DateField(help_text="Month being reviewed (first day of the month)")
    
    # Review content
    monthly_summary = models.TextField(help_text="Overall monthly summary")
    key_achievements = models.TextField(help_text="Key achievements this month")
    major_mistakes = models.TextField(help_text="Major mistakes and lessons")
    strategy_improvements = models.TextField(help_text="Strategy improvements made")
    goals_next_month = models.TextField(help_text="Goals for next month")
    
    # Performance metrics for the month
    total_trades = models.PositiveIntegerField(default=0)
    winning_trades = models.PositiveIntegerField(default=0)
    losing_trades = models.PositiveIntegerField(default=0)
    total_pnl = models.FloatField(default=0)
    max_drawdown = models.FloatField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-month']
        unique_together = ['user', 'month']
    
    def __str__(self):
        return f"Monthly Review - {self.month.strftime('%B %Y')}"
    
    def get_win_rate(self):
        """Calculate win rate for the month"""
        if self.total_trades > 0:
            return round((self.winning_trades / self.total_trades) * 100, 2)
        return 0


class TradingPsychology(models.Model):
    """Trading psychology and emotion tracking"""
    EMOTION_CHOICES = [
        ('FEAR', 'Fear'),
        ('GREED', 'Greed'),
        ('FOMO', 'FOMO (Fear of Missing Out)'),
        ('CONFIDENCE', 'Confidence'),
        ('ANXIETY', 'Anxiety'),
        ('EXCITEMENT', 'Excitement'),
        ('FRUSTRATION', 'Frustration'),
        ('CALM', 'Calm'),
        ('UNCERTAINTY', 'Uncertainty'),
        ('HOPEFUL', 'Hopeful'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='psychology_records')
    date = models.DateField()
    
    # Pre-trade emotions
    pre_trade_emotion = models.CharField(max_length=20, choices=EMOTION_CHOICES)
    pre_trade_confidence = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    pre_trade_stress_level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    
    # During trade emotions
    during_trade_emotion = models.CharField(max_length=20, choices=EMOTION_CHOICES, blank=True, null=True)
    during_trade_confidence = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], blank=True, null=True)
    
    # Post-trade emotions
    post_trade_emotion = models.CharField(max_length=20, choices=EMOTION_CHOICES)
    post_trade_confidence = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    post_trade_satisfaction = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    
    # Mental state
    sleep_quality = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], help_text="Sleep quality (1-10)")
    stress_level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], help_text="Overall stress level (1-10)")
    focus_level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], help_text="Focus level during trading (1-10)")
    
    # Notes
    mental_notes = models.TextField(blank=True, help_text="Mental state observations")
    improvement_notes = models.TextField(blank=True, help_text="Areas for mental improvement")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
        unique_together = ['user', 'date']
    
    def __str__(self):
        return f"{self.user.username} - Psychology - {self.date}"


class TradingGoal(models.Model):
    """Trading goals and targets"""
    GOAL_TYPE_CHOICES = [
        ('PROFIT', 'Profit Target'),
        ('WIN_RATE', 'Win Rate Target'),
        ('TRADE_COUNT', 'Trade Count Target'),
        ('RISK_MANAGEMENT', 'Risk Management'),
        ('LEARNING', 'Learning Goal'),
        ('HABIT', 'Habit Formation'),
    ]
    
    PERIOD_CHOICES = [
        ('DAILY', 'Daily'),
        ('WEEKLY', 'Weekly'),
        ('MONTHLY', 'Monthly'),
        ('QUARTERLY', 'Quarterly'),
        ('YEARLY', 'Yearly'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trading_goals')
    goal_type = models.CharField(max_length=20, choices=GOAL_TYPE_CHOICES)
    period = models.CharField(max_length=20, choices=PERIOD_CHOICES)
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    target_value = models.FloatField(help_text="Target value to achieve")
    current_value = models.FloatField(default=0, help_text="Current progress")
    
    start_date = models.DateField()
    end_date = models.DateField()
    
    is_achieved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"
    
    def get_progress_percentage(self):
        """Calculate progress percentage"""
        if self.target_value > 0:
            return min((self.current_value / self.target_value) * 100, 100)
        return 0
    
    def is_overdue(self):
        """Check if goal is overdue"""
        from django.utils import timezone
        return timezone.now().date() > self.end_date and not self.is_achieved


class MarketCondition(models.Model):
    """Market condition tracking"""
    CONDITION_CHOICES = [
        ('BULLISH', 'Bullish'),
        ('BEARISH', 'Bearish'),
        ('SIDEWAYS', 'Sideways'),
        ('VOLATILE', 'Volatile'),
        ('TRENDING', 'Trending'),
        ('RANGING', 'Ranging'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='market_conditions')
    date = models.DateField()
    
    market_condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    volatility_level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    sentiment = models.CharField(max_length=20, choices=TradingPsychology.EMOTION_CHOICES)
    
    # Market data
    market_index = models.CharField(max_length=50, blank=True, help_text="Nifty, Sensex, etc.")
    index_value = models.FloatField(blank=True, null=True)
    volume = models.BigIntegerField(blank=True, null=True)
    
    # News impact
    major_news = models.TextField(blank=True, help_text="Major market news")
    news_impact = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], blank=True, null=True, help_text="News impact (1-10)")
    
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
        unique_together = ['user', 'date']
    
    def __str__(self):
        return f"{self.user.username} - {self.market_condition} - {self.date}"


class TradingHabit(models.Model):
    """Trading habits tracking"""
    HABIT_TYPE_CHOICES = [
        ('GOOD', 'Good Habit'),
        ('BAD', 'Bad Habit'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trading_habits')
    habit_type = models.CharField(max_length=10, choices=HABIT_TYPE_CHOICES)
    name = models.CharField(max_length=200)
    description = models.TextField()
    
    # Tracking
    frequency = models.CharField(max_length=50, help_text="Daily, Weekly, etc.")
    target_count = models.IntegerField(default=1, help_text="Target occurrences")
    current_count = models.IntegerField(default=0)
    
    # Dates
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    is_achieved = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.name}"
    
    def get_progress_percentage(self):
        """Calculate habit progress"""
        if self.target_count > 0:
            return min((self.current_count / self.target_count) * 100, 100)
        return 0