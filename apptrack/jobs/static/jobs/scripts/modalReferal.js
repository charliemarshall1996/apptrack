document.addEventListener("DOMContentLoaded", function () {
    const addJobButton = document.getElementById("addJobButton");
    const referrerInput = document.getElementById("referrerInput");

    if (addJobButton && referrerInput) {
        addJobButton.addEventListener("click", function () {
            referrerInput.value = window.location.href; // Set the current page URL as the referrer
        });
    }
});
