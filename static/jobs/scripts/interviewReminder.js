document.addEventListener('DOMContentLoaded', function () {
    const reminderList = document.getElementById('reminderList');
    const addReminderForm = document.getElementById('addReminderForm');
    const saveReminderButton = document.getElementById('saveReminder');
    const addReminderAction = document.getElementById('addReminderAction');

    const reminders = [];

    saveReminderButton.addEventListener('click', function () {
        const formData = new FormData(addReminderForm);
        const reminderData = {};

        // Extract form data
        formData.forEach((value, key) => {
            reminderData[key] = value;
        });

        // Push Reminder data to the list
        reminders.push(reminderData);

        // Update the Reminder list
        const listItem = document.createElement('li');
        if (reminderData.unit == "d") {
            unit = "day";
        } else if (reminderData.unit == "h") {
            unit = "hour";
        } else {
            unit = "minute";
        }
        if (reminderData.offset > 1) {
            unit += "s";
        }
        listItem.className = 'list-group-item d-flex justify-content-between align-items-center';
        listItem.textContent = reminderData.offset + ' ' + unit; // Assuming "message" is a field in Reminder_form
        listItem.innerHTML += `
            <button type="button" class="btn btn-danger btn-sm" onclick="removeReminder(${reminders.length - 1})">
                Remove
            </button>
        `;
        reminderList.insertBefore(listItem, addReminderAction);

        // Close the modal
        const addReminderModal = bootstrap.Modal.getInstance(document.getElementById('addReminderModal'));
        const addInterviewModel = bootstrap.Modal.getInstance(document.getElementById('addInterview'));
        addReminderModal.hide();
        
        addInterviewModel.show();
        // Reset the Reminder form
        addReminderForm.reset();
    });

    window.removeReminder = function (index) {
        reminders.splice(index, 1); // Remove from the array
        reminderList.children[index].remove(); // Remove the corresponding list item
    };

    // On form submission, attach the Reminders to the form as hidden inputs
    const addInterviewForm = document.getElementById('addInterviewForm');
    addInterviewForm.addEventListener('submit', function (e) {
        // Serialize Reminders as a JSON string
        const hiddenInput = document.createElement('input');
        hiddenInput.type = 'hidden';
        hiddenInput.name = 'reminders';
        hiddenInput.value = JSON.stringify(reminders); // Convert Reminders array to JSON string
        addInterviewForm.appendChild(hiddenInput);
    });
});