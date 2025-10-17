from django.contrib import admin
from .models import Trade, WeeklyReview, MonthlyReview


@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'trade_type', 'date', 'profit_loss', 'percentage_gain_loss', 'setup_type', 'user']
    list_filter = ['trade_type', 'setup_type', 'date', 'user']
    search_fields = ['symbol', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'date', 'symbol', 'trade_type')
        }),
        ('Price Information', {
            'fields': ('entry_price', 'exit_price', 'quantity')
        }),
        ('Risk Management', {
            'fields': ('stop_loss', 'target_price')
        }),
        ('Results', {
            'fields': ('exit_reason', 'profit_loss', 'percentage_gain_loss')
        }),
        ('Analysis', {
            'fields': ('setup_type', 'confidence_level')
        }),
        ('Documentation', {
            'fields': ('screenshot_before', 'screenshot_after')
        }),
        ('Notes', {
            'fields': ('emotion_notes', 'learning_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(WeeklyReview)
class WeeklyReviewAdmin(admin.ModelAdmin):
    list_display = ['week_start_date', 'week_end_date', 'total_trades', 'total_pnl', 'user']
    list_filter = ['week_start_date', 'user']
    search_fields = ['user__username']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(MonthlyReview)
class MonthlyReviewAdmin(admin.ModelAdmin):
    list_display = ['month', 'total_trades', 'total_pnl', 'max_drawdown', 'user']
    list_filter = ['month', 'user']
    search_fields = ['user__username']
    readonly_fields = ['created_at', 'updated_at']
