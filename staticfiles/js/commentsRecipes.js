/*jshint esversion: 6 */
/**
* Initializes edit functionality for the provided edit buttons.
* 
* For each button in the `editButtons` collection:
* - Retrieves the associated comment's ID upon click.
* - Fetches the content of the corresponding comment.
* - Populates the `commentText` input/textarea with the comment's content for editing.
* - Updates the submit button's text to "Update".
* - Sets the form's action attribute to the `edit_comment/{commentId}` endpoint.
*/
document.addEventListener('DOMContentLoaded', function() {
  const editButtons = document.getElementsByClassName("btn-edit");
  const commentText = document.getElementById("id_content");
  const commentForm = document.getElementById("commentForm");
  const submitButton = document.getElementById("submitButton");

  for (let button of editButtons) {
    button.addEventListener("click", (e) => {
      let commentId = e.target.getAttribute("comment_id");
      let commentContent = document.getElementById(`comment${commentId}`).innerText;
      commentText.value = commentContent;
      submitButton.innerText = "Update";
      commentForm.setAttribute("action", `edit_comment/${commentId}`);
    });
    console.log("Edited");
  }


  /**
  * Initializes deletion functionality for comments.
  * 
  * For each button in the `deleteButtons` collection:
  * - Retrieves the associated comment's ID upon click.
  * - Updates the `deleteConfirm` link's href to point to the 
  * deletion endpoint for the specific comment.
  * - Displays a confirmation modal (`deleteModal`) to prompt 
  * the user for confirmation before deletion.
  */
  const deleteCommentModal = new bootstrap.Modal(document.getElementById("deleteCommentModal"));
  const deleteButtons = document.getElementsByClassName("delete-comment");
  const deleteConfirm = document.getElementById("deleteConfirm");

  for (let button of deleteButtons) {
    button.addEventListener("click", (e) => {
      deleteCommentModal.show();
      let commentId = e.target.getAttribute("comment_id");
      deleteConfirm.href = `delete_comment/${commentId}`;
    });
  }


  /* Close modal functionality.*/
  const closeModalButtons = document.getElementsByClassName("modal-close-btn");
  const deleteRecipeModal = new bootstrap.Modal(document.getElementById("deleteRecipeModal"));

  for (let button of closeModalButtons) {
    button.addEventListener("click", (e) => {
      deleteRecipeModal.hide();
      deleteCommentModal.hide();
    });
  }


  /* Initializes deletion functionality for recipe posts.*/
  const deleteRecipeButton = document.getElementsByClassName("delete-recipe");
  const deleteRecipeConfirm = document.getElementById("deleteRecipeConfirm");

  for (let button of deleteRecipeButton) {
      button.addEventListener("click", (e) => {
        deleteRecipeModal.show();
        let recipeId = e.target.getAttribute("recipe_id");
        deleteRecipeConfirm.href = `delete_submitted_recipe/${recipeId}`;
      });
    }


  /* Show alert if rating is missing */
  const form = document.getElementById("commentForm");
  const ratingInputs = document.querySelectorAll("input[name='rating']");
  const ratingContainer = document.querySelector(".rating");
  const messageElement = document.getElementById("ratingReminder");

  // Function to check if a rating is selected
  function isRatingSelected() {
      return Array.from(ratingInputs).some(input => input.checked);
  }

  // Initial page load - everything should be in its normal state
  function setInitialState() {
      submitButton.disabled = false;
      submitButton.classList.add("btn-success");
      submitButton.classList.remove("btn-secondary");
      ratingContainer.classList.remove("highlight");
  }

  // Update button state and UI based on rating selection
  function updateButtonState() {
      if (isRatingSelected()) {
          submitButton.disabled = false;
          submitButton.classList.remove("btn-secondary");
          submitButton.classList.add("btn-success");
          messageElement.style.display = "none";
          ratingContainer.classList.remove("highlight");
      }
  }

  // Handle form submission
  form.addEventListener('submit', function(event) {
      if (!isRatingSelected()) {
          event.preventDefault();  // Prevent form submission
          // Change button and UI after submission without rating
          submitButton.disabled = true;
          submitButton.classList.remove("btn-success");
          submitButton.classList.add("btn-secondary");
          messageElement.classList.add("rating-reminder-msg");
          ratingContainer.classList.add("highlight");
      }
  });

  // Attach event listeners to rating inputs
  ratingInputs.forEach(input => {
      input.addEventListener("change", updateButtonState);
  });

  setInitialState();  // Set the initial state when the page loads
});

