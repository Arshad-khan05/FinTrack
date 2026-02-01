/**
 * FinTrack - Animation Controllers
 * Advanced animations and effects
 */

/**
 * Confetti Effect
 */
function showConfetti(duration = 3000) {
    const confettiContainer = document.createElement('div');
    confettiContainer.className = 'confetti';
    document.body.appendChild(confettiContainer);
    
    const colors = ['#6366f1', '#8b5cf6', '#06b6d4', '#10b981', '#f59e0b'];
    const confettiCount = 50;
    
    for (let i = 0; i < confettiCount; i++) {
        const confetti = document.createElement('div');
        confetti.className = 'confetti-piece';
        confetti.style.left = Math.random() * 100 + '%';
        confetti.style.background = colors[Math.floor(Math.random() * colors.length)];
        confetti.style.animationDelay = Math.random() * 0.5 + 's';
        confetti.style.animationDuration = (Math.random() * 2 + 2) + 's';
        confettiContainer.appendChild(confetti);
    }
    
    setTimeout(() => {
        confettiContainer.remove();
    }, duration);
}

/**
 * Success Animation with Checkmark
 */
function showSuccessAnimation(message = 'Success!') {
    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay';
    overlay.innerHTML = `
        <div class="modal scale-in" style="text-align: center; max-width: 400px;">
            <svg class="checkmark" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52">
                <circle class="checkmark-circle" cx="26" cy="26" r="25" fill="none"/>
                <path class="checkmark-check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8"/>
            </svg>
            <h3 style="margin-top: 1.5rem; color: var(--success);">${message}</h3>
        </div>
    `;
    
    document.body.appendChild(overlay);
    
    // Show confetti
    showConfetti(2000);
    
    // Auto remove after 2 seconds
    setTimeout(() => {
        overlay.style.animation = 'fadeOut 0.3s ease-out';
        setTimeout(() => overlay.remove(), 300);
    }, 2000);
}

/**
 * Particle Effect on Click
 */
function createParticleEffect(x, y) {
    const colors = ['#6366f1', '#8b5cf6', '#06b6d4'];
    const particleCount = 10;
    
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.style.position = 'fixed';
        particle.style.left = x + 'px';
        particle.style.top = y + 'px';
        particle.style.width = '4px';
        particle.style.height = '4px';
        particle.style.borderRadius = '50%';
        particle.style.background = colors[Math.floor(Math.random() * colors.length)];
        particle.style.pointerEvents = 'none';
        particle.style.zIndex = '99999';
        
        const angle = (Math.PI * 2 * i) / particleCount;
        const velocity = 50 + Math.random() * 50;
        const vx = Math.cos(angle) * velocity;
        const vy = Math.sin(angle) * velocity;
        
        document.body.appendChild(particle);
        
        let posX = x;
        let posY = y;
        let opacity = 1;
        
        const animate = () => {
            posX += vx * 0.05;
            posY += vy * 0.05;
            opacity -= 0.02;
            
            particle.style.left = posX + 'px';
            particle.style.top = posY + 'px';
            particle.style.opacity = opacity;
            
            if (opacity > 0) {
                requestAnimationFrame(animate);
            } else {
                particle.remove();
            }
        };
        
        requestAnimationFrame(animate);
    }
}

/**
 * Add particle effects to buttons
 */
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.btn-primary, .btn-secondary').forEach(btn => {
        btn.addEventListener('click', (e) => {
            createParticleEffect(e.clientX, e.clientY);
        });
    });
});

/**
 * Ripple Effect for Cards
 */
function addRippleEffect(element) {
    element.addEventListener('click', function(e) {
        const ripple = document.createElement('span');
        const rect = this.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;
        
        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.className = 'ripple-effect';
        ripple.style.position = 'absolute';
        ripple.style.borderRadius = '50%';
        ripple.style.background = 'rgba(255, 255, 255, 0.3)';
        ripple.style.transform = 'scale(0)';
        ripple.style.animation = 'ripple 0.6s ease-out';
        ripple.style.pointerEvents = 'none';
        
        this.style.position = 'relative';
        this.style.overflow = 'hidden';
        this.appendChild(ripple);
        
        setTimeout(() => ripple.remove(), 600);
    });
}

// Add ripple to all cards
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.card, .icon-card, .action-card').forEach(card => {
        addRippleEffect(card);
    });
});

/**
 * Typing Effect
 */
function typeWriter(element, text, speed = 50) {
    let i = 0;
    element.textContent = '';
    
    function type() {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }
    
    type();
}

/**
 * Number Counter Animation (Enhanced)
 */
function animateNumber(element, start, end, duration = 2000, prefix = '', suffix = '') {
    const range = end - start;
    const increment = range / (duration / 16); // 60fps
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {
            current = end;
            clearInterval(timer);
        }
        
        const formatted = Math.round(current).toLocaleString('en-IN');
        element.textContent = prefix + formatted + suffix;
    }, 16);
}

/**
 * Progress Bar Animation
 */
function animateProgressBar(progressBar, targetPercentage, duration = 1000) {
    let currentPercentage = 0;
    const increment = targetPercentage / (duration / 16);
    
    const timer = setInterval(() => {
        currentPercentage += increment;
        if (currentPercentage >= targetPercentage) {
            currentPercentage = targetPercentage;
            clearInterval(timer);
        }
        progressBar.style.width = currentPercentage + '%';
    }, 16);
}

/**
 * Parallax Effect
 */
function initParallax() {
    const parallaxElements = document.querySelectorAll('[data-parallax]');
    
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        
        parallaxElements.forEach(el => {
            const speed = el.dataset.parallax || 0.5;
            const yPos = -(scrolled * speed);
            el.style.transform = `translateY(${yPos}px)`;
        });
    });
}

/**
 * Cursor Trail Effect (Optional, subtle)
 */
function initCursorTrail() {
    const trail = [];
    const trailLength = 10;
    
    document.addEventListener('mousemove', (e) => {
        const dot = document.createElement('div');
        dot.className = 'cursor-trail';
        dot.style.position = 'fixed';
        dot.style.left = e.clientX + 'px';
        dot.style.top = e.clientY + 'px';
        dot.style.width = '4px';
        dot.style.height = '4px';
        dot.style.borderRadius = '50%';
        dot.style.background = 'var(--primary)';
        dot.style.pointerEvents = 'none';
        dot.style.zIndex = '9999';
        dot.style.opacity = '0.5';
        
        document.body.appendChild(dot);
        trail.push(dot);
        
        if (trail.length > trailLength) {
            const removed = trail.shift();
            removed.remove();
        }
        
        setTimeout(() => {
            dot.style.transition = 'opacity 0.5s';
            dot.style.opacity = '0';
            setTimeout(() => dot.remove(), 500);
        }, 100);
    });
}

/**
 * Stagger Animation for Lists
 */
function staggerAnimation(selector, animationClass = 'fade-in') {
    const elements = document.querySelectorAll(selector);
    
    elements.forEach((el, index) => {
        setTimeout(() => {
            el.classList.add(animationClass);
        }, index * 100);
    });
}

/**
 * Floating Action Button Scroll Behavior
 */
function initFAB() {
    const fab = document.querySelector('.fab');
    
    if (fab) {
        window.addEventListener('scroll', () => {
            if (window.pageYOffset > 300) {
                fab.classList.add('visible');
            } else {
                fab.classList.remove('visible');
            }
        });
        
        fab.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
}

/**
 * Loading Screen
 */
function showLoadingScreen() {
    const loader = document.createElement('div');
    loader.id = 'loadingScreen';
    loader.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: var(--bg-primary);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        z-index: 99999;
    `;
    loader.innerHTML = `
        <div class="spinner spinner-lg"></div>
        <p style="margin-top: 2rem; color: var(--text-secondary);">Loading...</p>
    `;
    document.body.appendChild(loader);
}

function hideLoadingScreen() {
    const loader = document.getElementById('loadingScreen');
    if (loader) {
        loader.style.animation = 'fadeOut 0.3s ease-out';
        setTimeout(() => loader.remove(), 300);
    }
}

/**
 * Image Lazy Loading with Animation
 */
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.add('fade-in');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

/**
 * Smooth Page Transitions
 */
function initPageTransitions() {
    // Fade in on page load
    document.body.style.opacity = '0';
    window.addEventListener('load', () => {
        document.body.style.transition = 'opacity 0.3s';
        document.body.style.opacity = '1';
    });
    
    // Fade out on page leave
    document.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', (e) => {
            const href = link.getAttribute('href');
            if (href && !href.startsWith('#') && !link.target) {
                e.preventDefault();
                document.body.style.opacity = '0';
                setTimeout(() => {
                    window.location.href = href;
                }, 300);
            }
        });
    });
}

// Initialize animations on load
document.addEventListener('DOMContentLoaded', () => {
    initParallax();
    initFAB();
    initLazyLoading();
    // Uncomment if you want cursor trail effect
    // initCursorTrail();
});

// Expose functions globally
window.showConfetti = showConfetti;
window.showSuccessAnimation = showSuccessAnimation;
window.createParticleEffect = createParticleEffect;
window.addRippleEffect = addRippleEffect;
window.typeWriter = typeWriter;
window.animateNumber = animateNumber;
window.animateProgressBar = animateProgressBar;
window.staggerAnimation = staggerAnimation;
window.showLoadingScreen = showLoadingScreen;
window.hideLoadingScreen = hideLoadingScreen;
