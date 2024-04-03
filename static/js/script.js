// Get the alert element
const alertElement = document.getElementById('msg');

// Automatically dismiss the alert after 3 seconds (adjust the time as needed)
setTimeout(function() {
  alertElement.classList.remove('show');
  alertElement.classList.add('hide');
}, 3000); // 3000 milliseconds = 3 seconds
