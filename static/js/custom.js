// Custom JavaScript for Trading Journal

document.addEventListener('DOMContentLoaded', function() {
    // Auto-calculate P&L when entry/exit prices change
    const entryPriceInput = document.getElementById('id_entry_price');
    const exitPriceInput = document.getElementById('id_exit_price');
    const quantityInput = document.getElementById('id_quantity');
    const profitLossInput = document.getElementById('id_profit_loss');
    const percentageInput = document.getElementById('id_percentage_gain_loss');
    const tradeTypeSelect = document.getElementById('id_trade_type');

    function calculatePnL() {
        if (entryPriceInput && exitPriceInput && quantityInput && profitLossInput && percentageInput && tradeTypeSelect) {
            const entryPrice = parseFloat(entryPriceInput.value) || 0;
            const exitPrice = parseFloat(exitPriceInput.value) || 0;
            const quantity = parseInt(quantityInput.value) || 0;
            const tradeType = tradeTypeSelect.value;

            if (entryPrice > 0 && exitPrice > 0 && quantity > 0) {
                let profitLoss;
                if (tradeType === 'LONG') {
                    profitLoss = (exitPrice - entryPrice) * quantity;
                } else if (tradeType === 'SHORT') {
                    profitLoss = (entryPrice - exitPrice) * quantity;
                } else {
                    profitLoss = 0;
                }

                const percentage = entryPrice > 0 ? ((profitLoss / (entryPrice * quantity)) * 100) : 0;

                profitLossInput.value = profitLoss.toFixed(2);
                percentageInput.value = percentage.toFixed(2);
            }
        }
    }

    // Add event listeners for auto-calculation
    if (entryPriceInput) entryPriceInput.addEventListener('input', calculatePnL);
    if (exitPriceInput) exitPriceInput.addEventListener('input', calculatePnL);
    if (quantityInput) quantityInput.addEventListener('input', calculatePnL);
    if (tradeTypeSelect) tradeTypeSelect.addEventListener('change', calculatePnL);

    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('border-red-500');
                } else {
                    field.classList.remove('border-red-500');
                }
            });

            if (!isValid) {
                event.preventDefault();
                alert('Please fill in all required fields.');
            }
        });
    });

    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 5000);
    });

    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Initialize tooltips (if using a tooltip library)
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = this.getAttribute('data-tooltip');
            tooltip.style.position = 'absolute';
            tooltip.style.background = '#333';
            tooltip.style.color = 'white';
            tooltip.style.padding = '5px 10px';
            tooltip.style.borderRadius = '4px';
            tooltip.style.fontSize = '12px';
            tooltip.style.zIndex = '1000';
            document.body.appendChild(tooltip);

            const rect = this.getBoundingClientRect();
            tooltip.style.left = rect.left + 'px';
            tooltip.style.top = (rect.top - tooltip.offsetHeight - 5) + 'px';
        });

        element.addEventListener('mouseleave', function() {
            const tooltip = document.querySelector('.tooltip');
            if (tooltip) {
                tooltip.remove();
            }
        });
    });

    // Chart responsiveness
    const charts = document.querySelectorAll('canvas');
    charts.forEach(chart => {
        const ctx = chart.getContext('2d');
        if (ctx && ctx.chart) {
            window.addEventListener('resize', function() {
                ctx.chart.resize();
            });
        }
    });

    // Copy to clipboard functionality
    const copyButtons = document.querySelectorAll('[data-copy]');
    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const textToCopy = this.getAttribute('data-copy');
            navigator.clipboard.writeText(textToCopy).then(() => {
                const originalText = this.textContent;
                this.textContent = 'Copied!';
                setTimeout(() => {
                    this.textContent = originalText;
                }, 2000);
            });
        });
    });

    // Search functionality
    const searchInputs = document.querySelectorAll('[data-search]');
    searchInputs.forEach(input => {
        input.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const targetSelector = this.getAttribute('data-search');
            const targets = document.querySelectorAll(targetSelector);

            targets.forEach(target => {
                const text = target.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    target.style.display = '';
                } else {
                    target.style.display = 'none';
                }
            });
        });
    });

    // Date picker enhancements
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        // Set default value to today if empty
        if (!input.value) {
            const today = new Date().toISOString().split('T')[0];
            input.value = today;
        }
    });

    // Number input formatting
    const numberInputs = document.querySelectorAll('input[type="number"]');
    numberInputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.value && !isNaN(this.value)) {
                const num = parseFloat(this.value);
                if (this.step && this.step.includes('.')) {
                    const decimals = this.step.split('.')[1].length;
                    this.value = num.toFixed(decimals);
                }
            }
        });
    });
});

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR'
    }).format(amount);
}

function formatPercentage(value) {
    return new Intl.NumberFormat('en-US', {
        style: 'percent',
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }).format(value / 100);
}

function formatDate(date) {
    return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    }).format(new Date(date));
}

// Export functions for use in templates
window.TradingJournal = {
    formatCurrency,
    formatPercentage,
    formatDate
};
