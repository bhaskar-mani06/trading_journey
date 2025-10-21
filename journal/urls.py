from django.urls import path
from . import views
urlpatterns = [
    # Authentication - Local Django auth
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Main pages
    path('', views.home_view, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Trade management
    path('trades/', views.trade_list, name='trade_list'),
    path('trades/add/', views.trade_create, name='trade_create'),
    path('trades/<int:pk>/', views.trade_detail, name='trade_detail'),
    path('trades/<int:pk>/edit/', views.trade_edit, name='trade_edit'),
    path('trades/<int:pk>/delete/', views.trade_delete, name='trade_delete'),
    
    # Reviews
    path('reviews/weekly/', views.weekly_reviews, name='weekly_reviews'),
    path('reviews/weekly/add/', views.weekly_review_create, name='weekly_review_create'),
    path('reviews/monthly/', views.monthly_reviews, name='monthly_reviews'),
    path('reviews/monthly/add/', views.monthly_review_create, name='monthly_review_create'),
    
    # Analytics
    path('analytics/', views.analytics, name='analytics'),
    
    # Export/Reports
    path('export/csv/', views.export_trades_csv, name='export_csv'),
    path('export/pdf/', views.export_trades_pdf, name='export_pdf'),
    path('export/excel/', views.export_trades_excel, name='export_excel'),
    
    # Psychology & Mental Health
    path('psychology/', views.psychology_dashboard, name='psychology_dashboard'),
    path('psychology/add/', views.psychology_create, name='psychology_create'),
    path('psychology/<int:pk>/edit/', views.psychology_edit, name='psychology_edit'),
    
    # Goals & Targets
    path('goals/', views.goals_dashboard, name='goals_dashboard'),
    path('goals/add/', views.goal_create, name='goal_create'),
    path('goals/<int:pk>/edit/', views.goal_edit, name='goal_edit'),
    
    # Market Conditions
    path('market-conditions/', views.market_conditions, name='market_conditions'),
    path('market-conditions/add/', views.market_condition_create, name='market_condition_create'),
    
    # Trading Habits
    path('habits/', views.habits_dashboard, name='habits_dashboard'),
    path('habits/add/', views.habit_create, name='habit_create'),
    path('habits/<int:pk>/edit/', views.habit_edit, name='habit_edit'),
    
    # New Reports
    path('reports/monthly-summary/', views.monthly_summary, name='monthly_summary'),
    path('reports/tax-report/', views.tax_report, name='tax_report'),
    
    # Advanced Analytics
    path('analytics/portfolio-heatmap/', views.portfolio_heatmap, name='portfolio_heatmap'),
    path('analytics/confidence-performance/', views.confidence_performance, name='confidence_performance'),
    
    # Test view
    path('test/', views.test_view, name='test'),
]
