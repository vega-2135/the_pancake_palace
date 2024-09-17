document.getElementById('recipeForm').addEventListener('submit', function(event) {
    var inputFile = document.getElementById('img-ext').files[0];
    
    if (!inputFile) {
        alert("Please upload a file.");
        event.preventDefault();
        return;
    }

    // Get the file type (MIME type)
    var fileType = inputFile.type;

    // Allowed MIME types for PNG and JPG
    var allowedTypes = ['image/png', 'image/jpeg'];

    if (!allowedTypes.includes(fileType)) {
        alert("Only PNG or JPG files are allowed.");
        event.preventDefault();
    }
});
