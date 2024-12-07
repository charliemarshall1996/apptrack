document.addEventListener('DOMContentLoaded', function () {
    const alertList = document.getElementById('alertList');
    const addAlertForm = document.getElementById('addAlertForm');
    const saveAlertButton = document.getElementById('saveAlert');
    const addAlertAction = document.getElementById('addAlertAction');

    const alerts = [];

    saveAlertButton.addEventListener('click', function () {
        const formData = new FormData(addAlertForm);
        const alertData = {};

        // Extract form data
        formData.forEach((value, key) => {
            alertData[key] = value;
        });

        // Push alert data to the list
        alerts.push(alertData);

        // Update the alert list
        const listItem = document.createElement('li');
        listItem.className = 'list-group-item d-flex justify-content-between align-items-center';
        listItem.textContent = alertData.message; // Assuming "message" is a field in alert_form
        listItem.innerHTML += `
            <button type="button" class="btn btn-danger btn-sm" onclick="removeAlert(${alerts.length - 1})">
                Remove
            </button>
        `;
        alertList.insertBefore(listItem, addAlertAction);

        // Close the modal
        const addAlertModal = bootstrap.Modal.getInstance(document.getElementById('addAlertModal'));
        const addInterviewModel = bootstrap.Modal.getInstance(document.getElementById('addInterview'));
        addAlertModal.hide();
        
        addInterviewModel.show();
        // Reset the alert form
        addAlertForm.reset();
    });

    window.removeAlert = function (index) {
        alerts.splice(index, 1); // Remove from the array
        alertList.children[index].remove(); // Remove the corresponding list item
    };

    // On form submission, attach the alerts to the form as hidden inputs
    const addInterviewForm = document.getElementById('addInterviewForm');
    addInterviewForm.addEventListener('submit', function (e) {
        // Serialize alerts as a JSON string
        const hiddenInput = document.createElement('input');
        hiddenInput.type = 'hidden';
        hiddenInput.name = 'alerts';
        hiddenInput.value = JSON.stringify(alerts); // Convert alerts array to JSON string
        addInterviewForm.appendChild(hiddenInput);
    });
});