// Search functionality for envelope cards
document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('envelopeSearch');
    const envelopeCards = document.querySelectorAll('.envelope-card');

    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const searchTerm = e.target.value.toLowerCase();

            envelopeCards.forEach(card => {
                const envelopeName = (card.dataset.envelopeName || '').toLowerCase();
                if (envelopeName.includes(searchTerm)) {
                    card.style.display = '';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }

    // Animate progress bars
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0';
        setTimeout(() => {
            bar.style.width = width;
        }, 300);
    });
});
