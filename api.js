// API functions for Supabase
class TradingAPI {
    constructor() {
        this.userId = null;
    }

    setUserId(userId) {
        this.userId = userId;
    }

    // Trade operations
    async getTrades(filters = {}) {
        try {
            let query = supabase
                .from('trades')
                .select('*')
                .eq('user_id', this.userId)
                .order('date', { ascending: false });

            if (filters.date_from) {
                query = query.gte('date', filters.date_from);
            }
            if (filters.date_to) {
                query = query.lte('date', filters.date_to);
            }
            if (filters.symbol) {
                query = query.eq('symbol', filters.symbol);
            }
            if (filters.trade_type) {
                query = query.eq('trade_type', filters.trade_type);
            }
            if (filters.trade_status) {
                query = query.eq('trade_status', filters.trade_status);
            }

            const { data, error } = await query;
            if (error) throw error;
            return { success: true, data };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    async addTrade(tradeData) {
        try {
            const { data, error } = await supabase
                .from('trades')
                .insert([{ ...tradeData, user_id: this.userId }])
                .select();

            if (error) throw error;
            return { success: true, data: data[0] };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    async updateTrade(tradeId, tradeData) {
        try {
            const { data, error } = await supabase
                .from('trades')
                .update(tradeData)
                .eq('id', tradeId)
                .eq('user_id', this.userId)
                .select();

            if (error) throw error;
            return { success: true, data: data[0] };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    async deleteTrade(tradeId) {
        try {
            const { error } = await supabase
                .from('trades')
                .delete()
                .eq('id', tradeId)
                .eq('user_id', this.userId);

            if (error) throw error;
            return { success: true };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    // Dashboard statistics
    async getDashboardStats() {
        try {
            const trades = await this.getTrades();
            if (!trades.success) throw new Error(trades.error);

            const allTrades = trades.data;
            const closedTrades = allTrades.filter(t => t.trade_status === 'CLOSED');
            
            // Basic stats
            const totalTrades = closedTrades.length;
            const winningTrades = closedTrades.filter(t => t.profit_loss > 0).length;
            const losingTrades = closedTrades.filter(t => t.profit_loss < 0).length;
            const totalPnL = closedTrades.reduce((sum, t) => sum + parseFloat(t.profit_loss || 0), 0);
            const winRate = totalTrades > 0 ? (winningTrades / totalTrades) * 100 : 0;

            // Streak calculations
            const currentWinStreak = this.calculateCurrentWinStreak(closedTrades);
            const currentLossStreak = this.calculateCurrentLossStreak(closedTrades);
            const maxWinStreak = this.calculateMaxWinStreak(closedTrades);
            const maxLossStreak = this.calculateMaxLossStreak(closedTrades);

            // Today's P&L
            const today = new Date().toISOString().split('T')[0];
            const todayTrades = allTrades.filter(t => t.date === today);
            const todayPnL = todayTrades.reduce((sum, t) => sum + parseFloat(t.profit_loss || 0), 0);

            // This week's performance
            const weekStart = this.getWeekStart();
            const weekTrades = allTrades.filter(t => t.date >= weekStart);
            const weekPnL = weekTrades.reduce((sum, t) => sum + parseFloat(t.profit_loss || 0), 0);
            const weekWinRate = weekTrades.length > 0 ? 
                (weekTrades.filter(t => t.profit_loss > 0).length / weekTrades.length) * 100 : 0;

            // Best/Worst symbols
            const symbolPerformance = this.calculateSymbolPerformance(closedTrades);
            const bestSymbols = symbolPerformance.slice(0, 5);
            const worstSymbols = symbolPerformance.filter(s => s.total_pnl < 0).slice(0, 5);

            // Favorite symbols (most traded)
            const favoriteSymbols = this.calculateFavoriteSymbols(allTrades);

            // Recent trades
            const recentTrades = allTrades.slice(0, 5);

            // Monthly performance for charts
            const monthlyData = this.calculateMonthlyPerformance(closedTrades);

            return {
                success: true,
                data: {
                    totalTrades,
                    winningTrades,
                    losingTrades,
                    totalPnL: Math.round(totalPnL * 100) / 100,
                    winRate: Math.round(winRate * 10) / 10,
                    currentWinStreak,
                    currentLossStreak,
                    maxWinStreak,
                    maxLossStreak,
                    todayPnL: Math.round(todayPnL * 100) / 100,
                    todayTradesCount: todayTrades.length,
                    weekPnL: Math.round(weekPnL * 100) / 100,
                    weekTradesCount: weekTrades.length,
                    weekWinRate: Math.round(weekWinRate * 10) / 10,
                    bestSymbols,
                    worstSymbols,
                    favoriteSymbols,
                    recentTrades,
                    monthlyData
                }
            };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    // Helper methods for calculations
    calculateCurrentWinStreak(trades) {
        let streak = 0;
        for (const trade of trades) {
            if (trade.profit_loss > 0) {
                streak++;
            } else {
                break;
            }
        }
        return streak;
    }

    calculateCurrentLossStreak(trades) {
        let streak = 0;
        for (const trade of trades) {
            if (trade.profit_loss < 0) {
                streak++;
            } else {
                break;
            }
        }
        return streak;
    }

    calculateMaxWinStreak(trades) {
        let maxStreak = 0;
        let currentStreak = 0;
        
        for (const trade of trades) {
            if (trade.profit_loss > 0) {
                currentStreak++;
                maxStreak = Math.max(maxStreak, currentStreak);
            } else {
                currentStreak = 0;
            }
        }
        return maxStreak;
    }

    calculateMaxLossStreak(trades) {
        let maxStreak = 0;
        let currentStreak = 0;
        
        for (const trade of trades) {
            if (trade.profit_loss < 0) {
                currentStreak++;
                maxStreak = Math.max(maxStreak, currentStreak);
            } else {
                currentStreak = 0;
            }
        }
        return maxStreak;
    }

    calculateSymbolPerformance(trades) {
        const symbolMap = {};
        
        trades.forEach(trade => {
            if (!symbolMap[trade.symbol]) {
                symbolMap[trade.symbol] = {
                    symbol: trade.symbol,
                    count: 0,
                    total_pnl: 0,
                    avg_pnl: 0,
                    win_rate: 0
                };
            }
            
            symbolMap[trade.symbol].count++;
            symbolMap[trade.symbol].total_pnl += parseFloat(trade.profit_loss || 0);
        });

        return Object.values(symbolMap)
            .map(symbol => ({
                ...symbol,
                avg_pnl: symbol.total_pnl / symbol.count,
                win_rate: (trades.filter(t => t.symbol === symbol.symbol && t.profit_loss > 0).length / symbol.count) * 100
            }))
            .sort((a, b) => b.total_pnl - a.total_pnl);
    }

    calculateFavoriteSymbols(trades) {
        const symbolMap = {};
        
        trades.forEach(trade => {
            symbolMap[trade.symbol] = (symbolMap[trade.symbol] || 0) + 1;
        });

        return Object.entries(symbolMap)
            .map(([symbol, count]) => ({ symbol, trade_count: count }))
            .sort((a, b) => b.trade_count - a.trade_count)
            .slice(0, 10);
    }

    calculateMonthlyPerformance(trades) {
        const monthlyMap = {};
        
        trades.forEach(trade => {
            const month = trade.date.substring(0, 7); // YYYY-MM
            if (!monthlyMap[month]) {
                monthlyMap[month] = {
                    month: month,
                    pnl: 0,
                    trades: 0
                };
            }
            monthlyMap[month].pnl += parseFloat(trade.profit_loss || 0);
            monthlyMap[month].trades++;
        });

        return Object.values(monthlyMap).sort((a, b) => a.month.localeCompare(b.month));
    }

    getWeekStart() {
        const today = new Date();
        const dayOfWeek = today.getDay();
        const diff = today.getDate() - dayOfWeek + (dayOfWeek === 0 ? -6 : 1);
        const weekStart = new Date(today.setDate(diff));
        return weekStart.toISOString().split('T')[0];
    }

    // Psychology tracking
    async getPsychologyEntries() {
        try {
            const { data, error } = await supabase
                .from('trading_psychology')
                .select('*')
                .eq('user_id', this.userId)
                .order('date', { ascending: false });

            if (error) throw error;
            return { success: true, data };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    async addPsychologyEntry(psychologyData) {
        try {
            const { data, error } = await supabase
                .from('trading_psychology')
                .insert([{ ...psychologyData, user_id: this.userId }])
                .select();

            if (error) throw error;
            return { success: true, data: data[0] };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    // Goals tracking
    async getGoals() {
        try {
            const { data, error } = await supabase
                .from('trading_goals')
                .select('*')
                .eq('user_id', this.userId)
                .order('created_at', { ascending: false });

            if (error) throw error;
            return { success: true, data };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    async addGoal(goalData) {
        try {
            const { data, error } = await supabase
                .from('trading_goals')
                .insert([{ ...goalData, user_id: this.userId }])
                .select();

            if (error) throw error;
            return { success: true, data: data[0] };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }
}

// Global API instance
window.tradingAPI = new TradingAPI();
