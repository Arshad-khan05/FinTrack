// Calculate and display remaining amount in real-time
document.addEventListener('DOMContentLoaded', () => {
    const budgetInput = document.getElementById('budget');
    const spentInput = document.getElementById('spend');

    if (!budgetInput || !spentInput) return;

    function calculateRemaining() {
        const budget = parseFloat(budgetInput.value) || 0;
        const spent = parseFloat(spentInput.value) || 0;
        const remaining = budget - spent;
        // Placeholder for live preview if needed in future
    }

    budgetInput.addEventListener('input', calculateRemaining);
    spentInput.addEventListener('input', calculateRemaining);
});
