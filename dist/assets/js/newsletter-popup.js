// Newsletter Popup - Appears after 30 seconds
document.addEventListener('DOMContentLoaded', function() {
    // Check if user has already seen the popup
    const hasSeenPopup = localStorage.getItem('newsletter_popup_seen');
    const hasSubscribed = localStorage.getItem('newsletter_subscribed');
    
    // Don't show if already seen in last 7 days or already subscribed
    if (hasSeenPopup || hasSubscribed) {
        const seenDate = new Date(hasSeenPopup);
        const now = new Date();
        const daysSince = (now - seenDate) / (1000 * 60 * 60 * 24);
        
        if (daysSince < 7 || hasSubscribed) {
            return;
        }
    }
    
    // Show popup after 30 seconds
    setTimeout(function() {
        showNewsletterPopup();
    }, 30000); // 30 seconds
    
    function showNewsletterPopup() {
        // Create popup HTML
        const popup = document.createElement('div');
        popup.className = 'newsletter-popup-overlay';
        popup.innerHTML = `
            <div class="newsletter-popup">
                <button class="popup-close" aria-label="Close popup">&times;</button>
                <div class="popup-content">
                    <div class="popup-icon">⚡</div>
                    <h2>Join Our Wellness Community!</h2>
                    <p>Get weekly wellness insights, blog updates, and exclusive tips delivered every Tuesday.</p>
                    
                    <form class="popup-form" id="popup-newsletter-form">
                        <input 
                            type="email" 
                            name="email" 
                            placeholder="Enter your email address" 
                            required
                            class="popup-input"
                        >
                        <button type="submit" class="popup-button">
                            Subscribe Now
                        </button>
                    </form>
                    
                    <div class="popup-benefits">
                        <span>✅ Weekly updates</span>
                        <span>🚫 No spam</span>
                        <span>📚 Exclusive content</span>
                    </div>
                    
                    <p class="popup-note">We respect your privacy. Unsubscribe anytime.</p>
                </div>
            </div>
        `;
        
        document.body.appendChild(popup);
        
        // Prevent body scroll when popup is open
        document.body.style.overflow = 'hidden';
        
        // Close popup handlers
        const closeBtn = popup.querySelector('.popup-close');
        const overlay = popup.querySelector('.newsletter-popup-overlay');
        
        closeBtn.addEventListener('click', closePopup);
        overlay.addEventListener('click', function(e) {
            if (e.target === overlay) {
                closePopup();
            }
        });
        
        // Handle form submission
        const form = popup.querySelector('#popup-newsletter-form');
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const email = form.querySelector('input[type="email"]').value;
            
            // TODO: Replace with actual Mailchimp submission
            // For now, just show success message
            showSuccessMessage(popup);
            
            // Mark as subscribed
            localStorage.setItem('newsletter_subscribed', 'true');
            
            // Close popup after 2 seconds
            setTimeout(closePopup, 2000);
        });
        
        function closePopup() {
            popup.classList.add('popup-closing');
            document.body.style.overflow = '';
            
            setTimeout(function() {
                popup.remove();
            }, 300);
            
            // Mark popup as seen
            localStorage.setItem('newsletter_popup_seen', new Date().toISOString());
        }
        
        function showSuccessMessage(popup) {
            const content = popup.querySelector('.popup-content');
            content.innerHTML = `
                <div class="popup-success">
                    <div class="success-icon">✅</div>
                    <h2>Thank You!</h2>
                    <p>Check your email to confirm your subscription.</p>
                    <p class="success-note">You'll receive your first newsletter next Tuesday!</p>
                </div>
            `;
        }
    }
});

// Add CSS for popup
const style = document.createElement('style');
style.textContent = `
.newsletter-popup-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.7);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 10000;
    animation: fadeIn 0.3s ease;
}

.newsletter-popup-overlay.popup-closing {
    animation: fadeOut 0.3s ease;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes fadeOut {
    from { opacity: 1; }
    to { opacity: 0; }
}

.newsletter-popup {
    background: white;
    border-radius: 16px;
    max-width: 500px;
    width: 90%;
    max-height: 90vh;
    overflow-y: auto;
    position: relative;
    animation: slideUp 0.3s ease;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

@keyframes slideUp {
    from {
        transform: translateY(50px);
        opacity: 0;
    }
    to {
        transform: translateY(0);
        opacity: 1;
    }
}

.popup-close {
    position: absolute;
    top: 1rem;
    right: 1rem;
    background: none;
    border: none;
    font-size: 2rem;
    color: #666;
    cursor: pointer;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    transition: all 0.2s ease;
}

.popup-close:hover {
    background: #f0f0f0;
    color: #333;
}

.popup-content {
    padding: 3rem 2rem 2rem;
    text-align: center;
}

.popup-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
    animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
}

.popup-content h2 {
    font-size: 2rem;
    margin-bottom: 1rem;
    color: #1e293b;
}

.popup-content p {
    color: #64748b;
    margin-bottom: 1.5rem;
    line-height: 1.6;
}

.popup-form {
    margin-bottom: 1.5rem;
}

.popup-input {
    width: 100%;
    padding: 1rem 1.5rem;
    border: 2px solid #e2e8f0;
    border-radius: 8px;
    font-size: 1rem;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
}

.popup-input:focus {
    outline: none;
    border-color: #4f46e5;
    box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.popup-button {
    width: 100%;
    padding: 1rem 2rem;
    background: linear-gradient(135deg, #4f46e5, #10b981);
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 1.1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
}

.popup-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
}

.popup-benefits {
    display: flex;
    justify-content: center;
    gap: 1.5rem;
    flex-wrap: wrap;
    font-size: 0.9rem;
    color: #64748b;
    margin-bottom: 1rem;
}

.popup-note {
    font-size: 0.85rem;
    color: #94a3b8;
    margin-bottom: 0;
}

.popup-success {
    padding: 2rem 0;
}

.success-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
}

.popup-success h2 {
    color: #10b981;
    margin-bottom: 1rem;
}

.success-note {
    font-weight: 600;
    color: #4f46e5;
}

@media (max-width: 768px) {
    .popup-content {
        padding: 2.5rem 1.5rem 1.5rem;
    }
    
    .popup-content h2 {
        font-size: 1.5rem;
    }
    
    .popup-benefits {
        gap: 1rem;
        font-size: 0.85rem;
    }
}
`;
document.head.appendChild(style);