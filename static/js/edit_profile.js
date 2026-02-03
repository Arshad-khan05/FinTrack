document.addEventListener('DOMContentLoaded', () => {
    const newPass = document.getElementById('new_password');
    const confirmPass = document.getElementById('confirm_password');

    if (!newPass || !confirmPass) return;

    function validatePasswords() {
        if (newPass.value && confirmPass.value && newPass.value !== confirmPass.value) {
            confirmPass.setCustomValidity('Passwords do not match');
        } else {
            confirmPass.setCustomValidity('');
        }
    }

    newPass.addEventListener('input', validatePasswords);
    confirmPass.addEventListener('input', validatePasswords);
});
