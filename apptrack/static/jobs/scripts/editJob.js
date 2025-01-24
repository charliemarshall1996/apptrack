
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-bs-target^="#editJobModal"]').forEach(button => {
        button.addEventListener('click', function () {
            const modalId = this.getAttribute('data-bs-target');
            const editModal = document.querySelector(modalId);
            if (editModal) {
                const modalInstance = new bootstrap.Modal(editModal);
                modalInstance.show();
            }
        });
    });
});

