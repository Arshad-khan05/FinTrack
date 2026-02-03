// Toggle expense group
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

// Search functionality
document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('expenseSearch');
    const expenseGroups = document.querySelectorAll('.expense-group');

    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const searchTerm = e.target.value.toLowerCase();

            expenseGroups.forEach(group => {
                const envelopeName = (group.dataset.envelopeName || '').toLowerCase();
                const expenseItems = group.querySelectorAll('.expense-item');
                let hasMatch = false;

                expenseItems.forEach(item => {
                    const text = item.textContent.toLowerCase();
                    if (text.includes(searchTerm) || envelopeName.includes(searchTerm)) {
                        item.style.display = '';
                        hasMatch = true;
                    } else {
                        item.style.display = 'none';
                    }
                });

                group.style.display = hasMatch || envelopeName.includes(searchTerm) ? '' : 'none';
            });
        });
    }
});

// Confirm delete function
function confirmDeleteExpense(button, description) {
    confirmAction(
        `Are you sure you want to delete the expense "${description}"? This action cannot be undone.`,
        () => {
            button.closest('form').submit();
        }
    );
}
