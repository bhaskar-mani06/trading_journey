#!/usr/bin/env python
"""
Script to export Django trading journal as static HTML files
for Netlify hosting
"""

import os
import sys
import django
from django.conf import settings
import json
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trading_journal.settings')
django.setup()

from django.template.loader import render_to_string

def export_static():
    """Export static HTML files"""
    
    # Create static directory
    static_dir = 'netlify_static'
    os.makedirs(static_dir, exist_ok=True)
    
    # Sample data for demo
    sample_user = {
        'username': 'demo_user',
        'total_trades': 5,
        'winning_trades': 3,
        'losing_trades': 2,
        'win_rate': 60.0,
        'total_pnl': 15000.0,
        'avg_profit': 8000.0,
        'avg_loss': -2000.0,
        'avg_risk_reward': 1.5,
        'current_win_streak': 2,
        'current_loss_streak': 0,
        'max_win_streak': 3,
        'max_loss_streak': 1,
        'today_pnl': 2500.0,
        'today_trades_count': 1,
        'week_pnl': 5000.0,
        'week_trades_count': 2,
        'week_win_rate': 75.0,
    }
    
    sample_trades = [
        {
            'symbol': 'RELIANCE',
            'date': '2025-10-17',
            'trade_type': 'LONG',
            'profit_loss': 5000.0,
            'percentage_gain_loss': 2.5,
            'setup_type': 'BREAKOUT'
        },
        {
            'symbol': 'TCS',
            'date': '2025-10-16',
            'trade_type': 'SHORT',
            'profit_loss': -1500.0,
            'percentage_gain_loss': -1.2,
            'setup_type': 'PULLBACK'
        }
    ]
    
    sample_monthly_data = [
        {'month': 'Oct 2025', 'pnl': 5000, 'trades': 2},
        {'month': 'Sep 2025', 'pnl': 3000, 'trades': 1},
        {'month': 'Aug 2025', 'pnl': 2000, 'trades': 1},
    ]
    
    sample_setup_performance = [
        {'setup_type': 'BREAKOUT', 'count': 2, 'total_pnl': 4000, 'avg_pnl': 2000},
        {'setup_type': 'PULLBACK', 'count': 1, 'total_pnl': -1500, 'avg_pnl': -1500},
    ]
    
    # Render dashboard
    dashboard_html = render_to_string('journal/dashboard.html', {
        'user': sample_user,
        'total_trades': sample_user['total_trades'],
        'winning_trades': sample_user['winning_trades'],
        'losing_trades': sample_user['losing_trades'],
        'win_rate': sample_user['win_rate'],
        'total_pnl': sample_user['total_pnl'],
        'avg_profit': sample_user['avg_profit'],
        'avg_loss': sample_user['avg_loss'],
        'avg_risk_reward': sample_user['avg_risk_reward'],
        'current_win_streak': sample_user['current_win_streak'],
        'current_loss_streak': sample_user['current_loss_streak'],
        'max_win_streak': sample_user['max_win_streak'],
        'max_loss_streak': sample_user['max_loss_streak'],
        'today_pnl': sample_user['today_pnl'],
        'today_trades_count': sample_user['today_trades_count'],
        'week_pnl': sample_user['week_pnl'],
        'week_trades_count': sample_user['week_trades_count'],
        'week_win_rate': sample_user['week_win_rate'],
        'recent_trades': sample_trades,
        'monthly_data': json.dumps(sample_monthly_data),
        'setup_performance': sample_setup_performance,
    })
    
    # Write dashboard
    with open(f'{static_dir}/index.html', 'w', encoding='utf-8') as f:
        f.write(dashboard_html)
    
    # Create other pages
    pages = {
        'analytics.html': 'journal/analytics.html',
        'trade_list.html': 'journal/trade_list.html',
        'monthly_summary.html': 'journal/monthly_summary.html',
        'tax_report.html': 'journal/tax_report.html',
    }
    
    for filename, template in pages.items():
        try:
            html = render_to_string(template, {
                'user': sample_user,
                'trades': sample_trades,
            })
            with open(f'{static_dir}/{filename}', 'w', encoding='utf-8') as f:
                f.write(html)
        except Exception as e:
            print(f"Error creating {filename}: {e}")
    
    # Copy static files
    import shutil
    if os.path.exists('static'):
        shutil.copytree('static', f'{static_dir}/static', dirs_exist_ok=True)
    
    print(f"✅ Static files exported to {static_dir}/")
    print("📁 Files created:")
    print("  - index.html (Dashboard)")
    print("  - analytics.html")
    print("  - trade_list.html") 
    print("  - monthly_summary.html")
    print("  - tax_report.html")
    print("  - static/ (CSS, JS, Images)")

if __name__ == '__main__':
    export_static()
