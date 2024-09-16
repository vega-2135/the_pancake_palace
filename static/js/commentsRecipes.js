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
document.getElementById('commentForm').addEventListener('submit', function(event) {
    const ratingInputs = document.querySelectorAll('input[name="rating"]');
    let ratingSelected = false;

    for (let input of ratingInputs) {
        if (input.checked) {
            ratingSelected = true;
            break;
        }
    }

    if (!ratingSelected) {
        event.preventDefault(); // Prevent the form from submitting
        alert("You must rate the recipe if you want to leave a comment.");
    }
});