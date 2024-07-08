
document.getElementById("img-ext").addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file.size > 1258291) { 
        alert('Please upload an image smaller than 1.2 MiB.');
        // Clear the input field or prevent further actions
        event.target.value = '';
    }
});
