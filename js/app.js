// Main App Initialization
document.addEventListener('DOMContentLoaded', function() {
    // Initialize the app
    console.log('Trading Journal App Initialized');
    
    // Check if Supabase is properly configured
    if (!window.supabase) {
        console.error('Supabase not initialized. Please check your configuration.');
        showNotification('Configuration error. Please check your Supabase settings.', 'error');
        return;
    }
    
    // Initialize authentication
    if (window.authManager) {
        console.log('Authentication manager initialized');
    } else {
        console.error('Authentication manager not found');
    }
    
    // Initialize API
    if (window.tradingAPI) {
        console.log('Trading API initialized');
    } else {
        console.error('Trading API not found');
    }
    
    // Initialize dashboard
    if (window.dashboardManager) {
        console.log('Dashboard manager initialized');
    } else {
        console.error('Dashboard manager not found');
    }
    
    // Add some basic error handling
    window.addEventListener('error', function(e) {
        console.error('Global error:', e.error);
        showNotification('An error occurred. Please check the console for details.', 'error');
    });
    
    // Add unhandled promise rejection handling
    window.addEventListener('unhandledrejection', function(e) {
        console.error('Unhandled promise rejection:', e.reason);
        showNotification('An error occurred. Please check the console for details.', 'error');
    });
});

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR'
    }).format(amount);
}

function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function formatDateTime(dateString) {
    return new Date(dateString).toLocaleString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Export functions for global use
window.formatCurrency = formatCurrency;
window.formatDate = formatDate;
window.formatDateTime = formatDateTime;
