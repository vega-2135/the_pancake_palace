// Get the alert element
const alertElement = document.getElementById('msg');

// Automatically dismiss the alert after 3 seconds (adjust the time as needed)
setTimeout(function() {
  alertElement.classList.remove('show');
  alertElement.classList.add('hide');
}, 3000); // 3000 milliseconds = 3 seconds

function highlightStars(selectedStar) {
  // Highlight stars up to the selected star
  for (const starIndex = 1; starIndex <= selectedStar; starIndex++) {
      const star = document.getElementById('star' + starIndex);
      const label = document.querySelector('label[for="star' + starIndex + '"]');
      star.checked = true;
      label.style.color = '#ffca08'; 
  }
  
  // Reset color for stars after the selected star
  for (const nextStarIndex = selectedStar + 1; nextStarIndex <= 5; nextStarIndex++) {
      const star = document.getElementById('star' + nextStarIndex);
      const label = document.querySelector('label[for="star' + nextStarIndex + '"]');
      star.checked = false;
      label.style.color = ''; // This will reset color to default
  }
}