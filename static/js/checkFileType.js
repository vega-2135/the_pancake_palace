/*jshint esversion: 6 */
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("img-ext").addEventListener("change", function(event) {
        var file = event.target.files[0];
        if (file.size > 1258291) {
            alert("Please upload an image smaller than 1.2 MiB.");
            // Clear the input field or prevent further actions
            event.target.value = '';
        }

        var fileType = file.type;

        // Allowed MIME types for PNG and JPG
        var allowedTypes = ["image/png", "image/jpeg", "image/webp"];

        if (!allowedTypes.includes(fileType)) {
            alert("Only PNG, JPG or WEBP files are allowed.");
            event.preventDefault();
        }
    });
});