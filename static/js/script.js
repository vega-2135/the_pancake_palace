// Get the alert element
const alertElement = document.getElementById("msg");

// Automatically dismiss the alert after 2 seconds
setTimeout(function() {
  alertElement.classList.remove('show');
  alertElement.classList.add('hide');
}, 2000); 
