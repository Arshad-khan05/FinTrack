// Add stagger animation to action cards
document.addEventListener('DOMContentLoaded', () => {
    const cards = document.querySelectorAll('.action-card');
    cards.forEach((card, index) => {
        card.style.animationDelay = (index * 0.1) + 's';
    });
});
