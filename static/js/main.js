/**
 * FinTrack - Main JavaScript
 * Core functionality and utilities
 */

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    initMobileMenu();
    initToasts();
    initModals();
    initForms();
    initAnimations();
    initCountUp();
});

/**
 * Mobile Menu Toggle
 */
function initMobileMenu() {
    const toggle = document.querySelector('.navbar-toggle');
    const menu = document.querySelector('.navbar-menu');
    
    if (toggle && menu) {
        toggle.addEventListener('click', () => {
            menu.classList.toggle('active');
            toggle.classList.toggle('active');
            
            // Animate icon
            const icon = toggle.querySelector('i') || toggle.querySelector('span');
            if (icon) {
                icon.classList.toggle('rotate');
            }
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!toggle.contains(e.target) && !menu.contains(e.target)) {
                menu.classList.remove('active');
                toggle.classList.remove('active');
            }
        });
        
        // Close menu when clicking a link
        const menuLinks = menu.querySelectorAll('a');
        menuLinks.forEach(link => {
            link.addEventListener('click', () => {
                menu.classList.remove('active');
                toggle.classList.remove('active');
            });
        });
    }
}

/**
 * Toast Notifications
 * Converts Django messages to modern toast notifications
 */
function initToasts() {
    // Find Django messages and convert to toasts
    const messageList = document.querySelector('.messages');
    if (messageList) {
        const messages = messageList.querySelectorAll('li');
        
        messages.forEach((message, index) => {
            const messageText = message.textContent.trim();
            const messageTag = message.className.split(' ').find(c => 
                ['success', 'error', 'warning', 'info'].includes(c)
            ) || 'info';
            
            setTimeout(() => {
                showToast(messageText, messageTag);
            }, index * 200);
        });
        
        // Hide original message list
        messageList.style.display = 'none';
    }
}

/**
 * Show a toast notification
 */
function showToast(message, type = 'info', duration = 5000) {
    const container = getOrCreateToastContainer();
    
    const icons = {
        success: '✓',
        error: '✕',
        warning: '⚠',
        info: 'ℹ'
    };
    
    const titles = {
        success: 'Success',
        error: 'Error',
        warning: 'Warning',
        info: 'Info'
    };
    
    const toast = document.createElement('div');
    toast.className = `toast toast-${type} fade-in`;
    toast.innerHTML = `
        <span class="toast-icon">${icons[type]}</span>
        <div class="toast-content">
            <div class="toast-title">${titles[type]}</div>
            <div class="toast-message">${message}</div>
        </div>
        <button class="toast-close" onclick="this.parentElement.remove()">&times;</button>
    `;
    
    container.appendChild(toast);
    
    // Auto remove after duration
    if (duration > 0) {
        setTimeout(() => {
            toast.style.animation = 'slideOutRight 0.3s ease-out';
            setTimeout(() => toast.remove(), 300);
        }, duration);
    }
    
    return toast;
}

/**
 * Get or create toast container
 */
function getOrCreateToastContainer() {
    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
    }
    return container;
}

/**
 * Modal Management
 */
function initModals() {
    // Close modal on overlay click
    document.addEventListener('click', (e) => {
        if (e.target.classList.contains('modal-overlay')) {
            closeModal(e.target.querySelector('.modal'));
        }
    });
    
    // Close modal on close button click
    document.querySelectorAll('.modal-close').forEach(btn => {
        btn.addEventListener('click', () => {
            closeModal(btn.closest('.modal'));
        });
    });
    
    // Close modal on Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            const overlay = document.querySelector('.modal-overlay');
            if (overlay) {
                closeModal(overlay.querySelector('.modal'));
            }
        }
    });
}

/**
 * Open modal
 */
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        const overlay = document.createElement('div');
        overlay.className = 'modal-overlay';
        overlay.appendChild(modal.cloneNode(true));
        document.body.appendChild(overlay);
        document.body.style.overflow = 'hidden';
    }
}

/**
 * Close modal
 */
function closeModal(modal) {
    const overlay = modal?.closest('.modal-overlay');
    if (overlay) {
        overlay.style.animation = 'fadeOut 0.2s ease-out';
        setTimeout(() => {
            overlay.remove();
            document.body.style.overflow = '';
        }, 200);
    }
}

/**
 * Confirm dialog
 */
function confirmAction(message, onConfirm) {
    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay';
    overlay.innerHTML = `
        <div class="modal scale-in">
            <div class="modal-header">
                <h3 class="modal-title">Confirm Action</h3>
            </div>
            <div class="modal-body">
                <p>${message}</p>
            </div>
            <div class="modal-footer">
                <button class="btn btn-ghost" onclick="this.closest('.modal-overlay').remove(); document.body.style.overflow=''">
                    Cancel
                </button>
                <button class="btn btn-danger" id="confirmBtn">
                    Confirm
                </button>
            </div>
        </div>
    `;
    
    document.body.appendChild(overlay);
    document.body.style.overflow = 'hidden';
    
    overlay.querySelector('#confirmBtn').addEventListener('click', () => {
        onConfirm();
        overlay.remove();
        document.body.style.overflow = '';
    });
}

/**
 * Form Enhancements
 */
function initForms() {
    // Add loading state to forms on submit
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('[type="submit"]');
            if (submitBtn && !submitBtn.disabled) {
                submitBtn.disabled = true;
                submitBtn.classList.add('loading');
                submitBtn.dataset.originalText = submitBtn.textContent;
                submitBtn.innerHTML = '<span class="spinner spinner-sm"></span> Processing...';
            }
        });
    });
    
    // Real-time validation
    document.querySelectorAll('.form-input, .form-select, .form-textarea').forEach(input => {
        input.addEventListener('blur', () => {
            validateField(input);
        });
        
        input.addEventListener('input', () => {
            if (input.classList.contains('error')) {
                validateField(input);
            }
        });
    });
    
    // Auto-resize textareas
    document.querySelectorAll('.form-textarea').forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
    });
}

/**
 * Validate form field
 */
function validateField(field) {
    const errorEl = field.parentElement.querySelector('.form-error');
    
    if (field.validity.valid) {
        field.classList.remove('error');
        if (errorEl) errorEl.remove();
        return true;
    } else {
        field.classList.add('error');
        if (!errorEl) {
            const error = document.createElement('span');
            error.className = 'form-error';
            error.textContent = field.validationMessage;
            field.parentElement.appendChild(error);
        }
        field.classList.add('shake');
        setTimeout(() => field.classList.remove('shake'), 500);
        return false;
    }
}

/**
 * Scroll Animations
 */
function initAnimations() {
    const animatedElements = document.querySelectorAll(
        '.fade-in, .slide-up, .slide-left, .slide-right, .scale-in'
    );
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'none';
            }
        });
    }, {
        threshold: 0.1
    });
    
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        observer.observe(el);
    });
}

/**
 * Count Up Animation for Numbers
 */
function initCountUp() {
    const countElements = document.querySelectorAll('.count-up');
    
    countElements.forEach(el => {
        // Get target value from data attribute or text content
        const target = parseFloat(el.dataset.value || el.textContent.replace(/[^0-9.-]/g, ''));
        const duration = 2000; // 2 seconds
        const steps = 60;
        const increment = target / steps;
        const stepDuration = duration / steps;
        
        let current = 0;
        el.textContent = '₹ 0';
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const timer = setInterval(() => {
                        current += increment;
                        if (current >= target) {
                            current = target;
                            clearInterval(timer);
                        }
                        // Format as currency with rupee symbol
                        el.textContent = '₹ ' + Math.round(current).toLocaleString('en-IN');
                    }, stepDuration);
                    observer.unobserve(el);
                }
            });
        });
        
        observer.observe(el);
    });
}

/**
 * Search functionality
 */
function setupSearch(inputSelector, itemsSelector) {
    const searchInput = document.querySelector(inputSelector);
    const items = document.querySelectorAll(itemsSelector);
    
    if (searchInput && items.length > 0) {
        searchInput.addEventListener('input', (e) => {
            const searchTerm = e.target.value.toLowerCase();
            
            items.forEach(item => {
                const text = item.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    item.style.display = '';
                    item.classList.add('fade-in');
                } else {
                    item.style.display = 'none';
                }
            });
        });
    }
}

/**
 * Filter functionality
 */
function setupFilter(selectSelector, itemsSelector, dataAttribute) {
    const filterSelect = document.querySelector(selectSelector);
    const items = document.querySelectorAll(itemsSelector);
    
    if (filterSelect && items.length > 0) {
        filterSelect.addEventListener('change', (e) => {
            const filterValue = e.target.value;
            
            items.forEach(item => {
                if (filterValue === '' || item.dataset[dataAttribute] === filterValue) {
                    item.style.display = '';
                    item.classList.add('fade-in');
                } else {
                    item.style.display = 'none';
                }
            });
        });
    }
}

/**
 * Format currency
 */
function formatCurrency(amount, currency = '₹') {
    return currency + ' ' + parseFloat(amount).toLocaleString('en-IN', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}

/**
 * Format date
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

/**
 * Debounce function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Copy to clipboard
 */
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copied to clipboard!', 'success', 2000);
    }).catch(() => {
        showToast('Failed to copy', 'error', 2000);
    });
}

/**
 * Smooth scroll to element
 */
function scrollToElement(selector, offset = 0) {
    const element = document.querySelector(selector);
    if (element) {
        const top = element.getBoundingClientRect().top + window.pageYOffset - offset;
        window.scrollTo({
            top: top,
            behavior: 'smooth'
        });
    }
}

// Expose functions to global scope for inline event handlers
window.showToast = showToast;
window.openModal = openModal;
window.closeModal = closeModal;
window.confirmAction = confirmAction;
window.setupSearch = setupSearch;
window.setupFilter = setupFilter;
window.formatCurrency = formatCurrency;
window.formatDate = formatDate;
window.copyToClipboard = copyToClipboard;
window.scrollToElement = scrollToElement;
