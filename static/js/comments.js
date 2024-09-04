const editButtons = document.getElementsByClassName("btn-edit");
const commentText = document.getElementById("id_content");
const commentForm = document.getElementById("commentForm");
const submitButton = document.getElementById("submitButton");

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


const deleteCommentModal = new bootstrap.Modal(document.getElementById("deleteCommentModal"));
const deleteButtons = document.getElementsByClassName("delete-comment");
const deleteConfirm = document.getElementById("deleteConfirm");

/**
* Initializes deletion functionality for the provided delete buttons.
* 
* For each button in the `deleteButtons` collection:
* - Retrieves the associated comment's ID upon click.
* - Updates the `deleteConfirm` link's href to point to the 
* deletion endpoint for the specific comment.
* - Displays a confirmation modal (`deleteModal`) to prompt 
* the user for confirmation before deletion.
*/
for (let button of deleteButtons) {
  button.addEventListener("click", (e) => {
    deleteCommentModal.show();
    let commentId = e.target.getAttribute("comment_id");
    deleteConfir.href = `delete_comment/${commentId}`;
  });
}


const closeModalButtons = document.getElementsByClassName("modal-close-btn");
const deleteRecipeModal = new bootstrap.Modal(document.getElementById("deleteRecipeModal"));


for (let button of closeModalButtons) {
  button.addEventListener("click", (e) => {
    deleteRecipeModal.hide();
    deleteCommentModal.hide();
  });
}


const deleteRecipeButton = document.getElementsByClassName("delete-recipe");
const deleteRecipeConfirm = document.getElementById("deleteRecipeConfirm");

// /**
// * Initializes deletion functionality for the provided delete buttons.
// * 
// * For each button in the `deleteButtons` collection:
// * - Retrieves the associated comment's ID upon click.
// * - Updates the `deleteConfirm` link's href to point to the 
// * deletion endpoint for the specific comment.
// * - Displays a confirmation modal (`deleteModal`) to prompt 
// * the user for confirmation before deletion.
// */
for (let button of deleteRecipeButton) {
    button.addEventListener("click", (e) => {
      deleteRecipeModal.show();
      let recipeId = e.target.getAttribute("recipe_id");
      deleteRecipeConfirm.href = `delete_submitted_recipe/${recipeId}`;
    });
  }
