// Toggle group (same behavior as expense groups)
function toggleGroup(header) {
    const items = header.nextElementSibling;
    const icon = header.querySelector('.toggle-icon');

    if (items.style.display === 'none' || items.style.display === '') {
        items.style.display = 'flex';
        icon.textContent = '▲';
        items.classList.add('fade-in');
    } else {
        items.style.display = 'none';
        icon.textContent = '▼';
    }
}

// Expand all groups by default
document.addEventListener('DOMContentLoaded', () => {
    const headers = document.querySelectorAll('.expense-group-header');
    headers.forEach(header => {
        toggleGroup(header);
    });
});

// Search functionality for income groups
document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('incomeSearch') || document.getElementById('incomeSourceSearch');
    const groups = document.querySelectorAll('.expense-group, .card.envelope-card, .list-row');

    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const term = e.target.value.toLowerCase();
            groups.forEach(group => {
                const text = group.textContent.toLowerCase();
                group.style.display = text.includes(term) ? '' : 'none';
            });
        });
    }
});

// Confirm delete for income description or income source
function confirmDeleteIncome(button, description) {
    confirmAction(
        `Are you sure you want to delete "${description}"? This action cannot be undone.`,
        () => {
            button.closest('form').submit();
        }
    );
}
