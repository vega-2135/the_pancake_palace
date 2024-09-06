/*jshint esversion: 6 */
document.addEventListener('DOMContentLoaded', function() {
    const saveButton = document.getElementById('save-button');
    const removeButton = document.getElementById('remove-button');

    if (saveButton) {
        saveButton.addEventListener('click', function(event) {
            // Prevent the default link behavior
            event.preventDefault();
            // Perform the save operation here
            // After saving, manually redirect to the current URL to refresh the page
            window.location.href = window.location.href;
        });
    }
});