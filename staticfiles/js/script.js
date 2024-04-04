// Get the alert element
const alertElement = document.getElementById('msg');

// Automatically dismiss the alert after 3 seconds (adjust the time as needed)
setTimeout(function() {
  alertElement.classList.remove('show');
  alertElement.classList.add('hide');
}, 3000); // 3000 milliseconds = 3 seconds

// function highlightStars(selectedStar) {
//   for (let starIndex = 1; starIndex <= 5; starIndex++) {
//       const star = document.getElementById('star' + starIndex);
//       const label = document.querySelector('label[for="star' + starIndex + '"]');
//       if (starIndex <= selectedStar) {
//           label.style.color = '#ffca08'; 
//       } else {
//           label.style.color = ''; // Reset color to default
//       }
//   }
// }

// function highlightStars(selectedStar) {
//   for (let i = selectedStar; i <= 0; i--){
//     const label = document.querySelector(`label[for="star${i}"]`)
//     label.style.color = '#ffca08'; 
//   }

// }