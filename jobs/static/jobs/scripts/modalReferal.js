document.addEventListener("DOMContentLoaded", function () {
    const addJobButton = document.getElementById("addJobButton");
    const referrerInput = document.getElementById("referrerInput");

    if (addJobButton && referrerInput) {
        addJobButton.addEventListener("click", function () {
            referrerInput.value = window.location.href; // Set the current page URL as the referrer
        });
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const addJobButton = document.getElementById("editJobButton");
    const referrerInput = document.getElementById("editJobReferrer");

    if (addJobButton && referrerInput) {
        addJobButton.addEventListener("click", function () {
            referrerInput.value = window.location.href; // Set the current page URL as the referrer
        });
    }
});
