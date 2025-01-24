document.addEventListener('DOMContentLoaded', function () {
    const addInterviewModal = document.getElementById('addInterview');
    const addInterviewForm = document.getElementById('addInterviewForm');

    // Object to store form data
    const formData = {};

    // Save form data when the modal is hidden
    addInterviewModal.addEventListener('hide.bs.modal', function () {
        const formElements = addInterviewForm.elements;
        for (const element of formElements) {
            if (element.name) {
                formData[element.name] = element.value;
            }
        }
    });

    // Restore form data when the modal is shown
    addInterviewModal.addEventListener('show.bs.modal', function () {
        const formElements = addInterviewForm.elements;
        for (const element of formElements) {
            if (element.name && formData[element.name] !== undefined) {
                element.value = formData[element.name];
            }
        }
    });
});