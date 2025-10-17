// Authentication functions
class AuthManager {
    constructor() {
        this.currentUser = null;
        this.init();
    }

    async init() {
        // Check if user is already logged in
        const { data: { session } } = await supabase.auth.getSession();
        if (session) {
            this.currentUser = session.user;
            this.showAuthenticatedUI();
        } else {
            this.showUnauthenticatedUI();
        }

        // Listen for auth changes
        supabase.auth.onAuthStateChange((event, session) => {
            if (event === 'SIGNED_IN') {
                this.currentUser = session.user;
                this.showAuthenticatedUI();
            } else if (event === 'SIGNED_OUT') {
                this.currentUser = null;
                this.showUnauthenticatedUI();
            }
        });
    }

    showAuthenticatedUI() {
        document.getElementById('user-info').classList.remove('hidden');
        document.getElementById('login-buttons').classList.add('hidden');
        document.getElementById('main-content').classList.remove('hidden');
        document.getElementById('loading').classList.add('hidden');
        
        document.getElementById('user-email').textContent = this.currentUser.email;
        
        // Load dashboard
        if (window.dashboardManager) {
            window.dashboardManager.loadDashboard();
        }
    }

    showUnauthenticatedUI() {
        document.getElementById('user-info').classList.add('hidden');
        document.getElementById('login-buttons').classList.remove('hidden');
        document.getElementById('main-content').classList.add('hidden');
        document.getElementById('loading').classList.add('hidden');
    }

    async login(email, password) {
        try {
            const { data, error } = await supabase.auth.signInWithPassword({
                email: email,
                password: password
            });

            if (error) throw error;
            return { success: true, data };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    async register(email, password) {
        try {
            const { data, error } = await supabase.auth.signUp({
                email: email,
                password: password
            });

            if (error) throw error;
            return { success: true, data };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    async logout() {
        try {
            const { error } = await supabase.auth.signOut();
            if (error) throw error;
            return { success: true };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }
}

// Global auth manager instance
window.authManager = new AuthManager();

// Modal functions
function showLogin() {
    document.getElementById('login-modal').classList.remove('hidden');
    document.getElementById('register-modal').classList.add('hidden');
}

function hideLogin() {
    document.getElementById('login-modal').classList.add('hidden');
}

function showRegister() {
    document.getElementById('register-modal').classList.remove('hidden');
    document.getElementById('login-modal').classList.add('hidden');
}

function hideRegister() {
    document.getElementById('register-modal').classList.add('hidden');
}

async function logout() {
    const result = await window.authManager.logout();
    if (result.success) {
        showNotification('Logged out successfully', 'success');
    } else {
        showNotification('Error logging out: ' + result.error, 'error');
    }
}

// Form handlers
document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    
    const result = await window.authManager.login(email, password);
    
    if (result.success) {
        hideLogin();
        showNotification('Logged in successfully!', 'success');
    } else {
        showNotification('Login failed: ' + result.error, 'error');
    }
});

document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    
    const result = await window.authManager.register(email, password);
    
    if (result.success) {
        hideRegister();
        showNotification('Registration successful! Please check your email to confirm your account.', 'success');
    } else {
        showNotification('Registration failed: ' + result.error, 'error');
    }
});

// Notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 ${
        type === 'success' ? 'bg-green-500 text-white' :
        type === 'error' ? 'bg-red-500 text-white' :
        'bg-blue-500 text-white'
    }`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        notification.remove();
    }, 5000);
}
