// Dashboard Manager
class DashboardManager {
    constructor() {
        this.charts = {};
        this.stats = null;
    }

    async loadDashboard() {
        try {
            // Set user ID for API calls
            if (window.authManager.currentUser) {
                window.tradingAPI.setUserId(window.authManager.currentUser.id);
            }

            // Load dashboard stats
            const result = await window.tradingAPI.getDashboardStats();
            if (!result.success) {
                throw new Error(result.error);
            }

            this.stats = result.data;
            this.renderDashboard();
            this.initializeCharts();
        } catch (error) {
            console.error('Error loading dashboard:', error);
            showNotification('Error loading dashboard: ' + error.message, 'error');
        }
    }

    renderDashboard() {
        const dashboardHTML = `
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <!-- Quick Stats Row -->
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                    <div class="stat-card card-hover rounded-lg p-6 text-white">
                        <div class="flex items-center justify-between">
                            <div>
                                <p class="text-sm opacity-90">Today's P&L</p>
                                <p class="text-2xl font-bold">₹${this.stats.todayPnL}</p>
                                <p class="text-sm opacity-75">${this.stats.todayTradesCount} trades</p>
                            </div>
                            <i class="fas fa-calendar-day text-3xl opacity-75"></i>
                        </div>
                    </div>

                    <div class="stat-card green card-hover rounded-lg p-6 text-white">
                        <div class="flex items-center justify-between">
                            <div>
                                <p class="text-sm opacity-90">This Week</p>
                                <p class="text-2xl font-bold">₹${this.stats.weekPnL}</p>
                                <p class="text-sm opacity-75">${this.stats.weekWinRate}% win rate</p>
                            </div>
                            <i class="fas fa-chart-line text-3xl opacity-75"></i>
                        </div>
                    </div>

                    <div class="stat-card blue card-hover rounded-lg p-6 text-white">
                        <div class="flex items-center justify-between">
                            <div>
                                <p class="text-sm opacity-90">Win Streak</p>
                                <p class="text-2xl font-bold">${this.stats.currentWinStreak}</p>
                                <p class="text-sm opacity-75">Max: ${this.stats.maxWinStreak}</p>
                            </div>
                            <i class="fas fa-fire text-3xl opacity-75"></i>
                        </div>
                    </div>

                    <div class="stat-card purple card-hover rounded-lg p-6 text-white">
                        <div class="flex items-center justify-between">
                            <div>
                                <p class="text-sm opacity-90">Loss Streak</p>
                                <p class="text-2xl font-bold">${this.stats.currentLossStreak}</p>
                                <p class="text-sm opacity-75">Max: ${this.stats.maxLossStreak}</p>
                            </div>
                            <i class="fas fa-exclamation-triangle text-3xl opacity-75"></i>
                        </div>
                    </div>
                </div>

                <!-- Quick Actions -->
                <div class="bg-white rounded-lg shadow-lg p-6 mb-8">
                    <h2 class="text-xl font-bold text-gray-800 mb-4">
                        <i class="fas fa-bolt mr-2 text-yellow-500"></i>Quick Actions
                    </h2>
                    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                        <button onclick="showAddTradeModal()" class="bg-blue-500 hover:bg-blue-600 text-white p-4 rounded-lg transition-colors">
                            <i class="fas fa-plus mb-2 block text-xl"></i>
                            Add Trade
                        </button>
                        <button onclick="showAddPsychologyModal()" class="bg-green-500 hover:bg-green-600 text-white p-4 rounded-lg transition-colors">
                            <i class="fas fa-brain mb-2 block text-xl"></i>
                            Psychology
                        </button>
                        <button onclick="showAddGoalModal()" class="bg-purple-500 hover:bg-purple-600 text-white p-4 rounded-lg transition-colors">
                            <i class="fas fa-target mb-2 block text-xl"></i>
                            Add Goal
                        </button>
                        <button onclick="showAnalytics()" class="bg-orange-500 hover:bg-orange-600 text-white p-4 rounded-lg transition-colors">
                            <i class="fas fa-chart-bar mb-2 block text-xl"></i>
                            Analytics
                        </button>
                    </div>
                </div>

                <!-- Charts Section -->
                <div class="bg-white rounded-lg shadow-lg p-6 mb-8">
                    <div class="flex justify-between items-center mb-4">
                        <h2 class="text-xl font-bold text-gray-800">
                            <i class="fas fa-chart-area mr-2 text-blue-500"></i>Performance Charts
                        </h2>
                        <button onclick="toggleCharts()" class="text-gray-500 hover:text-gray-700">
                            <i id="charts-toggle-icon" class="fas fa-chevron-down"></i>
                        </button>
                    </div>
                    <div id="charts-container" class="space-y-6">
                        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                            <div>
                                <h3 class="text-lg font-semibold text-gray-700 mb-3">Monthly Performance</h3>
                                <canvas id="monthlyChart" width="400" height="200"></canvas>
                            </div>
                            <div>
                                <h3 class="text-lg font-semibold text-gray-700 mb-3">Win/Loss Distribution</h3>
                                <canvas id="winLossChart" width="400" height="200"></canvas>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Recent Trades -->
                <div class="bg-white rounded-lg shadow-lg p-6 mb-8">
                    <h2 class="text-xl font-bold text-gray-800 mb-4">
                        <i class="fas fa-history mr-2 text-green-500"></i>Recent Trades
                    </h2>
                    <div class="overflow-x-auto">
                        <table class="min-w-full divide-y divide-gray-200">
                            <thead class="bg-gray-50">
                                <tr>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Symbol</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">P&L</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                                </tr>
                            </thead>
                            <tbody class="bg-white divide-y divide-gray-200">
                                ${this.stats.recentTrades.map(trade => `
                                    <tr>
                                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${trade.date}</td>
                                        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${trade.symbol}</td>
                                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                            <span class="px-2 py-1 text-xs rounded-full ${trade.trade_type === 'LONG' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}">
                                                ${trade.trade_type}
                                            </span>
                                        </td>
                                        <td class="px-6 py-4 whitespace-nowrap text-sm ${trade.profit_loss >= 0 ? 'text-green-600' : 'text-red-600'}">
                                            ₹${trade.profit_loss || 0}
                                        </td>
                                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                            <span class="px-2 py-1 text-xs rounded-full ${trade.trade_status === 'CLOSED' ? 'bg-gray-100 text-gray-800' : 'bg-blue-100 text-blue-800'}">
                                                ${trade.trade_status}
                                            </span>
                                        </td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- Quick Links -->
                <div class="bg-white rounded-lg shadow-lg p-6">
                    <h2 class="text-xl font-bold text-gray-800 mb-4">
                        <i class="fas fa-link mr-2 text-purple-500"></i>Quick Links
                    </h2>
                    <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
                        <button onclick="showAllTrades()" class="bg-gray-100 hover:bg-gray-200 p-3 rounded-lg text-sm transition-colors">
                            <i class="fas fa-list mb-1 block text-lg"></i>
                            All Trades
                        </button>
                        <button onclick="showMonthlySummary()" class="bg-gray-100 hover:bg-gray-200 p-3 rounded-lg text-sm transition-colors">
                            <i class="fas fa-calendar-alt mb-1 block text-lg"></i>
                            Monthly Summary
                        </button>
                        <button onclick="showTaxReport()" class="bg-gray-100 hover:bg-gray-200 p-3 rounded-lg text-sm transition-colors">
                            <i class="fas fa-file-invoice mb-1 block text-lg"></i>
                            Tax Report
                        </button>
                        <button onclick="showPsychology()" class="bg-gray-100 hover:bg-gray-200 p-3 rounded-lg text-sm transition-colors">
                            <i class="fas fa-brain mb-1 block text-lg"></i>
                            Psychology
                        </button>
                        <button onclick="showGoals()" class="bg-gray-100 hover:bg-gray-200 p-3 rounded-lg text-sm transition-colors">
                            <i class="fas fa-target mb-1 block text-lg"></i>
                            Goals
                        </button>
                        <button onclick="showSettings()" class="bg-gray-100 hover:bg-gray-200 p-3 rounded-lg text-sm transition-colors">
                            <i class="fas fa-cog mb-1 block text-lg"></i>
                            Settings
                        </button>
                    </div>
                </div>
            </div>
        `;

        document.getElementById('main-content').innerHTML = dashboardHTML;
    }

    initializeCharts() {
        // Monthly Performance Chart
        const monthlyCtx = document.getElementById('monthlyChart').getContext('2d');
        this.charts.monthly = new Chart(monthlyCtx, {
            type: 'line',
            data: {
                labels: this.stats.monthlyData.map(d => d.month),
                datasets: [{
                    label: 'P&L',
                    data: this.stats.monthlyData.map(d => d.pnl),
                    borderColor: 'rgb(59, 130, 246)',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        }
                    },
                    x: {
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        }
                    }
                }
            }
        });

        // Win/Loss Distribution Chart
        const winLossCtx = document.getElementById('winLossChart').getContext('2d');
        this.charts.winLoss = new Chart(winLossCtx, {
            type: 'doughnut',
            data: {
                labels: ['Winning Trades', 'Losing Trades'],
                datasets: [{
                    data: [this.stats.winningTrades, this.stats.losingTrades],
                    backgroundColor: ['#10B981', '#EF4444'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }
}

// Global dashboard manager instance
window.dashboardManager = new DashboardManager();

// Chart toggle function
function toggleCharts() {
    const container = document.getElementById('charts-container');
    const icon = document.getElementById('charts-toggle-icon');
    
    if (container.style.display === 'none') {
        container.style.display = 'block';
        icon.className = 'fas fa-chevron-down';
    } else {
        container.style.display = 'none';
        icon.className = 'fas fa-chevron-right';
    }
}

// Placeholder functions for navigation
function showAddTradeModal() {
    showNotification('Add Trade modal will be implemented', 'info');
}

function showAddPsychologyModal() {
    showNotification('Psychology modal will be implemented', 'info');
}

function showAddGoalModal() {
    showNotification('Add Goal modal will be implemented', 'info');
}

function showAnalytics() {
    showNotification('Analytics page will be implemented', 'info');
}

function showAllTrades() {
    showNotification('All Trades page will be implemented', 'info');
}

function showMonthlySummary() {
    showNotification('Monthly Summary page will be implemented', 'info');
}

function showTaxReport() {
    showNotification('Tax Report page will be implemented', 'info');
}

function showPsychology() {
    showNotification('Psychology page will be implemented', 'info');
}

function showGoals() {
    showNotification('Goals page will be implemented', 'info');
}

function showSettings() {
    showNotification('Settings page will be implemented', 'info');
}
