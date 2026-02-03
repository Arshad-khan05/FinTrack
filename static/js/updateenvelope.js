// Search functionality for update envelope list

document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('envelopeSearch');
    const tableRows = document.querySelectorAll('tbody tr');

    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const searchTerm = e.target.value.toLowerCase();

            tableRows.forEach(row => {
                const envelopeName = (row.dataset.envelopeName || '').toLowerCase();
                if (envelopeName.includes(searchTerm)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    }
});

// Confirm delete function (relies on global confirmAction)
function confirmDelete(envelopeName, deleteUrl) {
    confirmAction(
        `Are you sure you want to delete the "${envelopeName}" envelope? This action cannot be undone.`,
        () => {
            window.location.href = deleteUrl;
        }
    );
}
